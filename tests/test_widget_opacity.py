"""Постоянная и временная прозрачность Qt-виджета."""

import unittest
from unittest.mock import patch

from PySide6.QtTest import QTest

from app.storage import load_app_settings
from app.ui import main_window as main_module
from app.ui.components import SwitchRow
from app.widget_settings import effective_widget_alpha, normalize_widget_opacity
from tests.qt_helpers import APP, isolated_main
from tests.test_timer_engine import finish_current_period, make_settings


class WidgetOpacityTests(unittest.TestCase):
    def test_safe_range_is_five_to_one_hundred_percent(self) -> None:
        self.assertEqual(normalize_widget_opacity(0), 5)
        self.assertEqual(normalize_widget_opacity(5), 5)
        self.assertEqual(normalize_widget_opacity(37), 37)
        self.assertEqual(normalize_widget_opacity(999), 100)
        self.assertAlmostEqual(effective_widget_alpha(5, False, False), 0.05)
        self.assertEqual(effective_widget_alpha(100, False, False), 1.0)

    def test_real_overrun_forces_one_and_continue_restores_exact_value(self) -> None:
        settings = make_settings()
        settings.widget_enabled = True
        settings.widget_opacity = 37
        settings.overrun_visual["opaque_widget_during_overrun"] = True
        with isolated_main(settings) as (window, _path, _statistics):
            self.assertAlmostEqual(window.widget_window.apply_opacity(), 0.37)
            finish_current_period(window.timer)
            window.timer.tick()
            window._refresh_labels()
            self.assertEqual(window.widget_window.apply_opacity(), 1.0)
            window.continue_manual_transition()
            self.assertAlmostEqual(window.widget_window.apply_opacity(), 0.37)
            self.assertEqual(window.settings.widget_opacity, 37)

    def test_disabling_temporary_opacity_during_overrun_restores_immediately(self) -> None:
        settings = make_settings()
        settings.widget_enabled = True
        settings.widget_opacity = 23
        settings.overrun_visual["opaque_widget_during_overrun"] = True
        with isolated_main(settings) as (window, _path, _statistics):
            finish_current_period(window.timer)
            window.timer.tick()
            self.assertEqual(window.widget_window.apply_opacity(), 1.0)
            window.set_overrun_widget_opacity(False)
            self.assertAlmostEqual(window.widget_window.apply_opacity(), 0.23)

    def test_temporary_value_is_not_saved_as_persistent(self) -> None:
        settings = make_settings()
        settings.widget_enabled = True
        settings.widget_opacity = 19
        settings.overrun_visual["opaque_widget_during_overrun"] = True
        with isolated_main(settings) as (window, path, _statistics):
            finish_current_period(window.timer)
            window.timer.tick()
            window.widget_window.apply_opacity()
            window._save_settings_now()
            self.assertEqual(load_app_settings(path).widget_opacity, 19)

    def test_slider_changes_share_one_deferred_write(self) -> None:
        settings = make_settings()
        settings.widget_enabled = True
        with isolated_main(settings) as (window, _path, _statistics):
            with patch.object(main_module, "save_app_settings") as save:
                window.set_widget_opacity(20)
                window.set_widget_opacity(21)
                window.set_widget_opacity(22)
                QTest.qWait(560)
                APP.processEvents()
            save.assert_called_once()
            self.assertEqual(window.settings.widget_opacity, 22)

    def test_opacity_ui_has_clear_text_and_common_toggle(self) -> None:
        with isolated_main() as (window, _path, _statistics):
            view = window.settings_view
            self.assertEqual(view.widget_opacity.minimum(), 5)
            self.assertEqual(view.widget_opacity.maximum(), 100)
            self.assertEqual(view.widget_opacity_label.text(), f"{view.widget_opacity.value()}%")
            self.assertIsInstance(view.overrun_opaque_widget, SwitchRow)
            labels = [label.text() for label in view.findChildren(type(view.widget_opacity_label))]
            self.assertTrue(any("Чем ниже значение" in text for text in labels))


if __name__ == "__main__":
    unittest.main()
