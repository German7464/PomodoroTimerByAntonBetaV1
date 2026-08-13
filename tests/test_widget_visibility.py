"""Единое управление видимостью плавающего виджета."""

from dataclasses import asdict
import inspect
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from app.models import AppSettings
from app.storage import load_app_settings, save_app_settings, save_json
from app.timer_engine import TimerEngine
from app.ui import main_window as main_window_module
from app.ui.main_window import MainWindow
from app.ui.settings_window import SettingsView
from app.ui.tray import TrayController
from app.ui.widget_window import WidgetWindow
from app.widget_settings import WIDGET_SIZE_CUSTOM, WIDGET_TYPE_EXPANDED
from tests.test_timer_engine import make_settings


class FakeToggle:
    """Минимальный переключатель для проверки внешней синхронизации."""

    def __init__(self, command) -> None:
        self.value = False
        self.command = command

    def set(self, value: bool) -> None:
        self.value = bool(value)

    def toggle(self) -> None:
        self.command(not self.value)


class FakeWidgetWindow:
    """Имитирует один переиспользуемый Toplevel без Tk."""

    def __init__(self, fail_show: bool = False) -> None:
        self.visible = False
        self.has_window = False
        self.created_windows = 0
        self.apply_calls = 0
        self.fail_show = fail_show
        self.on_visibility_requested = None

    def apply_settings(self, settings: AppSettings) -> None:
        self.apply_calls += 1
        if settings.widget_enabled and self.fail_show:
            raise RuntimeError("test show failure")
        if settings.widget_enabled and not self.has_window:
            self.has_window = True
            self.created_windows += 1
        self.visible = bool(settings.widget_enabled)

    def is_visible(self) -> bool:
        return self.visible

    def discard_window(self) -> None:
        self.visible = False
        self.has_window = False

    def close_from_window(self) -> None:
        self.on_visibility_requested(False)


def prepare_controller(settings: AppSettings, widget: FakeWidgetWindow) -> MainWindow:
    """Создаёт контроллер MainWindow без графического окружения."""
    window = MainWindow.__new__(MainWindow)
    window.settings = settings
    window.timer = TimerEngine(settings)
    window.widget_window = widget
    window.widget_visibility_switch = FakeToggle(window.set_widget_visibility)
    widget.on_visibility_requested = window.set_widget_visibility
    return window


