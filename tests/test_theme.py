"""Палитры, миграция и UI-контракты светлого/тёмного оформления."""

from dataclasses import asdict
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from app.storage import default_settings_data, load_app_settings, save_app_settings, save_json
from app.theme import (
    APPEARANCE_DARK,
    APPEARANCE_LIGHT,
    BUILTIN_THEME_NAMES,
    CUSTOM_THEME_NAME,
    CustomThemeDraft,
    DEFAULT_APPEARANCE_MODE,
    DEFAULT_THEME_NAME,
    PALETTES,
    THEME_NAMES,
    ThemePalette,
    default_custom_theme,
    get_palette,
    mode_color,
    normalize_appearance_mode,
    normalize_custom_theme,
    normalize_theme_name,
)
from app.timer_engine import TimerEngine
from app.ui import main_window as main_window_module
from app.ui.main_window import MainWindow
from app.ui.widget_window import WidgetWindow
from tests.test_timer_engine import finish_current_period, make_settings


REQUIRED_COLORS = {
    "background",
    "card_background",
    "secondary_background",
    "text_primary",
    "text_secondary",
    "accent",
    "accent_hover",
    "button_background",
    "button_text",
    "border",
    "disabled",
    "focus",
    "success",
    "warning",
    "error",
    "work",
    "short_break",
    "long_break",
    "overwork",
    "short_break_overrun",
    "long_break_overrun",
    "on_accent",
}


def relative_luminance(color: str) -> float:
    """Вычисляет WCAG luminance для цвета #RRGGBB."""
    values = []
    for offset in (1, 3, 5):
        channel = int(color[offset : offset + 2], 16) / 255
        values.append(
            channel / 12.92
            if channel <= 0.04045
            else ((channel + 0.055) / 1.055) ** 2.4,
        )
    return 0.2126 * values[0] + 0.7152 * values[1] + 0.0722 * values[2]


def contrast_ratio(first: str, second: str) -> float:
    """Возвращает WCAG contrast ratio двух цветов."""
    first_luminance = relative_luminance(first)
    second_luminance = relative_luminance(second)
    light = max(first_luminance, second_luminance)
    dark = min(first_luminance, second_luminance)
    return (light + 0.05) / (dark + 0.05)


class FakeButton:
    def __init__(self) -> None:
        self.text = ""

    def config(self, **values: str) -> None:
        self.text = values.get("text", self.text)


class FakeLabel:
    def __init__(self) -> None:
        self.values: dict[str, str] = {}

    def config(self, **values: str) -> None:
        self.values.update(values)


class FakeThemeManager:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def apply(
        self,
        theme_name: str,
        appearance_mode: str,
        custom_theme=None,
    ) -> ThemePalette:
        self.calls.append((theme_name, appearance_mode))
        return get_palette(theme_name, appearance_mode, custom_theme)

    def mode_style(self, _mode, waiting: bool) -> str:
        return "Overrun.TimerMode.TLabel" if waiting else "Work.TimerMode.TLabel"


class FakeSettingsView:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def sync_theme(self, theme_name: str, appearance_mode: str) -> None:
        self.calls.append((theme_name, appearance_mode))


class FakeWindow:
    def winfo_width(self) -> int:
        return 310

    def winfo_height(self) -> int:
        return 180


class FakeWidgetView:
    def __init__(self) -> None:
        self.applied: list[ThemePalette] = []
        self.update_calls = 0

    def apply_style(self, palette: ThemePalette, _parameters) -> None:
        self.applied.append(palette)

    def update(self) -> None:
        self.update_calls += 1


class FakeWidgetThemeManager:
    def __init__(self, palette: ThemePalette) -> None:
        self.palette = palette
        self.windows: list[object] = []

    def apply_to_window(self, window: object) -> None:
        self.windows.append(window)


