"""Интеграция с системным треем через Qt, без отдельного потока."""

from collections.abc import Callable

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QColor, QIcon, QPainter, QPen, QPixmap
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon


class TrayController:
    """Единственная иконка трея, работающая в GUI-потоке Qt."""

    def __init__(
        self,
        show_window: Callable[[], None],
        hide_window: Callable[[], None],
        toggle_timer: Callable[[], None],
        reset_timer: Callable[[], None],
        exit_app: Callable[[], None],
    ) -> None:
        app = QApplication.instance()
        if app is None:
            raise RuntimeError("TrayController требует созданный QApplication")
        self._show_window = show_window
        self.icon = QSystemTrayIcon(self._create_icon(), app)
        self.icon.setToolTip("Pomodoro Timer")
        menu = QMenu()
        self.menu = menu
        for text, callback in (
            ("Показать окно", show_window),
            ("Скрыть окно", hide_window),
            ("Старт / Пауза", toggle_timer),
            ("Сброс", reset_timer),
        ):
            action = QAction(text, menu)
            action.triggered.connect(callback)
            menu.addAction(action)
        menu.addSeparator()
        exit_action = QAction("Выход", menu)
        exit_action.triggered.connect(exit_app)
        menu.addAction(exit_action)
        self.icon.setContextMenu(menu)
        self.icon.activated.connect(self._activated)

    def start(self) -> None:
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.icon.show()

    def stop(self) -> None:
        self.icon.hide()

    def dispose(self) -> None:
        """Освобождает Qt-объекты при полном завершении или в UI-тесте."""
        self.icon.hide()
        self.icon.deleteLater()
        self.menu.deleteLater()

    def _activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason in (QSystemTrayIcon.ActivationReason.Trigger, QSystemTrayIcon.ActivationReason.DoubleClick):
            self._show_window()

    @staticmethod
    def _create_icon() -> QIcon:
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setPen(QPen(QColor("#0B5F59"), 3))
        painter.setBrush(QColor("#5BC7B8"))
        painter.drawEllipse(8, 10, 48, 48)
        painter.setPen(QPen(QColor("#FFFFFF"), 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawArc(18, 20, 28, 28, 90 * 16, 270 * 16)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#27754C"))
        painter.drawRoundedRect(28, 4, 8, 12, 3, 3)
        painter.end()
        return QIcon(pixmap)
