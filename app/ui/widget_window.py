"""Плавающий адаптивный виджет общего Pomodoro-таймера."""

from collections.abc import Callable
from copy import deepcopy
from dataclasses import dataclass
import tkinter as tk

from app.models import AppSettings
from app.theme import ThemeManager, ThemePalette, mode_color
from app.timer_engine import TimerEngine
from app.widget_settings import (
    WIDGET_MIN_SIZES,
    WIDGET_SIZE_CUSTOM,
    WIDGET_TYPE_COMPACT,
    WIDGET_TYPE_EXPANDED,
    WIDGET_TYPE_MINIMAL,
    WidgetSizeParameters,
    clamp_window_position,
    content_fitted_dimensions,
    normalize_widget_layouts,
    normalize_widget_type,
    widget_size_parameters,
)


@dataclass(frozen=True)
class WidgetActions:
    """Команды главного окна, доступные представлениям виджета."""

    toggle_timer: Callable[[], None]
    continue_period: Callable[[], None]
    skip_period: Callable[[], None]
    reset_timer: Callable[[], None]
    show_main_window: Callable[[], None]


@dataclass(frozen=True)
class WidgetDisplayState:
    """Единая модель отображения для всех трех разметок."""

    mode_name: str
    formatted_time: str
    completed_work_periods: int
    waiting_for_continue: bool
    primary_text: str


def widget_display_state(timer: TimerEngine) -> WidgetDisplayState:
    """Собирает UI-модель, включая знак плюс и название превышения из ядра."""
    if timer.state.waiting_for_continue:
        primary_text = "Продолжить"
    elif timer.state.is_running:
        primary_text = "Пауза"
    elif timer.state.remaining_seconds < timer.current_period_duration_seconds():
        primary_text = "Продолжить"
    else:
        primary_text = "Старт"
    return WidgetDisplayState(
        mode_name=timer.mode_name(),
        formatted_time=timer.formatted_time(),
        completed_work_periods=timer.state.completed_work_periods,
        waiting_for_continue=timer.state.waiting_for_continue,
        primary_text=primary_text,
    )


class WidgetView:
    """Общая основа разметок внутри единственного окна виджета."""

    def __init__(
        self,
        parent: tk.Widget,
        timer: TimerEngine,
        actions: WidgetActions,
    ) -> None:
        self.timer = timer
        self.actions = actions
        self.frame = tk.Frame(parent, borderwidth=0, highlightthickness=0)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.mode_label: tk.Label
        self.time_label: tk.Label
        self.buttons: list[tk.Button] = []
        self.accent_buttons: list[tk.Button] = []
        self.palette: ThemePalette | None = None
        self.drag_widgets: list[tk.Widget] = [self.frame]

    def update(self) -> None:
        """Подставляет состояние общего TimerEngine в готовую разметку."""
        display = widget_display_state(self.timer)
        self.mode_label.config(text=display.mode_name)
        self.time_label.config(text=display.formatted_time)
        self._apply_state_colors()

    def apply_style(
        self,
        palette: ThemePalette,
        parameters: WidgetSizeParameters,
    ) -> None:
        """Применяет цвета и адаптивные шрифты ко всем общим элементам."""
        self.palette = palette
        background = palette.card_background
        self.frame.configure(bg=background)
        self.mode_label.configure(
            bg=background,
            font=("Segoe UI Semibold", parameters.mode_font),
        )
        self.time_label.configure(
            bg=background,
            font=("Segoe UI Semibold", parameters.time_font),
        )
        for button in self.buttons:
            is_accent = button in self.accent_buttons
            button.configure(
                bg=palette.accent if is_accent else palette.secondary_background,
                fg=palette.on_accent if is_accent else palette.text_primary,
                activebackground=palette.accent_hover,
                activeforeground=palette.on_accent,
                disabledforeground=palette.disabled,
                highlightbackground=palette.border,
                highlightcolor=palette.focus,
                highlightthickness=1,
                font=("Segoe UI Semibold", parameters.button_font),
            )
        self._apply_state_colors()

    def _apply_state_colors(self) -> None:
        """Обновляет семантический цвет режима при обычном тике и превышении."""
        if self.palette is None:
            return
        state_color = mode_color(
            self.palette,
            self.timer.state.mode,
            self.timer.state.waiting_for_continue,
        )
        self.mode_label.configure(fg=state_color)
        self.time_label.configure(
            fg=self.palette.overrun
            if self.timer.state.waiting_for_continue
            else self.palette.text_primary,
        )

    def destroy(self) -> None:
        """Удаляет только содержимое, сохраняя Toplevel и TimerEngine."""
        self.frame.destroy()

    def _primary_text(self) -> str:
        """Возвращает подпись основной кнопки по текущему состоянию."""
        return widget_display_state(self.timer).primary_text

    def _handle_primary(self) -> None:
        """Направляет превышение в общий обработчик, остальные состояния — в toggle."""
        if self.timer.state.waiting_for_continue:
            self.actions.continue_period()
        else:
            self.actions.toggle_timer()

    def _button(
        self,
        parent: tk.Widget,
        text: str,
        command: Callable[[], None],
        *,
        accent: bool = False,
    ) -> tk.Button:
        """Создает одинаковую доступную кнопку без отдельной ttk-темы."""
        button = tk.Button(
            parent,
            text=text,
            command=command,
            relief=tk.FLAT,
            borderwidth=0,
            cursor="hand2",
            takefocus=True,
        )
        self.buttons.append(button)
        if accent:
            self.accent_buttons.append(button)
        return button