class ThemeTests(unittest.TestCase):
    """Проверяет шесть палитр и сохранение безопасного выбора."""

    def test_old_settings_receive_comet_light_without_losing_values(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            old_data = default_settings_data()
            old_data.pop("theme_name")
            old_data.pop("appearance_mode")
            old_data.pop("custom_theme")
            old_data.pop("overrun_visual")
            old_data.pop("widget_layouts")
            old_data.pop("widget_size")
            old_data["work_minutes"] = 47
            old_data["widget_x"] = 321
            save_json(path, old_data)

            settings = load_app_settings(path)

            self.assertEqual(settings.theme_name, DEFAULT_THEME_NAME)
            self.assertEqual(settings.appearance_mode, DEFAULT_APPEARANCE_MODE)
            self.assertEqual(settings.custom_theme, default_custom_theme())
            self.assertEqual(settings.work_minutes, 47)
            self.assertEqual(settings.widget_x, 321)

    def test_all_themes_have_light_dark_and_required_semantic_colors(self) -> None:
        self.assertEqual(tuple(PALETTES), BUILTIN_THEME_NAMES)
        self.assertIn(CUSTOM_THEME_NAME, THEME_NAMES)
        for theme_name in BUILTIN_THEME_NAMES:
            self.assertEqual(set(PALETTES[theme_name]), {APPEARANCE_LIGHT, APPEARANCE_DARK})
            for mode, palette in PALETTES[theme_name].items():
                with self.subTest(theme=theme_name, mode=mode):
                    self.assertEqual(set(palette.as_dict()), REQUIRED_COLORS)
                    for value in palette.as_dict().values():
                        self.assertRegex(value, r"^#[0-9A-F]{6}$")

    def test_every_palette_meets_text_and_state_contrast_targets(self) -> None:
        for theme_name, modes in PALETTES.items():
            for mode, palette in modes.items():
                with self.subTest(theme=theme_name, mode=mode):
                    for foreground in (
                        palette.text_primary,
                        palette.text_secondary,
                        palette.work,
                        palette.short_break,
                        palette.long_break,
                        palette.overwork,
                        palette.short_break_overrun,
                        palette.long_break_overrun,
                    ):
                        self.assertGreaterEqual(
                            contrast_ratio(foreground, palette.card_background),
                            4.5,
                        )
                    self.assertGreaterEqual(
                        contrast_ratio(palette.on_accent, palette.accent),
                        4.5,
                    )
                    self.assertGreaterEqual(
                        contrast_ratio(palette.on_accent, palette.accent_hover),
                        4.5,
                    )
                    self.assertGreaterEqual(
                        contrast_ratio(palette.text_primary, palette.border),
                        4.5,
                    )
                    self.assertGreaterEqual(
                        contrast_ratio(palette.button_text, palette.button_background),
                        4.5,
                    )

    def test_custom_light_and_dark_palettes_are_saved_separately(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            settings = make_settings()
            settings.theme_name = CUSTOM_THEME_NAME
            settings.custom_theme = default_custom_theme()
            settings.custom_theme[APPEARANCE_LIGHT]["accent"] = "#112233"
            settings.custom_theme[APPEARANCE_DARK]["accent"] = "#AABBCC"

            save_app_settings(path, settings)
            restored = load_app_settings(path)

            self.assertEqual(restored.custom_theme[APPEARANCE_LIGHT]["accent"], "#112233")
            self.assertEqual(restored.custom_theme[APPEARANCE_DARK]["accent"], "#AABBCC")
            self.assertEqual(
                get_palette(
                    CUSTOM_THEME_NAME,
                    APPEARANCE_DARK,
                    restored.custom_theme,
                ).accent,
                "#AABBCC",
            )

    def test_invalid_custom_colors_are_repaired_field_by_field(self) -> None:
        custom = {
            APPEARANCE_LIGHT: {
                "accent": "#123456",
                "text_primary": "broken",
            },
            APPEARANCE_DARK: "broken",
        }

        normalized = normalize_custom_theme(custom)

        self.assertEqual(normalized[APPEARANCE_LIGHT]["accent"], "#123456")
        self.assertEqual(
            normalized[APPEARANCE_LIGHT]["text_primary"],
            PALETTES[DEFAULT_THEME_NAME][APPEARANCE_LIGHT].text_primary,
        )
        self.assertEqual(
            normalized[APPEARANCE_DARK],
            PALETTES[DEFAULT_THEME_NAME][APPEARANCE_DARK].as_dict(),
        )

    def test_custom_draft_cancel_and_resets_restore_safe_copies(self) -> None:
        saved = default_custom_theme("Aurora")
        draft = CustomThemeDraft(saved)
        draft.value[APPEARANCE_LIGHT]["accent"] = "#010203"

        self.assertEqual(draft.cancel(), saved)
        draft.reset_mode(APPEARANCE_LIGHT)
        self.assertEqual(
            draft.value[APPEARANCE_LIGHT],
            PALETTES[DEFAULT_THEME_NAME][APPEARANCE_LIGHT].as_dict(),
        )
        self.assertEqual(draft.value[APPEARANCE_DARK], saved[APPEARANCE_DARK])
        draft.reset_all()
        self.assertEqual(draft.applied(), default_custom_theme())

    def test_invalid_theme_and_mode_fall_back_safely(self) -> None:
        self.assertEqual(normalize_theme_name("broken"), DEFAULT_THEME_NAME)
        self.assertEqual(normalize_appearance_mode("broken"), DEFAULT_APPEARANCE_MODE)
        self.assertIs(
            get_palette("broken", "broken"),
            PALETTES[DEFAULT_THEME_NAME][DEFAULT_APPEARANCE_MODE],
        )

    def test_selection_is_saved_and_restored_with_other_settings(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            settings = make_settings()
            settings.theme_name = "Aurora"
            settings.appearance_mode = APPEARANCE_DARK
            settings.work_minutes = 52
            settings.widget_opacity = 83

            save_app_settings(path, settings)
            restored = load_app_settings(path)

            self.assertEqual(restored.theme_name, "Aurora")
            self.assertEqual(restored.appearance_mode, APPEARANCE_DARK)
            self.assertEqual(restored.work_minutes, 52)
            self.assertEqual(restored.widget_opacity, 83)

    def test_theme_change_does_not_change_timer_state(self) -> None:
        timer = TimerEngine(make_settings())
        timer.start()
        timer.tick()
        before = asdict(timer.state)

        for theme_name in THEME_NAMES:
            for appearance_mode in (APPEARANCE_LIGHT, APPEARANCE_DARK):
                get_palette(theme_name, appearance_mode)

        self.assertEqual(asdict(timer.state), before)

    def test_open_widget_receives_palette_without_replacing_window(self) -> None:
        settings = make_settings()
        palette = get_palette("Warm", APPEARANCE_DARK)
        manager = FakeWidgetThemeManager(palette)
        widget = WidgetWindow.__new__(WidgetWindow)
        widget.settings = settings
        widget.window = FakeWindow()
        original_window = widget.window
        widget.view = FakeWidgetView()
        widget.theme_manager = manager

        widget.apply_theme(palette)

        self.assertIs(widget.window, original_window)
        self.assertEqual(widget.view.applied, [palette])
        self.assertEqual(widget.view.update_calls, 1)
        self.assertEqual(manager.windows, [original_window])

    def test_timer_modes_and_overrun_keep_distinct_semantic_colors(self) -> None:
        timer = TimerEngine(make_settings())
        palette = get_palette("Comet", APPEARANCE_LIGHT)
        normal_color = mode_color(palette, timer.state.mode)
        finish_current_period(timer)
        timer.tick()
        overrun_color = mode_color(
            palette,
            timer.state.mode,
            timer.state.waiting_for_continue,
        )

        self.assertEqual(normal_color, palette.work)
        self.assertEqual(overrun_color, palette.overrun)
        self.assertEqual(timer.mode_name(), "Переработка")
        self.assertTrue(timer.formatted_time().startswith("+"))

    def test_quick_toggle_and_settings_share_one_state_and_save_once(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            window = MainWindow.__new__(MainWindow)
            window.settings = make_settings()
            window.timer = TimerEngine(window.settings)
            window.theme_manager = FakeThemeManager()
            window.settings_view = FakeSettingsView()
            window.theme_toggle_button = FakeButton()
            window.mode_label = FakeLabel()

            with (
                patch.object(main_window_module, "SETTINGS_FILE", path),
                patch.object(main_window_module, "save_app_settings", wraps=save_app_settings) as save,
            ):
                window.apply_theme_selection("Aurora", APPEARANCE_DARK)
                window.apply_theme_selection("Aurora", APPEARANCE_DARK)
                window.toggle_appearance_mode()

            self.assertEqual(window.settings.theme_name, "Aurora")
            self.assertEqual(window.settings.appearance_mode, APPEARANCE_LIGHT)
            self.assertEqual(window.settings_view.calls[-1], ("Aurora", APPEARANCE_LIGHT))
            self.assertEqual(window.theme_toggle_button.text, "Тёмный режим")
            self.assertEqual(save.call_count, 2)
            restored = load_app_settings(path)
            self.assertEqual(restored.theme_name, "Aurora")
            self.assertEqual(restored.appearance_mode, APPEARANCE_LIGHT)


if __name__ == "__main__":
    unittest.main()
