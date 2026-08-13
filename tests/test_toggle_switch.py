"""Общий тематизированный переключатель двоичных настроек."""

import inspect
from pathlib import Path
from tempfile import TemporaryDirectory
import time
import tkinter as tk
import unittest

from app.theme import APPEARANCE_DARK, APPEARANCE_LIGHT, THEME_NAMES, get_palette
from app.theme import CUSTOM_THEME_NAME, default_custom_theme
from app.storage import load_app_settings, save_json
from app.ui.main_window import MainWindow
from app.ui.settings_window import SettingsView
from app.ui.toggle_switch import ToggleSwitch


class FakeThemeManager:
    def __init__(self) -> None:
        self.palette = get_palette("Comet", APPEARANCE_LIGHT)
        self.listeners = []

    def register(self, listener) -> None:
        self.listeners.append(listener)
        listener(self.palette)

    def unregister(self, listener) -> None:
        if listener in self.listeners:
            self.listeners.remove(listener)

    def apply(self, theme_name: str, mode: str) -> None:
        self.palette = get_palette(theme_name, mode)
        for listener in tuple(self.listeners):
            listener(self.palette)


class ToggleSwitchSourceContractTests(unittest.TestCase):
    def test_all_binary_settings_use_component_and_commands_stay_buttons(self) -> None:
        settings_source = inspect.getsource(SettingsView)
        main_source = inspect.getsource(MainWindow)

        self.assertNotIn("ttk.Checkbutton", settings_source)
        self.assertGreaterEqual(settings_source.count("self._add_toggle("), 11)
        self.assertIn('text="Отображать виджет"', main_source)
        self.assertIn('text="Тёмный режим"', main_source)
        self.assertGreaterEqual(main_source.count("ToggleSwitch("), 2)
        for command_label in (
            "Старт",
            "Пауза",
            "Продолжить и начать следующий период",
            "Пропустить период",
            "Сброс",
        ):
            self.assertIn(f'text="{command_label}"', main_source)

    def test_existing_boolean_setting_keys_keep_their_values(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            saved_values = {
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
            save_json(path, saved_values)

            settings = load_app_settings(path)

            for key, value in saved_values.items():
                with self.subTest(key=key):
                    self.assertEqual(getattr(settings, key), value)


class ToggleSwitchTests(unittest.TestCase):
    def setUp(self) -> None:
        try:
            self.root = tk.Tk()
        except tk.TclError as error:
            self.skipTest(f"Tk недоступен: {error}")
        self.root.withdraw()
        self.manager = FakeThemeManager()

    def tearDown(self) -> None:
        if hasattr(self, "root"):
            self.root.destroy()

    def make_switch(self, value=False, command=None, animations=False) -> ToggleSwitch:
        variable = tk.BooleanVar(self.root, value=value)
        switch = ToggleSwitch(
            self.root,
            text="Тестовая настройка",
            variable=variable,
            command=command,
            theme_manager=self.manager,
            animations_enabled=animations,
        )
        switch.pack(fill=tk.X)
        self.root.update_idletasks()
        return switch

    def test_on_and_off_have_exact_text_and_thumb_side(self) -> None:
        switch = self.make_switch(False)
        off_coords = switch.canvas.coords("thumb")
        off_center = (off_coords[0] + off_coords[2]) / 2
        self.assertEqual(switch.state_text, "ВЫКЛ")
        self.assertLess(off_center, switch._track_width / 2)

        switch.set(True)
        on_coords = switch.canvas.coords("thumb")
        on_center = (on_coords[0] + on_coords[2]) / 2
        self.assertEqual(switch.state_text, "ВКЛ")
        self.assertGreater(on_center, switch._track_width / 2)

    def test_one_action_changes_once_and_keyboard_uses_same_path(self) -> None:
        changes: list[bool] = []
        switch = self.make_switch(command=changes.append)
        self.root.deiconify()
        self.root.update()

        switch.label.event_generate("<ButtonPress-1>")
        switch.label.event_generate("<ButtonRelease-1>")
        self.root.update()
        switch._on_key(None)

        self.assertEqual(changes, [True, False])
        self.assertFalse(switch.value)
        self.assertTrue(switch.canvas.bind("<KeyPress-space>"))
        self.assertTrue(switch.canvas.bind("<KeyPress-Return>"))

    def test_rapid_actions_cancel_previous_animation_and_end_consistently(self) -> None:
        changes: list[bool] = []
        switch = self.make_switch(command=changes.append, animations=True)

        switch.toggle()
        first_job = switch._animation_id
        switch.toggle()
        switch.toggle()
        self.assertNotEqual(first_job, switch._animation_id)
        deadline = time.monotonic() + 0.3
        while time.monotonic() < deadline and switch.animation_active:
            self.root.update()
            time.sleep(0.01)

        self.assertEqual(changes, [True, False, True])
        self.assertTrue(switch.value)
        self.assertAlmostEqual(switch.thumb_fraction, 1.0)
        self.assertFalse(switch.animation_active)

    def test_external_change_updates_without_invoking_command(self) -> None:
        changes: list[bool] = []
        switch = self.make_switch(command=changes.append)

        switch.variable.set(True)

        self.assertTrue(switch.value)
        self.assertEqual(switch.state_label.cget("text"), "ВКЛ")
        self.assertEqual(changes, [])

    def test_disabled_switch_cannot_change(self) -> None:
        changes: list[bool] = []
        switch = self.make_switch(command=changes.append)
        switch.set_enabled(False)

        self.assertFalse(switch.toggle())
        switch._on_key(None)

        self.assertFalse(switch.value)
        self.assertEqual(changes, [])

    def test_all_themes_and_modes_supply_semantic_colors(self) -> None:
        switch = self.make_switch(True)
        for theme_name in THEME_NAMES:
            for mode in (APPEARANCE_LIGHT, APPEARANCE_DARK):
                with self.subTest(theme=theme_name, mode=mode):
                    self.manager.apply(theme_name, mode)
                    self.assertIs(switch._palette, self.manager.palette)
                    self.assertEqual(
                        switch.state_label.cget("foreground").upper(),
                        self.manager.palette.accent,
                    )

    def test_custom_theme_uses_user_accent_without_component_override(self) -> None:
        switch = self.make_switch(True)
        custom_theme = default_custom_theme()
        custom_theme[APPEARANCE_LIGHT]["accent"] = "#123456"
        palette = get_palette(CUSTOM_THEME_NAME, APPEARANCE_LIGHT, custom_theme)

        switch.apply_theme(palette)

        self.assertEqual(switch.state_label.cget("foreground").upper(), "#123456")

    def test_tk_scaling_enlarges_track_without_clipping_state_text(self) -> None:
        self.root.tk.call("tk", "scaling", 2.0)
        switch = self.make_switch(True)

        self.assertGreater(switch._track_width, 60)
        self.assertGreater(switch._track_height, 30)
        self.assertGreaterEqual(switch.winfo_reqheight(), switch.canvas.winfo_reqheight())
        self.assertEqual(switch.state_label.cget("text"), "ВКЛ")

    def test_destroy_cancels_animation_and_unregisters_listener(self) -> None:
        switch = self.make_switch(animations=True)
        switch.toggle()
        self.assertTrue(switch.animation_active)

        switch.destroy()

        self.assertFalse(switch.animation_active)
        self.assertEqual(self.manager.listeners, [])

if __name__ == "__main__":
    unittest.main()
