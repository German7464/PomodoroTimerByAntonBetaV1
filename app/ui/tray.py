"""Интеграция приложения с системным треем Windows."""

from collections.abc import Callable
import threading

import pystray
from PIL import Image, ImageDraw


class TrayController:
    """Управляет иконкой в трее и прокидывает команды в главное окно."""

    def __init__(
        self,
        show_window: Callable[[], None],
        hide_window: Callable[[], None],
        toggle_timer: Callable[[], None],
        reset_timer: Callable[[], None],
        exit_app: Callable[[], None],
    ) -> None:
        """Получает callback-и главного окна и создает pystray.Icon."""
        self._show_window = show_window
        self._hide_window = hide_window
        self._toggle_timer = toggle_timer
        self._reset_timer = reset_timer
        self._exit_app = exit_app
        self._thread: threading.Thread | None = None
        self.icon = pystray.Icon(
            "Pomodoro Timer",
            self._create_icon_image(),
            "Pomodoro Timer",
            self._create_menu(),
        )

    def start(self) -> None:
        """Запускает иконку трея в отдельном daemon-потоке."""
        if self._thread is not None and self._thread.is_alive():
            return

        self._thread = threading.Thread(target=self.icon.run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Останавливает иконку трея перед выходом из приложения."""
        self.icon.stop()

    def _create_menu(self) -> pystray.Menu:
        """Создает меню трея с основными действиями приложения."""
        return pystray.Menu(
            pystray.MenuItem("Показать окно", self._run(self._show_window)),
            pystray.MenuItem("Скрыть окно", self._run(self._hide_window)),
            pystray.MenuItem("Старт / Пауза", self._run(self._toggle_timer)),
            pystray.MenuItem("Сброс", self._run(self._reset_timer)),
            pystray.MenuItem("Выход", self._run(self._exit_app)),
        )

    def _run(self, callback: Callable[[], None]) -> Callable[[], None]:
        """Оборачивает callback, чтобы pystray вызывал единообразные команды."""
        def wrapped(*_args) -> None:
            callback()

        return wrapped

    def _create_icon_image(self) -> Image.Image:
        """Создает простую иконку Pomodoro без внешнего файла."""
        image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((8, 10, 56, 58), fill=(220, 68, 55, 255), outline=(120, 30, 25, 255), width=3)
        draw.rectangle((28, 4, 36, 14), fill=(60, 140, 70, 255))
        draw.arc((18, 20, 46, 48), start=90, end=360, fill=(255, 255, 255, 230), width=4)
        return image
