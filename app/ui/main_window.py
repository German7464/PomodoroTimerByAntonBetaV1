"""Главное окно Pomodoro Timer на Qt Widgets."""

from __future__ import annotations

from copy import deepcopy

from PySide6.QtCore import QEvent, Qt, QTimer
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.autostart import AutostartService
from app.config import APP_NAME, DATA_DIR_WARNING, SETTINGS_FILE, STATISTICS_FILE
from app.models import AppSettings, TimerMode
from app.i18n import (
    initialize_localization,
    normalize_language_code,
    timer_mode_text,
    tr,
)
from app.notifications import NotificationService
from app.overrun_effects import OverrunVisualController, OverrunVisualFrame, normalize_overrun_visual
from app.statistics import StatisticsService
from app.storage import load_app_settings, save_app_settings
from app.theme import (
    APPEARANCE_DARK,
    APPEARANCE_LIGHT,
    CUSTOM_THEME_NAME,
    ThemeManager,
    normalize_appearance_mode,
    normalize_custom_theme,
    normalize_theme_name,
)
from app.timer_engine import TimerEngine
from app.ui.components import AppButton, Card, FlowLayout, PageHeader, SwitchRow
from app.ui.design_system import TOKENS
from app.ui.help_window import HelpView
from app.ui.icons import application_icon
from app.ui.qt_app import Debouncer, QtScheduler, ensure_application
from app.ui.settings_window import SettingsView
from app.ui.stats_view import StatsView
from app.ui.timer_visual import TimerVisual
from app.ui.tray import TrayController
from app.ui.widget_window import WidgetActions, WidgetWindow
from app.widget_settings import normalize_widget_opacity
from app.window_geometry import (
    MAIN_WINDOW_MIN_HEIGHT,
    MAIN_WINDOW_MIN_WIDTH,
    fit_main_window_geometry,
)


