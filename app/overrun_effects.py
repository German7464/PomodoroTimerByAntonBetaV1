"""Чистый расчёт и единый планировщик визуальной индикации превышения."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, replace
from math import cos, pi
import time
from typing import Final

from app.models import TimerMode
from app.theme import ThemePalette, is_hex_color, mode_color


EFFECT_NONE: Final = "none"
EFFECT_PULSE: Final = "pulse"
EFFECT_SCALE: Final = "scale"
EFFECT_BEACONS: Final = "beacons"
EFFECT_BORDER: Final = "border"
EFFECT_WAVE: Final = "wave"
OVERRUN_EFFECTS: Final = (
    EFFECT_NONE,
    EFFECT_PULSE,
    EFFECT_SCALE,
    EFFECT_BEACONS,
    EFFECT_BORDER,
    EFFECT_WAVE,
)

# Значения из предыдущей версии распознаются только при миграции JSON.
LEGACY_EFFECT_NONE: Final = "Без дополнительного эффекта"
EFFECT_COLOR: Final = "Изменение цвета"
EFFECT_COLOR_PULSE: Final = "Цвет и пульсация"

SCOPE_DIGITS: Final = "digits"
SCOPE_CARD: Final = "card"
SCOPE_BOTH: Final = "both"
OVERRUN_SCOPES: Final = (SCOPE_DIGITS, SCOPE_CARD, SCOPE_BOTH)

SPEED_SLOW: Final = "slow"
SPEED_NORMAL: Final = "normal"
SPEED_FAST: Final = "fast"
OVERRUN_SPEEDS: Final = (SPEED_SLOW, SPEED_NORMAL, SPEED_FAST)

INTENSITY_WEAK: Final = "weak"
INTENSITY_MEDIUM: Final = "medium"
INTENSITY_STRONG: Final = "strong"
OVERRUN_INTENSITIES: Final = (
    INTENSITY_WEAK,
    INTENSITY_MEDIUM,
    INTENSITY_STRONG,
)

EFFECT_LABEL_KEYS: Final = {value: f"overrun.effect.{value}" for value in OVERRUN_EFFECTS}
SCOPE_LABEL_KEYS: Final = {value: f"overrun.scope.{value}" for value in OVERRUN_SCOPES}
SPEED_LABEL_KEYS: Final = {value: f"overrun.speed.{value}" for value in OVERRUN_SPEEDS}
INTENSITY_LABEL_KEYS: Final = {
    value: f"overrun.intensity.{value}" for value in OVERRUN_INTENSITIES
}

# Exact localized identifiers persisted by older versions.
_LEGACY_EFFECTS: Final = {
    "Без анимации": EFFECT_NONE,
    "Пульсация": EFFECT_PULSE,
    "Увеличение цифр": EFFECT_SCALE,
    "Сигнальные маячки": EFFECT_BEACONS,
    "Акцентная рамка": EFFECT_BORDER,
    "Волна-индикатор": EFFECT_WAVE,
}
_LEGACY_SCOPES: Final = {
    "Только цифры таймера": SCOPE_DIGITS,
    "Карточка таймера": SCOPE_CARD,
    "Цифры и карточка": SCOPE_BOTH,
}
_LEGACY_SPEEDS: Final = {
    "Медленно": SPEED_SLOW,
    "Обычно": SPEED_NORMAL,
    "Быстро": SPEED_FAST,
}
_LEGACY_INTENSITIES: Final = {
    "Слабо": INTENSITY_WEAK,
    "Средне": INTENSITY_MEDIUM,
    "Сильно": INTENSITY_STRONG,
}

OVERWORK_KEY: Final = "overwork"
SHORT_BREAK_OVERRUN_KEY: Final = "short_break_overrun"
LONG_BREAK_OVERRUN_KEY: Final = "long_break_overrun"
OVERRUN_COLOR_KEYS: Final = (
    OVERWORK_KEY,
    SHORT_BREAK_OVERRUN_KEY,
    LONG_BREAK_OVERRUN_KEY,
)

DEFAULT_EFFECT: Final = EFFECT_PULSE
DEFAULT_SCOPE: Final = SCOPE_BOTH
DEFAULT_SPEED: Final = SPEED_NORMAL
DEFAULT_INTENSITY: Final = INTENSITY_MEDIUM
FRAME_INTERVAL_MS: Final = 80

_SPEED_PERIODS: Final = {
    SPEED_SLOW: 2.8,
    SPEED_NORMAL: 1.9,
    SPEED_FAST: 1.2,
}
_INTENSITY_FACTORS: Final = {
    INTENSITY_WEAK: 0.24,
    INTENSITY_MEDIUM: 0.46,
    INTENSITY_STRONG: 0.68,
}
_CARD_FACTORS: Final = {
    INTENSITY_WEAK: 0.10,
    INTENSITY_MEDIUM: 0.18,
    INTENSITY_STRONG: 0.28,
}
_SCALE_FACTORS: Final = {
    INTENSITY_WEAK: 0.05,
    INTENSITY_MEDIUM: 0.10,
    INTENSITY_STRONG: 0.15,
}
_BORDER_WIDTHS: Final = {
    INTENSITY_WEAK: 1.0,
    INTENSITY_MEDIUM: 2.0,
    INTENSITY_STRONG: 3.0,
}


def default_overrun_visual() -> dict[str, object]:
    """Возвращает безопасные настройки; ``None`` у цвета означает «по теме»."""
    return {
        "effect": DEFAULT_EFFECT,
        "color_enabled": True,
        "scope": DEFAULT_SCOPE,
        "speed": DEFAULT_SPEED,
        "intensity": DEFAULT_INTENSITY,
        "animations_enabled": True,
        "opaque_widget_during_overrun": False,
        "colors": {key: None for key in OVERRUN_COLOR_KEYS},
    }


def normalize_overrun_visual(value: object) -> dict[str, object]:
    """Частично восстанавливает повреждённый раздел настроек эффекта."""
    defaults = default_overrun_visual()
    raw = value if isinstance(value, dict) else {}
    normalized = dict(defaults)
    raw_effect = raw.get("effect")
    legacy_effects = {
        LEGACY_EFFECT_NONE: (EFFECT_NONE, False),
        EFFECT_COLOR: (EFFECT_NONE, True),
        EFFECT_COLOR_PULSE: (EFFECT_PULSE, True),
    }
    migrated_effect = _LEGACY_EFFECTS.get(raw_effect, raw_effect)
    if migrated_effect in OVERRUN_EFFECTS:
        normalized["effect"] = migrated_effect
        legacy_color_default = defaults["color_enabled"]
    elif raw_effect in legacy_effects:
        normalized["effect"], legacy_color_default = legacy_effects[raw_effect]
    else:
        normalized["effect"] = defaults["effect"]
        legacy_color_default = defaults["color_enabled"]

    for key, allowed, legacy in (
        ("scope", OVERRUN_SCOPES, _LEGACY_SCOPES),
        ("speed", OVERRUN_SPEEDS, _LEGACY_SPEEDS),
        ("intensity", OVERRUN_INTENSITIES, _LEGACY_INTENSITIES),
    ):
        raw_candidate = raw.get(key)
        candidate = legacy.get(raw_candidate, raw_candidate)
        normalized[key] = candidate if candidate in allowed else defaults[key]
    for key, default in (
        ("color_enabled", legacy_color_default),
        ("animations_enabled", defaults["animations_enabled"]),
        ("opaque_widget_during_overrun", defaults["opaque_widget_during_overrun"]),
    ):
        candidate = raw.get(key, default)
        normalized[key] = candidate if isinstance(candidate, bool) else default
    raw_colors = raw.get("colors") if isinstance(raw.get("colors"), dict) else {}
    normalized["colors"] = {
        key: str(raw_colors[key]).strip().upper()
        if is_hex_color(raw_colors.get(key))
        else None
        for key in OVERRUN_COLOR_KEYS
    }
    return normalized


def overrun_key(mode: TimerMode) -> str:
    """Возвращает ключ отдельного цвета для завершившегося периода."""
    if mode == TimerMode.SHORT_BREAK:
        return SHORT_BREAK_OVERRUN_KEY
    if mode == TimerMode.LONG_BREAK:
        return LONG_BREAK_OVERRUN_KEY
    return OVERWORK_KEY


def resolved_overrun_color(
    visual: object,
    palette: ThemePalette,
    mode: TimerMode,
) -> str:
    """Выбирает пользовательское переопределение или цвет активной темы."""
    settings = normalize_overrun_visual(visual)
    override = settings["colors"][overrun_key(mode)]
    return override or mode_color(palette, mode, waiting_for_continue=True)


def interpolate_color(first: str, second: str, amount: float) -> str:
    """Линейно смешивает два цвета #RRGGBB с ограниченным коэффициентом."""
    factor = min(1.0, max(0.0, float(amount)))
    channels = []
    for offset in (1, 3, 5):
        start = int(first[offset : offset + 2], 16)
        finish = int(second[offset : offset + 2], 16)
        channels.append(round(start + (finish - start) * factor))
    return "#" + "".join(f"{channel:02X}" for channel in channels)


