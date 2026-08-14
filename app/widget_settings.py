"""Константы и чистая нормализация настроек плавающего виджета."""

from copy import deepcopy
from dataclasses import dataclass
from typing import Any


WIDGET_TYPE_MINIMAL = "Минималистичный"
WIDGET_TYPE_COMPACT = "Компактный"
WIDGET_TYPE_EXPANDED = "Расширенный"
WIDGET_TYPE_MICRO = "Микро"
WIDGET_TYPE_ROW = "Строка"
WIDGET_TYPE_RING = "Кольцо"
WIDGET_TYPE_SCOREBOARD = "Табло"
WIDGET_TYPES = (
    WIDGET_TYPE_MINIMAL,
    WIDGET_TYPE_COMPACT,
    WIDGET_TYPE_EXPANDED,
    WIDGET_TYPE_MICRO,
    WIDGET_TYPE_ROW,
    WIDGET_TYPE_RING,
    WIDGET_TYPE_SCOREBOARD,
)

WIDGET_TYPE_DESCRIPTIONS = {
    WIDGET_TYPE_MINIMAL: "Крупное время, название состояния и минимум деталей.",
    WIDGET_TYPE_COMPACT: "Классическая компактная карточка с основной кнопкой.",
    WIDGET_TYPE_EXPANDED: "Цикл и полный набор основных команд таймера.",
    WIDGET_TYPE_MICRO: "Самое маленькое окно: обычно только время.",
    WIDGET_TYPE_ROW: "Горизонтальная строка для края экрана.",
    WIDGET_TYPE_RING: "Время внутри кольцевого индикатора периода.",
    WIDGET_TYPE_SCOREBOARD: "Крупные моноширинные цифры в стиле спокойного табло.",
}

WIDGET_SIZE_SMALL = "Маленький"
WIDGET_SIZE_MEDIUM = "Средний"
WIDGET_SIZE_LARGE = "Большой"
WIDGET_SIZE_CUSTOM = "Пользовательский"
WIDGET_SIZES = (
    WIDGET_SIZE_SMALL,
    WIDGET_SIZE_MEDIUM,
    WIDGET_SIZE_LARGE,
    WIDGET_SIZE_CUSTOM,
)

DEFAULT_WIDGET_TYPE = WIDGET_TYPE_COMPACT
DEFAULT_WIDGET_SIZE = WIDGET_SIZE_SMALL
DEFAULT_WIDGET_X = 100
DEFAULT_WIDGET_Y = 100
MIN_WIDGET_OPACITY = 5


@dataclass(frozen=True)
class WidgetSizeParameters:
    """Размер окна и шрифтов для одного варианта виджета."""

    width: int
    height: int
    time_font: int
    mode_font: int
    button_font: int


WIDGET_SIZE_PRESETS: dict[str, dict[str, WidgetSizeParameters]] = {
    WIDGET_TYPE_MINIMAL: {
        WIDGET_SIZE_SMALL: WidgetSizeParameters(200, 110, 28, 9, 9),
        WIDGET_SIZE_MEDIUM: WidgetSizeParameters(260, 140, 38, 10, 10),
        WIDGET_SIZE_LARGE: WidgetSizeParameters(340, 180, 52, 12, 11),
    },
    WIDGET_TYPE_COMPACT: {
        WIDGET_SIZE_SMALL: WidgetSizeParameters(240, 145, 26, 10, 9),
        WIDGET_SIZE_MEDIUM: WidgetSizeParameters(310, 180, 36, 11, 10),
        WIDGET_SIZE_LARGE: WidgetSizeParameters(400, 230, 48, 13, 11),
    },
    WIDGET_TYPE_EXPANDED: {
        WIDGET_SIZE_SMALL: WidgetSizeParameters(400, 245, 30, 10, 9),
        WIDGET_SIZE_MEDIUM: WidgetSizeParameters(440, 280, 44, 12, 10),
        WIDGET_SIZE_LARGE: WidgetSizeParameters(560, 350, 58, 14, 12),
    },
    WIDGET_TYPE_MICRO: {
        WIDGET_SIZE_SMALL: WidgetSizeParameters(170, 96, 24, 8, 8),
        WIDGET_SIZE_MEDIUM: WidgetSizeParameters(220, 122, 32, 9, 9),
        WIDGET_SIZE_LARGE: WidgetSizeParameters(285, 158, 42, 10, 10),
    },
    WIDGET_TYPE_ROW: {
        WIDGET_SIZE_SMALL: WidgetSizeParameters(360, 100, 24, 9, 8),
        WIDGET_SIZE_MEDIUM: WidgetSizeParameters(460, 126, 34, 10, 9),
        WIDGET_SIZE_LARGE: WidgetSizeParameters(590, 158, 46, 12, 10),
    },
    WIDGET_TYPE_RING: {
        WIDGET_SIZE_SMALL: WidgetSizeParameters(220, 250, 24, 9, 8),
        WIDGET_SIZE_MEDIUM: WidgetSizeParameters(290, 325, 34, 10, 9),
        WIDGET_SIZE_LARGE: WidgetSizeParameters(380, 420, 46, 12, 10),
    },
    WIDGET_TYPE_SCOREBOARD: {
        WIDGET_SIZE_SMALL: WidgetSizeParameters(300, 145, 34, 9, 8),
        WIDGET_SIZE_MEDIUM: WidgetSizeParameters(405, 190, 48, 10, 9),
        WIDGET_SIZE_LARGE: WidgetSizeParameters(525, 240, 64, 12, 10),
    },
}

