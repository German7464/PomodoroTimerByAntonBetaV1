"""Интеграционные контракты профессионального Qt-интерфейса."""

from dataclasses import asdict
import unittest

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QStackedWidget

from app.overrun_effects import OVERRUN_EFFECTS, calculate_overrun_frame
from app.theme import APPEARANCE_DARK, APPEARANCE_LIGHT, BUILTIN_THEME_NAMES, CUSTOM_THEME_NAME
from app.ui.components import AppButton, Card, ToggleSwitch
from app.ui.widget_window import VIEW_CLASSES
from app.widget_settings import WIDGET_TYPES
from tests.qt_helpers import APP, isolated_main
from tests.test_timer_engine import finish_current_period, make_settings


class QtUiParityTests(unittest.TestCase):
    def test_navigation_and_component_library_are_qt(self) -> None:
        with isolated_main() as (window, _path, _statistics):
            self.assertIsInstance(window.page_stack, QStackedWidget)
            self.assertEqual(window.page_stack.count(), 4)
            self.assertIsInstance(window.start_button, AppButton)
            self.assertIsInstance(window.widget_visibility_switch.switch, ToggleSwitch)
            self.assertGreater(len(window.findChildren(Card)), 0)

    def test_all_seven_live_layouts_share_engine_and_window(self) -> None:
        settings = make_settings()
        settings.widget_enabled = True
        with isolated_main(settings) as (window, _path, _statistics):
            shell = window.widget_window.window
            timer = window.timer
            before = asdict(timer.state)
            for kind in WIDGET_TYPES:
                window.settings.widget_type = kind
                window.widget_window.apply_settings(window.settings)
                APP.processEvents()
                self.assertIs(window.widget_window.window, shell)
                self.assertIs(window.widget_window.view.timer, timer)
                self.assertIsInstance(window.widget_window.view, VIEW_CLASSES[kind])
            self.assertEqual(asdict(timer.state), before)

    def test_theme_matrix_and_effects_do_not_replace_timer_or_widget(self) -> None:
        settings = make_settings()
        settings.widget_enabled = True
        with isolated_main(settings) as (window, _path, _statistics):
            timer = window.timer
            shell = window.widget_window.window
            timer.start()
            timer.tick()
            before = asdict(timer.state)
            for theme in (*BUILTIN_THEME_NAMES, CUSTOM_THEME_NAME):
                for mode in (APPEARANCE_LIGHT, APPEARANCE_DARK):
                    window.apply_theme_selection(theme, mode, persist=False)
                    for effect in OVERRUN_EFFECTS:
                        frame = calculate_overrun_frame(
                            window.theme_manager.palette,
                            timer.state.mode,
                            {"effect": effect},
                            0.4,
                        )
                        window._apply_overrun_visual_frame(frame)
            self.assertIs(window.timer, timer)
            self.assertIs(window.widget_window.window, shell)
            self.assertEqual(asdict(timer.state), before)

    def test_widget_configuration_applies_live_without_timer_reset(self) -> None:
        settings = make_settings()
        settings.widget_enabled = True
        with isolated_main(settings) as (window, _path, _statistics):
            window.timer.start()
            window.timer.tick()
            before = asdict(window.timer.state)
            target = WIDGET_TYPES[-1]
            layouts = window.settings.widget_layouts
            window.set_widget_configuration(target, layouts[target]["size"], layouts, False)
            self.assertEqual(window.widget_window._active_view_type, target)
            self.assertFalse(bool(window.widget_window.window.windowFlags() & Qt.WindowType.WindowStaysOnTopHint))
            self.assertEqual(asdict(window.timer.state), before)

    def test_shutdown_stops_all_gui_schedulers(self) -> None:
        with isolated_main() as (window, _path, _statistics):
            window._schedule_tick()
            window.preview_overrun_visual(window.timer.state.mode, window.settings.overrun_visual)
            self.assertTrue(window._tick_timer.isActive())
            window._shutdown(quit_application=False)
            self.assertFalse(window._tick_timer.isActive())
            self.assertFalse(window.overrun_visual_controller.has_scheduled_frame)
            self.assertEqual(len(window._scheduler._timers), 0)


if __name__ == "__main__":
    unittest.main()
