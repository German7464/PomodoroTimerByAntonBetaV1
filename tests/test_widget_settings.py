"""Миграция геометрий, пресеты и UI-модель плавающего виджета."""

from dataclasses import asdict
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from app.storage import default_settings_data, load_app_settings, save_json
from app.timer_engine import TimerEngine
from app.ui.widget_window import (
    CompactWidgetView,
    ExpandedWidgetView,
    MinimalWidgetView,
    widget_display_state,
    widget_view_class,
)
from app.widget_settings import (
    DEFAULT_WIDGET_SIZE,
    DEFAULT_WIDGET_TYPE,
    WIDGET_MIN_SIZES,
    WIDGET_SIZE_CUSTOM,
    WIDGET_SIZE_LARGE,
    WIDGET_SIZE_MEDIUM,
    WIDGET_SIZE_PRESETS,
    WIDGET_SIZE_SMALL,
    WIDGET_TYPE_COMPACT,
    WIDGET_TYPE_EXPANDED,
    WIDGET_TYPE_MINIMAL,
    clamp_window_position,
    default_widget_layouts,
    normalize_widget_layouts,
    set_widget_layout_size,
    widget_size_parameters,
)
from tests.test_timer_engine import finish_current_period, make_settings


class WidgetSettingsTests(unittest.TestCase):
    """Проверяет безопасные настройки без создания Tk root."""

    def test_old_settings_get_compact_small_defaults(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            old_data = default_settings_data()
            old_data.pop("widget_size")
            old_data.pop("widget_layouts")
            old_data["widget_type"] = "Компактный"
            old_data["widget_x"] = 321
            old_data["widget_y"] = 123
            save_json(path, old_data)

            settings = load_app_settings(path)

            self.assertEqual(settings.widget_type, DEFAULT_WIDGET_TYPE)
            self.assertEqual(settings.widget_size, DEFAULT_WIDGET_SIZE)
            layout = settings.widget_layouts[WIDGET_TYPE_COMPACT]
            self.assertEqual(layout["x"], 321)
            self.assertEqual(layout["y"], 123)
            self.assertEqual(layout["width"], 240)
            self.assertEqual(layout["height"], 145)

    def test_unknown_widget_type_and_size_fall_back_safely(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            data = default_settings_data()
            data["widget_type"] = "Неизвестный"
            data["widget_size"] = "Огромный"
            data["widget_layouts"] = {"Компактный": "bad"}
            save_json(path, data)

            settings = load_app_settings(path)

            self.assertEqual(settings.widget_type, WIDGET_TYPE_COMPACT)
            self.assertEqual(settings.widget_size, WIDGET_SIZE_SMALL)
            self.assertEqual(settings.widget_layouts, default_widget_layouts())

    def test_all_three_types_select_distinct_view_classes(self) -> None:
        self.assertIs(widget_view_class(WIDGET_TYPE_MINIMAL), MinimalWidgetView)
        self.assertIs(widget_view_class(WIDGET_TYPE_COMPACT), CompactWidgetView)
        self.assertIs(widget_view_class(WIDGET_TYPE_EXPANDED), ExpandedWidgetView)
        self.assertIs(widget_view_class("bad"), CompactWidgetView)

    def test_small_medium_large_have_expected_parameters_for_each_type(self) -> None:
        for widget_type, presets in WIDGET_SIZE_PRESETS.items():
            previous_width = 0
            previous_height = 0
            for widget_size in (WIDGET_SIZE_SMALL, WIDGET_SIZE_MEDIUM, WIDGET_SIZE_LARGE):
                with self.subTest(widget_type=widget_type, widget_size=widget_size):
                    parameters = widget_size_parameters(widget_type, widget_size)
                    self.assertEqual(parameters, presets[widget_size])
                    self.assertGreater(parameters.width, previous_width)
                    self.assertGreater(parameters.height, previous_height)
                    previous_width = parameters.width
                    previous_height = parameters.height

    def test_custom_size_is_preserved_and_restored_per_type(self) -> None:
        layouts = default_widget_layouts()
        layouts[WIDGET_TYPE_EXPANDED] = {
            "size": WIDGET_SIZE_CUSTOM,
            "width": 777,
            "height": 444,
            "x": 50,
            "y": 60,
        }

        normalized = normalize_widget_layouts(layouts)

        self.assertEqual(normalized[WIDGET_TYPE_EXPANDED], layouts[WIDGET_TYPE_EXPANDED])
        self.assertEqual(normalized[WIDGET_TYPE_COMPACT]["size"], WIDGET_SIZE_SMALL)

    def test_invalid_custom_size_and_coordinates_are_repaired(self) -> None:
        layouts = {
            WIDGET_TYPE_MINIMAL: {
                "size": WIDGET_SIZE_CUSTOM,
                "width": -1,
                "height": "bad",
                "x": 999_999,
                "y": None,
            },
        }

        normalized = normalize_widget_layouts(layouts)
        minimum_width, minimum_height = WIDGET_MIN_SIZES[WIDGET_TYPE_MINIMAL]
        minimal = normalized[WIDGET_TYPE_MINIMAL]
        self.assertEqual(minimal["width"], minimum_width)
        self.assertEqual(minimal["height"], minimum_height)
        self.assertEqual(minimal["x"], 100_000)
        self.assertEqual(minimal["y"], 100)

        clamped = clamp_window_position(
            int(minimal["x"]),
            int(minimal["y"]),
            int(minimal["width"]),
            int(minimal["height"]),
            (0, 0, 1920, 1080),
        )
        self.assertLessEqual(clamped[0], 1920 - 48)
        self.assertLessEqual(clamped[1], 1080 - 48)

    def test_switching_layout_does_not_change_timer_state(self) -> None:
        timer = TimerEngine(make_settings())
        timer.state.remaining_seconds = 37
        timer.state.is_running = False
        before = asdict(timer.state)
        layouts = default_widget_layouts()

        for widget_type in (
            WIDGET_TYPE_MINIMAL,
            WIDGET_TYPE_COMPACT,
            WIDGET_TYPE_EXPANDED,
        ):
            layouts = set_widget_layout_size(layouts, widget_type, WIDGET_SIZE_MEDIUM)
            widget_view_class(widget_type)

        self.assertEqual(asdict(timer.state), before)

    def test_display_state_preserves_normal_and_overrun_text_for_all_views(self) -> None:
        timer = TimerEngine(make_settings())
        normal = widget_display_state(timer)
        self.assertEqual(normal.mode_name, "Работа")
        self.assertEqual(normal.formatted_time, "00:01:00")

        finish_current_period(timer)
        timer.tick()
        overrun = widget_display_state(timer)
        self.assertEqual(overrun.mode_name, "Переработка")
        self.assertEqual(overrun.formatted_time, "+00:00:01")
        self.assertEqual(overrun.primary_text, "Продолжить")

        for widget_type in (
            WIDGET_TYPE_MINIMAL,
            WIDGET_TYPE_COMPACT,
            WIDGET_TYPE_EXPANDED,
        ):
            with self.subTest(widget_type=widget_type):
                self.assertIsNotNone(widget_view_class(widget_type))
                self.assertTrue(overrun.waiting_for_continue)


if __name__ == "__main__":
    unittest.main()
