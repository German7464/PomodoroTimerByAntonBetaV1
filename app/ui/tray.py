"""Интеграция с системным треем через Qt, без отдельного потока."""

from collections.abc import Callable

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from app.theme import ThemeManager, ThemePalette
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
            raise RuntimeError("TrayController требует созданный QApplication")
        self._show_window = show_window
        self._theme_manager = theme_manager
        self.icon = QSystemTrayIcon(tray_icon(), app)
        self.icon.setToolTip("Pomodoro Timer")
        menu = QMenu()
        self.menu = menu
        self.actions: dict[str, QAction] = {}
        for text, callback in (
            ("Показать окно", show_window),
            ("Скрыть окно", hide_window),
            ("Старт / Пауза", toggle_timer),
            ("Сброс", reset_timer),
        ):
            action = QAction(text, menu)
            action.triggered.connect(callback)
            menu.addAction(action)
            self.actions[text] = action
        menu.addSeparator()
        exit_action = QAction("Выход", menu)
        exit_action.triggered.connect(exit_app)
        menu.addAction(exit_action)
        self.actions["Выход"] = exit_action
        self.icon.setContextMenu(menu)
        self.icon.activated.connect(self._activated)
        theme_manager.register(self._apply_theme)

    def start(self) -> None:
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.icon.show()

    def stop(self) -> None:
        self.icon.hide()

    def dispose(self) -> None:
        """Освобождает Qt-объекты при полном завершении или в UI-тесте."""
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
