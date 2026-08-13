"""Главное окно приложения Pomodoro Timer на Tkinter."""

from collections.abc import Callable
import tkinter as tk
from tkinter import messagebox, ttk

from app.autostart import AutostartService
from app.config import APP_NAME, DATA_DIR_WARNING, SETTINGS_FILE, STATISTICS_FILE
from app.models import AppSettings, TimerMode, TimeDisplayFormat
from app.notifications import NotificationService
from app.overrun_effects import (
    OverrunVisualController,
    OverrunVisualFrame,
    normalize_overrun_visual,
)
from app.statistics import StatisticsService
from app.storage import load_app_settings, save_app_settings
from app.theme import (
    APPEARANCE_DARK,
    APPEARANCE_LIGHT,
    CUSTOM_THEME_NAME,
    ThemeManager,
    Tooltip,
    normalize_custom_theme,
    normalize_appearance_mode,
    normalize_theme_name,
)
from app.timer_engine import TimerEngine
from app.ui.help_window import HelpView
from app.ui.overrun_surface import draw_beacon, draw_wave
from app.ui.settings_window import SettingsView
from app.ui.stats_view import StatsView
from app.ui.tray import TrayController
from app.ui.widget_window import WidgetActions, WidgetWindow
from app.widget_settings import normalize_widget_opacity


