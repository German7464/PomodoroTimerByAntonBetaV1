"""Функции для чтения и записи локальных JSON-файлов."""

import json
from pathlib import Path
from typing import Any

from app.config import (
    DEFAULT_AUTO_START_NEXT_PERIOD,
    DEFAULT_CYCLES_BEFORE_LONG_BREAK,
    DEFAULT_LONG_BREAK_MINUTES,
    DEFAULT_MINIMIZE_TO_TRAY_ON_START,
    DEFAULT_PROFILE_NAME,
    DEFAULT_SHORT_BREAK_MINUTES,
    DEFAULT_TIME_DISPLAY_FORMAT,
    DEFAULT_USE_LONG_BREAK,
    DEFAULT_WORK_MINUTES,
)
from app.models import AppSettings, TimeDisplayFormat
from app.overrun_effects import default_overrun_visual, normalize_overrun_visual
from app.theme import (
    DEFAULT_APPEARANCE_MODE,
    DEFAULT_THEME_NAME,
    default_custom_theme,
    normalize_custom_theme,
    normalize_appearance_mode,
    normalize_theme_name,
)
from app.widget_settings import (
    DEFAULT_WIDGET_SIZE,
    DEFAULT_WIDGET_TYPE,
    MIN_WIDGET_OPACITY,
    normalize_widget_layouts,
    normalize_widget_size,
    normalize_widget_type,
    set_widget_layout_size,
)


def load_json(path: Path, default: Any) -> Any:
    """Загружает JSON или возвращает значение по умолчанию, если файла нет."""
    if not path.exists():
        return default

    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return default


def save_json(path: Path, data: Any) -> None:
    """Сохраняет данные в JSON с читаемым форматированием."""
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def default_settings_data() -> dict[str, Any]:
    """Возвращает настройки по умолчанию в формате для JSON."""
    return {
        "active_profile": DEFAULT_PROFILE_NAME,
        "work_minutes": DEFAULT_WORK_MINUTES,
        "short_break_minutes": DEFAULT_SHORT_BREAK_MINUTES,
        "long_break_minutes": DEFAULT_LONG_BREAK_MINUTES,
        "notifications_enabled": True,
        "notification_sound_enabled": True,
        "work_end_message": "Рабочий период завершен. Время отдохнуть.",
        "short_break_end_message": "Короткий отдых завершен. Пора вернуться к работе.",
        "long_break_end_message": "Длинный отдых завершен. Пора начать новый рабочий период.",
        "autostart_enabled": False,
        "use_long_break": DEFAULT_USE_LONG_BREAK,
        "long_break_interval": DEFAULT_CYCLES_BEFORE_LONG_BREAK,
        "auto_start_next_period": DEFAULT_AUTO_START_NEXT_PERIOD,
        "time_display_format": DEFAULT_TIME_DISPLAY_FORMAT,
        "minimize_to_tray_on_start": DEFAULT_MINIMIZE_TO_TRAY_ON_START,
        "close_to_tray": True,
        "theme_name": DEFAULT_THEME_NAME,
        "appearance_mode": DEFAULT_APPEARANCE_MODE,
        "custom_theme": default_custom_theme(),
        "overrun_visual": default_overrun_visual(),
        "widget_enabled": False,
        "widget_type": DEFAULT_WIDGET_TYPE,
        "widget_size": DEFAULT_WIDGET_SIZE,
        "widget_layouts": normalize_widget_layouts(None),
        "widget_background_color": "#202124",
        "widget_text_color": "#ffffff",
        "widget_opacity": 100,
        "widget_always_on_top": True,
        "widget_x": 100,
        "widget_y": 100,
    }