class MinimalWidgetView(WidgetView):
    """Минимум элементов: состояние, крупное время и продолжение превышения."""

    def __init__(self, parent: tk.Widget, timer: TimerEngine, actions: WidgetActions) -> None:
        super().__init__(parent, timer, actions)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=3)

        self.mode_label = tk.Label(self.frame, anchor=tk.CENTER)
        self.mode_label.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=(8, 0))
        self.time_label = tk.Label(self.frame, anchor=tk.CENTER)
        self.time_label.grid(row=1, column=0, sticky=tk.NSEW, padx=10)
        self.continue_button = self._button(
            self.frame,
            "Продолжить",
            self.actions.continue_period,
            accent=True,
        )
        self.continue_button.grid(row=2, column=0, padx=12, pady=(0, 8))
        self.drag_widgets.extend((self.mode_label, self.time_label))

    def update(self) -> None:
        super().update()
        if widget_display_state(self.timer).waiting_for_continue:
            self.continue_button.grid()
        else:
            self.continue_button.grid_remove()


class CompactWidgetView(WidgetView):
    """Близкий к прежнему виджет с основной кнопкой старта или паузы."""

    def __init__(self, parent: tk.Widget, timer: TimerEngine, actions: WidgetActions) -> None:
        super().__init__(parent, timer, actions)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=2)

        self.mode_label = tk.Label(self.frame, anchor=tk.CENTER)
        self.mode_label.grid(row=0, column=0, sticky=tk.NSEW, padx=12, pady=(8, 0))
        self.time_label = tk.Label(self.frame, anchor=tk.CENTER)
        self.time_label.grid(row=1, column=0, sticky=tk.NSEW, padx=12)
        self.primary_button = self._button(
            self.frame,
            "Старт",
            self._handle_primary,
            accent=True,
        )
        self.primary_button.grid(row=2, column=0, padx=12, pady=(0, 10), ipadx=12)
        self.drag_widgets.extend((self.mode_label, self.time_label))

    def update(self) -> None:
        super().update()
        self.primary_button.config(text=self._primary_text())


