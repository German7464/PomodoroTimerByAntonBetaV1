"""Единственное Qt-окно с семью представлениями общего Pomodoro-таймера."""

from __future__ import annotations

from collections.abc import Callable
from copy import deepcopy
from dataclasses import dataclass

from PySide6.QtCore import QEvent, QPoint, QRect, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QWidget

from app.models import AppSettings, TimerMode, TimeDisplayFormat
from app.i18n import localization_manager, timer_mode_text, tr, trn
from app.overrun_effects import INACTIVE_FRAME, OverrunVisualFrame
from app.theme import ThemeManager, ThemePalette, mode_color
from app.timer_engine import TimerEngine
from app.ui.components import AppButton, Card, FlowLayout
from app.ui.design_system import TOKENS
from app.ui.qt_app import Debouncer
from app.ui.icons import application_icon
from app.ui.timer_visual import TimerVisual
from app.widget_settings import (
    WIDGET_MIN_SIZES,
    WIDGET_SIZE_CUSTOM,
    WIDGET_TYPE_COMPACT,
    WIDGET_TYPE_EXPANDED,
    WIDGET_TYPE_MICRO,
    WIDGET_TYPE_MINIMAL,
    WIDGET_TYPE_RING,
    WIDGET_TYPE_ROW,
    WIDGET_TYPE_SCOREBOARD,
    WidgetSizeParameters,
    clamp_window_position,
    effective_widget_alpha,
    normalize_widget_layouts,
    normalize_widget_type,
    widget_size_parameters,
)


@dataclass(frozen=True)
class WidgetActions:
    toggle_timer: Callable[[], None]
    continue_period: Callable[[], None]
    skip_period: Callable[[], None]
    reset_timer: Callable[[], None]
    show_main_window: Callable[[], None]


@dataclass(frozen=True)
class WidgetDisplayState:
    mode_name: str
    formatted_time: str
    completed_work_periods: int
    waiting_for_continue: bool
    primary_text: str


PRIMARY_ACTION_KEYS = ("action.start", "action.pause", "action.continue")


def primary_action_texts() -> tuple[str, ...]:
    return tuple(tr(key) for key in PRIMARY_ACTION_KEYS)


def widget_display_state(timer: TimerEngine) -> WidgetDisplayState:
    if timer.state.waiting_for_continue:
        primary_text = tr("action.continue")
    elif timer.state.is_running:
        primary_text = tr("action.pause")
    elif timer.state.remaining_seconds < timer.current_period_duration_seconds():
        primary_text = tr("action.continue")
    else:
        primary_text = tr("action.start")
    return WidgetDisplayState(
        timer_mode_text(
            timer.state.overrun_mode or timer.state.mode,
            timer.state.waiting_for_continue,
        ),
        timer.formatted_time(), timer.state.completed_work_periods,
        timer.state.waiting_for_continue, primary_text,
    )


def ring_progress(timer: TimerEngine) -> float | None:
    if timer.state.waiting_for_continue:
        return None
    duration = max(1, timer.current_period_duration_seconds())
    elapsed = duration - timer.state.remaining_seconds
    return min(1.0, max(0.0, elapsed / duration))


