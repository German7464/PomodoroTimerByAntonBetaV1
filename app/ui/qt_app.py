"""Общие адаптеры жизненного цикла Qt-приложения."""

from __future__ import annotations

from collections.abc import Callable, Sequence
import sys

from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

from app.config import APP_NAME
from app.ui.design_system import TOKENS


def ensure_application(argv: Sequence[str] | None = None) -> QApplication:
    """Создаёт единственный QApplication и задаёт общие Windows-параметры."""
    application = QApplication.instance()
    if application is None:
        application = QApplication(list(argv) if argv is not None else sys.argv)
    application.setApplicationName(APP_NAME)
    application.setOrganizationName("PomodoroTimerByAnton")
    application.setQuitOnLastWindowClosed(False)
    font = QFont(TOKENS.typography.family, TOKENS.typography.body)
    font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
    application.setFont(font)
    return application


class QtScheduler:
    """Адаптирует одноразовые QTimer к контракту OverrunVisualController."""

    def __init__(self, parent) -> None:
        self.parent = parent
        self._timers: set[QTimer] = set()

    def schedule(self, delay_ms: int, callback: Callable[[], None]) -> QTimer:
        timer = QTimer(self.parent)
        timer.setSingleShot(True)

        def fire() -> None:
            self._timers.discard(timer)
            timer.deleteLater()
            callback()

        timer.timeout.connect(fire)
        self._timers.add(timer)
        timer.start(max(0, int(delay_ms)))
        return timer

    def cancel(self, handle: object) -> None:
        if not isinstance(handle, QTimer):
            return
        self._timers.discard(handle)
        handle.stop()
        handle.deleteLater()

    def stop_all(self) -> None:
        for timer in tuple(self._timers):
            timer.stop()
            timer.deleteLater()
        self._timers.clear()


class Debouncer:
    """Один отложенный callback для записи настроек после потока UI-событий."""

    def __init__(self, parent, delay_ms: int, callback: Callable[[], None]) -> None:
        self.timer = QTimer(parent)
        self.timer.setSingleShot(True)
        self.timer.setInterval(delay_ms)
        self.timer.timeout.connect(callback)

    def trigger(self) -> None:
        self.timer.start()

    def flush(self) -> None:
        if not self.timer.isActive():
            return
        self.timer.stop()
        self.timer.timeout.emit()

    def cancel(self) -> None:
        self.timer.stop()