def normalize_settings_data(raw_data: Any) -> dict[str, Any]:
    """Дополняет старые настройки новыми полями и исправляет опасные значения."""
    defaults = default_settings_data()
    if not isinstance(raw_data, dict):
        return defaults

    settings = defaults | raw_data
    settings["use_long_break"] = bool(settings["use_long_break"])
    settings["notifications_enabled"] = bool(settings["notifications_enabled"])
    settings["notification_sound_enabled"] = bool(settings["notification_sound_enabled"])
    settings["auto_start_next_period"] = bool(settings["auto_start_next_period"])
    settings["minimize_to_tray_on_start"] = bool(settings["minimize_to_tray_on_start"])
    settings["close_to_tray"] = bool(settings["close_to_tray"])
    settings["theme_name"] = normalize_theme_name(settings.get("theme_name"))
    settings["appearance_mode"] = normalize_appearance_mode(
        settings.get("appearance_mode"),
    )
    settings["custom_theme"] = normalize_custom_theme(settings.get("custom_theme"))
    settings["overrun_visual"] = normalize_overrun_visual(
        settings.get("overrun_visual"),
    )
    settings["widget_enabled"] = bool(settings["widget_enabled"])
    settings["widget_always_on_top"] = bool(settings["widget_always_on_top"])
    settings["widget_type"] = normalize_widget_type(settings.get("widget_type"))
    raw_layouts = raw_data.get("widget_layouts")
    settings["widget_layouts"] = normalize_widget_layouts(
        raw_layouts,
        legacy_x=raw_data.get("widget_x", 100),
        legacy_y=raw_data.get("widget_y", 100),
        active_type=settings["widget_type"],
    )
    active_layout = settings["widget_layouts"][settings["widget_type"]]
    if "widget_size" in raw_data:
        settings["widget_size"] = normalize_widget_size(raw_data.get("widget_size"))
    else:
        settings["widget_size"] = normalize_widget_size(active_layout.get("size"))
    settings["widget_layouts"] = set_widget_layout_size(
        settings["widget_layouts"],
        settings["widget_type"],
        settings["widget_size"],
    )
    active_layout = settings["widget_layouts"][settings["widget_type"]]
    settings["widget_background_color"] = _safe_color(settings["widget_background_color"], "#202124")
    settings["widget_text_color"] = _safe_color(settings["widget_text_color"], "#ffffff")

    for key, default_value in (
        ("work_end_message", "Рабочий период завершен. Время отдохнуть."),
        ("short_break_end_message", "Короткий отдых завершен. Пора вернуться к работе."),
        ("long_break_end_message", "Длинный отдых завершен. Пора начать новый рабочий период."),
    ):
        message = str(settings.get(key, "")).strip()
        settings[key] = message or default_value

    try:
        settings["widget_opacity"] = min(
            100,
            max(MIN_WIDGET_OPACITY, int(settings["widget_opacity"])),
        )
    except (TypeError, ValueError):
        settings["widget_opacity"] = 100

    # Эти поля оставлены для обратной совместимости со старыми версиями.
    settings["widget_x"] = int(active_layout["x"])
    settings["widget_y"] = int(active_layout["y"])

    for key, default_value in (
        ("work_minutes", DEFAULT_WORK_MINUTES),
        ("short_break_minutes", DEFAULT_SHORT_BREAK_MINUTES),
        ("long_break_minutes", DEFAULT_LONG_BREAK_MINUTES),
    ):
        try:
            settings[key] = max(1, int(settings[key]))
        except (TypeError, ValueError):
            settings[key] = default_value

    try:
        settings["long_break_interval"] = max(1, int(settings["long_break_interval"]))
    except (TypeError, ValueError):
        settings["long_break_interval"] = DEFAULT_CYCLES_BEFORE_LONG_BREAK

    allowed_formats = {format_item.value for format_item in TimeDisplayFormat}
    if settings["time_display_format"] not in allowed_formats:
        settings["time_display_format"] = DEFAULT_TIME_DISPLAY_FORMAT

    return settings


def load_app_settings(path: Path) -> AppSettings:
    """Загружает настройки приложения и мягко мигрирует старый формат."""
    path_existed = path.exists()
    raw_data = load_json(path, default_settings_data())
    settings_data = normalize_settings_data(raw_data)
    if not path_existed or raw_data != settings_data:
        save_json(path, settings_data)
    known_settings = {
        key: value
        for key, value in settings_data.items()
        if key in AppSettings.__dataclass_fields__
    }
    return AppSettings(**known_settings)


def save_app_settings(path: Path, settings: AppSettings) -> None:
    """Сохраняет настройки приложения в settings.json."""
    settings.theme_name = normalize_theme_name(settings.theme_name)
    settings.appearance_mode = normalize_appearance_mode(settings.appearance_mode)
    settings.custom_theme = normalize_custom_theme(settings.custom_theme)
    settings.overrun_visual = normalize_overrun_visual(settings.overrun_visual)
    settings.widget_type = normalize_widget_type(settings.widget_type)
    settings.widget_layouts = normalize_widget_layouts(
        settings.widget_layouts,
        legacy_x=settings.widget_x,
        legacy_y=settings.widget_y,
        active_type=settings.widget_type,
    )
    active_layout = settings.widget_layouts[settings.widget_type]
    settings.widget_size = normalize_widget_size(
        active_layout.get("size"),
        normalize_widget_size(settings.widget_size),
    )
    settings.widget_x = int(active_layout["x"])
    settings.widget_y = int(active_layout["y"])
    save_json(path, settings.__dict__)


def _safe_color(value: Any, default: str) -> str:
    """Возвращает HEX-цвет или безопасное значение по умолчанию."""
    color = str(value or "").strip()
    if len(color) == 7 and color.startswith("#"):
        try:
            int(color[1:], 16)
            return color
        except ValueError:
            return default
    return default
