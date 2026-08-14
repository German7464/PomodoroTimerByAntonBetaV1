"""Функциональное соответствие ядра и новых Qt-представлений."""

from dataclasses import asdict
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from PySide6.QtWidgets import QWidget

from app.models import TimerMode
from app.notifications import NotificationService
from app.statistics import StatisticsService
from app.theme import ThemeManager
from app.timer_engine import TimerEngine
from app.ui.widget_window import WidgetActions
from tests.qt_helpers import APP, isolated_main
from tests.test_timer_engine import finish_current_period, make_settings


class UiContractTests(unittest.TestCase):
    def test_main_window_and_widget_render_the_same_timer_state(self) -> None:
        settings = make_settings()
        settings.widget_enabled = True
        with isolated_main(settings) as (window, _settings, _statistics):
            finish_current_period(window.timer)
            window.timer.tick()
            window._refresh_labels()
            APP.processEvents()
            visual = window.widget_window.view.timer_visual
            self.assertEqual(window.timer_visual.mode_label.text(), "Переработка")
            self.assertEqual(window.timer_visual.time_label.text(), "+00:00:01")
            self.assertEqual(visual.mode_label.text(), window.timer_visual.mode_label.text())
            self.assertEqual(visual.time_label.text(), window.timer_visual.time_label.text())
            self.assertTrue(window.continue_button.isEnabled())
            self.assertFalse(window.skip_button.isEnabled())

    def test_continue_handler_records_overrun_only_once(self) -> None:
        with isolated_main(make_settings()) as (window, _settings, _statistics):
            completed = finish_current_period(window.timer)
            window.timer.tick()
            window.timer.tick()
            window.statistics.record_completed_period(
                completed.mode, completed.duration_seconds, use_long_break=False,
            )
            window.continue_after_notification()
            window.continue_manual_transition()
            stats = window.statistics.all_time_stats()
            self.assertEqual(stats["overwork_seconds"], 2)
            self.assertEqual(stats["work_seconds"], 60)
            self.assertEqual(stats["completed_work_periods"], 1)
            self.assertEqual(window.timer.state.mode, TimerMode.SHORT_BREAK)
            self.assertTrue(window.timer.state.is_running)

    def test_automatic_flow_leaves_all_overrun_statistics_zero(self) -> None:
        with TemporaryDirectory() as directory:
            timer = TimerEngine(make_settings(auto_start=True))
            completed = finish_current_period(timer)
            statistics = StatisticsService(Path(directory) / "statistics.json")
            statistics.record_completed_period(
                completed.mode, completed.duration_seconds, use_long_break=False,
            )
            stats = statistics.all_time_stats()
            self.assertEqual(stats["work_seconds"], 60)
            self.assertEqual(stats["overwork_seconds"], 0)
            self.assertFalse(timer.state.waiting_for_continue)

    def test_closing_notification_does_not_continue_or_lose_overrun(self) -> None:
        timer = TimerEngine(make_settings())
        finish_current_period(timer)
        timer.tick()
        before = asdict(timer.state)
        parent = QWidget()
        manager = ThemeManager(parent)
        service = NotificationService(parent, timer.settings, manager)
        service._show_popup("Проверка", "Продолжить", lambda: timer.continue_to_next_period())
        APP.processEvents()
        service._active_window.close()
        APP.processEvents()
        self.assertEqual(asdict(timer.state), before)
        timer.tick()
        self.assertEqual(timer.state.overrun_seconds, 2)
        parent.close()

    def test_full_exit_saves_pending_overrun(self) -> None:
        with isolated_main(make_settings()) as (window, _settings, _statistics):
            finish_current_period(window.timer)
            window.timer.tick()
            window.timer.tick()
            window.exit_app()
            self.assertEqual(window.statistics.all_time_stats()["overwork_seconds"], 2)
            self.assertFalse(window.timer.state.waiting_for_continue)
            self.assertFalse(window._tick_timer.isActive())

    def test_widget_uses_shared_engine_and_common_continue(self) -> None:
        settings = make_settings()
        settings.widget_enabled = True
        with isolated_main(settings) as (window, _settings, _statistics):
            self.assertIs(window.widget_window.timer, window.timer)
            self.assertIs(window.widget_window.view.timer, window.timer)
            actions = window.widget_window.actions
            self.assertIsInstance(actions, WidgetActions)
            finish_current_period(window.timer)
            window.timer.tick()
            window.widget_window.view._handle_primary()
            window.widget_window.view._handle_primary()
            self.assertEqual(window.statistics.all_time_stats()["overwork_seconds"], 1)
            self.assertFalse(window.timer.state.waiting_for_continue)


if __name__ == "__main__":
    unittest.main()
