"""Тематизированные уведомления о завершении периодов на Qt Widgets."""

from collections.abc import Callable

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QWidget

from app.models import AppSettings, TimerMode
from app.theme import ThemeManager
from app.ui.components import AppButton, Card
from app.ui.design_system import TOKENS
from app.ui.icons import application_icon

try:
    import winsound
except ImportError:  # pragma: no cover
    winsound = None


class NotificationService:
    """Показывает одно доступное уведомление без изменения TimerEngine."""

    def __init__(
        self,
        parent: QWidget,
        settings: AppSettings,
        theme_manager: ThemeManager | None = None,
    ) -> None:
        self.parent = parent
        self.settings = settings
        self.theme_manager = theme_manager
        self._active_window: QDialog | None = None

    def update_settings(self, settings: AppSettings) -> None:
        self.settings = settings

    def notify_period_finished(
        self,
        completed_mode: TimerMode,
        next_mode: TimerMode,
        on_continue: Callable[[], None],
    ) -> None:
        if not self.settings.notifications_enabled:
            return
        if self.settings.notification_sound_enabled:
            self.play_sound()
        message = self._build_message(completed_mode, next_mode)
        if self.settings.auto_start_next_period:
            self._show_popup(message, "Закрыть", None)
        else:
            self._show_popup(message, "Продолжить", on_continue)

    def play_sound(self) -> None:
        if winsound is not None:
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
        else:
            QApplication.beep()

    def dismiss(self) -> None:
        window = self._active_window
        self._active_window = None
        if window is not None:
            window.close()
            window.deleteLater()

    def _build_message(self, completed_mode: TimerMode, next_mode: TimerMode) -> str:
        completed_text = self._completed_period_text(completed_mode)
        next_text = next_mode.value.lower()
        if self.settings.auto_start_next_period:
            return f"{completed_text}\n\nСледующий период уже запущен: {next_text}."
        return f"{completed_text}\n\nНажмите «Продолжить», чтобы начать {next_text}."

    @staticmethod
    def _completed_period_text(mode: TimerMode) -> str:
        if mode == TimerMode.WORK:
            return "Рабочий период завершён."
        if mode == TimerMode.SHORT_BREAK:
            return "Короткий отдых завершён."
        return "Длинный отдых завершён."

    def _show_popup(
        self,
        message: str,
        button_text: str,
        command: Callable[[], None] | None,
    ) -> None:
        self.dismiss()
        window = QDialog(self.parent, Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint)
        self._active_window = window
        window.setWindowTitle("Pomodoro Timer")
        window.setWindowIcon(application_icon())
        window.setModal(False)
        window.setMinimumWidth(410)
        window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        layout = QVBoxLayout(window)
        layout.setContentsMargins(TOKENS.spacing.md, TOKENS.spacing.md, TOKENS.spacing.md, TOKENS.spacing.md)
        card = Card(window, padding=TOKENS.spacing.lg)
        label = QLabel(message, card)
        label.setWordWrap(True)
        label.setProperty("role", "subtitle")
        card.content_layout.addWidget(label)
        button = AppButton(
            button_text,
            card,
            variant="primary",
            theme_manager=self.theme_manager,
        )

        def handle_button() -> None:
            window.accept()
            if command is not None:
                command()

        button.clicked.connect(handle_button)
        card.content_layout.addWidget(button, 0, Qt.AlignmentFlag.AlignRight)
        layout.addWidget(card)
        if self.theme_manager is not None:
            self.theme_manager.apply_to_window(window)
        window.finished.connect(lambda _result, target=window: self._clear_if_active(target))
        window.show()
        window.raise_()
        window.activateWindow()
        if self.settings.auto_start_next_period:
            timeout = QTimer(window)
            timeout.setSingleShot(True)
            timeout.timeout.connect(window.close)
            timeout.start(10_000)

    def _clear_if_active(self, window: QDialog) -> None:
        if self._active_window is window:
            self._active_window = None
