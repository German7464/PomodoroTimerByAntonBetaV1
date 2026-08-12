"""Контракты общего состояния между ядром и Tkinter-адаптерами."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from app.models import TimerMode
from app.notifications import NotificationService
from app.statistics import StatisticsService
from app.timer_engine import TimerEngine
from app.ui.main_window import MainWindow
from app.ui.widget_window import WidgetWindow
from app.ui.widget_window import WidgetActions, WidgetView
from tests.test_timer_engine import finish_current_period, make_settings


class FakeWidget:
    """Минимальная замена Tk-виджета для проверки config/state."""

    def __init__(self, state: str = "normal") -> None:
        self.values = {"state": state, "text": ""}

    def config(self, **values) -> None:
        self.values.update(values)

    def __getitem__(self, key: str):
        return self.values[key]


class FakeWidgetWindow:
    """Запоминает отображение того же TimerEngine, что использует окно."""

    def __init__(self, timer: TimerEngine) -> None:
        self.timer = timer
        self.mode = ""
        self.time = ""

    def update(self) -> None:
        self.mode = self.timer.mode_name()
        self.time = self.timer.formatted_time()


class FakePopup:
    """Окно уведомления без Tk."""

    def __init__(self) -> None:
        self.destroyed = False

    def winfo_exists(self) -> bool:
        return not self.destroyed

    def destroy(self) -> None:
        self.destroyed = True


class CounterObject:
    """Считает вызовы произвольных методов через явные адаптеры."""

    def __init__(self) -> None:
        self.calls = 0

    def refresh(self) -> None:
        self.calls += 1

    def dismiss(self) -> None:
        self.calls += 1

    def stop(self) -> None:
        self.calls += 1

    def destroy(self) -> None:
        self.calls += 1


class FakeButton:
    """Кнопка, вызывающая сохраненную команду без Tk."""

    def __init__(self, command) -> None:
        self.command = command

    def invoke(self) -> None:
        self.command()


def prepare_main_window(timer: TimerEngine, statistics: StatisticsService) -> MainWindow:
    """Создает MainWindow без графического окружения для вызова обработчиков."""
    window = MainWindow.__new__(MainWindow)
    window.timer = timer
    window.statistics = statistics
    window.notifications = CounterObject()
    window.stats_view = CounterObject()
    window.start_button = FakeWidget()
    window.pause_button = FakeWidget()
    window.skip_button = FakeWidget()
    window.reset_button = FakeWidget()
    window.continue_button = FakeWidget()
    window.mode_label = FakeWidget()
    window.time_label = FakeWidget()
    window.status_label = FakeWidget()
    window.widget_window = FakeWidgetWindow(timer)
    return window


class UiContractTests(unittest.TestCase):
    """Проверяет единый переход и одинаковое отображение состояния."""

    def test_main_window_and_widget_render_the_same_timer_state(self) -> None:
        with TemporaryDirectory() as directory:
            timer = TimerEngine(make_settings())
            finish_current_period(timer)
            timer.tick()
            statistics = StatisticsService(Path(directory) / "statistics.json")
            window = prepare_main_window(timer, statistics)

            window._refresh_labels()

            self.assertEqual(window.mode_label.values["text"], "Переработка")
            self.assertEqual(window.time_label.values["text"], "+00:00:01")
            self.assertEqual(window.widget_window.mode, window.mode_label.values["text"])
            self.assertEqual(window.widget_window.time, window.time_label.values["text"])
            self.assertEqual(window.continue_button.values["state"], "normal")
            self.assertEqual(window.skip_button.values["state"], "disabled")

    def test_continue_handler_records_overrun_only_once(self) -> None:
        with TemporaryDirectory() as directory:
            timer = TimerEngine(make_settings())
            completed = finish_current_period(timer)
            timer.tick()
            timer.tick()
            statistics = StatisticsService(Path(directory) / "statistics.json")
            statistics.record_completed_period(
                completed.mode,
                completed.duration_seconds,
                use_long_break=False,
            )
            window = prepare_main_window(timer, statistics)

            window.continue_after_notification()
            window.continue_manual_transition()

            self.assertEqual(statistics.all_time_stats()["overwork_seconds"], 2)
            self.assertEqual(statistics.all_time_stats()["work_seconds"], 60)
            self.assertEqual(statistics.all_time_stats()["completed_work_periods"], 1)
            self.assertEqual(timer.state.mode, TimerMode.SHORT_BREAK)
            self.assertTrue(timer.state.is_running)
            self.assertEqual(window.notifications.calls, 1)

    def test_automatic_flow_leaves_all_overrun_statistics_zero(self) -> None:
        with TemporaryDirectory() as directory:
            timer = TimerEngine(make_settings(auto_start=True))
            completed = finish_current_period(timer)
            statistics = StatisticsService(Path(directory) / "statistics.json")

            statistics.record_completed_period(
                completed.mode,
                completed.duration_seconds,
                use_long_break=False,
            )

            stats = statistics.all_time_stats()
            self.assertEqual(stats["work_seconds"], 60)
            self.assertEqual(stats["overwork_seconds"], 0)
            self.assertEqual(stats["short_break_overrun_seconds"], 0)
            self.assertEqual(stats["long_break_overrun_seconds"], 0)
            self.assertFalse(timer.state.waiting_for_continue)

    def test_closing_notification_does_not_continue_or_lose_overrun(self) -> None:
        timer = TimerEngine(make_settings())
        finish_current_period(timer)
        timer.tick()
        popup = FakePopup()
        notifications = NotificationService.__new__(NotificationService)
        notifications._active_window = popup

        notifications.dismiss()

        self.assertTrue(popup.destroyed)
        self.assertIsNone(notifications._active_window)
        self.assertTrue(timer.state.waiting_for_continue)
        self.assertEqual(timer.state.overrun_seconds, 1)
        timer.tick()
        self.assertEqual(timer.state.overrun_seconds, 2)

    def test_full_exit_saves_pending_overrun(self) -> None:
        with TemporaryDirectory() as directory:
            timer = TimerEngine(make_settings())
            finish_current_period(timer)
            timer.tick()
            timer.tick()
            statistics = StatisticsService(Path(directory) / "statistics.json")
            window = prepare_main_window(timer, statistics)
            window.tray = CounterObject()
            window.root = CounterObject()

            window.exit_app()

            self.assertEqual(statistics.all_time_stats()["overwork_seconds"], 2)
            self.assertFalse(timer.state.waiting_for_continue)
            self.assertEqual(window.tray.calls, 1)
            self.assertEqual(window.root.calls, 1)

    def test_widget_adapter_reads_the_shared_engine(self) -> None:
        timer = TimerEngine(make_settings())
        finish_current_period(timer)
        timer.tick()
        widget = WidgetWindow.__new__(WidgetWindow)
        widget.timer = timer
        widget.settings = make_settings()
        widget.settings.widget_enabled = True
        widget.window = object()
        widget.view = FakeWidgetWindow(timer)

        widget.update()

        self.assertEqual(widget.view.mode, timer.mode_name())
        self.assertEqual(widget.view.time, timer.formatted_time())

    def test_widget_continue_uses_main_window_common_handler(self) -> None:
        with TemporaryDirectory() as directory:
            timer = TimerEngine(make_settings())
            finish_current_period(timer)
            timer.tick()
            statistics = StatisticsService(Path(directory) / "statistics.json")
            window = prepare_main_window(timer, statistics)
            actions = WidgetActions(
                toggle_timer=lambda: None,
                continue_period=window.continue_manual_transition,
                skip_period=lambda: None,
                reset_timer=lambda: None,
                show_main_window=lambda: None,
            )
            view = WidgetView.__new__(WidgetView)
            view.timer = timer
            view.actions = actions
            continue_button = FakeButton(view._handle_primary)

            continue_button.invoke()
            continue_button.invoke()

            self.assertEqual(statistics.all_time_stats()["overwork_seconds"], 1)
            self.assertFalse(timer.state.waiting_for_continue)
            self.assertEqual(window.notifications.calls, 1)


if __name__ == "__main__":
    unittest.main()
