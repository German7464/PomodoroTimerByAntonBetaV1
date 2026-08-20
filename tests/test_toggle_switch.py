"""Проверки единого Qt-переключателя двоичных настроек."""

from pathlib import Path
from tempfile import TemporaryDirectory
import inspect
import unittest

from PySide6.QtCore import Qt
from PySide6.QtTest import QTest

from app.storage import load_app_settings, save_json
from app.theme import APPEARANCE_DARK, APPEARANCE_LIGHT, CUSTOM_THEME_NAME, THEME_NAMES, ThemeManager, default_custom_theme
from app.ui.components import AppButton, SwitchRow, ToggleSwitch
from app.ui.main_window import MainWindow
from app.ui.settings_window import SettingsView
from tests.qt_helpers import APP, isolated_main


class ToggleSwitchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = ThemeManager()
        self.manager.apply("Comet", APPEARANCE_LIGHT)

    def make_switch(self, checked=False, animations=False):
        switch = ToggleSwitch(
            checked,
            theme_manager=self.manager,
            animations_enabled=lambda: animations,
            accessible_name="Тестовая настройка",
        )
        switch.show()
        APP.processEvents()
        return switch

    def test_on_and_off_have_exact_text_and_thumb_side(self) -> None:
        switch = self.make_switch(False)
        self.assertEqual(switch.state_text, "ВЫКЛ")
        self.assertEqual(switch.thumb_fraction, 0.0)
        switch.set(True)
        self.assertEqual(switch.state_text, "ВКЛ")
        self.assertEqual(switch.thumb_fraction, 1.0)
        switch.close()

    def test_mouse_and_keyboard_change_once(self) -> None:
        switch = self.make_switch(False)
        changes = []
        switch.valueChanged.connect(changes.append)
        QTest.mouseClick(switch, Qt.MouseButton.LeftButton)
        switch.setFocus()
        QTest.keyClick(switch, Qt.Key.Key_Return)
        self.assertEqual(changes, [True, False])
        switch.close()

    def test_rapid_actions_end_in_real_state(self) -> None:
        switch = self.make_switch(False, animations=True)
        changes = []
        switch.valueChanged.connect(changes.append)
        for _ in range(3):
            switch.click()
        QTest.qWait(220)
        self.assertEqual(changes, [True, False, True])
        self.assertTrue(switch.value)
        self.assertAlmostEqual(switch.thumb_fraction, 1.0)
        self.assertFalse(switch.animation_active)
        switch.close()

    def test_external_change_does_not_emit(self) -> None:
        switch = self.make_switch(False)
        changes = []
        switch.valueChanged.connect(changes.append)
        switch.set_value(True)
        self.assertTrue(switch.value)
        self.assertEqual(changes, [])
        switch.close()

    def test_disabled_switch_cannot_change(self) -> None:
        switch = self.make_switch(False)
        switch.setEnabled(False)
        QTest.mouseClick(switch, Qt.MouseButton.LeftButton)
        self.assertFalse(switch.value)
        switch.close()

    def test_all_themes_and_custom_palette_are_consumed(self) -> None:
        switch = self.make_switch(True)
        for name in THEME_NAMES:
            for mode in (APPEARANCE_LIGHT, APPEARANCE_DARK):
                custom = default_custom_theme()
                if name == CUSTOM_THEME_NAME:
                    custom[mode]["accent"] = "#123456"
                palette = self.manager.apply(name, mode, custom)
                self.assertEqual(switch._palette, palette)
        switch.close()

    def test_scalable_size_keeps_status_and_track(self) -> None:
        switch = self.make_switch(True)
        self.assertGreaterEqual(switch.sizeHint().width(), 108)
        self.assertGreaterEqual(switch.sizeHint().height(), 28)
        self.assertEqual(switch.state_text, "ВКЛ")
        switch.close()

    def test_close_cancels_animation(self) -> None:
        switch = self.make_switch(False, animations=True)
        switch.click()
        self.assertTrue(switch.animation_active)
        switch.close()
        self.assertFalse(switch.animation_active)


class ToggleSwitchContractTests(unittest.TestCase):
    def test_binary_controls_use_component_and_commands_remain_buttons(self) -> None:
        settings_source = inspect.getsource(SettingsView)
        main_source = inspect.getsource(MainWindow)
        self.assertNotIn("QCheckBox", settings_source)
        self.assertIn("SwitchRow", settings_source)
        self.assertIn('"timer.widget.show"', main_source)
        for command_key in ("action.start", "action.pause", "action.continue", "action.skip", "action.reset"):
            self.assertIn(command_key, main_source)
        with isolated_main() as (window, _settings, _statistics):
            self.assertTrue(all(isinstance(row, SwitchRow) for row in window.settings_view.toggle_switches))
            self.assertIsInstance(window.start_button, AppButton)
            self.assertIsInstance(window.continue_button, AppButton)

    def test_existing_boolean_setting_keys_keep_their_values(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            values = {
                "use_long_break": False,
                "notifications_enabled": False,
                "notification_sound_enabled": True,
                "auto_start_next_period": True,
                "widget_enabled": True,
                "widget_always_on_top": False,
                "minimize_to_tray_on_start": True,
                "close_to_tray": False,
                "autostart_enabled": True,
            }
            save_json(path, values)
            settings = load_app_settings(path)
            for key, value in values.items():
                self.assertEqual(getattr(settings, key), value)


if __name__ == "__main__":
    unittest.main()
