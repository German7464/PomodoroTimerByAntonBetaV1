"""Интеграция с системным треем через Qt, без отдельного потока."""

from collections.abc import Callable

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from app.theme import ThemeManager, ThemePalette
from app.i18n import localization_manager, tr
from app.ui.design_system import build_application_palette, build_menu_stylesheet
from app.ui.icons import tray_icon


class TrayController:
    """Единственная иконка трея, работающая в GUI-потоке Qt."""

    def __init__(
        self,
        show_window: Callable[[], None],
        hide_window: Callable[[], None],
        toggle_timer: Callable[[], None],
        reset_timer: Callable[[], None],
        exit_app: Callable[[], None],
        theme_manager: ThemeManager,
    ) -> None:
        app = QApplication.instance()
        if app is None:
            raise RuntimeError("TrayController requires an existing QApplication")
        self._show_window = show_window
        self._theme_manager = theme_manager
        self._disposed = False
        self.icon = QSystemTrayIcon(tray_icon(), app)
        self.icon.setToolTip("Pomodoro Timer")
        menu = QMenu()
        self.menu = menu
        self.actions: dict[str, QAction] = {}
        for key, callback in (
            ("tray.show", show_window),
            ("tray.hide", hide_window),
            ("tray.start_pause", toggle_timer),
            ("tray.reset", reset_timer),
        ):
            action = QAction(tr(key), menu)
            action.triggered.connect(callback)
            menu.addAction(action)
            self.actions[key] = action
        menu.addSeparator()
        exit_action = QAction(tr("tray.exit"), menu)
        exit_action.triggered.connect(exit_app)
        menu.addAction(exit_action)
        self.actions["tray.exit"] = exit_action
        self.icon.setContextMenu(menu)
        self.icon.activated.connect(self._activated)
        theme_manager.register(self._apply_theme)
        localization_manager().language_changed.connect(self._retranslate_ui)

    def start(self) -> None:
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.icon.show()

    def stop(self) -> None:
        self.icon.hide()

    def dispose(self) -> None:
        """Освобождает Qt-объекты при полном завершении или в UI-тесте."""
        if self._disposed:
            return
        self._disposed = True
        localization_manager().language_changed.disconnect(self._retranslate_ui)
        self.icon.hide()
        self._theme_manager.unregister(self._apply_theme)
        self.icon.deleteLater()
        self.menu.deleteLater()

    def _apply_theme(self, palette: ThemePalette) -> None:
        """Обновляет уже созданное QMenu напрямую, без пересоздания трея."""
        stylesheet = build_menu_stylesheet(palette)
        if self.menu.styleSheet() != stylesheet:
            self.menu.setStyleSheet(stylesheet)
        self.menu.setPalette(build_application_palette(palette))
        self.menu.update()

    def _activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason in (QSystemTrayIcon.ActivationReason.Trigger, QSystemTrayIcon.ActivationReason.DoubleClick):
            self._show_window()

    def _retranslate_ui(self, _language_code: str) -> None:
        self.icon.setToolTip("Pomodoro Timer")
        for key, action in self.actions.items():
            action.setText(tr(key))
        self.menu.adjustSize()
        self.menu.update()
