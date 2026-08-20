"""Тематизированные уведомления о завершении периодов на Qt Widgets."""

from collections.abc import Callable

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QWidget

from app.models import AppSettings, TimerMode
from app.i18n import localization_manager, timer_mode_text, tr
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
        self._active_label: QLabel | None = None
        self._active_button: AppButton | None = None
        self._active_modes: tuple[TimerMode, TimerMode] | None = None
        self._disposed = False
        localization_manager().language_changed.connect(self._retranslate_active)

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
            self._show_popup(message, "action.close", None, completed_mode, next_mode)
        else:
            self._show_popup(message, "action.continue", on_continue, completed_mode, next_mode)

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
        self._active_label = None
        self._active_button = None
        self._active_modes = None

    def dispose(self) -> None:
        """Закрывает уведомление и снимает глобальную подписку при завершении UI."""
        if self._disposed:
            return
        self._disposed = True
        localization_manager().language_changed.disconnect(self._retranslate_active)
        self.dismiss()

    def _build_message(self, completed_mode: TimerMode, next_mode: TimerMode) -> str:
        completed_text = self._completed_period_text(completed_mode)
        next_text = timer_mode_text(next_mode)
        if self.settings.auto_start_next_period:
            return tr(
                "notification.auto_transition",
                completed=completed_text,
                next_period=next_text,
            )
        return tr(
            "notification.manual_transition",
            completed=completed_text,
            next_period=next_text,
        )

    @staticmethod
    def _completed_period_text(mode: TimerMode) -> str:
        if mode == TimerMode.WORK:
            return tr("notification.completed.work")
        if mode == TimerMode.SHORT_BREAK:
            return tr("notification.completed.short_break")
        return tr("notification.completed.long_break")

    def _show_popup(
        self,
        message: str,
        button_key: str,
        command: Callable[[], None] | None,
        completed_mode: TimerMode | None = None,
        next_mode: TimerMode | None = None,
    ) -> None:
        self.dismiss()
        window = QDialog(self.parent, Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint)
        self._active_window = window
        self._active_modes = (
            (completed_mode, next_mode)
            if completed_mode is not None and next_mode is not None
            else None
        )
        window.setWindowTitle("Pomodoro Timer")
        window.setWindowIcon(application_icon())
        window.setModal(False)
        window.setMinimumWidth(410)
        window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        layout = QVBoxLayout(window)
        layout.setContentsMargins(TOKENS.spacing.md, TOKENS.spacing.md, TOKENS.spacing.md, TOKENS.spacing.md)
        card = Card(window, padding=TOKENS.spacing.lg)
        label = QLabel(message, card)
        self._active_label = label
        label.setWordWrap(True)
        label.setProperty("role", "subtitle")
        card.content_layout.addWidget(label)
        button = AppButton(
            tr(button_key),
            card,
            variant="primary",
            theme_manager=self.theme_manager,
        )
        button.setProperty("translationKey", button_key)
        self._active_button = button

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
            self._active_label = None
            self._active_button = None
            self._active_modes = None

    def _retranslate_active(self, _language_code: str) -> None:
        if self._active_window is None or self._active_modes is None:
            return
        completed_mode, next_mode = self._active_modes
        self._active_window.setWindowTitle("Pomodoro Timer")
        if self._active_label is not None:
            self._active_label.setText(self._build_message(completed_mode, next_mode))
        if self._active_button is not None:
            self._active_button.setText(tr(str(self._active_button.property("translationKey"))))
            self._active_button.updateGeometry()
        self._active_window.adjustSize()