class ExpandedWidgetView(WidgetView):
    """Расширенное представление с циклом и основными командами."""

    def __init__(self, parent: tk.Widget, timer: TimerEngine, actions: WidgetActions) -> None:
        super().__init__(parent, timer, actions)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        header = tk.Frame(self.frame, borderwidth=0, highlightthickness=0)
        header.grid(row=0, column=0, sticky=tk.EW, padx=14, pady=(10, 0))
        header.columnconfigure(0, weight=1)
        self.mode_label = tk.Label(header, anchor=tk.W)
        self.mode_label.grid(row=0, column=0, sticky=tk.W)
        self.cycle_label = tk.Label(header, anchor=tk.E)
        self.cycle_label.grid(row=0, column=1, sticky=tk.E)

        self.time_label = tk.Label(self.frame, anchor=tk.CENTER)
        self.time_label.grid(row=1, column=0, sticky=tk.NSEW, padx=14, pady=4)

        controls = tk.Frame(self.frame, borderwidth=0, highlightthickness=0)
        controls.grid(row=2, column=0, sticky=tk.EW, padx=12, pady=(0, 10))
        for column in range(4):
            controls.columnconfigure(column, weight=1)
        self.primary_button = self._button(
            controls,
            "Старт",
            self._handle_primary,
            accent=True,
        )
        self.primary_button.grid(row=0, column=0, sticky=tk.EW, padx=2)
        self.skip_button = self._button(controls, "Пропустить", self.actions.skip_period)
        self.skip_button.grid(row=0, column=1, sticky=tk.EW, padx=2)
        self.reset_button = self._button(controls, "Сброс", self.actions.reset_timer)
        self.reset_button.grid(row=0, column=2, sticky=tk.EW, padx=2)
        self.open_button = self._button(controls, "Открыть", self.actions.show_main_window)
        self.open_button.grid(row=0, column=3, sticky=tk.EW, padx=2)
        self.header = header
        self.controls = controls
        self.drag_widgets.extend((header, self.mode_label, self.cycle_label, self.time_label))

    def update(self) -> None:
        super().update()
        display = widget_display_state(self.timer)
        self.cycle_label.config(
            text=f"Рабочих периодов: {display.completed_work_periods}",
        )
        self.primary_button.config(text=self._primary_text())
        protected_state = tk.DISABLED if display.waiting_for_continue else tk.NORMAL
        self.skip_button.config(state=protected_state)
        self.reset_button.config(state=protected_state)

    def apply_style(
        self,
        palette: ThemePalette,
        parameters: WidgetSizeParameters,
    ) -> None:
        super().apply_style(palette, parameters)
        background = palette.card_background
        for container in (self.header, self.controls):
            container.configure(bg=background)
        self.cycle_label.configure(
            bg=background,
            fg=palette.text_secondary,
            font=("Segoe UI", parameters.mode_font),
        )


WIDGET_VIEW_CLASSES: dict[str, type[WidgetView]] = {
    WIDGET_TYPE_MINIMAL: MinimalWidgetView,
    WIDGET_TYPE_COMPACT: CompactWidgetView,
    WIDGET_TYPE_EXPANDED: ExpandedWidgetView,
}


def widget_view_class(widget_type: str) -> type[WidgetView]:
    """Возвращает класс представления после безопасной нормализации типа."""
    return WIDGET_VIEW_CLASSES[normalize_widget_type(widget_type)]


