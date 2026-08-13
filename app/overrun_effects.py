"""Чистый расчёт и единый планировщик визуальной индикации превышения."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, replace
from math import cos, pi
import time
from typing import Final

from app.models import TimerMode
from app.theme import ThemePalette, is_hex_color, mode_color


EFFECT_NONE: Final = "Без дополнительного эффекта"
EFFECT_COLOR: Final = "Изменение цвета"
EFFECT_PULSE: Final = "Пульсация"
EFFECT_COLOR_PULSE: Final = "Цвет и пульсация"
OVERRUN_EFFECTS: Final = (
    EFFECT_NONE,
    EFFECT_COLOR,
    EFFECT_PULSE,
    EFFECT_COLOR_PULSE,
)

SCOPE_DIGITS: Final = "Только цифры таймера"
SCOPE_CARD: Final = "Карточка таймера"
SCOPE_BOTH: Final = "Цифры и карточка"
OVERRUN_SCOPES: Final = (SCOPE_DIGITS, SCOPE_CARD, SCOPE_BOTH)

SPEED_SLOW: Final = "Медленно"
SPEED_NORMAL: Final = "Обычно"
SPEED_FAST: Final = "Быстро"
OVERRUN_SPEEDS: Final = (SPEED_SLOW, SPEED_NORMAL, SPEED_FAST)

INTENSITY_WEAK: Final = "Слабо"
INTENSITY_MEDIUM: Final = "Средне"
INTENSITY_STRONG: Final = "Сильно"
OVERRUN_INTENSITIES: Final = (
    INTENSITY_WEAK,
    INTENSITY_MEDIUM,
    INTENSITY_STRONG,
)

OVERWORK_KEY: Final = "overwork"
SHORT_BREAK_OVERRUN_KEY: Final = "short_break_overrun"
LONG_BREAK_OVERRUN_KEY: Final = "long_break_overrun"
OVERRUN_COLOR_KEYS: Final = (
    OVERWORK_KEY,
    SHORT_BREAK_OVERRUN_KEY,
    LONG_BREAK_OVERRUN_KEY,
)

DEFAULT_EFFECT: Final = EFFECT_COLOR_PULSE
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


def default_overrun_visual() -> dict[str, object]:
    """Возвращает безопасные настройки; ``None`` у цвета означает «по теме»."""
    return {
        "effect": DEFAULT_EFFECT,
        "scope": DEFAULT_SCOPE,
        "speed": DEFAULT_SPEED,
        "intensity": DEFAULT_INTENSITY,
        "animations_enabled": True,
        "colors": {key: None for key in OVERRUN_COLOR_KEYS},
    }


def normalize_overrun_visual(value: object) -> dict[str, object]:
    """Частично восстанавливает повреждённый раздел настроек эффекта."""
    defaults = default_overrun_visual()
    raw = value if isinstance(value, dict) else {}
    normalized = dict(defaults)
    for key, allowed in (
        ("effect", OVERRUN_EFFECTS),
        ("scope", OVERRUN_SCOPES),
        ("speed", OVERRUN_SPEEDS),
        ("intensity", OVERRUN_INTENSITIES),
    ):
        candidate = raw.get(key)
        normalized[key] = candidate if candidate in allowed else defaults[key]
    animation_value = raw.get(
        "animations_enabled",
        defaults["animations_enabled"],
    )
    normalized["animations_enabled"] = (
        animation_value
        if isinstance(animation_value, bool)
        else defaults["animations_enabled"]
    )
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


@dataclass(frozen=True)
class OverrunVisualFrame:
    """Один общий кадр для главного окна и открытого виджета."""

    active: bool
    mode: TimerMode | None = None
    digits_color: str | None = None
    card_background: str | None = None
    phase: float = 0.0
    preview: bool = False


INACTIVE_FRAME: Final = OverrunVisualFrame(active=False)


def calculate_overrun_frame(
    palette: ThemePalette,
    mode: TimerMode,
    visual: object,
    elapsed_seconds: float,
) -> OverrunVisualFrame:
    """Рассчитывает кадр без обращения к Tkinter, таймеру и статистике."""
    settings = normalize_overrun_visual(visual)
    effect = settings["effect"]
    if effect == EFFECT_NONE:
        return OverrunVisualFrame(active=True, mode=mode)

    scope = settings["scope"]
    intensity = settings["intensity"]
    animations_enabled = bool(settings["animations_enabled"])
    has_pulse = effect in {EFFECT_PULSE, EFFECT_COLOR_PULSE} and animations_enabled
    phase = pulse_phase(elapsed_seconds, settings["speed"]) if has_pulse else 1.0
    state_color = resolved_overrun_color(settings, palette, mode)

    if effect == EFFECT_PULSE and has_pulse:
        digit_amount = phase * _INTENSITY_FACTORS[intensity]
        card_amount = phase * _CARD_FACTORS[intensity]
    elif effect == EFFECT_COLOR_PULSE and has_pulse:
        # Цвет состояния остается основой, а мягкая фаза слегка возвращает его
        # к обычному цвету — знак и название состояния при этом не меняются.
        digit_amount = 1.0 - ((1.0 - phase) * _INTENSITY_FACTORS[intensity] * 0.55)
        card_amount = _CARD_FACTORS[intensity] * (0.55 + 0.45 * phase)
    else:
        # При отключении движения пульсирующие варианты становятся статическими.
        digit_amount = 1.0
        card_amount = _CARD_FACTORS[intensity]

    digits_color = None
    if scope in {SCOPE_DIGITS, SCOPE_BOTH}:
        digits_color = interpolate_color(palette.text_primary, state_color, digit_amount)

    card_background = None
    if scope in {SCOPE_CARD, SCOPE_BOTH}:
        card_background = interpolate_color(
            palette.card_background,
            state_color,
            card_amount,
        )

    return OverrunVisualFrame(
        active=True,
        mode=mode,
        digits_color=digits_color,
        card_background=card_background,
        phase=phase,
    )


def visual_uses_animation(visual: object) -> bool:
    """Определяет, нужен ли периодический callback для фактического эффекта."""
    settings = normalize_overrun_visual(visual)
    return bool(settings["animations_enabled"]) and settings["effect"] in {
        EFFECT_PULSE,
        EFFECT_COLOR_PULSE,
    }


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
            # Tk может уже уничтожать окно; состояние всё равно очищено локально.
            pass
