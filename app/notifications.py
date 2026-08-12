"""Уведомления о завершении периодов таймера."""

from collections.abc import Callable
import tkinter as tk
from tkinter import ttk

from app.models import AppSettings, TimerMode
from app.theme import ThemeManager

try:
    import winsound
except ImportError:  # pragma: no cover - на не-Windows системах winsound недоступен.
    winsound = None


class NotificationService:
    """Показывает уведомления о периодах без сторонних библиотек."""

    def __init__(
        self,
        parent: tk.Tk,
        settings: AppSettings,
        theme_manager: ThemeManager | None = None,
    ) -> None:
        """Запоминает главное окно, чтобы показывать уведомления поверх него."""
        self.parent = parent
        self.settings = settings
        self.theme_manager = theme_manager
        self._active_window: tk.Toplevel | None = None

    def update_settings(self, settings: AppSettings) -> None:
        """Применяет новые настройки уведомлений."""
        self.settings = settings

    def notify_period_finished(
        self,
        completed_mode: TimerMode,
        next_mode: TimerMode,
        on_continue: Callable[[], None],
    ) -> None:
        """Показывает уведомление с поведением под автоматический или ручной режим."""
        if not self.settings.notifications_enabled:
            return

        if self.settings.notification_sound_enabled:
            self.play_sound()

        message = self._build_message(completed_mode, next_mode)
        if self.settings.auto_start_next_period:
            self._show_popup(message=message, button_text="Закрыть", command=None)
        else:
            self._show_popup(message=message, button_text="Продолжить", command=on_continue)

    def play_sound(self) -> None:
        """Воспроизводит стандартный системный звук Windows, если он доступен."""
        if winsound is not None:
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
        else:
            self.parent.bell()

    def dismiss(self) -> None:
        """Закрывает активное уведомление, не продолжая таймер автоматически."""
        if self._active_window is not None:
            self._destroy_popup(self._active_window)

    def _build_message(self, completed_mode: TimerMode, next_mode: TimerMode) -> str:
        """Собирает понятный текст уведомления с учетом режима перехода."""
        completed_text = self._completed_period_text(completed_mode)
        next_text = next_mode.value.lower()

        if self.settings.auto_start_next_period:
            return (
                f"{completed_text}\n"
                "Режим: автоматический переход.\n"
                f"Следующий период уже запущен: {next_text}."
            )

        return (
            f"{completed_text}\n"
            "Режим: ручной переход.\n"
            f"Нажмите «Продолжить», чтобы начать {next_text}."
        )

    def _completed_period_text(self, mode: TimerMode) -> str:
        """Возвращает строку о завершенном периоде."""
        if mode == TimerMode.WORK:
            return "Рабочий период завершен."
        if mode == TimerMode.SHORT_BREAK:
            return "Короткий отдых завершен."
        return "Длинный отдых завершен."

    def _show_popup(
        self,
        message: str,
        button_text: str,
        command: Callable[[], None] | None,
    ) -> None:
        """Создает аккуратное окно уведомления с одной главной кнопкой."""
        self.dismiss()
        window = tk.Toplevel(self.parent)
        self._active_window = window
        window.title("Pomodoro Timer")
        window.resizable(False, False)
        window.transient(self.parent)
        window.attributes("-topmost", True)

        frame = ttk.Frame(window, padding=20, style="Card.TFrame")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            frame,
            text=message,
            wraplength=360,
            justify=tk.LEFT,
            style="Card.TLabel",
        ).pack(pady=(0, 16))

        def handle_button() -> None:
            # В ручном режиме callback выполняет единый переход и запись
            # статистики. Закрытие крестиком этот callback не вызывает.
            if command is not None:
                command()
            self._destroy_popup(window)

        ttk.Button(
            frame,
            text=button_text,
            command=handle_button,
            style="Accent.TButton",
        ).pack(anchor=tk.E)
        window.protocol("WM_DELETE_WINDOW", lambda: self._destroy_popup(window))
        if self.theme_manager is not None:
            self.theme_manager.apply_to_window(window)

        if self.settings.auto_start_next_period:
            window.after(10000, lambda: self._destroy_popup(window))

    def _destroy_popup(self, window: tk.Toplevel) -> None:
        """Безопасно уничтожает окно и очищает ссылку на него."""
        try:
            if window.winfo_exists():
                window.destroy()
        except tk.TclError:
            pass
        if self._active_window is window:
            self._active_window = None
