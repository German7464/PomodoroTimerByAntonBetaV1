"""Настройки, математика и жизненный цикл индикации превышения."""

from dataclasses import asdict
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from app.models import TimerMode
from app.overrun_effects import (
    EFFECT_BEACONS,
    EFFECT_BORDER,
    EFFECT_NONE,
    EFFECT_PULSE,
    EFFECT_SCALE,
    EFFECT_WAVE,
    EFFECT_COLOR_PULSE,
    LEGACY_EFFECT_NONE,
    INACTIVE_FRAME,
    LONG_BREAK_OVERRUN_KEY,
    OVERWORK_KEY,
    OVERRUN_EFFECTS,
    OverrunVisualController,
    OverrunVisualFrame,
    SHORT_BREAK_OVERRUN_KEY,
    SCOPE_BOTH,
    SCOPE_CARD,
    SCOPE_DIGITS,
    calculate_overrun_frame,
    cycle_phase,
    default_overrun_visual,
    interpolate_color,
    normalize_overrun_visual,
    pulse_phase,
    resolved_overrun_color,
)
from app.profiles import ProfilesService
from app.storage import default_settings_data, load_app_settings, save_app_settings, save_json
from app.theme import APPEARANCE_DARK, APPEARANCE_LIGHT, get_palette
from app.timer_engine import TimerEngine
from app.ui.main_window import MainWindow
from tests.test_timer_engine import make_settings


class FakeScheduler:
    """Детерминированный аналог after/after_cancel с монотонными часами."""

    def __init__(self) -> None:
        self.now = 10.0
        self._next_id = 0
        self.jobs: dict[int, object] = {}

    def schedule(self, _delay: int, callback):
        self._next_id += 1
        self.jobs[self._next_id] = callback
        return self._next_id

    def cancel(self, job_id: object) -> None:
        self.jobs.pop(int(job_id), None)

    def run_next(self, advance: float = 0.08) -> None:
        self.now += advance
        job_id = min(self.jobs)
        callback = self.jobs.pop(job_id)
        callback()


class FakeThemeManager:
    def __init__(self) -> None:
        self.calls: list[tuple[str | None, str | None]] = []

    def apply_timer_effect(self, digits: str | None, card: str | None) -> None:
        self.calls.append((digits, card))


class FakeWidgetWindow:
    def __init__(self) -> None:
        self.frames: list[OverrunVisualFrame] = []

    def apply_overrun_visual(self, frame: OverrunVisualFrame) -> None:
        self.frames.append(frame)