class WidgetView(QWidget):
    """Общая основа без таймера и без анимационного цикла."""

    def __init__(self, parent: QWidget, timer: TimerEngine, actions: WidgetActions, theme_manager: ThemeManager) -> None:
        super().__init__(parent)
        self.timer = timer
        self.actions = actions
        self.theme_manager = theme_manager
        self.timer_visual: TimerVisual
        self.primary_button: AppButton | None = None
        self.overrun_frame = INACTIVE_FRAME
        self._animations_enabled = lambda: bool(
            self.timer.settings.overrun_visual.get("animations_enabled", True)
        )
        localization_manager().language_changed.connect(self._retranslate_ui)

    def update_view(self) -> None:
        display = widget_display_state(self.timer)
        self.timer_visual.set_state(
            display.mode_name, display.formatted_time, self.timer.state.mode,
            display.waiting_for_continue,
        )
        if self.primary_button is not None:
            self.primary_button.setText(display.primary_text)
            primary_visible = self._primary_visible(display)
            if not primary_visible and self.primary_button.hasFocus():
                self.focusNextChild()
            self.primary_button.setVisible(primary_visible)
            self.primary_button.setFocusPolicy(
                Qt.FocusPolicy.StrongFocus if primary_visible else Qt.FocusPolicy.NoFocus
            )
        self._after_update(display)

    def _after_update(self, _display: WidgetDisplayState) -> None:
        pass

    def _primary_visible(self, _display: WidgetDisplayState) -> bool:
        return True

    def _handle_primary(self) -> None:
        if self.timer.state.waiting_for_continue:
            self.actions.continue_period()
        else:
            self.actions.toggle_timer()

    def _make_primary_button(self, text: str) -> AppButton:
        button = AppButton(
            text,
            self,
            variant="primary",
            theme_manager=self.theme_manager,
            reserved_texts=primary_action_texts(),
            animations_enabled=self._animations_enabled,
        )
        button.clicked.connect(self._handle_primary)
        return button

    def _retranslate_ui(self, _language_code: str) -> None:
        if self.primary_button is not None:
            self.primary_button.set_reserved_texts(primary_action_texts())
        self.update_view()
        self.updateGeometry()

    def apply_style(self, _palette: ThemePalette, parameters: WidgetSizeParameters) -> None:
        self.timer_visual.set_base_font_size(parameters.time_font, parameters.mode_font)
        if self.primary_button is not None:
            font = self.primary_button.font()
            font.setPointSize(parameters.button_font)
            self.primary_button.setFont(font)

    def apply_overrun_visual(self, frame: OverrunVisualFrame) -> None:
        self.overrun_frame = frame
        self.timer_visual.apply_overrun_frame(
            frame,
            short_format=self.timer.settings.time_display_format == TimeDisplayFormat.MINUTES_SECONDS.value,
        )
        self.update_view()


class MinimalWidgetView(WidgetView):
    def __init__(self, parent, timer, actions, theme_manager) -> None:
        super().__init__(parent, timer, actions, theme_manager)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        self.timer_visual = TimerVisual(theme_manager, self, base_font_size=28, mode_font_size=10)
        layout.addWidget(self.timer_visual, 1)
        self.primary_button = self._make_primary_button(tr("action.continue"))
        layout.addWidget(self.primary_button)

    def _primary_visible(self, display: WidgetDisplayState) -> bool:
        return display.waiting_for_continue


class CompactWidgetView(WidgetView):
    def __init__(self, parent, timer, actions, theme_manager) -> None:
        super().__init__(parent, timer, actions, theme_manager)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        self.timer_visual = TimerVisual(theme_manager, self, base_font_size=28, mode_font_size=10)
        layout.addWidget(self.timer_visual, 1)
        self.primary_button = self._make_primary_button(tr("action.start"))
        layout.addWidget(self.primary_button)


