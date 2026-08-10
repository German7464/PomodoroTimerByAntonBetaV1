"""Ядро таймера, не зависящее от графического интерфейса."""

from app.models import AppSettings, PeriodCompletion, TimeDisplayFormat, TimerMode, TimerState


class TimerEngine:
    """Управляет режимами, временем и состоянием Pomodoro-таймера."""

    def __init__(self, settings: AppSettings) -> None:
        """Создает остановленный таймер в первом рабочем периоде."""
        self.settings = settings
        self._update_durations()

        self.state = TimerState(
            mode=TimerMode.WORK,
            remaining_seconds=self.work_seconds,
            is_running=False,
            completed_work_periods=0,
        )

    def start(self) -> None:
        """Запускает отсчет времени."""
        self.state.is_running = True

    def toggle_pause(self) -> None:
        """Переключает таймер между паузой и продолжением."""
        self.state.is_running = not self.state.is_running

    def pause(self) -> None:
        """Ставит отсчет времени на паузу."""
        self.state.is_running = False

    def reset(self) -> None:
        """Полностью сбрасывает таймер к первому рабочему периоду."""
        self.state = TimerState(
            mode=TimerMode.WORK,
            remaining_seconds=self.work_seconds,
            is_running=False,
            completed_work_periods=0,
        )

    def skip_period(self) -> TimerMode:
        """Пропускает текущий период и возвращает режим, который был пропущен."""
        # При ручном пропуске сохраняем состояние запуска: если таймер шел,
        # следующий период тоже продолжит идти.
        skipped_mode = self.state.mode
        was_running = self.state.is_running
        self._switch_to_next_period(count_work_completion=False)
        self.state.is_running = was_running
        return skipped_mode

    def tick(self) -> PeriodCompletion | None:
        """Уменьшает время и возвращает завершенный период, если он дошел до конца."""
        if not self.state.is_running:
            return None

        if self.state.remaining_seconds > 0:
            self.state.remaining_seconds -= 1

        if self.state.remaining_seconds == 0:
            completed_period = PeriodCompletion(
                mode=self.state.mode,
                duration_seconds=self.current_period_duration_seconds(),
            )
            self._switch_to_next_period(count_work_completion=True)
            self.state.is_running = self.settings.auto_start_next_period
            return completed_period

        return None

    def update_settings(self, settings: AppSettings) -> None:
        """Применяет новые настройки без сброса текущего времени."""
        self.settings = settings
        self._update_durations()

    def mode_name(self) -> str:
        """Возвращает название текущего режима для показа в интерфейсе."""
        return self.state.mode.value

    def current_period_duration_seconds(self) -> int:
        """Возвращает полную длительность текущего периода в секундах."""
        if self.state.mode == TimerMode.WORK:
            return self.work_seconds
        if self.state.mode == TimerMode.SHORT_BREAK:
            return self.short_break_seconds
        return self.long_break_seconds

    def formatted_time(self) -> str:
        """Возвращает оставшееся время в выбранном пользователем формате."""
        if self.settings.time_display_format == TimeDisplayFormat.MINUTES_SECONDS.value:
            minutes, seconds = divmod(self.state.remaining_seconds, 60)
            return f"{minutes:02d}:{seconds:02d}"

        hours, remainder = divmod(self.state.remaining_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def _switch_to_next_period(self, count_work_completion: bool) -> None:
        """Выбирает следующий режим по правилам Pomodoro."""
        if self.state.mode == TimerMode.WORK:
            if count_work_completion:
                self.state.completed_work_periods += 1

            should_use_long_break = (
                count_work_completion
                and self.settings.use_long_break
                and self.state.completed_work_periods % self.settings.long_break_interval == 0
            )
            if should_use_long_break:
                self._set_period(TimerMode.LONG_BREAK, self.long_break_seconds)
            else:
                self._set_period(TimerMode.SHORT_BREAK, self.short_break_seconds)
            return

        self._set_period(TimerMode.WORK, self.work_seconds)

    def _set_period(self, mode: TimerMode, seconds: int) -> None:
        """Меняет режим и задает длительность нового периода."""
        self.state.mode = mode
        self.state.remaining_seconds = seconds

    def _update_durations(self) -> None:
        """Пересчитывает длительности периодов из текущих настроек."""
        self.work_seconds = self.settings.work_minutes * 60
        self.short_break_seconds = self.settings.short_break_minutes * 60
        self.long_break_seconds = self.settings.long_break_minutes * 60