class OverrunEffectsTests(unittest.TestCase):
    def test_old_settings_receive_effect_defaults_without_losing_data(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            old = default_settings_data()
            old.pop("overrun_visual")
            old["work_minutes"] = 43
            save_json(path, old)

            restored = load_app_settings(path)

            self.assertEqual(restored.overrun_visual, default_overrun_visual())
            self.assertEqual(restored.work_minutes, 43)

    def test_three_overrides_save_restore_and_other_settings_survive(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            settings = make_settings()
            settings.widget_opacity = 82
            settings.overrun_visual = default_overrun_visual()
            settings.overrun_visual["colors"] = {
                OVERWORK_KEY: "#112233",
                SHORT_BREAK_OVERRUN_KEY: "#445566",
                LONG_BREAK_OVERRUN_KEY: "#778899",
            }

            save_app_settings(path, settings)
            restored = load_app_settings(path)

            self.assertEqual(restored.overrun_visual["colors"], settings.overrun_visual["colors"])
            self.assertEqual(restored.widget_opacity, 82)

    def test_profile_preserves_effect_configuration(self) -> None:
        with TemporaryDirectory() as directory:
            settings = make_settings()
            settings.overrun_visual = normalize_overrun_visual(
                {
                    "effect": EFFECT_BORDER,
                    "scope": SCOPE_CARD,
                    "speed": "Быстро",
                    "intensity": "Сильно",
                    "animations_enabled": False,
                    "colors": {OVERWORK_KEY: "#123456"},
                },
            )
            service = ProfilesService(Path(directory) / "profiles.json")

            profile = service.save_profile("effect", settings)
            restored = service.settings_from_profile(profile)

            self.assertEqual(restored.overrun_visual, settings.overrun_visual)

    def test_invalid_partial_section_is_repaired_by_field(self) -> None:
        value = {
            "effect": "unknown",
            "scope": SCOPE_CARD,
            "animations_enabled": False,
            "colors": {
                OVERWORK_KEY: "broken",
                SHORT_BREAK_OVERRUN_KEY: "#abcdef",
            },
        }

        normalized = normalize_overrun_visual(value)

        self.assertEqual(normalized["effect"], EFFECT_PULSE)
        self.assertEqual(normalized["scope"], SCOPE_CARD)
        self.assertFalse(normalized["animations_enabled"])
        self.assertIsNone(normalized["colors"][OVERWORK_KEY])
        self.assertEqual(normalized["colors"][SHORT_BREAK_OVERRUN_KEY], "#ABCDEF")
        self.assertIsNone(normalized["colors"][LONG_BREAK_OVERRUN_KEY])

        self.assertTrue(
            normalize_overrun_visual({"animations_enabled": "broken"})[
                "animations_enabled"
            ],
        )

    def test_legacy_effect_names_migrate_to_primary_effect_and_color_toggle(self) -> None:
        legacy_combined = normalize_overrun_visual({"effect": EFFECT_COLOR_PULSE})
        legacy_none = normalize_overrun_visual({"effect": LEGACY_EFFECT_NONE})

        self.assertEqual(legacy_combined["effect"], EFFECT_PULSE)
        self.assertTrue(legacy_combined["color_enabled"])
        self.assertEqual(legacy_none["effect"], EFFECT_NONE)
        self.assertFalse(legacy_none["color_enabled"])
        self.assertFalse(legacy_none["opaque_widget_during_overrun"])

    def test_all_effect_and_scope_choices_are_preserved(self) -> None:
        self.assertEqual(
            OVERRUN_EFFECTS,
            (
                EFFECT_NONE,
                EFFECT_PULSE,
                EFFECT_SCALE,
                EFFECT_BEACONS,
                EFFECT_BORDER,
                EFFECT_WAVE,
            ),
        )
        for effect in OVERRUN_EFFECTS:
            for scope in (SCOPE_DIGITS, SCOPE_CARD, SCOPE_BOTH):
                with self.subTest(effect=effect, scope=scope):
                    normalized = normalize_overrun_visual(
                        {"effect": effect, "scope": scope},
                    )
                    self.assertEqual(normalized["effect"], effect)
                    self.assertEqual(normalized["scope"], scope)

    def test_all_effects_calculate_expected_target_areas(self) -> None:
        palette = get_palette("Comet", APPEARANCE_LIGHT)
        for effect in OVERRUN_EFFECTS:
            for scope in (SCOPE_DIGITS, SCOPE_CARD, SCOPE_BOTH):
                with self.subTest(effect=effect, scope=scope):
                    frame = calculate_overrun_frame(
                        palette,
                        TimerMode.WORK,
                        {
                            "effect": effect,
                            "scope": scope,
                            "speed": "Быстро",
                            "intensity": "Сильно",
                        },
                        0.6,
                    )
                    self.assertEqual(
                        frame.digits_color is not None,
                        scope in {SCOPE_DIGITS, SCOPE_BOTH},
                    )
                    self.assertEqual(
                        frame.card_background is not None,
                        scope in {SCOPE_CARD, SCOPE_BOTH},
                    )

    def test_three_states_resolve_their_own_colors(self) -> None:
        palette = get_palette("Comet", APPEARANCE_LIGHT)
        visual = default_overrun_visual()
        visual["colors"] = {
            OVERWORK_KEY: "#010203",
            SHORT_BREAK_OVERRUN_KEY: "#040506",
            LONG_BREAK_OVERRUN_KEY: "#070809",
        }

        self.assertEqual(resolved_overrun_color(visual, palette, TimerMode.WORK), "#010203")
        self.assertEqual(
            resolved_overrun_color(visual, palette, TimerMode.SHORT_BREAK),
            "#040506",
        )
        self.assertEqual(
            resolved_overrun_color(visual, palette, TimerMode.LONG_BREAK),
            "#070809",
        )

    def test_intermediate_color_and_phase_are_bounded(self) -> None:
        self.assertEqual(interpolate_color("#000000", "#FFFFFF", 0.5), "#808080")
        self.assertEqual(interpolate_color("#000000", "#FFFFFF", -2), "#000000")
        self.assertEqual(interpolate_color("#000000", "#FFFFFF", 2), "#FFFFFF")
        for elapsed in (0, 0.1, 1, 20):
            self.assertGreaterEqual(pulse_phase(elapsed, "Обычно"), 0.0)
            self.assertLessEqual(pulse_phase(elapsed, "Обычно"), 1.0)
            self.assertGreaterEqual(cycle_phase(elapsed, "Обычно"), 0.0)
            self.assertLess(cycle_phase(elapsed, "Обычно"), 1.0)

    def test_four_structural_effects_have_bounded_frames(self) -> None:
        palette = get_palette("Comet", APPEARANCE_LIGHT)
        scale = calculate_overrun_frame(
            palette,
            TimerMode.WORK,
            {"effect": EFFECT_SCALE, "intensity": "Сильно"},
            0.5,
        )
        beacons = calculate_overrun_frame(
            palette,
            TimerMode.SHORT_BREAK,
            {"effect": EFFECT_BEACONS},
            0.5,
        )
        border = calculate_overrun_frame(
            palette,
            TimerMode.LONG_BREAK,
            {"effect": EFFECT_BORDER},
            0.5,
        )
        wave = calculate_overrun_frame(
            palette,
            TimerMode.WORK,
            {"effect": EFFECT_WAVE},
            0.5,
        )

        self.assertGreater(scale.digit_scale, 1.0)
        self.assertLessEqual(scale.digit_scale, 1.15)
        self.assertGreater(beacons.beacon_level, 0.0)
        self.assertIsNotNone(beacons.effect_color)
        self.assertIsNotNone(border.border_color)
        self.assertGreater(border.border_width, 0.0)
        self.assertIsNotNone(wave.wave_position)
        self.assertGreaterEqual(wave.wave_position, 0.0)
        self.assertLessEqual(wave.wave_position, 1.0)

    def test_no_effect_and_ordinary_period_do_not_add_visual_overrides(self) -> None:
        palette = get_palette("Comet", APPEARANCE_LIGHT)
        frame = calculate_overrun_frame(
            palette,
            TimerMode.WORK,
            {"effect": EFFECT_NONE, "color_enabled": False},
            1.0,
        )
        scheduler = FakeScheduler()
        frames: list[OverrunVisualFrame] = []
        controller = OverrunVisualController(
            scheduler.schedule,
            scheduler.cancel,
            frames.append,
            lambda: scheduler.now,
        )
        controller.sync_actual(False, TimerMode.WORK, default_overrun_visual(), palette)

        self.assertTrue(frame.active)
        self.assertIsNone(frame.digits_color)
        self.assertIsNone(frame.card_background)
        self.assertEqual(frames[-1], INACTIVE_FRAME)
        self.assertFalse(controller.has_scheduled_frame)

    def test_repeated_sync_keeps_exactly_one_animation_callback(self) -> None:
        palette = get_palette("Aurora", APPEARANCE_DARK)
        scheduler = FakeScheduler()
        frames: list[OverrunVisualFrame] = []
        controller = OverrunVisualController(
            scheduler.schedule,
            scheduler.cancel,
            frames.append,
            lambda: scheduler.now,
        )
        visual = default_overrun_visual()

        controller.sync_actual(True, TimerMode.WORK, visual, palette)
        first_job = set(scheduler.jobs)
        controller.sync_actual(True, TimerMode.WORK, visual, palette)
        controller.sync_actual(True, TimerMode.WORK, visual, palette)

        self.assertEqual(set(scheduler.jobs), first_job)
        self.assertEqual(len(scheduler.jobs), 1)
        self.assertEqual(len(frames), 1)

    def test_switching_each_new_effect_replaces_the_single_callback(self) -> None:
        palette = get_palette("Aurora", APPEARANCE_DARK)
        scheduler = FakeScheduler()
        frames: list[OverrunVisualFrame] = []
        controller = OverrunVisualController(
            scheduler.schedule,
            scheduler.cancel,
            frames.append,
            lambda: scheduler.now,
        )
        previous_job: int | None = None
        for effect in (EFFECT_SCALE, EFFECT_BEACONS, EFFECT_BORDER, EFFECT_WAVE):
            visual = default_overrun_visual()
            visual["effect"] = effect
            controller.sync_actual(True, TimerMode.WORK, visual, palette)
            self.assertEqual(len(scheduler.jobs), 1)
            current_job = next(iter(scheduler.jobs))
            if previous_job is not None:
                self.assertNotEqual(current_job, previous_job)
            previous_job = current_job
            self.assertEqual(frames[-1].effect, effect)

        controller.sync_actual(False, TimerMode.WORK, visual, palette)
        self.assertEqual(scheduler.jobs, {})
        self.assertEqual(frames[-1], INACTIVE_FRAME)

    def test_animation_disabled_keeps_static_color_without_callback(self) -> None:
        palette = get_palette("Warm", APPEARANCE_DARK)
        visual = default_overrun_visual()
        visual["effect"] = EFFECT_PULSE
        visual["animations_enabled"] = False
        scheduler = FakeScheduler()
        frames: list[OverrunVisualFrame] = []
        controller = OverrunVisualController(
            scheduler.schedule,
            scheduler.cancel,
            frames.append,
            lambda: scheduler.now,
        )

        controller.sync_actual(True, TimerMode.SHORT_BREAK, visual, palette)

        self.assertFalse(controller.has_scheduled_frame)
        self.assertEqual(scheduler.jobs, {})
        self.assertIsNotNone(frames[-1].digits_color)

    def test_continue_reset_or_exit_stop_callback_and_restore_frame(self) -> None:
        palette = get_palette("Comet", APPEARANCE_DARK)
        scheduler = FakeScheduler()
        frames: list[OverrunVisualFrame] = []
        controller = OverrunVisualController(
            scheduler.schedule,
            scheduler.cancel,
            frames.append,
            lambda: scheduler.now,
        )
        controller.sync_actual(True, TimerMode.LONG_BREAK, default_overrun_visual(), palette)
        self.assertEqual(len(scheduler.jobs), 1)

        controller.sync_actual(False, TimerMode.WORK, default_overrun_visual(), palette)
        self.assertEqual(scheduler.jobs, {})
        self.assertEqual(frames[-1], INACTIVE_FRAME)
        controller.stop()
        self.assertEqual(frames[-1], INACTIVE_FRAME)

    def test_preview_and_theme_change_do_not_mutate_timer_state(self) -> None:
        timer = TimerEngine(make_settings())
        timer.start()
        timer.tick()
        before = asdict(timer.state)
        scheduler = FakeScheduler()
        frames: list[OverrunVisualFrame] = []
        controller = OverrunVisualController(
            scheduler.schedule,
            scheduler.cancel,
            frames.append,
            lambda: scheduler.now,
        )
        light = get_palette("Comet", APPEARANCE_LIGHT)
        dark = get_palette("Comet", APPEARANCE_DARK)
        controller.sync_actual(False, timer.state.mode, default_overrun_visual(), light)
        controller.start_preview(TimerMode.WORK, default_overrun_visual(), light, 2.0)
        self.assertTrue(frames[-1].preview)
        light_preview_color = frames[-1].digits_color
        controller.sync_actual(False, timer.state.mode, default_overrun_visual(), dark)
        self.assertTrue(frames[-1].preview)
        self.assertNotEqual(frames[-1].digits_color, light_preview_color)
        scheduler.run_next(advance=3.0)

        self.assertEqual(asdict(timer.state), before)
        self.assertEqual(frames[-1], INACTIVE_FRAME)

    def test_main_and_widget_receive_the_same_frame_object(self) -> None:
        window = MainWindow.__new__(MainWindow)
        window.theme_manager = FakeThemeManager()
        window.widget_window = FakeWidgetWindow()
        frame = OverrunVisualFrame(
            active=True,
            mode=TimerMode.WORK,
            digits_color="#123456",
            card_background="#654321",
        )

        window._apply_overrun_visual_frame(frame)

        self.assertEqual(window.theme_manager.calls[-1], ("#123456", "#654321"))
        self.assertIs(window.widget_window.frames[-1], frame)


if __name__ == "__main__":
    unittest.main()