class ExpandedWidgetView(WidgetView):
    def __init__(self, parent, timer, actions, theme_manager) -> None:
        super().__init__(parent, timer, actions, theme_manager)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(TOKENS.spacing.xs, TOKENS.spacing.xs, TOKENS.spacing.xs, TOKENS.spacing.xs)
        layout.setSpacing(TOKENS.spacing.xs)
        self.timer_visual = TimerVisual(theme_manager, self, base_font_size=34, mode_font_size=11)
        layout.addWidget(self.timer_visual, 1)
        self.cycle_label = QLabel(trn("widget.completed_work_periods", 0), self)
        self.cycle_label.setProperty("role", "caption")
        self.cycle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.cycle_label)
        self.action_panel = QWidget(self)
        self.action_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.action_layout = FlowLayout(
            self.action_panel,
            horizontal_spacing=TOKENS.spacing.xs,
            vertical_spacing=TOKENS.spacing.xs,
        )
        self.primary_button = self._make_primary_button(tr("action.start"))
        self.skip_button = AppButton(
            tr("action.skip"), self.action_panel, variant="ghost", theme_manager=theme_manager,
            animations_enabled=self._animations_enabled,
        )
        self.skip_button.clicked.connect(actions.skip_period)
        self.reset_button = AppButton(
            tr("action.reset"), self.action_panel, variant="ghost", theme_manager=theme_manager,
            animations_enabled=self._animations_enabled,
        )
        self.reset_button.clicked.connect(actions.reset_timer)
        self.open_button = AppButton(
            tr("action.open"), self.action_panel, variant="ghost", icon_name="window",
            theme_manager=theme_manager, animations_enabled=self._animations_enabled,
        )
        self.open_button.setAccessibleName(tr("action.open_main_window"))
        self.open_button.setToolTip(tr("action.open_main_window"))
        self.open_button.clicked.connect(actions.show_main_window)
        for button in (self.primary_button, self.skip_button, self.reset_button, self.open_button):
            self.action_layout.addWidget(button)
        layout.addWidget(self.action_panel)
        self._open_button_compact: bool | None = None

    def _after_update(self, display: WidgetDisplayState) -> None:
        self.cycle_label.setText(
            trn("widget.completed_work_periods", display.completed_work_periods)
        )
        self.skip_button.setEnabled(not display.waiting_for_continue)
        self.reset_button.setEnabled(not display.waiting_for_continue)
        self._update_action_layout()

    def apply_style(self, palette, parameters) -> None:
        super().apply_style(palette, parameters)
        for button in (self.skip_button, self.reset_button, self.open_button):
            font = button.font()
            font.setPointSize(parameters.button_font)
            button.setFont(font)
            button.updateGeometry()
        if self.primary_button is not None:
            self.primary_button.updateGeometry()
        self._update_action_layout()

    def resizeEvent(self, event) -> None:  # noqa: N802 - Qt API
        super().resizeEvent(event)
        self._update_action_layout()

    def _update_action_layout(self) -> None:
        """Сохраняет полные подписи; при нехватке ширины компактным становится только «Открыть»."""
        if not hasattr(self, "action_layout"):
            return
        outer_width = TOKENS.spacing.xs * 2
        available_width = max(1, self.width() - outer_width)
        full_row_width = (
            self.primary_button.sizeHint().width()
            + self.skip_button.sizeHint().width()
            + self.reset_button.sizeHint().width()
            + self.open_button.width_for_text(tr("action.open"))
            + TOKENS.spacing.xs * 3
        )
        compact = available_width < full_row_width
        if compact != self._open_button_compact:
            self._open_button_compact = compact
            self.open_button.setText("" if compact else tr("action.open"))
            self.open_button.updateGeometry()
        required_height = self.action_layout.heightForWidth(available_width)
        if self.action_panel.minimumHeight() != required_height:
            self.action_panel.setMinimumHeight(required_height)
        self.action_layout.invalidate()
        self.action_panel.updateGeometry()

    def _retranslate_ui(self, language_code: str) -> None:
        self.skip_button.setText(tr("action.skip"))
        self.reset_button.setText(tr("action.reset"))
        self.open_button.setAccessibleName(tr("action.open_main_window"))
        self.open_button.setToolTip(tr("action.open_main_window"))
        self._open_button_compact = None
        super()._retranslate_ui(language_code)
        self._update_action_layout()


class MicroWidgetView(WidgetView):
    def __init__(self, parent, timer, actions, theme_manager) -> None:
        super().__init__(parent, timer, actions, theme_manager)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(2)
        self.timer_visual = TimerVisual(theme_manager, self, base_font_size=25, mode_font_size=9, show_mode=False)
        layout.addWidget(self.timer_visual, 1)
        self.primary_button = self._make_primary_button(tr("action.continue"))
        layout.addWidget(self.primary_button)

    def _after_update(self, display: WidgetDisplayState) -> None:
        self.timer_visual.mode_label.setVisible(display.waiting_for_continue or self.overrun_frame.preview)

    def _primary_visible(self, display: WidgetDisplayState) -> bool:
        return display.waiting_for_continue


class RowWidgetView(WidgetView):
    def __init__(self, parent, timer, actions, theme_manager) -> None:
        super().__init__(parent, timer, actions, theme_manager)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        self.mode_label = QLabel(timer_mode_text(TimerMode.WORK), self)
        self.mode_label.setProperty("role", "mode")
        self.mode_label.setWordWrap(True)
        layout.addWidget(self.mode_label, 1)
        self.timer_visual = TimerVisual(theme_manager, self, base_font_size=26, mode_font_size=9, show_mode=False)
        layout.addWidget(self.timer_visual, 2)
        self.primary_button = self._make_primary_button(tr("action.start"))
        layout.addWidget(self.primary_button, 1)
        theme_manager.register(self._apply_row_theme)

    def _after_update(self, display: WidgetDisplayState) -> None:
        self.mode_label.setText(display.mode_name)
        self._apply_row_theme(self.theme_manager.palette)

    def _apply_row_theme(self, palette: ThemePalette) -> None:
        self.mode_label.setStyleSheet(
            f"color: {mode_color(palette, self.timer.state.mode, self.timer.state.waiting_for_continue)}; background: transparent;"
        )


