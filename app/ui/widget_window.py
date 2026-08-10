"""Плавающее окно-виджет, которое показывает состояние общего таймера."""

import tkinter as tk

from app.config import SETTINGS_FILE
from app.models import AppSettings
from app.storage import save_app_settings
from app.timer_engine import TimerEngine


class WidgetWindow:
    """Маленькое окно таймера, использующее общий TimerEngine приложения."""

    WIDTH = 220
    HEIGHT = 96

    def __init__(self, parent: tk.Tk, timer: TimerEngine, settings: AppSettings) -> None:
        """Создает виджет, но не создает отдельный таймер."""
        self.parent = parent
        self.timer = timer
        self.settings = settings
        self.window: tk.Toplevel | None = None
        self.mode_label: tk.Label | None = None
        self.time_label: tk.Label | None = None
        self._drag_offset_x = 0
        self._drag_offset_y = 0
        self.apply_settings(settings)

    def apply_settings(self, settings: AppSettings) -> None:
        """Применяет настройки виджета: цвета, прозрачность и поверх окон."""
        self.settings = settings

        if not settings.widget_enabled:
            self.hide()
            return

        self._ensure_window()
        if self.window is None:
            return

        self.window.geometry(
            f"{self.WIDTH}x{self.HEIGHT}+{settings.widget_x}+{settings.widget_y}",
        )
        self.window.configure(bg=settings.widget_background_color)
        self.window.attributes("-alpha", settings.widget_opacity / 100)
        self.window.attributes("-topmost", settings.widget_always_on_top)

        for label in (self.mode_label, self.time_label):
            if label is not None:
                label.configure(
                    bg=settings.widget_background_color,
                    fg=settings.widget_text_color,
                )

        self.update()
        self.window.deiconify()

    def update(self) -> None:
        """Обновляет текст виджета по состоянию общего таймера."""
        if self.window is None or not self.settings.widget_enabled:
            return

        if self.mode_label is not None:
            self.mode_label.config(text=self.timer.mode_name())
        if self.time_label is not None:
            self.time_label.config(text=self.timer.formatted_time())

    def hide(self) -> None:
        """Скрывает виджет, если он был создан."""
        if self.window is not None:
            self.window.withdraw()

    def _ensure_window(self) -> None:
        """Создает окно виджета при первом включении."""
        if self.window is not None:
            return

        self.window = tk.Toplevel(self.parent)
        self.window.title("Виджет Pomodoro")
        self.window.resizable(False, False)
        self.window.minsize(self.WIDTH, self.HEIGHT)
        self.window.protocol("WM_DELETE_WINDOW", self.hide)

        self.mode_label = tk.Label(
            self.window,
            anchor="center",
            font=("Segoe UI", 10, "bold"),
        )
        self.mode_label.pack(fill=tk.X, padx=16, pady=(12, 2))

        self.time_label = tk.Label(
            self.window,
            anchor="center",
            font=("Segoe UI", 22, "bold"),
        )
        self.time_label.pack(fill=tk.X, padx=16, pady=(0, 12))

        for widget in (self.window, self.mode_label, self.time_label):
            widget.bind("<ButtonPress-1>", self._start_drag)
            widget.bind("<B1-Motion>", self._drag)
            widget.bind("<ButtonRelease-1>", self._finish_drag)

    def _start_drag(self, event: tk.Event) -> None:
        """Запоминает точку, за которую пользователь схватил виджет."""
        if self.window is None:
            return
        self._drag_offset_x = event.x_root - self.window.winfo_x()
        self._drag_offset_y = event.y_root - self.window.winfo_y()

    def _drag(self, event: tk.Event) -> None:
        """Перемещает окно вслед за мышью."""
        if self.window is None:
            return
        x = max(0, event.x_root - self._drag_offset_x)
        y = max(0, event.y_root - self._drag_offset_y)
        self.window.geometry(f"+{x}+{y}")

    def _finish_drag(self, _event: tk.Event) -> None:
        """Сохраняет последнюю позицию виджета в settings.json."""
        if self.window is None:
            return
        self.settings.widget_x = max(0, self.window.winfo_x())
        self.settings.widget_y = max(0, self.window.winfo_y())
        save_app_settings(SETTINGS_FILE, self.settings)
