"""Модели данных, которые используются в приложении."""

from dataclasses import dataclass, field
from enum import Enum


class TimerMode(Enum):
    """Режимы таймера, между которыми переключается Pomodoro."""

    WORK = "Работа"
    SHORT_BREAK = "Короткий отдых"
    LONG_BREAK = "Длинный отдых"


class TimeDisplayFormat(Enum):
    """Доступные форматы отображения оставшегося времени."""

    HOURS_MINUTES_SECONDS = "HH:MM:SS"
    MINUTES_SECONDS = "MM:SS"


@dataclass
class TimerProfile:
    """Профиль с набором настроек, который можно сохранить и применить."""

    name: str
    work_minutes: int
    short_break_minutes: int
    long_break_minutes: int
    use_long_break: bool = True
    long_break_interval: int = 4
    auto_start_next_period: bool = True
    time_display_format: str = TimeDisplayFormat.HOURS_MINUTES_SECONDS.value
    notifications_enabled: bool = True
    notification_sound_enabled: bool = True
    work_end_message: str = "Рабочий период завершен. Время отдохнуть."
    short_break_end_message: str = "Короткий отдых завершен. Пора вернуться к работе."
    long_break_end_message: str = "Длинный отдых завершен. Пора начать новый рабочий период."
    autostart_enabled: bool = False
    minimize_to_tray_on_start: bool = False
    close_to_tray: bool = True
    theme_name: str = "Comet"
    appearance_mode: str = "light"
    widget_enabled: bool = False
    widget_type: str = "Компактный"
    widget_size: str = "Маленький"
    widget_layouts: dict[str, dict[str, int | str]] = field(default_factory=dict)
    widget_background_color: str = "#202124"
    widget_text_color: str = "#ffffff"
    widget_opacity: int = 100
    widget_always_on_top: bool = True
    widget_x: int = 100
    widget_y: int = 100


@dataclass
class AppSettings:
    """Пользовательские настройки приложения."""

    active_profile: str
    work_minutes: int = 25
    short_break_minutes: int = 5
    long_break_minutes: int = 15
    notifications_enabled: bool = True
    notification_sound_enabled: bool = True
    work_end_message: str = "Рабочий период завершен. Время отдохнуть."
    short_break_end_message: str = "Короткий отдых завершен. Пора вернуться к работе."
    long_break_end_message: str = "Длинный отдых завершен. Пора начать новый рабочий период."
    autostart_enabled: bool = False
    use_long_break: bool = True
    long_break_interval: int = 4
    auto_start_next_period: bool = True
    time_display_format: str = TimeDisplayFormat.HOURS_MINUTES_SECONDS.value
    minimize_to_tray_on_start: bool = False
    close_to_tray: bool = True
    theme_name: str = "Comet"
    appearance_mode: str = "light"
    widget_enabled: bool = False
    widget_type: str = "Компактный"
    widget_size: str = "Маленький"
    widget_layouts: dict[str, dict[str, int | str]] = field(default_factory=dict)
    widget_background_color: str = "#202124"
    widget_text_color: str = "#ffffff"
    widget_opacity: int = 100
    widget_always_on_top: bool = True
    widget_x: int = 100
    widget_y: int = 100


@dataclass
class TimerState:
    """Текущее состояние таймера, которое отображает интерфейс."""

    mode: TimerMode
    remaining_seconds: int
    is_running: bool = False
    completed_work_periods: int = 0
    waiting_for_continue: bool = False
    overrun_seconds: int = 0
    overrun_mode: TimerMode | None = None
    next_mode: TimerMode | None = None


@dataclass
class PeriodCompletion:
    """Информация о периоде, который дошел до конца без пропуска."""

    mode: TimerMode
    duration_seconds: int
    next_mode: TimerMode


@dataclass
class OverrunCompletion:
    """Превышение завершенного периода, зафиксированное одним действием."""

    mode: TimerMode
    duration_seconds: int