class RingDisplay(QWidget):
    def __init__(self, timer: TimerEngine, theme_manager: ThemeManager, parent: QWidget) -> None:
        super().__init__(parent)
        self.timer = timer
        self.theme_manager = theme_manager
        self.palette = theme_manager.palette
        self.frame = INACTIVE_FRAME
        self.progress = 0.0
        self.overrun = False
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        self.visual = TimerVisual(theme_manager, self, base_font_size=25, mode_font_size=9)
        self.visual.setStyleSheet("background: transparent;")
        layout.addWidget(self.visual)
        theme_manager.register(self._theme_changed)

    def _theme_changed(self, palette: ThemePalette) -> None:
        self.palette = palette
        self.update()

    def set_progress(self, progress: float | None) -> None:
        self.overrun = progress is None
        self.progress = 1.0 if progress is None else min(1.0, max(0.0, progress))
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        side = min(self.width(), self.height()) - 14
        rect = QRect((self.width() - side) // 2, (self.height() - side) // 2, side, side)
        pen_width = max(5, side // 24)
        base_pen = QPen(QColor(self.palette.border), pen_width)
        base_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(base_pen)
        painter.drawArc(rect, 0, 360 * 16)
        color = mode_color(self.palette, self.timer.state.mode, self.overrun)
        if self.frame.effect_color:
            color = self.frame.effect_color
        progress_pen = QPen(QColor(color), pen_width)
        progress_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(progress_pen)
        span = 360 if self.overrun else 360 * self.progress
        painter.drawArc(rect, 90 * 16, -round(span * 16))


class RingWidgetView(WidgetView):
    def __init__(self, parent, timer, actions, theme_manager) -> None:
        super().__init__(parent, timer, actions, theme_manager)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        self.ring = RingDisplay(timer, theme_manager, self)
        self.timer_visual = self.ring.visual
        layout.addWidget(self.ring, 1)
        self.primary_button = self._make_primary_button(tr("action.start"))
        layout.addWidget(self.primary_button)

    def _after_update(self, _display: WidgetDisplayState) -> None:
        self.ring.set_progress(ring_progress(self.timer))

    def apply_overrun_visual(self, frame: OverrunVisualFrame) -> None:
        self.ring.frame = frame
        super().apply_overrun_visual(frame)
        self.ring.update()


class ScoreboardWidgetView(WidgetView):
    def __init__(self, parent, timer, actions, theme_manager) -> None:
        super().__init__(parent, timer, actions, theme_manager)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        self.timer_visual = TimerVisual(theme_manager, self, base_font_size=38, mode_font_size=10, mono=True)
        layout.addWidget(self.timer_visual, 1)
        self.primary_button = self._make_primary_button(tr("action.start"))
        layout.addWidget(self.primary_button)


VIEW_CLASSES = {
    WIDGET_TYPE_MINIMAL: MinimalWidgetView,
    WIDGET_TYPE_COMPACT: CompactWidgetView,
    WIDGET_TYPE_EXPANDED: ExpandedWidgetView,
    WIDGET_TYPE_MICRO: MicroWidgetView,
    WIDGET_TYPE_ROW: RowWidgetView,
    WIDGET_TYPE_RING: RingWidgetView,
    WIDGET_TYPE_SCOREBOARD: ScoreboardWidgetView,
}


def widget_view_class(widget_type: str) -> type[WidgetView]:
    return VIEW_CLASSES[normalize_widget_type(widget_type)]


class WidgetShell(QWidget):
    geometryChanged = Signal()
    closeRequested = Signal()

    def moveEvent(self, event) -> None:  # noqa: N802
        super().moveEvent(event)
        self.geometryChanged.emit()

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self.geometryChanged.emit()

    def closeEvent(self, event) -> None:  # noqa: N802
        event.ignore()
        self.hide()
        self.closeRequested.emit()


class WidgetWindow:
    """Владелец одного переиспользуемого Qt-окна виджета."""

    SAVE_DELAY_MS = 500

    def __init__(
        self,
        parent: QWidget,
        timer: TimerEngine,
        settings: AppSettings,
        actions: WidgetActions,
        save_settings: Callable[[AppSettings], None],
        on_visibility_requested: Callable[[bool], None],
        on_layout_changed: Callable[[AppSettings], None] | None = None,
        theme_manager: ThemeManager | None = None,
    ) -> None:
        if theme_manager is None:
            raise ValueError("WidgetWindow requires the shared ThemeManager")
        self.parent = parent
        self.timer = timer
        self.settings = settings
        self.actions = actions
        self._save_settings = save_settings
        self._on_visibility_requested = on_visibility_requested
        self._on_layout_changed = on_layout_changed
        self.theme_manager = theme_manager
        self.window: WidgetShell | None = None
        self.view: WidgetView | None = None
        self._active_view_type: str | None = None
        self._overrun_frame = INACTIVE_FRAME
        self._accept_geometry = False
        self._programmatic_size: tuple[int, int] | None = None
        self._geometry_debouncer: Debouncer | None = None
        self._topmost: bool | None = None
        theme_manager.register(self.apply_theme)
        localization_manager().language_changed.connect(self._retranslate_ui)

    def apply_settings(self, settings: AppSettings) -> None:
        previous_type = self._active_view_type
        captured = self._capture_current_layout()
        settings.widget_type = normalize_widget_type(settings.widget_type)
        settings.widget_layouts = normalize_widget_layouts(
            settings.widget_layouts, legacy_x=settings.widget_x, legacy_y=settings.widget_y,
            active_type=settings.widget_type,
        )
        if captured is not None and previous_type is not None and previous_type != settings.widget_type:
            settings.widget_layouts[previous_type] = captured
        self.settings = settings
        if not settings.widget_enabled:
            if self.window is not None:
                self.window.hide()
            return
        self._ensure_window()
        if self.window is None:
            return
        if self._active_view_type != settings.widget_type:
            self._rebuild_view(settings.widget_type)
        layout = settings.widget_layouts[settings.widget_type]
        settings.widget_size = str(layout["size"])
        width, height = int(layout["width"]), int(layout["height"])
        x, y = clamp_window_position(int(layout["x"]), int(layout["y"]), width, height, self._screen_bounds())
        layout.update({"x": x, "y": y})
        settings.widget_x, settings.widget_y = x, y
        self._accept_geometry = False
        self._programmatic_size = (width, height)
        minimum = WIDGET_MIN_SIZES[settings.widget_type]
        self.window.setMinimumSize(*minimum)
        self._apply_topmost(settings.widget_always_on_top)
        self.window.resize(width, height)
        self.window.move(x, y)
        self._apply_view_style(width, height, settings.widget_size)
        self.update()
        self.window.show()
        self.theme_manager.apply_to_window(self.window)
        self.window.raise_()
        self.apply_opacity()
        QTimer.singleShot(250, self._enable_geometry_capture)

    def _apply_topmost(self, enabled: bool) -> None:
        if self.window is None:
            return
        enabled = bool(enabled)
        if self._topmost == enabled:
            return
        flags = Qt.WindowType.Tool | Qt.WindowType.WindowTitleHint | Qt.WindowType.WindowCloseButtonHint
        if enabled:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        visible = self.window.isVisible()
        self.window.setWindowFlags(flags)
        self._topmost = enabled
        if visible:
            self.window.show()

    def update(self) -> None:
        if self.view is not None and self.is_visible():
            self.view.update_view()

    def apply_overrun_visual(self, frame: OverrunVisualFrame) -> None:
        self._overrun_frame = frame
        if self.view is not None:
            self.view.apply_overrun_visual(frame)
        self.apply_opacity()

    def apply_opacity(self) -> float:
        visual = self.settings.overrun_visual if isinstance(self.settings.overrun_visual, dict) else {}
        alpha = effective_widget_alpha(
            self.settings.widget_opacity,
            bool(visual.get("opaque_widget_during_overrun", False)),
            self.timer.state.waiting_for_continue,
        )
        if self.window is not None:
            self.window.setWindowOpacity(alpha)
        return alpha

    def apply_theme(self, palette: ThemePalette) -> None:
        if self.window is None or self.view is None:
            return
        parameters = widget_size_parameters(
            self.settings.widget_type, self.settings.widget_size,
            self.window.width(), self.window.height(),
        )
        self.view.apply_style(palette, parameters)
        self.view.apply_overrun_visual(self._overrun_frame)
        self.window.update()

    def is_visible(self) -> bool:
        return self.window is not None and self.window.isVisible()

    def discard_window(self) -> None:
        if self.window is not None:
            self.window.closeRequested.disconnect()
            self.window.deleteLater()
        self.window = None
        self.view = None
        self._active_view_type = None
        self._geometry_debouncer = None
        self._topmost = None

    def close(self) -> None:
        if self._geometry_debouncer is not None:
            self._geometry_debouncer.flush()
        if self.window is not None:
            self.window.hide()
            self.window.deleteLater()
        self.window = None
        self.view = None
        self.theme_manager.unregister(self.apply_theme)
        self._topmost = None

    def _ensure_window(self) -> None:
        if self.window is not None:
            return
        self.window = WidgetShell(self.parent)
        self.window.setWindowTitle(tr("widget.window_title"))
        self.window.setWindowIcon(application_icon())
        self.window.closeRequested.connect(lambda: self._on_visibility_requested(False))
        self.window.geometryChanged.connect(self._on_geometry_changed)
        self._geometry_debouncer = Debouncer(self.window, self.SAVE_DELAY_MS, self._persist_current_layout)

    def _retranslate_ui(self, _language_code: str) -> None:
        if self.window is not None:
            self.window.setWindowTitle(tr("widget.window_title"))
        if self.view is not None:
            self.view.update_view()

    def _rebuild_view(self, widget_type: str) -> None:
        if self.window is None:
            return
        if self.view is not None:
            self.view.hide()
            self.view.deleteLater()
        self.view = widget_view_class(widget_type)(self.window, self.timer, self.actions, self.theme_manager)
        layout = self.window.layout()
        if layout is None:
            layout = QVBoxLayout(self.window)
            layout.setContentsMargins(0, 0, 0, 0)
        else:
            while layout.count():
                item = layout.takeAt(0)
                if item.widget() is not None and item.widget() is not self.view:
                    item.widget().deleteLater()
        layout.addWidget(self.view)
        self._active_view_type = normalize_widget_type(widget_type)
        self.view.apply_overrun_visual(self._overrun_frame)

    def _enable_geometry_capture(self) -> None:
        self._accept_geometry = True
        self._programmatic_size = None

    def _on_geometry_changed(self) -> None:
        if not self._accept_geometry or self.window is None:
            return
        layout = self.settings.widget_layouts[self.settings.widget_type]
        size_changed = (self.window.width(), self.window.height()) != (int(layout["width"]), int(layout["height"]))
        if size_changed:
            self.settings.widget_size = WIDGET_SIZE_CUSTOM
            layout["size"] = WIDGET_SIZE_CUSTOM
            self._apply_view_style(self.window.width(), self.window.height(), WIDGET_SIZE_CUSTOM)
        if self._geometry_debouncer is not None:
            self._geometry_debouncer.trigger()

    def _apply_view_style(self, width: int, height: int, size: str) -> None:
        if self.view is not None:
            self.view.apply_style(self.theme_manager.palette, widget_size_parameters(self.settings.widget_type, size, width, height))

    def _capture_current_layout(self) -> dict[str, int | str] | None:
        if self.window is None or self._active_view_type is None:
            return None
        point = self.window.pos()
        layout = self.settings.widget_layouts[self._active_view_type]
        layout.update({
            "size": str(layout["size"]),
            "width": self.window.width(), "height": self.window.height(),
            "x": point.x(), "y": point.y(),
        })
        self.settings.widget_x, self.settings.widget_y = point.x(), point.y()
        return deepcopy(layout)

    def _persist_current_layout(self) -> None:
        if self._capture_current_layout() is None:
            return
        self._save_settings(self.settings)
        if self._on_layout_changed is not None:
            self._on_layout_changed(self.settings)

    @staticmethod
    def _screen_bounds() -> tuple[int, int, int, int]:
        screens = QApplication.screens()
        if not screens:
            return (0, 0, 1, 1)
        united = screens[0].availableGeometry()
        for screen in screens[1:]:
            united = united.united(screen.availableGeometry())
        return united.x(), united.y(), united.width(), united.height()