class WidgetWindow:
    """Одно окно с переключаемыми представлениями общего TimerEngine."""

    SAVE_DELAY_MS = 500

    def __init__(
        self,
        parent: tk.Tk,
        timer: TimerEngine,
        settings: AppSettings,
        actions: WidgetActions,
        save_settings: Callable[[AppSettings], None],
        on_visibility_requested: Callable[[bool], None],
        on_layout_changed: Callable[[AppSettings], None] | None = None,
        theme_manager: ThemeManager | None = None,
    ) -> None:
        self.parent = parent
        self.timer = timer
        self.settings = settings
        self.actions = actions
        self._save_settings = save_settings
        self._on_visibility_requested = on_visibility_requested
        self._on_layout_changed = on_layout_changed
        self.theme_manager = theme_manager
        self.window: tk.Toplevel | None = None
        self.view: WidgetView | None = None
        self._active_view_type: str | None = None
        self._drag_offset_x = 0
        self._drag_offset_y = 0
        self._save_after_id: str | None = None
        self._enable_configure_after_id: str | None = None
        self._accept_user_configure = False
        self._programmatic_size: tuple[int, int] | None = None
        self._last_size: tuple[int, int] | None = None
        self._content_expanded = False
        if self.theme_manager is not None:
            self.theme_manager.register(self.apply_theme)

    def apply_settings(self, settings: AppSettings) -> None:
        """Мгновенно применяет вид, размер и прежние параметры без сброса таймера."""
        previous_settings = getattr(self, "settings", None)
        previous_type = self._active_view_type
        captured_layout = self._capture_current_layout() if self.window is not None else None

        settings.widget_type = normalize_widget_type(settings.widget_type)
        settings.widget_layouts = normalize_widget_layouts(
            settings.widget_layouts,
            legacy_x=settings.widget_x,
            legacy_y=settings.widget_y,
            active_type=settings.widget_type,
        )
        if captured_layout is not None and previous_type is not None:
            incoming_layout = settings.widget_layouts[previous_type]
            if previous_type != settings.widget_type:
                settings.widget_layouts[previous_type] = captured_layout
            else:
                incoming_layout["x"] = captured_layout["x"]
                incoming_layout["y"] = captured_layout["y"]
                if previous_settings.widget_size == settings.widget_size:
                    settings.widget_layouts[previous_type] = captured_layout

        self.settings = settings
        if not settings.widget_enabled:
            if self.window is not None:
                self.window.withdraw()
            return

        self._ensure_window()
        if self.window is None:
            return
        if self._active_view_type != settings.widget_type:
            self._rebuild_view(settings.widget_type)

        layout = settings.widget_layouts[settings.widget_type]
        settings.widget_size = str(layout["size"])
        width = int(layout["width"])
        height = int(layout["height"])
        x, y = clamp_window_position(
            int(layout["x"]),
            int(layout["y"]),
            width,
            height,
            self._screen_bounds(),
        )
        layout["x"] = x
        layout["y"] = y
        settings.widget_x = x
        settings.widget_y = y
        minimum_width, minimum_height = WIDGET_MIN_SIZES[settings.widget_type]
        self.window.minsize(minimum_width, minimum_height)
        self.window.resizable(True, True)
        palette = self._palette()
        self.window.configure(bg=palette.card_background)
        self.window.attributes("-alpha", settings.widget_opacity / 100)
        self.window.attributes("-topmost", settings.widget_always_on_top)
        self._set_geometry(width, height, x, y)
        self._apply_view_style(width, height, settings.widget_size)
        self.update()
        self.window.deiconify()

    def update(self) -> None:
        """Обновляет активное представление без собственного цикла after()."""
        if (
            self.window is None
            or self.view is None
            or not self.settings.widget_enabled
        ):
            return
        self.view.update()
        self._fit_window_to_content()

    def apply_theme(self, palette: ThemePalette) -> None:
        """Обновляет открытый виджет без смены типа, геометрии или TimerEngine."""
        if self.window is None or self.view is None:
            return
        if self.theme_manager is not None:
            self.theme_manager.apply_to_window(self.window)
        width = max(1, self.window.winfo_width())
        height = max(1, self.window.winfo_height())
        parameters = widget_size_parameters(
            self.settings.widget_type,
            self.settings.widget_size,
            width,
            height,
        )
        self.view.apply_style(palette, parameters)
        self.view.update()
        self._fit_window_to_content()

    def is_visible(self) -> bool:
        """Возвращает фактическую видимость единственного Toplevel."""
        if self.window is None:
            return False
        try:
            return bool(self.window.winfo_exists()) and self.window.state() != "withdrawn"
        except tk.TclError:
            return False

    def discard_window(self) -> None:
        """Уничтожает частично созданное окно после ошибки показа."""
        window = self.window
        self.window = None
        self.view = None
        self._active_view_type = None
        self._accept_user_configure = False
        self._programmatic_size = None
        self._last_size = None
        self._content_expanded = False
        self._save_after_id = None
        self._enable_configure_after_id = None
        if window is None:
            return
        try:
            window.destroy()
        except tk.TclError:
            pass

    def _request_hide(self) -> None:
        """Передает закрытие крестиком единому контроллеру видимости."""
        self._on_visibility_requested(False)

    def _ensure_window(self) -> None:
        """Создает Toplevel один раз за весь срок жизни приложения."""
        if self.window is not None:
            return
        self.window = tk.Toplevel(self.parent)
        self.window.title("Виджет Pomodoro")
        self.window.protocol("WM_DELETE_WINDOW", self._request_hide)
        self.window.bind("<Configure>", self._on_configure)

    def _rebuild_view(self, widget_type: str) -> None:
        """Заменяет только разметку внутри уже существующего окна."""
        if self.window is None:
            return
        if self.view is not None:
            self.view.destroy()
        view_class = widget_view_class(widget_type)
        self.view = view_class(self.window, self.timer, self.actions)
        self._active_view_type = normalize_widget_type(widget_type)
        self._content_expanded = False
        for widget in self.view.drag_widgets:
            widget.bind("<ButtonPress-1>", self._start_drag)
            widget.bind("<B1-Motion>", self._drag)
            widget.bind("<ButtonRelease-1>", self._finish_drag)

    def _set_geometry(self, width: int, height: int, x: int, y: int) -> None:
        """Применяет сохраненную геометрию, не помечая ее как ручную."""
        if self.window is None:
            return
        self._accept_user_configure = False
        self._programmatic_size = (width, height)
        self._last_size = (width, height)
        self.window.geometry(f"{width}x{height}{x:+d}{y:+d}")
        if self._enable_configure_after_id is not None:
            self.window.after_cancel(self._enable_configure_after_id)
        self._enable_configure_after_id = self.window.after(
            250,
            self._enable_user_configure,
        )

    def _enable_user_configure(self) -> None:
        self._enable_configure_after_id = None
        self._accept_user_configure = True

    def _on_configure(self, event: tk.Event) -> None:
        """Перестраивает шрифты и отложенно сохраняет ручную геометрию."""
        if self.window is None or event.widget is not self.window:
            return
        width = max(1, int(event.width))
        height = max(1, int(event.height))
        size_changed = self._last_size is not None and self._last_size != (width, height)
        self._last_size = (width, height)

        if self._accept_user_configure and size_changed:
            self.settings.widget_size = WIDGET_SIZE_CUSTOM
            layout = self.settings.widget_layouts[self.settings.widget_type]
            layout["size"] = WIDGET_SIZE_CUSTOM
            self._programmatic_size = None
            self._content_expanded = False

        current_size = (
            WIDGET_SIZE_CUSTOM
            if self.settings.widget_size == WIDGET_SIZE_CUSTOM
            else self.settings.widget_size
        )
        self._apply_view_style(width, height, current_size)
        if self._accept_user_configure:
            self._schedule_layout_save()

    def _apply_view_style(self, width: int, height: int, widget_size: str) -> None:
        if self.view is None:
            return
        parameters = widget_size_parameters(
            self.settings.widget_type,
            widget_size,
            width,
            height,
        )
        self.view.apply_style(self._palette(), parameters)

    def _palette(self) -> ThemePalette:
        """Возвращает текущую общую палитру с безопасным fallback."""
        if self.theme_manager is not None:
            return self.theme_manager.palette
        from app.theme import get_palette

        return get_palette(self.settings.theme_name, self.settings.appearance_mode)

    def _fit_window_to_content(self) -> None:
        """Не дает DPI и длинным названиям обрезать элементы, не меняя пресет."""
        if self.window is None or self.view is None:
            return
        frame = getattr(self.view, "frame", None)
        if frame is None:
            return
        frame.update_idletasks()
        layout = self.settings.widget_layouts[self.settings.widget_type]
        target_width = int(layout["width"])
        target_height = int(layout["height"])
        required_width = frame.winfo_reqwidth()
        required_height = frame.winfo_reqheight()
        minimum_width, minimum_height = WIDGET_MIN_SIZES[self.settings.widget_type]
        fitted_width, fitted_height = content_fitted_dimensions(
            target_width,
            target_height,
            required_width,
            required_height,
            minimum_width,
            minimum_height,
        )
        self.window.minsize(
            max(minimum_width, required_width),
            max(minimum_height, required_height),
        )

        current_width = max(1, self.window.winfo_width())
        current_height = max(1, self.window.winfo_height())
        if (current_width, current_height) == (fitted_width, fitted_height):
            self._content_expanded = (
                fitted_width != target_width or fitted_height != target_height
            )
            return
        must_expand = current_width < fitted_width or current_height < fitted_height
        if not must_expand and not self._content_expanded:
            return

        x, y = clamp_window_position(
            int(layout["x"]),
            int(layout["y"]),
            fitted_width,
            fitted_height,
            self._screen_bounds(),
        )
        self._set_geometry(fitted_width, fitted_height, x, y)
        self._content_expanded = (
            fitted_width != target_width or fitted_height != target_height
        )

    def _schedule_layout_save(self) -> None:
        """Не пишет JSON на каждом пикселе перемещения или resize."""
        if self.window is None:
            return
        if self._save_after_id is not None:
            self.window.after_cancel(self._save_after_id)
        self._save_after_id = self.window.after(
            self.SAVE_DELAY_MS,
            self._persist_current_layout,
        )

    def _capture_current_layout(self) -> dict[str, int | str] | None:
        """Снимает геометрию окна без записи на диск."""
        if self.window is None or self._active_view_type is None:
            return None
        try:
            width = max(1, self.window.winfo_width())
            height = max(1, self.window.winfo_height())
            x = self.window.winfo_x()
            y = self.window.winfo_y()
        except tk.TclError:
            return None
        layout = self.settings.widget_layouts[self._active_view_type]
        layout.update(
            {
                "size": self.settings.widget_size,
                "width": width,
                "height": height,
                "x": x,
                "y": y,
            },
        )
        self.settings.widget_x = x
        self.settings.widget_y = y
        return deepcopy(layout)

    def _persist_current_layout(self) -> None:
        """Сохраняет один итог движения/resize и уведомляет форму настроек."""
        self._save_after_id = None
        layout = self._capture_current_layout()
        if layout is None:
            return
        self._save_settings(self.settings)
        if self._on_layout_changed is not None:
            self._on_layout_changed(self.settings)

    def _screen_bounds(self) -> tuple[int, int, int, int]:
        """Возвращает доступную виртуальную область, известную Tk."""
        if self.window is None:
            return (0, 0, 1, 1)
        try:
            x = self.window.winfo_vrootx()
            y = self.window.winfo_vrooty()
            width = self.window.winfo_vrootwidth()
            height = self.window.winfo_vrootheight()
            if width <= 1 or height <= 1:
                width = self.window.winfo_screenwidth()
                height = self.window.winfo_screenheight()
            return (x, y, width, height)
        except tk.TclError:
            return (0, 0, 1, 1)

    def _start_drag(self, event: tk.Event) -> None:
        """Запоминает точку начала перемещения за свободную область."""
        if self.window is None:
            return
        self._drag_offset_x = event.x_root - self.window.winfo_x()
        self._drag_offset_y = event.y_root - self.window.winfo_y()

    def _drag(self, event: tk.Event) -> None:
        """Перемещает окно без записи настроек на каждом событии мыши."""
        if self.window is None:
            return
        x = event.x_root - self._drag_offset_x
        y = event.y_root - self._drag_offset_y
        self.window.geometry(f"{x:+d}{y:+d}")

    def _finish_drag(self, _event: tk.Event) -> None:
        """Сохраняет только итоговую позицию после отпускания мыши."""
        self._persist_current_layout()
