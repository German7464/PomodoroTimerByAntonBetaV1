"""Ядро таймера, не зависящее от графического интерфейса."""

from app.models import (
    AppSettings,
    OverrunCompletion,
    PeriodCompletion,
    TimeDisplayFormat,
    TimerMode,
    TimerState,
)


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

    def start(self) -> bool:
        """Запускает отсчет, если таймер не ждет ручного перехода."""
        if self.state.waiting_for_continue:
            return False
        self.state.is_running = True
        return True

    def toggle_pause(self) -> bool:
        """Переключает паузу, не останавливая подсчет ручного превышения."""
        if self.state.waiting_for_continue:
            return False
        self.state.is_running = not self.state.is_running
        return True

    def pause(self) -> bool:
        """Ставит обычный период на паузу."""
        if self.state.waiting_for_continue:
            return False
        self.state.is_running = False
        return True

    def reset(self) -> bool:
        """Сбрасывает таймер, кроме защищенного ручного перехода."""
        if self.state.waiting_for_continue:
            return False
        self.state = TimerState(
            mode=TimerMode.WORK,
            remaining_seconds=self.work_seconds,
            is_running=False,
            completed_work_periods=0,
        )
        return True

    def skip_period(self) -> TimerMode | None:
        """Пропускает текущий период и возвращает режим, который был пропущен."""
        if self.state.waiting_for_continue:
            return None

        # При ручном пропуске сохраняем состояние запуска: если таймер шел,
        # следующий период тоже продолжит идти.
        skipped_mode = self.state.mode
        was_running = self.state.is_running
        next_mode = self._next_mode_after(self.state.mode, count_work_completion=False)
        self._set_period(next_mode)
        self.state.is_running = was_running
        return skipped_mode

    def tick(self) -> PeriodCompletion | None:
        """Уменьшает время и возвращает завершенный период, если он дошел до конца."""
        if not self.state.is_running:
            return None

        if self.state.waiting_for_continue:
            self.state.overrun_seconds += 1
            return None

        if self.state.remaining_seconds > 0:
            self.state.remaining_seconds -= 1

        if self.state.remaining_seconds == 0:
            completed_mode = self.state.mode
            next_mode = self._next_mode_after(completed_mode, count_work_completion=True)
            completed_period = PeriodCompletion(
                mode=completed_mode,
                duration_seconds=self.current_period_duration_seconds(),
                next_mode=next_mode,
            )

            if self.settings.auto_start_next_period:
                self._set_period(next_mode)
                self.state.is_running = True
            else:
                self.state.waiting_for_continue = True
                self.state.overrun_seconds = 0
                self.state.overrun_mode = completed_mode
                self.state.next_mode = next_mode
                # Ручное ожидание остается активным: следующие тики считают
                # прямое превышение, а не запускают новый период.
                self.state.is_running = True
            return completed_period

        return None

    def continue_to_next_period(self) -> OverrunCompletion | None:
        """Фиксирует превышение и сразу запускает ожидающий следующий период."""
        completion = self._take_overrun_completion()
        if completion is None:
            return None

        next_mode = self.state.next_mode
        if next_mode is None:  # Защита от частично поврежденного состояния.
            return None

        self._clear_manual_transition()
        self._set_period(next_mode)
        self.state.is_running = True
        return completion

    def finalize_overrun_on_exit(self) -> OverrunCompletion | None:
        """Завершает превышение для сохранения перед полным выходом."""
        completion = self._take_overrun_completion()
        if completion is None:
            return None

        self._clear_manual_transition()
        self.state.is_running = False
        return completion

    def update_settings(self, settings: AppSettings) -> None:
        """Применяет новые настройки без сброса текущего времени."""
        self.settings = settings
        self._update_durations()

    def mode_name(self) -> str:
        """Возвращает название текущего режима для показа в интерфейсе."""
        if self.state.waiting_for_continue:
            if self.state.overrun_mode == TimerMode.WORK:
                return "Переработка"
            if self.state.overrun_mode == TimerMode.SHORT_BREAK:
                return "Короткий отдых сверх нормы"
            if self.state.overrun_mode == TimerMode.LONG_BREAK:
                return "Длинный отдых сверх нормы"
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
        seconds_to_format = (
            self.state.overrun_seconds
            if self.state.waiting_for_continue
            else self.state.remaining_seconds
        )
        prefix = "+" if self.state.waiting_for_continue else ""

        if self.settings.time_display_format == TimeDisplayFormat.MINUTES_SECONDS.value:
            minutes, seconds = divmod(seconds_to_format, 60)
            return f"{prefix}{minutes:02d}:{seconds:02d}"

        hours, remainder = divmod(seconds_to_format, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{prefix}{hours:02d}:{minutes:02d}:{seconds:02d}"

    def _next_mode_after(
        self,
        completed_mode: TimerMode,
        count_work_completion: bool,
    ) -> TimerMode:
        """Возвращает следующий режим и при завершении учитывает рабочий период."""
        if completed_mode == TimerMode.WORK:
            if count_work_completion:
                self.state.completed_work_periods += 1

            should_use_long_break = (
                count_work_completion
                and self.settings.use_long_break
                and self.state.completed_work_periods % max(1, self.settings.long_break_interval) == 0
            )
            if should_use_long_break:
                return TimerMode.LONG_BREAK
            return TimerMode.SHORT_BREAK

        return TimerMode.WORK

    def _set_period(self, mode: TimerMode) -> None:
        """Меняет режим и задает актуальную длительность нового периода."""
        self.state.mode = mode
        self.state.remaining_seconds = self._duration_for_mode(mode)

    def _duration_for_mode(self, mode: TimerMode) -> int:
        """Возвращает длительность указанного режима из текущих настроек."""
        if mode == TimerMode.WORK:
            return self.work_seconds
        if mode == TimerMode.SHORT_BREAK:
            return self.short_break_seconds
        return self.long_break_seconds

    def _take_overrun_completion(self) -> OverrunCompletion | None:
        """Собирает текущее превышение, не изменяя состояние."""
        if not self.state.waiting_for_continue or self.state.overrun_mode is None:
            return None
        return OverrunCompletion(
            mode=self.state.overrun_mode,
            duration_seconds=self.state.overrun_seconds,
        )

    def _clear_manual_transition(self) -> None:
        """Очищает служебные поля завершенного ручного перехода."""
        self.state.waiting_for_continue = False
        self.state.overrun_seconds = 0
        self.state.overrun_mode = None
        self.state.next_mode = None

    def _update_durations(self) -> None:
        """Пересчитывает длительности периодов из текущих настроек."""
        self.work_seconds = self.settings.work_minutes * 60
        self.short_break_seconds = self.settings.short_break_minutes * 60
        self.long_break_seconds = self.settings.long_break_minutes * 60