class MainWindow(QMainWindow):
    """Профессиональная Qt-оболочка над единым состоянием приложения."""

    def __init__(self) -> None:
        self.application = ensure_application()
        super().__init__()
        self.root = self  # Совместимый атрибут для внешних диагностик.
        self.setObjectName("MainWindow")
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(application_icon())
        self.setMinimumSize(MAIN_WINDOW_MIN_WIDTH, MAIN_WINDOW_MIN_HEIGHT)
        self._exiting = False
        self._geometry_ready = False

        self.settings = load_app_settings(SETTINGS_FILE)
        self.localization = initialize_localization(
            self.application,
            self.settings.ui_language,
        )
        self._sync_interface_motion_setting()
        self._settings_save = Debouncer(self, 500, self._save_settings_now)
        self._layout_resize = Debouncer(self, 80, self._apply_responsive_layout)
        self._restore_main_window_geometry()
        self.theme_manager = ThemeManager(self)
        self.theme_manager.apply(
            self.settings.theme_name,
            self.settings.appearance_mode,
            self.settings.custom_theme,
        )
        self.autostart = AutostartService()
        self.timer = TimerEngine(self.settings)
        self.statistics = StatisticsService(STATISTICS_FILE)

        self._scheduler = QtScheduler(self)
        self._tick_timer = QTimer(self)
        self._tick_timer.setInterval(1000)
        self._tick_timer.setTimerType(Qt.TimerType.PreciseTimer)
        self._tick_timer.timeout.connect(self._tick_once)

        self.notifications = NotificationService(self, self.settings, self.theme_manager)
        self.widget_window = WidgetWindow(
            self,
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
            self._scheduler.schedule,
            self._scheduler.cancel,
            self._apply_overrun_visual_frame,
        )
        self.tray = TrayController(
            show_window=self.show_window,
            hide_window=self.hide_to_tray,
            toggle_timer=self.toggle_timer_from_tray,
            reset_timer=self.reset,
            exit_app=self.exit_app,
            theme_manager=self.theme_manager,
        )

        self._build_ui()
        self.localization.language_changed.connect(self._retranslate_ui)
        self._geometry_ready = True
        self._apply_responsive_layout()
        self.set_widget_visibility(self.settings.widget_enabled, persist=False)
        self.apply_theme_selection(
            self.settings.theme_name,
            self.settings.appearance_mode,
            persist=False,
        )
        self._refresh_labels()
        if DATA_DIR_WARNING:
            QTimer.singleShot(
                350,
                lambda: QMessageBox.warning(
                    self,
                    tr("error.data.portable_title"),
                    tr(DATA_DIR_WARNING),
                ),
            )

    def _build_ui(self) -> None:
        root = QWidget(self)
        root.setObjectName("AppRoot")
        self.setCentralWidget(root)
        layout = QHBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sidebar = QFrame(root)
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(TOKENS.controls.sidebar_width)
        side = QVBoxLayout(self.sidebar)
        side.setContentsMargins(TOKENS.spacing.md, TOKENS.spacing.xl, TOKENS.spacing.md, TOKENS.spacing.lg)
        side.setSpacing(TOKENS.spacing.xs)
        self.brand_label = QLabel("Pomodoro", self.sidebar)
        self.brand_label.setProperty("role", "pageTitle")
        side.addWidget(self.brand_label)
        self.brand_subtitle = QLabel(tr("main.brand_subtitle"), self.sidebar)
        self.brand_subtitle.setProperty("role", "caption")
        side.addWidget(self.brand_subtitle)
        side.addSpacing(TOKENS.spacing.xl)

        self.page_stack = QStackedWidget(root)
        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)
        nav_specs = (
            ("nav.timer", "timer"),
            ("nav.statistics", "statistics"),
            ("nav.settings", "settings"),
            ("nav.help", "help"),
        )
        self._nav_specs = nav_specs
        self.nav_buttons: list[AppButton] = []
        for index, (key, icon) in enumerate(nav_specs):
            button = AppButton(tr(key), self.sidebar, variant="ghost", icon_name=icon, theme_manager=self.theme_manager)
            button.setProperty("nav", True)
            button.setCheckable(True)
            button.clicked.connect(lambda _checked=False, target=index: self.page_stack.setCurrentIndex(target))
            self.nav_group.addButton(button, index)
            self.nav_buttons.append(button)
            side.addWidget(button)
        side.addStretch(1)
        self.version_label = QLabel("Qt 6 · Windows", self.sidebar)
        self.version_label.setProperty("role", "caption")
        side.addWidget(self.version_label)
        layout.addWidget(self.sidebar)

        self.page_stack.addWidget(self._build_timer_page())
        self.stats_view = StatsView(self.page_stack, self.statistics, self.theme_manager)
        self.page_stack.addWidget(self.stats_view)
        self.settings_view = SettingsView(
            self.page_stack,
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
            on_widget_configuration_change=self.set_widget_configuration,
            on_language_change=self.set_interface_language,
            theme_manager=self.theme_manager,
        )
        self.page_stack.addWidget(self.settings_view)
        self.help_view = HelpView(self.page_stack)
        self.page_stack.addWidget(self.help_view)
        self.page_stack.currentChanged.connect(self._page_changed)
        layout.addWidget(self.page_stack, 1)
        self.nav_buttons[0].setChecked(True)

    def _build_timer_page(self) -> QWidget:
        page = QWidget(self)
        outer = QVBoxLayout(page)
        self.timer_page_layout = outer
        outer.setContentsMargins(TOKENS.spacing.xxl, TOKENS.spacing.xl, TOKENS.spacing.xxl, TOKENS.spacing.xl)
        outer.setSpacing(TOKENS.spacing.lg)
        header = PageHeader("timer.page.title", "timer.page.subtitle", page)
        self.appearance_mode_switch = SwitchRow(
            "settings.appearance.dark_mode",
            self.settings.appearance_mode == APPEARANCE_DARK,
            page,
            theme_manager=self.theme_manager,
            animations_enabled=lambda: bool(self.settings.overrun_visual.get("animations_enabled", True)),
        )
        self.appearance_mode_switch.valueChanged.connect(self.set_dark_appearance)
        header.actions.addWidget(self.appearance_mode_switch)
        outer.addWidget(header)

        timer_card = Card(page, padding=TOKENS.spacing.lg, shadow=True, theme_manager=self.theme_manager)
        self.timer_visual = TimerVisual(self.theme_manager, timer_card, base_font_size=72, mode_font_size=17)
        timer_card.content_layout.addWidget(self.timer_visual, 1)
        self.status_label = QLabel(tr("timer.status.stopped"), timer_card)
        self.status_label.setProperty("role", "statusChip")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setAccessibleName(tr("timer.status.accessible_name"))
        timer_card.content_layout.addWidget(self.status_label, 0, Qt.AlignmentFlag.AlignCenter)

        controls = FlowLayout(horizontal_spacing=TOKENS.spacing.sm, vertical_spacing=TOKENS.spacing.sm)
        self.start_button = AppButton(tr("action.start"), timer_card, variant="primary", icon_name="play", theme_manager=self.theme_manager)
        self.start_button.clicked.connect(self.start)
        self.pause_button = AppButton(tr("action.pause"), timer_card, icon_name="pause", theme_manager=self.theme_manager)
        self.pause_button.clicked.connect(self.toggle_pause)
        self.skip_button = AppButton(tr("action.skip"), timer_card, variant="ghost", icon_name="skip", theme_manager=self.theme_manager)
        self.skip_button.clicked.connect(self.skip_period)
        self.reset_button = AppButton(tr("action.reset"), timer_card, variant="ghost", icon_name="reset", theme_manager=self.theme_manager)
        self.reset_button.clicked.connect(self.reset)
        for button in (self.start_button, self.pause_button, self.skip_button, self.reset_button):
            controls.addWidget(button)
        timer_card.content_layout.addLayout(controls)
        self.continue_button = AppButton(
            tr("action.continue_next_period"),
            timer_card,
            variant="primary",
            icon_name="play",
            theme_manager=self.theme_manager,
        )
        self.continue_button.clicked.connect(self.continue_manual_transition)
        timer_card.content_layout.addWidget(self.continue_button, 0, Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(timer_card, 1)

        widget_card = Card(page, padding=TOKENS.spacing.md)
        self.widget_visibility_switch = SwitchRow(
            "timer.widget.show",
            self.settings.widget_enabled,
            widget_card,
            description="timer.widget.show.description",
            theme_manager=self.theme_manager,
            animations_enabled=lambda: bool(self.settings.overrun_visual.get("animations_enabled", True)),
        )
        self.widget_visibility_switch.valueChanged.connect(self.set_widget_visibility)
        widget_card.content_layout.addWidget(self.widget_visibility_switch)
        outer.addWidget(widget_card)
        return page

    def run(self) -> None:
        """Запускает Qt event loop; все GUI-объекты уже принадлежат одному потоку."""
        self.tray.start()
        self._tick_timer.start()
        if self.settings.minimize_to_tray_on_start:
            self.hide()
        else:
            self.show()
        self.application.exec()

    def start(self) -> None:
        self.timer.start()
        self._refresh_labels()

    def toggle_pause(self) -> None:
        self.timer.toggle_pause()
        self._refresh_labels()

    def skip_period(self) -> None:
        self.overrun_visual_controller.stop_preview()
        skipped_mode = self.timer.skip_period()
        if skipped_mode is not None:
            self.statistics.record_skipped_period(skipped_mode)
            self.stats_view.refresh()
        self._refresh_labels()

    def reset(self) -> None:
        self.overrun_visual_controller.stop_preview()
        if self.timer.reset():
            self.statistics.record_reset()
            self.stats_view.refresh()
        self._refresh_labels()

    def apply_settings(self, settings: AppSettings, autostart_changed: bool = False) -> None:
        should_reset_timer = self._duration_settings_changed(settings)
        settings.main_window_geometry = deepcopy(self.settings.main_window_geometry)
        if autostart_changed:
            try:
                self.autostart.set_enabled(settings.autostart_enabled)
            except RuntimeError as error:
                QMessageBox.warning(
                    self,
                    tr("settings.tray.autostart_title"),
                    tr(str(error)),
                )
                settings.autostart_enabled = self.settings.autostart_enabled
        self._settings_save.cancel()
        settings.overrun_visual = normalize_overrun_visual(settings.overrun_visual)
        self.settings = settings
        self.settings.ui_language = normalize_language_code(settings.ui_language)
        self._sync_interface_motion_setting()
        self.settings_view.settings = settings
        self.settings_view.update_autostart_status(self.autostart.status())
        self.localization.set_language(self.settings.ui_language)
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
        self._refresh_labels()

    def _sync_interface_motion_setting(self) -> None:
        """Делает существующее отключение движения общим для UI-анимаций."""
        visual = self.settings.overrun_visual if isinstance(self.settings.overrun_visual, dict) else {}
        self.application.setProperty(
            "animationsEnabled",
            bool(visual.get("animations_enabled", True)),
        )

    def show_window(self) -> None:
        self._sync_widget_visibility()
        self._ensure_main_window_visible()
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def showEvent(self, event) -> None:  # noqa: N802 - Qt API
        super().showEvent(event)
        if hasattr(self, "page_stack"):
            QTimer.singleShot(0, lambda: self.theme_manager.refresh_widget_tree(self, visible_only=True))

    def _page_changed(self, index: int) -> None:
        if 0 <= index < self.page_stack.count():
            self.theme_manager.refresh_widget_tree(self.page_stack.widget(index), visible_only=False)

    def hide_to_tray(self) -> None:
        self.hide()

    def on_window_close(self) -> None:
        if self.settings.close_to_tray:
            self.hide_to_tray()
        else:
            self.exit_app()

    def closeEvent(self, event: QCloseEvent) -> None:  # noqa: N802
        if self._exiting:
            event.accept()
            return
        if self.settings.close_to_tray:
            event.ignore()
            self.hide_to_tray()
            return
        event.ignore()
        self.exit_app()

    def exit_app(self) -> None:
        self._shutdown(quit_application=True)

    def _shutdown(self, *, quit_application: bool) -> None:
        """Единообразно освобождает GUI; тесты могут не завершать общий QApplication."""
        if self._exiting:
            return
        self._exiting = True
        self._settings_save.flush()
        overrun = self.timer.finalize_overrun_on_exit()
        if overrun is not None:
            self.statistics.record_overrun(overrun.mode, overrun.duration_seconds)
        self._tick_timer.stop()
        self.notifications.dispose()
        self.overrun_visual_controller.stop()
        self._scheduler.stop_all()
        self.widget_window.close()
        self.tray.dispose()
        self.close()
        if quit_application:
            self.application.quit()

    def toggle_timer_from_tray(self) -> None:
        if self.timer.state.waiting_for_continue:
            self.show_window()
        elif self.timer.state.is_running:
            self.timer.pause()
        else:
            self.timer.start()
        self._refresh_labels()

    def set_dark_appearance(self, enabled: bool) -> None:
        self.apply_theme_selection(
            self.settings.theme_name,
            APPEARANCE_DARK if enabled else APPEARANCE_LIGHT,
        )

    def set_interface_language(self, language_code: str) -> bool:
        normalized = normalize_language_code(language_code)
        changed = self.settings.ui_language != normalized
        self.settings.ui_language = normalized
        self.localization.set_language(normalized)
        if hasattr(self, "settings_view"):
            self.settings_view.settings.ui_language = normalized
            self.settings_view.sync_language(normalized)
        if changed:
            save_app_settings(SETTINGS_FILE, self.settings)
        return changed

    def apply_theme_selection(
        self,
        theme_name: str,
        appearance_mode: str,
        *,
        custom_theme: object = None,
        persist: bool = True,
    ) -> bool:
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
        self._sync_appearance_switch()
        self._sync_overrun_visual()
        if changed and persist:
            save_app_settings(SETTINGS_FILE, self.settings)
        return changed

    def preview_custom_theme(self, custom_theme: dict[str, dict[str, str]], appearance_mode: str) -> None:
        self.theme_manager.apply(CUSTOM_THEME_NAME, normalize_appearance_mode(appearance_mode), custom_theme)
        self._sync_overrun_visual()

    def apply_custom_theme(self, custom_theme: dict[str, dict[str, str]], appearance_mode: str) -> None:
        self.apply_theme_selection(CUSTOM_THEME_NAME, appearance_mode, custom_theme=custom_theme)

    def cancel_theme_preview(self) -> None:
        self.theme_manager.apply(
            self.settings.theme_name,
            self.settings.appearance_mode,
            self.settings.custom_theme,
        )
        self._sync_overrun_visual()

    def preview_overrun_visual(self, mode: TimerMode, visual: dict[str, object]) -> None:
        self.overrun_visual_controller.start_preview(mode, visual, self.theme_manager.palette)

    def set_widget_opacity(self, opacity: int) -> None:
        self.settings.widget_opacity = normalize_widget_opacity(opacity)
        self.widget_window.apply_opacity()
        if hasattr(self, "settings_view"):
            self.settings_view.sync_widget_opacity(self.settings.widget_opacity)
        self._settings_save.trigger()

    def set_overrun_widget_opacity(self, enabled: bool) -> None:
        normalized = bool(enabled)
        visual = dict(self.settings.overrun_visual)
        if bool(visual.get("opaque_widget_during_overrun", False)) == normalized:
            return
        visual["opaque_widget_during_overrun"] = normalized
        self.settings.overrun_visual = normalize_overrun_visual(visual)
        self.widget_window.apply_opacity()
        if hasattr(self, "settings_view"):
            self.settings_view.sync_overrun_widget_opacity(normalized)
        self._settings_save.trigger()

    def set_widget_configuration(
        self,
        widget_type: str,
        widget_size: str,
        widget_layouts: dict,
        always_on_top: bool,
    ) -> None:
        """Применяет вид/размер/позицию немедленно без изменения TimerEngine."""
        self.settings.widget_type = widget_type
        self.settings.widget_size = widget_size
        self.settings.widget_layouts = deepcopy(widget_layouts)
        self.settings.widget_always_on_top = bool(always_on_top)
        self.widget_window.apply_settings(self.settings)
        self._settings_save.trigger()

    def _save_settings_now(self) -> None:
        self._capture_main_window_geometry()
        save_app_settings(SETTINGS_FILE, self.settings)

    def resizeEvent(self, event) -> None:  # noqa: N802 - Qt API
        if self._geometry_ready:
            self._layout_resize.trigger()
            if not self.isMaximized() and not self.isMinimized():
                self._settings_save.trigger()
        super().resizeEvent(event)

    def moveEvent(self, event) -> None:  # noqa: N802 - Qt API
        if self._geometry_ready and not self.isMaximized() and not self.isMinimized():
            self._settings_save.trigger()
        super().moveEvent(event)

    def _apply_responsive_layout(self) -> None:
        if not hasattr(self, "sidebar"):
            return
        width = self.width()
        if width < 1200:
            sidebar_width = 72
            collapsed = True
            self.brand_label.setVisible(False)
            self.brand_subtitle.setVisible(False)
            self.version_label.setVisible(False)
        else:
            sidebar_width = TOKENS.controls.sidebar_width
            collapsed = False
            self.brand_label.setVisible(True)
            self.brand_subtitle.setVisible(True)
            self.version_label.setVisible(True)
        self.sidebar.setFixedWidth(sidebar_width)
        labels = tuple(tr(key) for key, _icon in self._nav_specs)
        for button, label in zip(self.nav_buttons, labels, strict=True):
            button.setText("" if collapsed else label)
            button.setToolTip(label if collapsed else "")
            button.setAccessibleName(label)
        margin = TOKENS.spacing.lg if width < 980 else TOKENS.spacing.xl
        self.timer_page_layout.setContentsMargins(
            margin, TOKENS.spacing.lg, margin, TOKENS.spacing.lg,
        )

    def _screen_rectangles(self) -> list[tuple[int, int, int, int]]:
        rectangles = []
        primary = self.application.primaryScreen()
        screens = list(self.application.screens())
        if primary in screens:
            screens.remove(primary)
            screens.insert(0, primary)
        for screen in screens:
            geometry = screen.availableGeometry()
            rectangles.append((geometry.x(), geometry.y(), geometry.width(), geometry.height()))
        return rectangles

    def _restore_main_window_geometry(self) -> None:
        geometry = fit_main_window_geometry(
            self.settings.main_window_geometry,
            self._screen_rectangles(),
        )
        self.resize(geometry["width"], geometry["height"])
        self.move(geometry["x"], geometry["y"])
        self.settings.main_window_geometry = geometry

    def _ensure_main_window_visible(self) -> None:
        current = {
            "x": self.x(), "y": self.y(),
            "width": self.width(), "height": self.height(),
        }
        geometry = fit_main_window_geometry(current, self._screen_rectangles())
        if geometry != current:
            self.resize(geometry["width"], geometry["height"])
            self.move(geometry["x"], geometry["y"])
        self.settings.main_window_geometry = geometry

    def _capture_main_window_geometry(self) -> None:
        if not self._geometry_ready or self.isMaximized() or self.isMinimized():
            return
        self.settings.main_window_geometry = {
            "x": self.x(), "y": self.y(),
            "width": self.width(), "height": self.height(),
        }

    def _sync_appearance_switch(self) -> None:
        if hasattr(self, "appearance_mode_switch"):
            self.appearance_mode_switch.setChecked(self.settings.appearance_mode == APPEARANCE_DARK)

    def set_widget_visibility(self, visible: bool, *, persist: bool = True) -> bool:
        requested = bool(visible)
        previous = bool(self.settings.widget_enabled)
        self.settings.widget_enabled = requested
        error: Exception | None = None
        try:
            self.widget_window.apply_settings(self.settings)
            if self.widget_window.is_visible() != requested:
                raise RuntimeError(tr("error.widget.state_mismatch"))
        except Exception as caught:
            error = caught
            if requested:
                self.widget_window.discard_window()
        actual = self.widget_window.is_visible()
        self.settings.widget_enabled = actual
        if (persist and previous != actual) or actual != requested:
            try:
                save_app_settings(SETTINGS_FILE, self.settings)
            except OSError as save_error:
                error = error or save_error
        self._sync_widget_visibility()
        if error is not None:
            QMessageBox.warning(
                self,
                tr("settings.widget.dialog_title"),
                tr(
                    "error.widget.show" if requested else "error.widget.hide",
                    error=error,
                ),
            )
            return False
        return True

    def _sync_widget_visibility(self) -> None:
        visible = self.widget_window.is_visible()
        self.settings.widget_enabled = visible
        if hasattr(self, "widget_visibility_switch"):
            self.widget_visibility_switch.setChecked(visible)

    def _on_widget_layout_changed(self, settings: AppSettings) -> None:
        self.settings = settings
        if hasattr(self, "settings_view"):
            self.settings_view.sync_widget_layouts(settings)

    def continue_after_notification(self) -> None:
        self.continue_manual_transition()

    def continue_manual_transition(self) -> None:
        overrun = self.timer.continue_to_next_period()
        if overrun is not None:
            self.statistics.record_overrun(overrun.mode, overrun.duration_seconds)
            self.notifications.dismiss()
            self.stats_view.refresh()
        self._refresh_labels()

    def _schedule_tick(self) -> None:
        """Совместимый публичный запуск единственного секундного QTimer."""
        if not self._tick_timer.isActive():
            self._tick_timer.start()

    def _tick_once(self) -> None:
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

    def _refresh_labels(self) -> None:
        previewing = self.overrun_visual_controller.preview_active
        if not previewing:
            status = tr("timer.overrun.waiting_status") if self.timer.state.waiting_for_continue else ""
            self.timer_visual.set_state(
                timer_mode_text(
                    self.timer.state.overrun_mode or self.timer.state.mode,
                    self.timer.state.waiting_for_continue,
                ),
                self.timer.formatted_time(),
                self.timer.state.overrun_mode or self.timer.state.mode,
                self.timer.state.waiting_for_continue,
                status,
            )
        self.widget_window.update()
        self._sync_overrun_visual()
        self._sync_timer_buttons()

        if self.timer.state.waiting_for_continue:
            status_text = tr("timer.status.overrun")
        elif self.timer.state.is_running:
            status_text = tr("timer.status.running")
        elif self.timer.state.remaining_seconds < self.timer.current_period_duration_seconds():
            status_text = tr("timer.status.paused")
        else:
            status_text = tr("timer.status.stopped")
        self.status_label.setText(status_text)

    def _sync_overrun_visual(self) -> None:
        state = self.timer.state
        self.overrun_visual_controller.sync_actual(
            state.waiting_for_continue,
            state.overrun_mode or state.mode,
            self.settings.overrun_visual,
            self.theme_manager.palette,
        )

    def _apply_overrun_visual_frame(self, frame: OverrunVisualFrame) -> None:
        self.timer_visual.apply_overrun_frame(
            frame,
            short_format=self.settings.time_display_format == "MM:SS",
        )
        self.widget_window.apply_overrun_visual(frame)
        if not frame.active and not frame.preview:
            self.timer_visual.reset_preview_state(
                timer_mode_text(
                    self.timer.state.overrun_mode or self.timer.state.mode,
                    self.timer.state.waiting_for_continue,
                ),
                self.timer.formatted_time(),
                self.timer.state.overrun_mode or self.timer.state.mode,
                self.timer.state.waiting_for_continue,
            )

    def _sync_timer_buttons(self) -> None:
        waiting = self.timer.state.waiting_for_continue
        running = self.timer.state.is_running
        progressed = self.timer.state.remaining_seconds < self.timer.current_period_duration_seconds()
        self.continue_button.setVisible(waiting)
        self.continue_button.setEnabled(waiting)
        for button in (self.start_button, self.pause_button, self.skip_button, self.reset_button):
            button.setEnabled(not waiting)
        self.start_button.setEnabled(not waiting and not running)
        self.pause_button.setEnabled(not waiting and (running or progressed))
        self.pause_button.setText(tr("action.pause" if running else "action.continue"))

    def changeEvent(self, event: QEvent) -> None:  # noqa: N802 - Qt API
        if event.type() == QEvent.Type.LanguageChange:
            self.setProperty(
                "languageChangeCount",
                int(self.property("languageChangeCount") or 0) + 1,
            )
        super().changeEvent(event)

    def _retranslate_ui(self, language_code: str) -> None:
        self.setWindowTitle(APP_NAME)
        self.brand_subtitle.setText(tr("main.brand_subtitle"))
        self.status_label.setAccessibleName(tr("timer.status.accessible_name"))
        self.start_button.setText(tr("action.start"))
        self.skip_button.setText(tr("action.skip"))
        self.reset_button.setText(tr("action.reset"))
        self.continue_button.setText(tr("action.continue_next_period"))
        self.settings_view.sync_language(language_code)
        self._apply_responsive_layout()
        self._refresh_labels()
        self.updateGeometry()

    def _duration_settings_changed(self, new_settings: AppSettings) -> bool:
        return (
            self.settings.work_minutes != new_settings.work_minutes
            or self.settings.short_break_minutes != new_settings.short_break_minutes
            or self.settings.long_break_minutes != new_settings.long_break_minutes
        )


def main_window_snapshot_settings(window: MainWindow) -> dict[str, object]:
    """Минимальный диагностический срез для UI-тестов без чтения JSON."""
    return {
        "mode": window.timer.state.mode,
        "remaining_seconds": window.timer.state.remaining_seconds,
        "running": window.timer.state.is_running,
        "waiting": window.timer.state.waiting_for_continue,
        "theme": window.settings.theme_name,
        "appearance": window.settings.appearance_mode,
        "widget_visible": window.widget_window.is_visible(),
    }
