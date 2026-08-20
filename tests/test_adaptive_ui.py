"""Регрессии адаптивной Qt-компоновки, контраста, трея и ресурсов Windows."""

from __future__ import annotations

from dataclasses import asdict
import struct
import unittest
from unittest.mock import patch

from PySide6.QtCore import QTimer
from PySide6.QtGui import QPalette

from app.theme import (
    APPEARANCE_DARK,
    APPEARANCE_LIGHT,
    PALETTES,
    contrast_ratio,
)
from app.storage import load_app_settings
from app.ui.components import AppButton, ThemedScrollArea
from app.ui.icons import ICON_DIR, application_icon, tray_icon
from app.window_geometry import fit_main_window_geometry
from tests.qt_helpers import APP, isolated_main
from tests.test_timer_engine import make_settings


class AdaptiveUiTests(unittest.TestCase):
    def test_all_main_pages_open_without_recreating_stack(self) -> None:
        with isolated_main() as (window, _settings, _statistics):
            stack = window.page_stack
            pages = [stack.widget(index) for index in range(stack.count())]
            for index in range(stack.count()):
                stack.setCurrentIndex(index)
                APP.processEvents()
                self.assertIs(stack.widget(index), pages[index])
                self.assertTrue(stack.currentWidget().isVisible() or not window.isVisible())

    def test_dark_theme_colors_scrollareas_viewports_and_tray_menu(self) -> None:
        with isolated_main() as (window, _settings, _statistics):
            window.show()
            window.page_stack.setCurrentIndex(2)
            window.apply_theme_selection("Comet", APPEARANCE_DARK, persist=False)
            APP.processEvents()
            palette = window.theme_manager.palette
            for scroll in window.settings_view.findChildren(ThemedScrollArea):
                with self.subTest(scroll=scroll.objectName()):
                    self.assertEqual(
                        scroll.viewport().palette().color(QPalette.ColorRole.Window).name().upper(),
                        palette.background,
                    )
                    self.assertEqual(
                        scroll.viewport().palette().color(QPalette.ColorRole.Base).name().upper(),
                        palette.background,
                    )
            menu_palette = window.tray.menu.palette()
            self.assertEqual(menu_palette.color(QPalette.ColorRole.Base).name().upper(), palette.card_background)
            self.assertEqual(menu_palette.color(QPalette.ColorRole.Text).name().upper(), palette.text_primary)
            self.assertEqual(menu_palette.color(QPalette.ColorRole.Highlight).name().upper(), palette.accent)
            self.assertEqual(
                menu_palette.color(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text).name().upper(),
                palette.disabled,
            )
            self.assertIn("QMenu::item:selected", window.tray.menu.styleSheet())
            self.assertIn(palette.card_background, window.tray.menu.styleSheet())
            self.assertIn(palette.text_primary, window.tray.menu.styleSheet())
            self.assertEqual(
                {action.text() for action in window.tray.actions.values()},
                {"Показать окно", "Скрыть окно", "Старт / Пауза", "Сброс", "Выход"},
            )

    def test_builtin_themes_cover_primary_secondary_disabled_and_actions(self) -> None:
        for theme, modes in PALETTES.items():
            for mode, palette in modes.items():
                pairs = (
                    (palette.text_primary, palette.background),
                    (palette.text_primary, palette.card_background),
                    (palette.text_secondary, palette.background),
                    (palette.text_secondary, palette.card_background),
                    (palette.disabled, palette.background),
                    (palette.disabled, palette.card_background),
                    (palette.button_text, palette.button_background),
                    (palette.on_accent, palette.accent),
                )
                for foreground, background in pairs:
                    with self.subTest(theme=theme, mode=mode, foreground=foreground, background=background):
                        self.assertGreaterEqual(contrast_ratio(foreground, background), 4.5)

    def test_theme_editor_wraps_long_actions_on_small_window(self) -> None:
        with isolated_main() as (window, _settings, _statistics):
            window.settings_view._open_theme_editor()
            editor = window.settings_view.theme_editor
            self.assertIsNotNone(editor)
            editor.resize(editor.minimumWidth(), max(editor.minimumHeight(), 560))
            APP.processEvents()
            buttons = (
                editor.create_button,
                editor.preview_button,
                editor.reset_mode_button,
                editor.reset_all_button,
                editor.cancel_button,
                editor.apply_button,
            )
            for button in buttons:
                with self.subTest(button=button.text()):
                    self.assertGreaterEqual(button.width(), button.minimumSizeHint().width())
                    self.assertTrue(button.isVisible())
            self.assertTrue(editor.scroll.isVisible())
            self.assertTrue(editor.footer_widget.isVisible())
            screen = editor.screen() or APP.primaryScreen()
            self.assertLessEqual(editor.width(), screen.availableGeometry().width())
            self.assertLessEqual(editor.height(), screen.availableGeometry().height())
            editor.cancel()

    def test_main_layout_breakpoints_fit_supported_screen_profiles(self) -> None:
        profiles = (
            ((1280, 720), (1024, 576), 72),
            ((1366, 768), (1093, 614), 72),
            ((1600, 900), (1280, 720), 220),
            ((1920, 1080), (1440, 864), 220),
        )
        with isolated_main() as (window, _settings, _statistics):
            window.show()
            for screen_size, client_size, sidebar_width in profiles:
                with self.subTest(screen=screen_size):
                    window.resize(*client_size)
                    window._apply_responsive_layout()
                    APP.processEvents()
                    self.assertEqual(window.sidebar.width(), sidebar_width)
                    self.assertGreater(window.timer_visual.width(), 0)
                    for button in window.findChildren(AppButton):
                        if button.isVisible() and not button.property("nav"):
                            self.assertGreaterEqual(button.width(), button.minimumSizeHint().width())

    def test_window_geometry_defaults_restore_and_clamp(self) -> None:
        default = fit_main_window_geometry({}, [(0, 0, 1280, 720)])
        self.assertEqual(default, {"x": 128, "y": 72, "width": 1024, "height": 576})
        restored = fit_main_window_geometry(
            {"x": 5000, "y": -5000, "width": 1100, "height": 700},
            [(0, 0, 1366, 728)],
        )
        self.assertGreaterEqual(restored["x"], 0)
        self.assertGreaterEqual(restored["y"], 0)
        self.assertLessEqual(restored["x"] + restored["width"], 1366)
        self.assertLessEqual(restored["y"] + restored["height"], 728)

    def test_main_window_geometry_is_saved_without_losing_other_settings(self) -> None:
        settings = make_settings()
        settings.work_minutes = 47
        with isolated_main(settings) as (window, settings_path, _statistics):
            window.resize(900, 620)
            window.move(10, 20)
            APP.processEvents()
            window._save_settings_now()
            restored = load_app_settings(settings_path)
            self.assertEqual(restored.work_minutes, 47)
            self.assertEqual(restored.main_window_geometry["width"], window.width())
            self.assertEqual(restored.main_window_geometry["height"], window.height())
            self.assertEqual(restored.main_window_geometry["x"], window.x())
            self.assertEqual(restored.main_window_geometry["y"], window.y())

    def test_twenty_theme_switches_keep_ui_timer_and_single_qss(self) -> None:
        settings = make_settings()
        settings.widget_enabled = True
        with isolated_main(settings) as (window, _settings, _statistics):
            window.timer.start()
            window.timer.tick()
            timer_state = asdict(window.timer.state)
            stack = window.page_stack
            widget_shell = window.widget_window.window
            listeners = len(window.theme_manager._listeners)
            timers = len(APP.findChildren(QTimer))
            stylesheet_installs = window.theme_manager.stylesheet_install_count
            for index in range(20):
                window.apply_theme_selection(
                    "Aurora" if index % 3 == 0 else "Comet",
                    APPEARANCE_DARK if index % 2 else APPEARANCE_LIGHT,
                    persist=False,
                )
                APP.processEvents()
            self.assertIs(window.page_stack, stack)
            self.assertIs(window.widget_window.window, widget_shell)
            self.assertEqual(asdict(window.timer.state), timer_state)
            self.assertEqual(len(window.theme_manager._listeners), listeners)
            self.assertEqual(len(APP.findChildren(QTimer)), timers)
            self.assertEqual(window.theme_manager.stylesheet_install_count, stylesheet_installs)

    def test_complete_icon_set_is_loaded_by_application_window_and_tray(self) -> None:
        expected_sizes = (16, 20, 24, 32, 48, 64, 128, 256)
        for size in expected_sizes:
            self.assertTrue((ICON_DIR / f"app-{size}.png").is_file())
        ico = (ICON_DIR / "app.ico").read_bytes()
        self.assertEqual(struct.unpack_from("<HHH", ico, 0), (0, 1, len(expected_sizes)))
        self.assertTrue((ICON_DIR / "app.svg").is_file())
        self.assertFalse(application_icon().isNull())
        self.assertFalse(tray_icon().isNull())
        self.assertFalse(APP.windowIcon().isNull())
        with isolated_main() as (window, _settings, _statistics):
            self.assertFalse(window.windowIcon().isNull())
            self.assertFalse(window.tray.icon.icon().isNull())

    def test_native_title_theme_is_reapplied_after_window_creation(self) -> None:
        with isolated_main() as (window, _settings, _statistics):
            with patch("app.ui.qt_app.apply_windows_title_bar") as apply_title:
                window.theme_manager.apply_to_window(window)
                APP.processEvents()
            self.assertGreaterEqual(apply_title.call_count, 2)
            self.assertTrue(all(call.args[0] is window for call in apply_title.call_args_list))


if __name__ == "__main__":
    unittest.main()