def pulse_phase(elapsed_seconds: float, speed: object) -> float:
    """Возвращает мягкую косинусную фазу 0..1 для монотонного времени."""
    normalized_speed = speed if speed in OVERRUN_SPEEDS else DEFAULT_SPEED
    period = _SPEED_PERIODS[normalized_speed]
    elapsed = max(0.0, float(elapsed_seconds))
    return (1.0 - cos(2.0 * pi * (elapsed % period) / period)) / 2.0


def cycle_phase(elapsed_seconds: float, speed: object) -> float:
    """Возвращает линейную фазу 0..1 для спокойного движения волны."""
    normalized_speed = speed if speed in OVERRUN_SPEEDS else DEFAULT_SPEED
    period = _SPEED_PERIODS[normalized_speed]
    elapsed = max(0.0, float(elapsed_seconds))
    return (elapsed % period) / period


@dataclass(frozen=True)
class OverrunVisualFrame:
    """Один общий кадр для главного окна и открытого виджета."""

    active: bool
    mode: TimerMode | None = None
    digits_color: str | None = None
    card_background: str | None = None
    phase: float = 0.0
    preview: bool = False
    effect: str = EFFECT_NONE
    effect_color: str | None = None
    digit_scale: float = 1.0
    beacon_level: float = 0.0
    border_color: str | None = None
    border_width: float = 0.0
    wave_position: float | None = None