WIDGET_MIN_SIZES: dict[str, tuple[int, int]] = {
    WIDGET_TYPE_MINIMAL: (180, 100),
    WIDGET_TYPE_COMPACT: (230, 135),
    WIDGET_TYPE_EXPANDED: (330, 245),
    WIDGET_TYPE_MICRO: (160, 88),
    WIDGET_TYPE_ROW: (340, 90),
    WIDGET_TYPE_RING: (205, 230),
    WIDGET_TYPE_SCOREBOARD: (280, 130),
}


def normalize_widget_opacity(value: Any, default: int = 100) -> int:
    """Ограничивает постоянную непрозрачность диапазоном 5–100 процентов."""
    return _bounded_int(value, default, MIN_WIDGET_OPACITY, 100)


def effective_widget_alpha(
    opacity: Any,
    opaque_during_overrun: bool,
    overrun_active: bool,
) -> float:
    """Возвращает системный alpha без изменения постоянной настройки."""
    if opaque_during_overrun and overrun_active:
        return 1.0
    return normalize_widget_opacity(opacity) / 100.0


def normalize_widget_type(value: Any) -> str:
    """Возвращает поддерживаемый тип или совместимый компактный вариант."""
    text = str(value or "").strip()
    return text if text in WIDGET_TYPES else DEFAULT_WIDGET_TYPE


def normalize_widget_size(value: Any, default: str = DEFAULT_WIDGET_SIZE) -> str:
    """Возвращает поддерживаемый размер или безопасное значение по умолчанию."""
    text = str(value or "").strip()
    return text if text in WIDGET_SIZES else default


def widget_size_parameters(
    widget_type: str,
    widget_size: str,
    width: Any | None = None,
    height: Any | None = None,
) -> WidgetSizeParameters:
    """Возвращает параметры пресета или масштабирует шрифты для ручного размера."""
    normalized_type = normalize_widget_type(widget_type)
    normalized_size = normalize_widget_size(widget_size)
    if normalized_size != WIDGET_SIZE_CUSTOM:
        return WIDGET_SIZE_PRESETS[normalized_type][normalized_size]

    minimum_width, minimum_height = WIDGET_MIN_SIZES[normalized_type]
    custom_width = _bounded_int(width, minimum_width, minimum_width, 2400)
    custom_height = _bounded_int(height, minimum_height, minimum_height, 1600)
    medium = WIDGET_SIZE_PRESETS[normalized_type][WIDGET_SIZE_MEDIUM]
    scale = min(custom_width / medium.width, custom_height / medium.height)
    scale = min(1.8, max(0.75, scale))
    return WidgetSizeParameters(
        width=custom_width,
        height=custom_height,
        time_font=max(18, round(medium.time_font * scale)),
        mode_font=max(8, round(medium.mode_font * scale)),
        button_font=max(8, round(medium.button_font * scale)),
    )


def default_widget_layouts() -> dict[str, dict[str, int | str]]:
    """Создает независимые начальные геометрии для всех типов."""
    layouts: dict[str, dict[str, int | str]] = {}
    for widget_type in WIDGET_TYPES:
        parameters = widget_size_parameters(widget_type, DEFAULT_WIDGET_SIZE)
        layouts[widget_type] = {
            "size": DEFAULT_WIDGET_SIZE,
            "width": parameters.width,
            "height": parameters.height,
            "x": DEFAULT_WIDGET_X,
            "y": DEFAULT_WIDGET_Y,
        }
    return layouts