class MainWindow:
    """Главное окно с таймером, статистикой, настройками, справкой и треем."""

    def __init__(self) -> None:
        """Создает интерфейс и общую логику приложения."""
        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.resizable(False, False)
        self._settings_save_after_id: str | None = None

        self.settings = load_app_settings(SETTINGS_FILE)
        self.theme_manager = ThemeManager(self.root)
        self.theme_manager.apply(
            self.settings.theme_name,
            self.settings.appearance_mode,
            self.settings.custom_theme,
        )
        self.autostart = AutostartService()

        self.timer = TimerEngine(self.settings)
        self.statistics = StatisticsService(STATISTICS_FILE)
        self.notifications = NotificationService(
            self.root,
            self.settings,
            self.theme_manager,
        )
        self.widget_window = WidgetWindow(
            self.root,
            self.timer,
            self.settings,
            actions=WidgetActions(
                toggle_timer=self.toggle_timer_from_tray,
                continue_period=self.continue_manual_transition,
                skip_period=self.skip_period,
                reset_timer=self.reset,
                show_main_window=self.show_window,
            ),
            save_settings=lambda settings: save_app_settings(SETTINGS_FILE, settings),
            on_visibility_requested=self.set_widget_visibility,
            on_layout_changed=self._on_widget_layout_changed,
            theme_manager=self.theme_manager,
        )
        self.overrun_visual_controller = OverrunVisualController(
            self.root.after,
            self.root.after_cancel,
            self._apply_overrun_visual_frame,
        )

        self.tray = TrayController(
            show_window=self._schedule(self.show_window),
            hide_window=self._schedule(self.hide_to_tray),
            toggle_timer=self._schedule(self.toggle_timer_from_tray),
            reset_timer=self._schedule(self.reset),
            exit_app=self._schedule(self.exit_app),
        )
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        timer_tab = ttk.Frame(notebook, padding=24)
        notebook.add(timer_tab, text="Таймер")

        self.stats_view = StatsView(notebook, self.statistics)
        notebook.add(self.stats_view, text="Статистика")

        self.settings_view = SettingsView(
            notebook,
            self.settings,
            self.apply_settings,
            self.autostart.status(),
            on_theme_change=self.apply_theme_selection,
            on_custom_theme_preview=self.preview_custom_theme,
            on_custom_theme_apply=self.apply_custom_theme,
            on_theme_preview_cancel=self.cancel_theme_preview,
            on_overrun_preview=self.preview_overrun_visual,
            on_widget_opacity_change=self.set_widget_opacity,
            on_overrun_opacity_change=self.set_overrun_widget_opacity,
            theme_manager=self.theme_manager,
        )
        notebook.add(self.settings_view, text="Настройки")

        self.help_view = HelpView(notebook)
        notebook.add(self.help_view, text="Справка")

        toolbar = ttk.Frame(timer_tab, style="Toolbar.TFrame")
        toolbar.pack(fill=tk.X, pady=(0, 16))
        ttk.Label(toolbar, text="Фокус-сессия", style="Heading.TLabel").pack(side=tk.LEFT)
        self.theme_toggle_button = ttk.Button(
            toolbar,
            command=self.toggle_appearance_mode,
            style="Ghost.TButton",
        )
        self.theme_toggle_button.pack(side=tk.RIGHT)
        self.theme_toggle_tooltip = Tooltip(
            self.theme_toggle_button,
            "Переключить светлый или тёмный режим",
            self.theme_manager,
        )

        palette = self.theme_manager.palette
        self.timer_border = tk.Frame(
            timer_tab,
            borderwidth=0,
            highlightthickness=3,
            highlightbackground=palette.card_background,
            bg=palette.card_background,
        )
        self.timer_border.pack(fill=tk.BOTH, expand=True)
        self.timer_card = ttk.Frame(
            self.timer_border,
            style="TimerCard.TFrame",
            padding=(34, 28),
        )
        self.timer_card.pack(fill=tk.BOTH, expand=True)

        self.mode_label = ttk.Label(
            self.timer_card,
            text=self.timer.mode_name(),
            style=self.theme_manager.mode_style(
                self.timer.state.mode,
                self.timer.state.waiting_for_continue,
            ),
        )
        self.mode_label.pack(pady=(0, 8))

        self.timer_display = tk.Frame(
            self.timer_card,
            borderwidth=0,
            highlightthickness=0,
            bg=palette.card_background,
        )
        self.timer_display.pack(pady=(6, 10))
        self.timer_display.columnconfigure(1, weight=1)
        self.main_left_beacon = tk.Canvas(
            self.timer_display,
            width=20,
            height=20,
            borderwidth=0,
            highlightthickness=0,
            bg=palette.card_background,
        )
        self.main_left_beacon.grid(row=0, column=0, padx=(0, 8))
        self.time_label = ttk.Label(
            self.timer_display,
            text=self.timer.formatted_time(),
            style="TimerCard.Timer.TLabel",
        )
        self.time_label.grid(row=0, column=1)
        self.main_right_beacon = tk.Canvas(
            self.timer_display,
            width=20,
            height=20,
            borderwidth=0,
            highlightthickness=0,
            bg=palette.card_background,
        )
        self.main_right_beacon.grid(row=0, column=2, padx=(8, 0))
        self.main_wave_canvas = tk.Canvas(
            self.timer_display,
            height=10,
            width=240,
            borderwidth=0,
            highlightthickness=0,
            bg=palette.card_background,
        )
        self.main_wave_canvas.grid(row=1, column=1, sticky=tk.EW, pady=(2, 0))

        self.status_label = ttk.Label(
            self.timer_card,
            text="Таймер остановлен",
            style="TimerCard.Secondary.TLabel",
        )
        self.status_label.pack(pady=(0, 22))

        controls = ttk.Frame(self.timer_card, style="TimerCard.TFrame")
        controls.pack()

        self.start_button = ttk.Button(
            controls,
            text="Старт",
            command=self.start,
            style="Accent.TButton",
        )
        self.start_button.grid(row=0, column=0, padx=5)

        self.pause_button = ttk.Button(
            controls,
            text="Пауза",
            command=self.toggle_pause,
            state=tk.DISABLED,
        )
        self.pause_button.grid(row=0, column=1, padx=5)

        self.skip_button = ttk.Button(
            controls,
            text="Пропустить период",
            command=self.skip_period,
        )
        self.skip_button.grid(
            row=0,
            column=2,
            padx=5,
        )
        self.reset_button = ttk.Button(controls, text="Сброс", command=self.reset)
        self.reset_button.grid(row=0, column=3, padx=5)

        self.continue_button = ttk.Button(
            controls,
            text="Продолжить и начать следующий период",
            command=self.continue_manual_transition,
            state=tk.DISABLED,
            style="Accent.TButton",
        )
        self.continue_button.grid(row=1, column=0, columnspan=4, pady=(12, 0))

        self.widget_toggle_button = ttk.Button(
            controls,
            text="Показать виджет",
            command=self.toggle_widget_visibility,
            style="Ghost.TButton",
        )
        self.widget_toggle_button.grid(
            row=2,
            column=0,
            columnspan=4,
            pady=(12, 0),
        )

        self._sync_theme_button()
        self.set_widget_visibility(self.settings.widget_enabled, persist=False)
        self.apply_theme_selection(
            self.settings.theme_name,
            self.settings.appearance_mode,
            persist=False,
        )

        if DATA_DIR_WARNING:
            self.root.after(300, lambda: messagebox.showwarning("Portable-режим", DATA_DIR_WARNING))

    def run(self) -> None:
        """Запускает трей и цикл обработки событий Tkinter."""
        self.tray.start()
        self._schedule_tick()
        if self.settings.minimize_to_tray_on_start:
            self.root.after(200, self.hide_to_tray)
        self.root.mainloop()

    def start(self) -> None:
        """Запускает отсчет времени."""
        if not self.timer.start():
            self._refresh_labels()
            return
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL, text="Пауза")
        self._refresh_labels()

    def toggle_pause(self) -> None:
        """Ставит таймер на паузу или продолжает отсчет."""
        if not self.timer.toggle_pause():
            self._refresh_labels()
            return
        self._sync_timer_buttons()
        self._refresh_labels()

    def skip_period(self) -> None:
        """Пропускает текущий период Pomodoro."""
        controller = getattr(self, "overrun_visual_controller", None)
        if controller is not None:
            controller.stop_preview()
        skipped_mode = self.timer.skip_period()
        if skipped_mode is None:
            self._refresh_labels()
            return
        self.statistics.record_skipped_period(skipped_mode)
        self.stats_view.refresh()
        self._refresh_labels()

    def apply_settings(self, settings: AppSettings, autostart_changed: bool = False) -> None:
        """Сохраняет настройки и применяет их к текущему таймеру."""
        should_reset_timer = self._duration_settings_changed(settings)
        if autostart_changed:
            # Autostart changes HKCU Run, so it must happen only after an explicit user toggle.
            try:
                self.autostart.set_enabled(settings.autostart_enabled)
            except RuntimeError as error:
                messagebox.showwarning("Автозапуск", str(error))
                settings.autostart_enabled = self.settings.autostart_enabled
                self.settings_view.autostart_enabled_var.set(settings.autostart_enabled)

        self._cancel_deferred_settings_save()
        self.settings_view.update_autostart_status(self.autostart.status())
        settings.overrun_visual = normalize_overrun_visual(settings.overrun_visual)
        self.settings = settings
        self.apply_theme_selection(
            settings.theme_name,
            settings.appearance_mode,
            custom_theme=settings.custom_theme,
            persist=False,
        )
        self.timer.update_settings(settings)
        self.notifications.update_settings(settings)
        self.set_widget_visibility(settings.widget_enabled, persist=False)
        save_app_settings(SETTINGS_FILE, settings)
        if should_reset_timer and not self.timer.state.waiting_for_continue:
            self.timer.reset()
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED, text="Пауза")
        self._refresh_labels()

    def reset(self) -> None:
        """Сбрасывает таймер и обновляет подписи в окне."""
        controller = getattr(self, "overrun_visual_controller", None)
        if controller is not None:
            controller.stop_preview()
        if not self.timer.reset():
            self._refresh_labels()
            return
        self.statistics.record_reset()
        self.stats_view.refresh()
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED, text="Пауза")
        self._refresh_labels()

    def show_window(self) -> None:
        """Показывает главное окно из трея."""
        self._sync_widget_visibility()
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def hide_to_tray(self) -> None:
        """Скрывает главное окно, оставляя таймер, виджет и трей работать."""
        self.root.withdraw()

    def on_window_close(self) -> None:
        """Обрабатывает закрытие окна согласно настройке пользователя."""
        if self.settings.close_to_tray:
            self.hide_to_tray()
        else:
            self.exit_app()

    def exit_app(self) -> None:
        """Полностью завершает приложение и убирает иконку трея."""
        self._flush_deferred_settings_save()
        overrun = self.timer.finalize_overrun_on_exit()
        if overrun is not None:
            self.statistics.record_overrun(overrun.mode, overrun.duration_seconds)
        self.notifications.dismiss()
        controller = getattr(self, "overrun_visual_controller", None)
        if controller is not None:
            controller.stop()
        self.tray.stop()
        self.root.destroy()

    def toggle_timer_from_tray(self) -> None:
        """Запускает или ставит таймер на паузу из меню трея."""
        if self.timer.state.waiting_for_continue:
            # Во время превышения команда трея не должна незаметно остановить
            # подсчет. Главное окно содержит явную кнопку продолжения.
            self.show_window()
            self._refresh_labels()
            return
        if self.timer.state.is_running:
            self.timer.pause()
        else:
            self.timer.start()
        self._sync_timer_buttons()
        self._refresh_labels()

    def toggle_widget_visibility(self) -> None:
        """Переключает виджет единственной пользовательской кнопкой."""
        self.set_widget_visibility(not self.widget_window.is_visible())

    def toggle_appearance_mode(self) -> None:
        """Быстро переключает светлый/тёмный режим общей активной темы."""
        next_mode = (
            APPEARANCE_LIGHT
            if self.settings.appearance_mode == APPEARANCE_DARK
            else APPEARANCE_DARK
        )
        self.apply_theme_selection(self.settings.theme_name, next_mode)

    def apply_theme_selection(
        self,
        theme_name: str,
        appearance_mode: str,
        *,
        custom_theme: object = None,
        persist: bool = True,
    ) -> bool:
        """Применяет тему ко всем открытым окнам и сохраняет только реальный выбор."""
        normalized_theme = normalize_theme_name(theme_name)
        normalized_mode = normalize_appearance_mode(appearance_mode)
        normalized_custom = normalize_custom_theme(
            self.settings.custom_theme if custom_theme is None else custom_theme,
        )
        changed = (
            self.settings.theme_name != normalized_theme
            or self.settings.appearance_mode != normalized_mode
            or self.settings.custom_theme != normalized_custom
        )
        self.settings.theme_name = normalized_theme
        self.settings.appearance_mode = normalized_mode
        self.settings.custom_theme = normalized_custom
        self.theme_manager.apply(normalized_theme, normalized_mode, normalized_custom)
        if hasattr(self, "settings_view"):
            self.settings_view.sync_theme(normalized_theme, normalized_mode)
        self._sync_theme_button()
        if hasattr(self, "mode_label"):
            self.mode_label.config(
                style=self.theme_manager.mode_style(
                    self.timer.state.mode,
                    self.timer.state.waiting_for_continue,
                ),
            )
        if hasattr(self, "overrun_visual_controller"):
            self._sync_overrun_visual()
        if changed and persist:
            save_app_settings(SETTINGS_FILE, self.settings)
        return changed

    def preview_custom_theme(
        self,
        custom_theme: dict[str, dict[str, str]],
        appearance_mode: str,
    ) -> None:
        """Временно оформляет все окна черновиком без изменения настроек и JSON."""
        normalized_mode = normalize_appearance_mode(appearance_mode)
        self.theme_manager.apply(CUSTOM_THEME_NAME, normalized_mode, custom_theme)
        if hasattr(self, "mode_label"):
            self.mode_label.config(
                style=self.theme_manager.mode_style(
                    self.timer.state.mode,
                    self.timer.state.waiting_for_continue,
                ),
            )
        self._sync_overrun_visual()

    def apply_custom_theme(
        self,
        custom_theme: dict[str, dict[str, str]],
        appearance_mode: str,
    ) -> None:
        """Сохраняет подтверждённую пользовательскую копию одним действием."""
        self.apply_theme_selection(
            CUSTOM_THEME_NAME,
            appearance_mode,
            custom_theme=custom_theme,
        )

    def cancel_theme_preview(self) -> None:
        """Возвращает сохранённое оформление после отмены редактора."""
        self.theme_manager.apply(
            self.settings.theme_name,
            self.settings.appearance_mode,
            self.settings.custom_theme,
        )
        if hasattr(self, "mode_label"):
            self.mode_label.config(
                style=self.theme_manager.mode_style(
                    self.timer.state.mode,
                    self.timer.state.waiting_for_continue,
                ),
            )
        self._sync_overrun_visual()

    def preview_overrun_visual(
        self,
        mode: TimerMode,
        visual: dict[str, object],
    ) -> None:
        """Запускает краткий визуальный пример без команд TimerEngine."""
        self.overrun_visual_controller.start_preview(
            mode,
            visual,
            self.theme_manager.palette,
        )

    def set_widget_opacity(self, opacity: int) -> None:
        """Сразу меняет alpha и сохраняет итог ползунка с задержкой."""
        self.settings.widget_opacity = normalize_widget_opacity(opacity)
        self.widget_window.apply_opacity()
        if hasattr(self, "settings_view"):
            self.settings_view.sync_widget_opacity(self.settings.widget_opacity)
        self._schedule_settings_save()

    def set_overrun_widget_opacity(self, enabled: bool) -> None:
        """Сразу включает временные 1.0, не меняя постоянное значение alpha."""
        visual = dict(self.settings.overrun_visual)
        visual["opaque_widget_during_overrun"] = bool(enabled)
        self.settings.overrun_visual = normalize_overrun_visual(visual)
        self.widget_window.apply_opacity()
        self._schedule_settings_save()

    def _schedule_settings_save(self) -> None:
        """Объединяет поток изменений ползунка в одну запись JSON."""
        self._cancel_deferred_settings_save()
        self._settings_save_after_id = self.root.after(
            500,
            self._flush_deferred_settings_save,
        )

    def _cancel_deferred_settings_save(self) -> None:
        after_id = getattr(self, "_settings_save_after_id", None)
        self._settings_save_after_id = None
        if after_id is None:
            return
        try:
            self.root.after_cancel(after_id)
        except tk.TclError:
            pass

    def _flush_deferred_settings_save(self) -> None:
        """Сохраняет постоянные настройки; временный alpha в модель не входит."""
        if getattr(self, "_settings_save_after_id", None) is None:
            return
        self._cancel_deferred_settings_save()
        save_app_settings(SETTINGS_FILE, self.settings)

    def _sync_theme_button(self) -> None:
        """Обновляет понятный текст и подсказку быстрого переключателя."""
        if not hasattr(self, "theme_toggle_button"):
            return
        dark_is_active = self.settings.appearance_mode == APPEARANCE_DARK
        target_label = "Светлый режим" if dark_is_active else "Тёмный режим"
        self.theme_toggle_button.config(text=target_label)
        if hasattr(self, "theme_toggle_tooltip"):
            self.theme_toggle_tooltip.text = (
                f"Переключить на {target_label.lower()}. "
                f"Текущая тема: {self.settings.theme_name}."
            )

    def set_widget_visibility(self, visible: bool, *, persist: bool = True) -> bool:
        """Применяет, сохраняет и отражает единое состояние видимости виджета."""
        requested_visibility = bool(visible)
        self.settings.widget_enabled = requested_visibility
        error: Exception | None = None
        try:
            self.widget_window.apply_settings(self.settings)
            if self.widget_window.is_visible() != requested_visibility:
                raise RuntimeError("окно не перешло в запрошенное состояние")
        except Exception as caught_error:  # UI boundary: show must not stop the timer.
            error = caught_error
            if requested_visibility:
                self.widget_window.discard_window()

        actual_visibility = self.widget_window.is_visible()
        self.settings.widget_enabled = actual_visibility
        if persist or actual_visibility != requested_visibility:
            try:
                save_app_settings(SETTINGS_FILE, self.settings)
            except OSError as save_error:
                if error is None:
                    error = save_error
        self._sync_widget_visibility()

        if error is not None:
            action = "показать" if requested_visibility else "скрыть"
            messagebox.showwarning(
                "Виджет",
                f"Не удалось {action} виджет: {error}",
            )
            return False
        return True

    def _sync_widget_visibility(self) -> None:
        """Сверяет подпись кнопки и настройку с фактическим Toplevel."""
        visible = self.widget_window.is_visible()
        self.settings.widget_enabled = visible
        if hasattr(self, "widget_toggle_button"):
            self.widget_toggle_button.config(
                text="Скрыть виджет" if visible else "Показать виджет",
            )

    def _on_widget_layout_changed(self, settings: AppSettings) -> None:
        """Синхронизирует ручной размер с уже открытой формой настроек."""
        self.settings = settings
        if hasattr(self, "settings_view"):
            self.settings_view.sync_widget_layouts(settings)

    def continue_after_notification(self) -> None:
        """Продолжает таймер через общий обработчик кнопок уведомления и окна."""
        self.continue_manual_transition()

    def continue_manual_transition(self) -> None:
        """Один раз сохраняет превышение и запускает ожидающий период."""
        overrun = self.timer.continue_to_next_period()
        if overrun is None:
            self._refresh_labels()
            return

        self.statistics.record_overrun(overrun.mode, overrun.duration_seconds)
        self.notifications.dismiss()
        self.stats_view.refresh()
        self._sync_timer_buttons()
        self._refresh_labels()

    def _schedule_tick(self) -> None:
        """Обновляет таймер один раз в секунду через планировщик Tkinter."""
        completed_period = self.timer.tick()
        if completed_period is not None:
            self.statistics.record_completed_period(
                completed_period.mode,
                completed_period.duration_seconds,
                self.settings.use_long_break,
            )
            self.notifications.notify_period_finished(
                completed_period.mode,
                completed_period.next_mode,
                self.continue_after_notification,
            )
            self.stats_view.refresh()
        self._refresh_labels()
        self.root.after(1000, self._schedule_tick)

    def _refresh_labels(self) -> None:
        """Обновляет подписи в интерфейсе по текущему состоянию таймера."""
        controller = getattr(self, "overrun_visual_controller", None)
        if controller is None or not controller.preview_active:
            self.mode_label.config(
                text=self.timer.mode_name(),
                style=self.theme_manager.mode_style(
                    self.timer.state.mode,
                    self.timer.state.waiting_for_continue,
                ),
            )
            self.time_label.config(text=self.timer.formatted_time())
        self.widget_window.update()
        self._sync_overrun_visual()

        if self.timer.state.waiting_for_continue:
            self.status_label.config(
                text="Период завершен — превышение считается до продолжения",
            )
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.DISABLED, text="Пауза")
            self.skip_button.config(state=tk.DISABLED)
            self.reset_button.config(state=tk.DISABLED)
            self.continue_button.config(state=tk.NORMAL)
            return

        self.skip_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)
        self.continue_button.config(state=tk.DISABLED)
        if self.timer.state.is_running:
            self.status_label.config(text="Таймер запущен")
            self.pause_button.config(text="Пауза")
        elif str(self.pause_button["state"]) == tk.DISABLED:
            self.status_label.config(text="Таймер остановлен")
            self.pause_button.config(text="Пауза")
        else:
            self.status_label.config(text="Таймер на паузе")
            self.pause_button.config(text="Продолжить")

    def _sync_overrun_visual(self) -> None:
        """Передаёт контроллеру только фактический переход в/из превышения."""
        if not hasattr(self, "overrun_visual_controller"):
            return
        state = self.timer.state
        mode = state.overrun_mode or state.mode
        self.overrun_visual_controller.sync_actual(
            state.waiting_for_continue,
            mode,
            self.settings.overrun_visual,
            self.theme_manager.palette,
        )

    def _apply_overrun_visual_frame(self, frame: OverrunVisualFrame) -> None:
        """Применяет единый кадр к карточке и единственному окну виджета."""
        self.theme_manager.apply_timer_effect(
            frame.digits_color,
            frame.card_background,
        )
        if hasattr(self, "timer_border"):
            palette = self.theme_manager.palette
            background = frame.card_background or palette.card_background
            border = frame.border_color or background
            self.timer_border.configure(
                bg=background,
                highlightbackground=border,
                highlightcolor=border,
            )
            self.timer_display.configure(bg=background)
            self.time_label.configure(
                font=("Segoe UI Semibold", max(20, round(52 * frame.digit_scale))),
            )
            draw_beacon(self.main_left_beacon, frame, palette)
            draw_beacon(self.main_right_beacon, frame, palette)
            draw_wave(self.main_wave_canvas, frame, palette)
        if hasattr(self, "widget_window"):
            self.widget_window.apply_overrun_visual(frame)
        if not hasattr(self, "mode_label"):
            return

        if frame.preview and frame.mode is not None:
            names = {
                TimerMode.WORK: "Переработка",
                TimerMode.SHORT_BREAK: "Короткий отдых сверх нормы",
                TimerMode.LONG_BREAK: "Длинный отдых сверх нормы",
            }
            preview_time = (
                "+00:03"
                if self.settings.time_display_format == TimeDisplayFormat.MINUTES_SECONDS.value
                else "+00:00:03"
            )
            self.mode_label.config(
                text=names[frame.mode],
                style=self.theme_manager.mode_style(frame.mode, True),
            )
            self.time_label.config(text=preview_time)
        elif not frame.active:
            self.mode_label.config(
                text=self.timer.mode_name(),
                style=self.theme_manager.mode_style(
                    self.timer.state.mode,
                    self.timer.state.waiting_for_continue,
                ),
            )
            self.time_label.config(text=self.timer.formatted_time())

    def _sync_timer_buttons(self) -> None:
        """Синхронизирует кнопки после команд из трея."""
        if self.timer.state.waiting_for_continue:
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.DISABLED, text="Пауза")
            self.skip_button.config(state=tk.DISABLED)
            self.reset_button.config(state=tk.DISABLED)
            self.continue_button.config(state=tk.NORMAL)
            return

        self.skip_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)
        self.continue_button.config(state=tk.DISABLED)
        if self.timer.state.is_running:
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL, text="Пауза")
        else:
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.NORMAL, text="Продолжить")

    def _duration_settings_changed(self, new_settings: AppSettings) -> bool:
        """Проверяет, изменились ли длительности периодов таймера."""
        return (
            self.settings.work_minutes != new_settings.work_minutes
            or self.settings.short_break_minutes != new_settings.short_break_minutes
            or self.settings.long_break_minutes != new_settings.long_break_minutes
        )

    def _schedule(self, callback: Callable[[], None]) -> Callable[[], None]:
        """Безопасно выполняет команду трея в потоке Tkinter."""
        def wrapped() -> None:
            self.root.after(0, callback)

        return wrapped
