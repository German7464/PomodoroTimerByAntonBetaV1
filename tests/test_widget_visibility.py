"""Единое Qt-состояние видимости плавающего виджета."""

from dataclasses import asdict
from pathlib import Path
from tempfile import TemporaryDirectory
import inspect
import unittest
from unittest.mock import patch

from app.storage import load_app_settings, save_json
from app.ui.settings_window import SettingsView
from app.ui.tray import TrayController
from app.widget_settings import (
    WIDGET_SIZE_CUSTOM,
    WIDGET_TYPE_COMPACT,
    WIDGET_TYPE_EXPANDED,
)
from tests.qt_helpers import APP, isolated_main
from tests.test_timer_engine import make_settings


class WidgetVisibilityTests(unittest.TestCase):
    def test_saved_false_starts_hidden_with_switch_off(self) -> None:
        settings = make_settings()
        settings.widget_enabled = False
        with isolated_main(settings) as (window, _path, _statistics):
            self.assertFalse(window.widget_window.is_visible())
            self.assertFalse(window.widget_visibility_switch.isChecked())

    def test_saved_true_starts_visible_with_switch_on(self) -> None:
        settings = make_settings()
        settings.widget_enabled = True
        with isolated_main(settings) as (window, _path, _statistics):
            self.assertTrue(window.widget_window.is_visible())
            self.assertTrue(window.widget_visibility_switch.isChecked())

    def test_switch_and_widget_close_persist_one_state(self) -> None:
        settings = make_settings()
        settings.widget_enabled = False
        with isolated_main(settings) as (window, path, _statistics):
            timer_before = asdict(window.timer.state)
            window.widget_visibility_switch.switch.click()
            APP.processEvents()
            self.assertTrue(load_app_settings(path).widget_enabled)
            window.widget_window.window.close()
            APP.processEvents()
            self.assertFalse(load_app_settings(path).widget_enabled)
            self.assertFalse(window.widget_visibility_switch.isChecked())
            self.assertEqual(asdict(window.timer.state), timer_before)

    def test_repeated_show_reuses_existing_window(self) -> None:
        with isolated_main(make_settings()) as (window, _path, _statistics):
            window.set_widget_visibility(True)
            shell = window.widget_window.window
            window.set_widget_visibility(True)
            window.set_widget_visibility(False)
            window.set_widget_visibility(True)
            self.assertIs(window.widget_window.window, shell)
            self.assertTrue(window.widget_window.is_visible())

    def test_type_custom_size_and_position_survive_visibility_changes(self) -> None:
        settings = make_settings()
        settings.widget_type = WIDGET_TYPE_EXPANDED
        settings.widget_size = WIDGET_SIZE_CUSTOM
        settings.widget_layouts[WIDGET_TYPE_EXPANDED] = {
            "size": WIDGET_SIZE_CUSTOM, "width": 611, "height": 377, "x": 234, "y": 345,
        }
        with isolated_main(settings) as (window, path, _statistics):
            window.set_widget_visibility(True)
            expected = dict(window.settings.widget_layouts[WIDGET_TYPE_EXPANDED])
            window.set_widget_visibility(False)
            window.set_widget_visibility(True)
            restored = load_app_settings(path)
            self.assertEqual(restored.widget_type, WIDGET_TYPE_EXPANDED)
            self.assertEqual(restored.widget_layouts[WIDGET_TYPE_EXPANDED], expected)

    def test_show_failure_returns_to_hidden_state(self) -> None:
        with isolated_main(make_settings()) as (window, path, _statistics):
            with patch.object(window.widget_window, "apply_settings", side_effect=RuntimeError("test")):
                self.assertFalse(window.set_widget_visibility(True))
            self.assertFalse(window.settings.widget_enabled)
            self.assertFalse(load_app_settings(path).widget_enabled)
            self.assertFalse(window.widget_visibility_switch.isChecked())

    def test_legacy_settings_keep_visibility_and_position(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            save_json(path, {"widget_enabled": True, "widget_type": "Компактный", "widget_x": 321, "widget_y": 123})
            settings = load_app_settings(path)
            self.assertTrue(settings.widget_enabled)
            self.assertEqual(settings.widget_layouts[WIDGET_TYPE_COMPACT]["x"], 321)
            self.assertEqual(settings.widget_layouts[WIDGET_TYPE_COMPACT]["y"], 123)

    def test_settings_has_no_visibility_control_and_keeps_widget_options(self) -> None:
        source = inspect.getsource(SettingsView._build_widget_page)
        tray_source = inspect.getsource(TrayController)
        self.assertNotIn("widget_enabled", source)
        self.assertNotIn("timer.widget.show", tray_source)
        self.assertIn('"settings.widget.type"', source)
        self.assertIn('"settings.widget.size"', source)
        self.assertIn('"settings.widget.always_on_top"', source)


if __name__ == "__main__":
    unittest.main()
