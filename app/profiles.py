"""Работа с пользовательскими профилями настроек."""

from copy import deepcopy
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
from app.models import AppSettings, TimerProfile, TimeDisplayFormat
from app.storage import load_json, save_json
from app.theme import (
    DEFAULT_APPEARANCE_MODE,
    DEFAULT_THEME_NAME,
    normalize_appearance_mode,
    normalize_theme_name,
)
from app.widget_settings import (
    DEFAULT_WIDGET_SIZE,
    DEFAULT_WIDGET_TYPE,
    MIN_WIDGET_OPACITY,
    default_widget_layouts,
    normalize_widget_layouts,
    normalize_widget_size,
    normalize_widget_type,
    set_widget_layout_size,
)


def default_profile() -> TimerProfile:
    """Возвращает стандартный профиль, который всегда доступен пользователю."""
    return TimerProfile(
        name=DEFAULT_PROFILE_NAME,
        work_minutes=DEFAULT_WORK_MINUTES,
        short_break_minutes=DEFAULT_SHORT_BREAK_MINUTES,
        long_break_minutes=DEFAULT_LONG_BREAK_MINUTES,
        use_long_break=DEFAULT_USE_LONG_BREAK,
        long_break_interval=DEFAULT_CYCLES_BEFORE_LONG_BREAK,
        auto_start_next_period=DEFAULT_AUTO_START_NEXT_PERIOD,
        time_display_format=DEFAULT_TIME_DISPLAY_FORMAT,
        notifications_enabled=True,
        notification_sound_enabled=True,
        work_end_message="Рабочий период завершен. Время отдохнуть.",
        short_break_end_message="Короткий отдых завершен. Пора вернуться к работе.",
        long_break_end_message="Длинный отдых завершен. Пора начать новый рабочий период.",
        autostart_enabled=False,
        minimize_to_tray_on_start=DEFAULT_MINIMIZE_TO_TRAY_ON_START,
        close_to_tray=True,
        theme_name=DEFAULT_THEME_NAME,
        appearance_mode=DEFAULT_APPEARANCE_MODE,
        widget_enabled=False,
        widget_type=DEFAULT_WIDGET_TYPE,
        widget_size=DEFAULT_WIDGET_SIZE,
        widget_layouts=default_widget_layouts(),
        widget_background_color="#202124",
        widget_text_color="#ffffff",
        widget_opacity=100,
        widget_always_on_top=True,
        widget_x=100,
        widget_y=100,
    )


