"""Точка входа в приложение Pomodoro Timer."""

from collections.abc import Callable
from typing import Protocol

from app.single_instance import (
    ALREADY_RUNNING_KEY,
    SingleInstanceError,
    SingleInstanceLock,
    show_native_message,
)
from app.early_i18n import early_tr


class RunnableWindow(Protocol):
    """Минимальный контракт окна для тестирования точки входа без GUI."""

    def run(self) -> None:
        """Запускает цикл приложения."""


def main(
    lock_factory: Callable[[], SingleInstanceLock] = SingleInstanceLock,
    window_factory: Callable[[], RunnableWindow] | None = None,
    message_function: Callable[..., None] = show_native_message,
) -> int:
    """Получает mutex до импорта Qt и запускает только первый экземпляр."""
    lock = lock_factory()
    try:
        acquired = lock.acquire()
    except SingleInstanceError as error:
        message_function(early_tr(error.key, **error.parameters), error=True)
        return 1

    if not acquired:
        message_function(early_tr(ALREADY_RUNNING_KEY))
        return 0

    try:
        if window_factory is None:
            # Импорт отложен: второй процесс не создает QApplication и не загружает
            # настройки/трей перед проверкой единственного экземпляра.
            from app.ui.main_window import MainWindow

            window_factory = MainWindow
        window = window_factory()
        window.run()
        return 0
    finally:
        try:
            lock.release()
        except SingleInstanceError as error:
            message_function(early_tr(error.key, **error.parameters), error=True)


if __name__ == "__main__":
    raise SystemExit(main())