def normalize_widget_layouts(
    value: Any,
    *,
    legacy_x: Any = DEFAULT_WIDGET_X,
    legacy_y: Any = DEFAULT_WIDGET_Y,
    active_type: str = DEFAULT_WIDGET_TYPE,
) -> dict[str, dict[str, int | str]]:
    """Мигрирует и проверяет отдельную геометрию каждого типа."""
    layouts = default_widget_layouts()
    raw_layouts = value if isinstance(value, dict) else {}
    normalized_active_type = normalize_widget_type(active_type)

    for widget_type in WIDGET_TYPES:
        raw_layout = raw_layouts.get(widget_type, {})
        if not isinstance(raw_layout, dict):
            raw_layout = {}

        size = normalize_widget_size(raw_layout.get("size"))
        parameters = widget_size_parameters(
            widget_type,
            size,
            raw_layout.get("width"),
            raw_layout.get("height"),
        )
        default_layout = layouts[widget_type]
        layouts[widget_type] = {
            "size": size,
            "width": parameters.width,
            "height": parameters.height,
            "x": _safe_coordinate(raw_layout.get("x"), int(default_layout["x"])),
            "y": _safe_coordinate(raw_layout.get("y"), int(default_layout["y"])),
        }

    if not raw_layouts:
        # Старый формат имел только одну пару координат и соответствовал
        # компактному виджету. Другие типы получают независимые defaults.
        layouts[normalized_active_type]["x"] = _safe_coordinate(
            legacy_x,
            DEFAULT_WIDGET_X,
        )
        layouts[normalized_active_type]["y"] = _safe_coordinate(
            legacy_y,
            DEFAULT_WIDGET_Y,
        )

    return layouts


def set_widget_layout_size(
    layouts: dict[str, dict[str, int | str]],
    widget_type: str,
    widget_size: str,
) -> dict[str, dict[str, int | str]]:
    """Возвращает копию геометрий с выбранным размером активного типа."""
    normalized_type = normalize_widget_type(widget_type)
    normalized_size = normalize_widget_size(widget_size)
    result = deepcopy(layouts)
    layout = result.setdefault(
        normalized_type,
        default_widget_layouts()[normalized_type],
    )
    parameters = widget_size_parameters(
        normalized_type,
        normalized_size,
        layout.get("width"),
        layout.get("height"),
    )
    layout.update(
        {
            "size": normalized_size,
            "width": parameters.width,
            "height": parameters.height,
        },
    )
    return result


def clamp_window_position(
    x: int,
    y: int,
    width: int,
    height: int,
    screen_bounds: tuple[int, int, int, int],
    visible_pixels: int = 48,
) -> tuple[int, int]:
    """Оставляет заметную часть окна внутри доступной области экрана."""
    screen_x, screen_y, screen_width, screen_height = screen_bounds
    if screen_width <= 0 or screen_height <= 0:
        return DEFAULT_WIDGET_X, DEFAULT_WIDGET_Y

    visible_x = min(max(1, visible_pixels), width, screen_width)
    visible_y = min(max(1, visible_pixels), height, screen_height)
    minimum_x = screen_x - width + visible_x
    maximum_x = screen_x + screen_width - visible_x
    minimum_y = screen_y - height + visible_y
    maximum_y = screen_y + screen_height - visible_y
    return (
        min(maximum_x, max(minimum_x, x)),
        min(maximum_y, max(minimum_y, y)),
    )


def content_fitted_dimensions(
    width: int,
    height: int,
    required_width: int,
    required_height: int,
    minimum_width: int,
    minimum_height: int,
) -> tuple[int, int]:
    """Расширяет клиентскую область, если DPI или длинный текст требуют больше места."""
    return (
        max(1, int(width), int(required_width), int(minimum_width)),
        max(1, int(height), int(required_height), int(minimum_height)),
    )


def _safe_coordinate(value: Any, default: int) -> int:
    """Ограничивает координату разумным диапазоном до проверки экрана."""
    try:
        return min(100_000, max(-100_000, int(value)))
    except (TypeError, ValueError):
        return default


def _bounded_int(value: Any, default: int, minimum: int, maximum: int) -> int:
    """Преобразует значение в целое число заданного диапазона."""
    try:
        return min(maximum, max(minimum, int(value)))
    except (TypeError, ValueError):
        return default
