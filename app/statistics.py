"""Логика статистики завершенных Pomodoro-периодов."""

import json
from copy import deepcopy
from datetime import date
from pathlib import Path
from typing import Any

from app.models import TimerMode


STAT_KEYS = (
    "work_seconds",
    "rest_seconds",
    "completed_work_periods",
    "completed_short_breaks",
    "completed_long_breaks",
    "skipped_periods",
    "timer_resets",
    "completed_pomodoro_cycles",
)


def empty_stats_block() -> dict[str, int]:
    """Создает пустой набор счетчиков статистики."""
    return {key: 0 for key in STAT_KEYS}


def default_statistics_data() -> dict[str, Any]:
    """Создает структуру statistics.json по умолчанию."""
    return {
        "version": 1,
        "days": {},
        "all_time": empty_stats_block(),
    }


class StatisticsService:
    """Сохраняет и считает статистику завершений, пропусков и сбросов."""

    def __init__(self, path: Path) -> None:
        """Загружает статистику или создает новый файл, если его еще нет."""
        self.path = path
        self.data = self._load_or_create()

    def record_completed_period(
        self,
        mode: TimerMode,
        duration_seconds: int,
        use_long_break: bool,
    ) -> None:
        """Записывает период, который сам дошел до конца."""
        today_stats = self._today_stats()
        all_time_stats = self.data["all_time"]

        for stats in (today_stats, all_time_stats):
            if mode == TimerMode.WORK:
                stats["work_seconds"] += duration_seconds
                stats["completed_work_periods"] += 1
            elif mode == TimerMode.SHORT_BREAK:
                stats["rest_seconds"] += duration_seconds
                stats["completed_short_breaks"] += 1
                if not use_long_break:
                    stats["completed_pomodoro_cycles"] += 1
            elif mode == TimerMode.LONG_BREAK:
                stats["rest_seconds"] += duration_seconds
                stats["completed_long_breaks"] += 1
                stats["completed_pomodoro_cycles"] += 1

        self._save()

    def record_skipped_period(self, mode: TimerMode) -> None:
        """Записывает ручной пропуск периода без зачета времени."""
        _ = mode
        self._increment_counter("skipped_periods")

    def record_reset(self) -> None:
        """Записывает нажатие кнопки сброса таймера."""
        self._increment_counter("timer_resets")

    def reset_all(self) -> None:
        """Полностью очищает статистику."""
        self.data = default_statistics_data()
        self._save()

    def today_stats(self) -> dict[str, int]:
        """Возвращает статистику за сегодняшний день."""
        return deepcopy(self._today_stats())

    def all_time_stats(self) -> dict[str, int]:
        """Возвращает статистику за все время."""
        return deepcopy(self.data["all_time"])

    def _increment_counter(self, key: str) -> None:
        """Увеличивает один счетчик за сегодня и за все время."""
        self._today_stats()[key] += 1
        self.data["all_time"][key] += 1
        self._save()

    def _today_key(self) -> str:
        """Возвращает текущую дату в формате YYYY-MM-DD."""
        return date.today().isoformat()

    def _today_stats(self) -> dict[str, int]:
        """Возвращает счетчики за сегодня, создавая их при необходимости."""
        days = self.data.setdefault("days", {})
        return days.setdefault(self._today_key(), empty_stats_block())

    def _load_or_create(self) -> dict[str, Any]:
        """Читает JSON и восстанавливает структуру, если файл поврежден."""
        data = default_statistics_data()

        if self.path.exists():
            try:
                with self.path.open("r", encoding="utf-8") as file:
                    loaded_data = json.load(file)
                data = self._normalize_data(loaded_data)
            except (json.JSONDecodeError, OSError):
                data = default_statistics_data()

        self.data = data
        self._save()
        return data

    def _normalize_data(self, raw_data: Any) -> dict[str, Any]:
        """Дополняет недостающие поля, чтобы старый JSON не ломал программу."""
        if not isinstance(raw_data, dict):
            return default_statistics_data()

        normalized = default_statistics_data()
        normalized["version"] = raw_data.get("version", 1)

        if isinstance(raw_data.get("all_time"), dict):
            normalized["all_time"].update(self._normalize_stats_block(raw_data["all_time"]))

        if isinstance(raw_data.get("days"), dict):
            for day_key, day_stats in raw_data["days"].items():
                if isinstance(day_stats, dict):
                    normalized["days"][day_key] = self._normalize_stats_block(day_stats)

        return normalized

    def _normalize_stats_block(self, raw_stats: dict[str, Any]) -> dict[str, int]:
        """Приводит один блок счетчиков к ожидаемому набору чисел."""
        stats = empty_stats_block()
        for key in STAT_KEYS:
            try:
                stats[key] = max(0, int(raw_stats.get(key, 0)))
            except (TypeError, ValueError):
                stats[key] = 0
        return stats

    def _save(self) -> None:
        """Сохраняет статистику в пользовательскую папку."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=2)