INACTIVE_FRAME: Final = OverrunVisualFrame(active=False)


def calculate_overrun_frame(
    palette: ThemePalette,
    mode: TimerMode,
    visual: object,
    elapsed_seconds: float,
) -> OverrunVisualFrame:
    """Рассчитывает кадр без обращения к GUI, таймеру и статистике."""
    settings = normalize_overrun_visual(visual)
    effect = settings["effect"]
    scope = settings["scope"]
    intensity = settings["intensity"]
    animations_enabled = bool(settings["animations_enabled"])
    animated = effect != EFFECT_NONE and animations_enabled
    phase = pulse_phase(elapsed_seconds, settings["speed"]) if animated else 0.5
    state_color = resolved_overrun_color(settings, palette, mode)
    color_enabled = bool(settings["color_enabled"])

    digit_amount = 1.0
    card_amount = _CARD_FACTORS[intensity]
    if effect == EFFECT_PULSE and animated:
        if color_enabled:
            digit_amount = 1.0 - ((1.0 - phase) * _INTENSITY_FACTORS[intensity] * 0.55)
            card_amount *= 0.55 + (0.45 * phase)
        else:
            digit_amount = phase * _INTENSITY_FACTORS[intensity]
            card_amount = phase * _CARD_FACTORS[intensity]

    digits_color = None
    if scope in {SCOPE_DIGITS, SCOPE_BOTH} and (color_enabled or effect == EFFECT_PULSE):
        digits_color = interpolate_color(palette.text_primary, state_color, digit_amount)

    card_background = None
    if scope in {SCOPE_CARD, SCOPE_BOTH} and (color_enabled or effect == EFFECT_PULSE):
        card_background = interpolate_color(
            palette.card_background,
            state_color,
            card_amount,
        )

    digit_scale = 1.0
    if effect == EFFECT_SCALE and animated:
        digit_scale += _SCALE_FACTORS[intensity] * phase

    beacon_level = 0.0
    if effect == EFFECT_BEACONS:
        beacon_level = 0.35 + (0.65 * phase) if animated else 0.72

    border_color = None
    border_width = 0.0
    if effect == EFFECT_BORDER:
        border_amount = 0.45 + (0.55 * phase) if animated else 0.72
        border_color = interpolate_color(palette.border, state_color, border_amount)
        border_width = _BORDER_WIDTHS[intensity]

    wave_position = None
    if effect == EFFECT_WAVE:
        wave_position = (
            cycle_phase(elapsed_seconds, settings["speed"])
            if animated
            else 0.5
        )

    return OverrunVisualFrame(
        active=True,
        mode=mode,
        digits_color=digits_color,
        card_background=card_background,
        phase=phase,
        effect=effect,
        effect_color=state_color,
        digit_scale=digit_scale,
        beacon_level=beacon_level,
        border_color=border_color,
        border_width=border_width,
        wave_position=wave_position,
    )


def visual_uses_animation(visual: object) -> bool:
    """Определяет, нужен ли периодический callback для фактического эффекта."""
    settings = normalize_overrun_visual(visual)
    return bool(settings["animations_enabled"]) and settings["effect"] != EFFECT_NONE


