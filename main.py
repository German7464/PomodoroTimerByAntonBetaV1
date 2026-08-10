"""Точка входа в приложение Pomodoro Timer."""

from app.ui.main_window import MainWindow


def main() -> None:
    """Создает и запускает главное окно приложения."""
    window = MainWindow()
    window.run()


if __name__ == "__main__":
    main()
