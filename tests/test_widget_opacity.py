"""Постоянная и временная системная непрозрачность виджета."""

import inspect
import unittest
from unittest.mock import patch

from app.ui import main_window as main_window_module
from app.ui.main_window import MainWindow
from app.overrun_effects import default_overrun_visual
from app.timer_engine import TimerEngine
from app.ui.settings_window import SettingsView
from app.ui.widget_window import WidgetWindow
from tests.test_timer_engine import make_settings


class FakeTopLevel:
    def __init__(self) -> None:
        self.alpha = None

    def attributes(self, name: str, value: float) -> None:
        if name == "-alpha":
            self.alpha = value


class FakeVariable:
    def __init__(self, value: bool) -> None:
        self.value = value

    def get(self) -> bool:
        return self.value


class FakeButton:
    def __init__(self) -> None:
        self.text = ""

    def config(self, **values: str) -> None:
        self.text = values.get("text", self.text)


class FakeRoot:
    def __init__(self) -> None:
        self.next_id = 0
        self.jobs: dict[str, object] = {}

    def after(self, _delay: int, callback):
        self.next_id += 1
        job_id = str(self.next_id)
        self.jobs[job_id] = callback
        return job_id

    def after_cancel(self, job_id: str) -> None:
        self.jobs.pop(job_id, None)


class FakeOpacityWidget:
    def __init__(self) -> None:
        self.calls = 0

    def apply_opacity(self) -> None:
        self.calls += 1


class FakeSettingsView:
    def sync_widget_opacity(self, _opacity: int) -> None:
        pass


class WidgetOpacityTests(unittest.TestCase):
    def _widget(self, opacity: int, opaque: bool) -> WidgetWindow:
        settings = make_settings()
        settings.widget_opacity = opacity
        settings.overrun_visual = default_overrun_visual()
        settings.overrun_visual["opaque_widget_during_overrun"] = opaque
        widget = WidgetWindow.__new__(WidgetWindow)
        widget.settings = settings
        widget.timer = TimerEngine(settings)
        widget.window = FakeTopLevel()
        return widget

    def test_real_overrun_forces_one_and_restores_exact_value(self) -> None:
        widget = self._widget(17, True)
        self.assertEqual(widget.apply_opacity(), 0.17)

        widget.timer.state.waiting_for_continue = True
        self.assertEqual(widget.apply_opacity(), 1.0)
        self.assertEqual(widget.settings.widget_opacity, 17)

        widget.timer.state.waiting_for_continue = False
        self.assertEqual(widget.apply_opacity(), 0.17)
        self.assertEqual(widget.window.alpha, 0.17)

    def test_disabling_temporary_opacity_during_overrun_restores_immediately(self) -> None:
        widget = self._widget(41, True)
        widget.timer.state.waiting_for_continue = True
        self.assertEqual(widget.apply_opacity(), 1.0)

        widget.settings.overrun_visual["opaque_widget_during_overrun"] = False

        self.assertEqual(widget.apply_opacity(), 0.41)
        self.assertEqual(widget.settings.widget_opacity, 41)

    def test_toggle_button_text_is_explicit_and_not_a_checkbox(self) -> None:
        view = SettingsView.__new__(SettingsView)
        view.overrun_opaque_widget_var = FakeVariable(True)
        view.overrun_opaque_button = FakeButton()
        view._sync_overrun_opaque_button()
        self.assertEqual(
            view.overrun_opaque_button.text,
            "Непрозрачный при превышении: ВКЛ",
        )

        source = inspect.getsource(SettingsView._build_overrun_settings)
        self.assertIn("self.overrun_opaque_button = ttk.Button", source)
        self.assertNotIn(
            'text="Непрозрачный при превышении',
            inspect.getsource(SettingsView._build_widget_settings),
        )

    def test_opacity_ui_uses_clear_label_and_explanation(self) -> None:
        source = inspect.getsource(SettingsView._build_widget_settings)
        self.assertIn("Непрозрачность виджета", source)
        self.assertIn("Чем ниже значение, тем прозрачнее виджет.", source)
        self.assertIn("command=self._on_widget_opacity_changed", source)

    def test_slider_changes_share_one_deferred_settings_write(self) -> None:
        window = MainWindow.__new__(MainWindow)
        window.settings = make_settings()
        window.root = FakeRoot()
        window.widget_window = FakeOpacityWidget()
        window.settings_view = FakeSettingsView()
        window._settings_save_after_id = None

        with patch.object(main_window_module, "save_app_settings") as save:
            for opacity in (10, 20, 33):
                window.set_widget_opacity(opacity)
            self.assertEqual(len(window.root.jobs), 1)
            self.assertEqual(window.settings.widget_opacity, 33)
            self.assertEqual(window.widget_window.calls, 3)
            self.assertEqual(save.call_count, 0)

            callback = next(iter(window.root.jobs.values()))
            callback()
            self.assertEqual(save.call_count, 1)


if __name__ == "__main__":
    unittest.main()
