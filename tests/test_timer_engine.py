"""Переходы и форматирование независимого ядра таймера."""

import unittest

from app.models import AppSettings, TimeDisplayFormat, TimerMode
from app.timer_engine import TimerEngine


def make_settings(
    *,
    auto_start: bool = False,
    time_format: str = TimeDisplayFormat.HOURS_MINUTES_SECONDS.value,
) -> AppSettings:
    """Создает компактные настройки для тестов."""
    return AppSettings(
        active_profile="Тест",
        work_minutes=1,
        short_break_minutes=1,
        long_break_minutes=1,
        use_long_break=False,
        auto_start_next_period=auto_start,
        time_display_format=time_format,
        notifications_enabled=False,
    )


def finish_current_period(engine: TimerEngine):
    """Доводит текущий режим до граничного тика."""
    engine.state.remaining_seconds = 1
    engine.start()
    return engine.tick()


class TimerEngineTests(unittest.TestCase):
    """Проверяет автоматические и ручные переходы."""

    def test_automatic_transition_does_not_create_overrun(self) -> None:
        engine = TimerEngine(make_settings(auto_start=True))

        completed = finish_current_period(engine)

        self.assertIsNotNone(completed)
        self.assertEqual(completed.mode, TimerMode.WORK)
        self.assertEqual(completed.next_mode, TimerMode.SHORT_BREAK)
        self.assertEqual(engine.state.mode, TimerMode.SHORT_BREAK)
        self.assertTrue(engine.state.is_running)
        self.assertFalse(engine.state.waiting_for_continue)
        self.assertEqual(engine.state.overrun_seconds, 0)
        self.assertIsNone(engine.continue_to_next_period())

    def test_manual_work_completion_starts_overwork_without_switching(self) -> None:
        engine = TimerEngine(make_settings())

        completed = finish_current_period(engine)

        self.assertIsNotNone(completed)
        self.assertEqual(completed.mode, TimerMode.WORK)
        self.assertTrue(engine.state.waiting_for_continue)
        self.assertEqual(engine.state.mode, TimerMode.WORK)
        self.assertEqual(engine.state.next_mode, TimerMode.SHORT_BREAK)
        self.assertEqual(engine.mode_name(), "Переработка")
        self.assertEqual(engine.formatted_time(), "+00:00:00")

        self.assertIsNone(engine.tick())
        self.assertEqual(engine.state.overrun_seconds, 1)
        self.assertEqual(engine.state.mode, TimerMode.WORK)

    def test_next_period_waits_for_continue_then_starts_immediately(self) -> None:
        engine = TimerEngine(make_settings())
        finish_current_period(engine)
        engine.tick()
        engine.tick()

        self.assertEqual(engine.state.mode, TimerMode.WORK)
        self.assertEqual(engine.state.remaining_seconds, 0)

        overrun = engine.continue_to_next_period()

        self.assertIsNotNone(overrun)
        self.assertEqual(overrun.mode, TimerMode.WORK)
        self.assertEqual(overrun.duration_seconds, 2)
        self.assertEqual(engine.state.mode, TimerMode.SHORT_BREAK)
        self.assertEqual(engine.state.remaining_seconds, 60)
        self.assertTrue(engine.state.is_running)
        self.assertFalse(engine.state.waiting_for_continue)
        self.assertIsNone(engine.continue_to_next_period())

    def test_short_and_long_break_overrun_names_are_distinct(self) -> None:
        cases = (
            (TimerMode.SHORT_BREAK, "Короткий отдых сверх нормы"),
            (TimerMode.LONG_BREAK, "Длинный отдых сверх нормы"),
        )

        for mode, expected_name in cases:
            with self.subTest(mode=mode):
                engine = TimerEngine(make_settings())
                engine.state.mode = mode
                completed = finish_current_period(engine)
                engine.tick()

                self.assertEqual(completed.mode, mode)
                self.assertEqual(engine.mode_name(), expected_name)
                self.assertEqual(engine.state.mode, mode)
                overrun = engine.continue_to_next_period()
                self.assertEqual(overrun.mode, mode)
                self.assertEqual(overrun.duration_seconds, 1)
                self.assertEqual(engine.state.mode, TimerMode.WORK)

    def test_completed_period_is_emitted_once(self) -> None:
        engine = TimerEngine(make_settings())

        first_event = finish_current_period(engine)
        later_events = [engine.tick(), engine.tick(), engine.tick()]

        self.assertIsNotNone(first_event)
        self.assertEqual(later_events, [None, None, None])
        self.assertEqual(engine.state.completed_work_periods, 1)

    def test_both_time_formats_show_plus_sign(self) -> None:
        engine = TimerEngine(make_settings())
        finish_current_period(engine)
        engine.state.overrun_seconds = 3723
        self.assertEqual(engine.formatted_time(), "+01:02:03")

        engine.update_settings(
            make_settings(time_format=TimeDisplayFormat.MINUTES_SECONDS.value),
        )
        self.assertEqual(engine.formatted_time(), "+62:03")

    def test_unsafe_commands_are_ignored_during_manual_wait(self) -> None:
        engine = TimerEngine(make_settings())
        finish_current_period(engine)
        engine.tick()
        before = engine.state.overrun_seconds

        self.assertFalse(engine.start())
        self.assertFalse(engine.pause())
        self.assertFalse(engine.toggle_pause())
        self.assertIsNone(engine.skip_period())
        self.assertFalse(engine.reset())
        self.assertTrue(engine.state.waiting_for_continue)
        self.assertEqual(engine.state.overrun_seconds, before)

        engine.tick()
        self.assertEqual(engine.state.overrun_seconds, before + 1)

    def test_exit_finalization_is_idempotent(self) -> None:
        engine = TimerEngine(make_settings())
        finish_current_period(engine)
        engine.tick()
        engine.tick()

        overrun = engine.finalize_overrun_on_exit()

        self.assertEqual(overrun.mode, TimerMode.WORK)
        self.assertEqual(overrun.duration_seconds, 2)
        self.assertFalse(engine.state.waiting_for_continue)
        self.assertFalse(engine.state.is_running)
        self.assertIsNone(engine.finalize_overrun_on_exit())


if __name__ == "__main__":
    unittest.main()