class ProfilesService:
    """Загружает, сохраняет, применяет и удаляет профили настроек."""

    def __init__(self, path: Path) -> None:
        """Создает сервис и сразу подготавливает profiles.json."""
        self.path = path
        self.profiles = self._load_profiles()
        self._save_profiles()

    def names(self) -> list[str]:
        """Возвращает список имен профилей для отображения в интерфейсе."""
        return [profile.name for profile in self.profiles]

    def get_profile(self, name: str) -> TimerProfile | None:
        """Ищет профиль по имени."""
        for profile in self.profiles:
            if profile.name == name:
                return profile
        return None

    def save_profile(self, name: str, settings: AppSettings) -> TimerProfile:
        """Сохраняет текущие настройки как профиль с указанным именем."""
        profile = TimerProfile(
            name=name,
            work_minutes=settings.work_minutes,
            short_break_minutes=settings.short_break_minutes,
            long_break_minutes=settings.long_break_minutes,
            use_long_break=settings.use_long_break,
            long_break_interval=settings.long_break_interval,
            auto_start_next_period=settings.auto_start_next_period,
            time_display_format=settings.time_display_format,
            notifications_enabled=settings.notifications_enabled,
            notification_sound_enabled=settings.notification_sound_enabled,
            work_end_message=settings.work_end_message,
            short_break_end_message=settings.short_break_end_message,
            long_break_end_message=settings.long_break_end_message,
            autostart_enabled=settings.autostart_enabled,
            minimize_to_tray_on_start=settings.minimize_to_tray_on_start,
            close_to_tray=settings.close_to_tray,
            theme_name=settings.theme_name,
            appearance_mode=settings.appearance_mode,
            widget_enabled=settings.widget_enabled,
            widget_type=settings.widget_type,
            widget_size=settings.widget_size,
            widget_layouts=deepcopy(settings.widget_layouts),
            widget_background_color=settings.widget_background_color,
            widget_text_color=settings.widget_text_color,
            widget_opacity=settings.widget_opacity,
            widget_always_on_top=settings.widget_always_on_top,
            widget_x=settings.widget_x,
            widget_y=settings.widget_y,
        )

        self.profiles = [item for item in self.profiles if item.name != name]
        self.profiles.append(profile)
        self._ensure_default_profile()
        self._save_profiles()
        return profile

    def delete_profile(self, name: str) -> bool:
        """Удаляет профиль, кроме стандартного профиля по умолчанию."""
        if name == DEFAULT_PROFILE_NAME:
            return False

        old_count = len(self.profiles)
        self.profiles = [profile for profile in self.profiles if profile.name != name]
        self._ensure_default_profile()
        self._save_profiles()
        return len(self.profiles) != old_count

    def settings_from_profile(self, profile: TimerProfile) -> AppSettings:
        """Создает настройки приложения на основе выбранного профиля."""
        return AppSettings(
            active_profile=profile.name,
            work_minutes=profile.work_minutes,
            short_break_minutes=profile.short_break_minutes,
            long_break_minutes=profile.long_break_minutes,
            notifications_enabled=profile.notifications_enabled,
            notification_sound_enabled=profile.notification_sound_enabled,
            work_end_message=profile.work_end_message,
            short_break_end_message=profile.short_break_end_message,
            long_break_end_message=profile.long_break_end_message,
            autostart_enabled=profile.autostart_enabled,
            use_long_break=profile.use_long_break,
            long_break_interval=profile.long_break_interval,
            auto_start_next_period=profile.auto_start_next_period,
            time_display_format=profile.time_display_format,
            minimize_to_tray_on_start=profile.minimize_to_tray_on_start,
            close_to_tray=profile.close_to_tray,
            theme_name=profile.theme_name,
            appearance_mode=profile.appearance_mode,
            widget_enabled=profile.widget_enabled,
            widget_type=profile.widget_type,
            widget_size=profile.widget_size,
            widget_layouts=deepcopy(profile.widget_layouts),
            widget_background_color=profile.widget_background_color,
            widget_text_color=profile.widget_text_color,
            widget_opacity=profile.widget_opacity,
            widget_always_on_top=profile.widget_always_on_top,
            widget_x=profile.widget_x,
            widget_y=profile.widget_y,
        )

    def default_settings(self) -> AppSettings:
        """Возвращает настройки стандартного профиля."""
        return self.settings_from_profile(default_profile())

    def _load_profiles(self) -> list[TimerProfile]:
        """Читает profiles.json и не падает, если файл отсутствует или поврежден."""
        raw_profiles = load_json(self.path, [])
        if not isinstance(raw_profiles, list):
            raw_profiles = []

        profiles = []
        for item in raw_profiles:
            profile = self._profile_from_data(item)
            if profile is not None:
                profiles.append(profile)

        self.profiles = profiles
        self._ensure_default_profile()
        return self.profiles

    def _profile_from_data(self, data: Any) -> TimerProfile | None:
        """Проверяет один профиль из JSON и дополняет недостающие поля."""
        if not isinstance(data, dict):
            return None

        name = str(data.get("name", "")).strip()
        if not name:
            return None

        defaults = default_profile().__dict__
        normalized = defaults | data
        normalized["name"] = name

        for key in ("work_minutes", "short_break_minutes", "long_break_minutes"):
            normalized[key] = self._positive_int(normalized.get(key), defaults[key])

        normalized["long_break_interval"] = self._positive_int(
            normalized.get("long_break_interval", normalized.get("cycles_before_long_break")),
            DEFAULT_CYCLES_BEFORE_LONG_BREAK,
        )
        normalized["use_long_break"] = bool(normalized["use_long_break"])
        normalized["auto_start_next_period"] = bool(normalized["auto_start_next_period"])
        normalized["notifications_enabled"] = bool(normalized["notifications_enabled"])
        normalized["notification_sound_enabled"] = bool(normalized["notification_sound_enabled"])
        normalized["autostart_enabled"] = bool(normalized["autostart_enabled"])
        normalized["minimize_to_tray_on_start"] = bool(normalized["minimize_to_tray_on_start"])
        normalized["close_to_tray"] = bool(normalized["close_to_tray"])
        normalized["theme_name"] = normalize_theme_name(normalized.get("theme_name"))
        normalized["appearance_mode"] = normalize_appearance_mode(
            normalized.get("appearance_mode"),
        )
        normalized["widget_enabled"] = bool(normalized["widget_enabled"])
        normalized["widget_always_on_top"] = bool(normalized["widget_always_on_top"])
        normalized["widget_type"] = normalize_widget_type(normalized.get("widget_type"))
        normalized["widget_layouts"] = normalize_widget_layouts(
            normalized.get("widget_layouts"),
            legacy_x=normalized.get("widget_x", 100),
            legacy_y=normalized.get("widget_y", 100),
            active_type=normalized["widget_type"],
        )
        active_layout = normalized["widget_layouts"][normalized["widget_type"]]
        normalized["widget_size"] = normalize_widget_size(
            normalized.get("widget_size", active_layout["size"]),
        )
        normalized["widget_layouts"] = set_widget_layout_size(
            normalized["widget_layouts"],
            normalized["widget_type"],
            normalized["widget_size"],
        )
        normalized["widget_background_color"] = self._safe_color(
            normalized["widget_background_color"],
            "#202124",
        )
        normalized["widget_text_color"] = self._safe_color(
            normalized["widget_text_color"],
            "#ffffff",
        )
        normalized["widget_opacity"] = min(
            100,
            max(
                MIN_WIDGET_OPACITY,
                self._positive_int(normalized["widget_opacity"], 100),
            ),
        )
        for key, default_value in (
            ("work_end_message", "Рабочий период завершен. Время отдохнуть."),
            ("short_break_end_message", "Короткий отдых завершен. Пора вернуться к работе."),
            ("long_break_end_message", "Длинный отдых завершен. Пора начать новый рабочий период."),
        ):
            message = str(normalized.get(key, "")).strip()
            normalized[key] = message or default_value
        active_layout = normalized["widget_layouts"][normalized["widget_type"]]
        normalized["widget_x"] = int(active_layout["x"])
        normalized["widget_y"] = int(active_layout["y"])

        allowed_formats = {format_item.value for format_item in TimeDisplayFormat}
        if normalized["time_display_format"] not in allowed_formats:
            normalized["time_display_format"] = DEFAULT_TIME_DISPLAY_FORMAT

        normalized.pop("cycles_before_long_break", None)
        known_profile = {
            key: value
            for key, value in normalized.items()
            if key in TimerProfile.__dataclass_fields__
        }
        return TimerProfile(**known_profile)

    def _ensure_default_profile(self) -> None:
        """Гарантирует, что стандартный профиль всегда есть в списке."""
        self.profiles = [
            profile for profile in self.profiles if profile.name != DEFAULT_PROFILE_NAME
        ]
        self.profiles.insert(0, default_profile())

    def _save_profiles(self) -> None:
        """Сохраняет профили в JSON."""
        save_json(self.path, [profile.__dict__ for profile in self.profiles])

    def _positive_int(self, value: Any, default: int) -> int:
        """Преобразует значение в положительное целое число."""
        try:
            return max(1, int(value))
        except (TypeError, ValueError):
            return default

    def _safe_color(self, value: Any, default: str) -> str:
        """Проверяет HEX-цвет профиля."""
        color = str(value or "").strip()
        if len(color) == 7 and color.startswith("#"):
            try:
                int(color[1:], 16)
                return color
            except ValueError:
                return default
        return default

    def _non_negative_int(self, value: Any, default: int) -> int:
        """Преобразует значение в неотрицательное целое число."""
        try:
            return max(0, int(value))
        except (TypeError, ValueError):
            return default