class WidgetVisibilityTests(unittest.TestCase):
    """Проверяет видимость, сохранение и единый пользовательский переключатель."""

    def test_saved_false_starts_hidden_with_switch_off(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            settings = make_settings()
            settings.widget_enabled = False
            save_app_settings(path, settings)
            loaded = load_app_settings(path)
            widget = FakeWidgetWindow()
            window = prepare_controller(loaded, widget)

            with patch.object(main_window_module, "SETTINGS_FILE", path):
                self.assertTrue(window.set_widget_visibility(loaded.widget_enabled, persist=False))

            self.assertFalse(widget.visible)
            self.assertEqual(widget.created_windows, 0)
            self.assertFalse(window.widget_visibility_switch.value)

    def test_saved_true_starts_visible_with_switch_on(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            settings = make_settings()
            settings.widget_enabled = True
            save_app_settings(path, settings)
            loaded = load_app_settings(path)
            widget = FakeWidgetWindow()
            window = prepare_controller(loaded, widget)

            with patch.object(main_window_module, "SETTINGS_FILE", path):
                self.assertTrue(window.set_widget_visibility(loaded.widget_enabled, persist=False))

            self.assertTrue(widget.visible)
            self.assertEqual(widget.created_windows, 1)
            self.assertTrue(window.widget_visibility_switch.value)

    def test_switch_and_window_close_persist_one_state(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            settings = make_settings()
            widget = FakeWidgetWindow()
            window = prepare_controller(settings, widget)
            timer_before = asdict(window.timer.state)

            with patch.object(main_window_module, "SETTINGS_FILE", path):
                window.widget_visibility_switch.toggle()
                self.assertTrue(load_app_settings(path).widget_enabled)
                self.assertTrue(window.widget_visibility_switch.value)

                widget.close_from_window()
                self.assertFalse(load_app_settings(path).widget_enabled)

            self.assertFalse(widget.visible)
            self.assertFalse(window.widget_visibility_switch.value)
            self.assertEqual(asdict(window.timer.state), timer_before)

    def test_repeated_show_reuses_existing_window(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            widget = FakeWidgetWindow()
            window = prepare_controller(make_settings(), widget)

            with patch.object(main_window_module, "SETTINGS_FILE", path):
                window.set_widget_visibility(True)
                window.set_widget_visibility(True)
                window.set_widget_visibility(False)
                window.set_widget_visibility(True)

            self.assertTrue(widget.visible)
            self.assertEqual(widget.created_windows, 1)

    def test_type_custom_size_and_position_survive_visibility_changes(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            settings = load_app_settings(path)
            settings.widget_type = WIDGET_TYPE_EXPANDED
            settings.widget_size = WIDGET_SIZE_CUSTOM
            settings.widget_layouts[WIDGET_TYPE_EXPANDED] = {
                "size": WIDGET_SIZE_CUSTOM,
                "width": 611,
                "height": 377,
                "x": 234,
                "y": 345,
            }
            widget = FakeWidgetWindow()
            window = prepare_controller(settings, widget)

            with patch.object(main_window_module, "SETTINGS_FILE", path):
                window.set_widget_visibility(True)
                window.set_widget_visibility(False)
                window.set_widget_visibility(True)

            restored = load_app_settings(path)
            self.assertEqual(restored.widget_type, WIDGET_TYPE_EXPANDED)
            self.assertEqual(restored.widget_size, WIDGET_SIZE_CUSTOM)
            self.assertEqual(
                restored.widget_layouts[WIDGET_TYPE_EXPANDED],
                settings.widget_layouts[WIDGET_TYPE_EXPANDED],
            )

    def test_show_failure_returns_to_hidden_state_without_crashing(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            widget = FakeWidgetWindow(fail_show=True)
            window = prepare_controller(make_settings(), widget)

            with (
                patch.object(main_window_module, "SETTINGS_FILE", path),
                patch.object(main_window_module.messagebox, "showwarning") as warning,
            ):
                self.assertFalse(window.set_widget_visibility(True))

            self.assertFalse(window.settings.widget_enabled)
            self.assertFalse(load_app_settings(path).widget_enabled)
            self.assertFalse(window.widget_visibility_switch.value)
            warning.assert_called_once()

    def test_legacy_settings_keep_visibility_and_position(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            save_json(
                path,
                {
                    "widget_enabled": True,
                    "widget_type": "Компактный",
                    "widget_x": 321,
                    "widget_y": 123,
                },
            )

            settings = load_app_settings(path)

            self.assertTrue(settings.widget_enabled)
            self.assertEqual(settings.widget_layouts["Компактный"]["x"], 321)
            self.assertEqual(settings.widget_layouts["Компактный"]["y"], 123)

    def test_settings_ui_has_no_visibility_checkbox_and_keeps_other_controls(self) -> None:
        source = inspect.getsource(SettingsView)
        tray_source = inspect.getsource(TrayController)

        self.assertNotIn("Виджет включен", source)
        self.assertNotIn("widget_enabled_var", source)
        self.assertNotIn("Показать / скрыть виджет", tray_source)
        self.assertNotIn("toggle_widget", tray_source)
        self.assertIn("Тип виджета:", source)
        self.assertIn("Размер виджета:", source)
        self.assertIn("Поверх всех окон", source)

        view = SettingsView.__new__(SettingsView)
        view.settings = make_settings()
        view.settings.widget_enabled = True
        profile_settings = make_settings()
        profile_settings.widget_enabled = False
        view._preserve_widget_visibility(profile_settings)
        self.assertTrue(profile_settings.widget_enabled)

    def test_widget_close_requests_the_common_hidden_state(self) -> None:
        requests: list[bool] = []
        widget = WidgetWindow.__new__(WidgetWindow)
        widget._on_visibility_requested = requests.append

        widget._request_hide()

        self.assertEqual(requests, [False])


if __name__ == "__main__":
    unittest.main()