class OverrunVisualController:
    """Поддерживает один callback и общую фазу для всех UI-представлений."""

    def __init__(
        self,
        schedule: Callable[[int, Callable[[], None]], object],
        cancel: Callable[[object], None],
        on_frame: Callable[[OverrunVisualFrame], None],
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._schedule = schedule
        self._cancel = cancel
        self._on_frame = on_frame
        self._clock = clock
        self._after_id: object | None = None
        self._started_at = self._clock()
        self._active = False
        self._mode: TimerMode | None = None
        self._visual = default_overrun_visual()
        self._palette: ThemePalette | None = None
        self._preview_until: float | None = None
        self._actual: tuple[bool, TimerMode | None, object, ThemePalette] | None = None

    @property
    def has_scheduled_frame(self) -> bool:
        """Доступный тестам признак единственного запланированного callback."""
        return self._after_id is not None

    @property
    def preview_active(self) -> bool:
        return self._preview_until is not None

    def sync_actual(
        self,
        active: bool,
        mode: TimerMode | None,
        visual: object,
        palette: ThemePalette,
    ) -> None:
        """Синхронизирует реальное состояние, не прерывая короткий предпросмотр."""
        self._actual = (bool(active), mode, visual, palette)
        if self.preview_active:
            if self._palette != palette and self._mode is not None:
                self._activate(True, self._mode, self._visual, palette)
            return
        self._activate(bool(active), mode, visual, palette)

    def start_preview(
        self,
        mode: TimerMode,
        visual: object,
        palette: ThemePalette,
        duration_seconds: float = 4.0,
    ) -> None:
        """Показывает фиктивное состояние, не касаясь TimerEngine и статистики."""
        self._preview_until = self._clock() + max(0.1, float(duration_seconds))
        self._activate(True, mode, visual, palette, restart_phase=True)

    def stop_preview(self) -> None:
        """Немедленно завершает предпросмотр и возвращает фактическое состояние."""
        if not self.preview_active:
            return
        self._preview_until = None
        self._restore_actual()

    def stop(self) -> None:
        """Отменяет callback при выходе и полностью восстанавливает обычные цвета."""
        self._preview_until = None
        self._actual = None
        self._cancel_scheduled()
        self._active = False
        self._mode = None
        self._palette = None
        self._on_frame(INACTIVE_FRAME)

    def _activate(
        self,
        active: bool,
        mode: TimerMode | None,
        visual: object,
        palette: ThemePalette,
        *,
        restart_phase: bool = False,
    ) -> None:
        normalized_visual = normalize_overrun_visual(visual)
        was_same_state = self._active and self._mode == mode
        same_configuration = (
            self._active == bool(active and mode is not None)
            and self._mode == (mode if active and mode is not None else None)
            and self._visual == normalized_visual
            and self._palette == palette
        )
        if same_configuration and not restart_phase:
            return
        self._active = bool(active and mode is not None)
        self._mode = mode if self._active else None
        self._visual = normalized_visual
        self._palette = palette
        if restart_phase or not was_same_state:
            self._started_at = self._clock()
        self._cancel_scheduled()
        if not self._active:
            self._on_frame(INACTIVE_FRAME)
            return
        self._emit_frame()
        self._schedule_next()

    def _emit_frame(self) -> None:
        if not self._active or self._mode is None or self._palette is None:
            self._on_frame(INACTIVE_FRAME)
            return
        frame = calculate_overrun_frame(
            self._palette,
            self._mode,
            self._visual,
            self._clock() - self._started_at,
        )
        if self.preview_active:
            frame = replace(frame, preview=True)
        self._on_frame(frame)

    def _schedule_next(self) -> None:
        if not self._active or self._after_id is not None:
            return
        if self.preview_active:
            delay = FRAME_INTERVAL_MS if visual_uses_animation(self._visual) else max(
                1,
                round((self._preview_until - self._clock()) * 1000),
            )
            self._after_id = self._schedule(delay, self._tick)
        elif visual_uses_animation(self._visual):
            self._after_id = self._schedule(FRAME_INTERVAL_MS, self._tick)

    def _tick(self) -> None:
        self._after_id = None
        if self.preview_active and self._clock() >= self._preview_until:
            self._preview_until = None
            self._restore_actual()
            return
        self._emit_frame()
        self._schedule_next()

    def _restore_actual(self) -> None:
        if self._actual is None:
            self._cancel_scheduled()
            self._active = False
            self._mode = None
            self._on_frame(INACTIVE_FRAME)
            return
        active, mode, visual, palette = self._actual
        self._activate(active, mode, visual, palette, restart_phase=True)

    def _cancel_scheduled(self) -> None:
        after_id = self._after_id
        self._after_id = None
        if after_id is None:
            return
        try:
            self._cancel(after_id)
        except Exception:
            # GUI может уже уничтожать планировщик; состояние очищено локально.
            pass
