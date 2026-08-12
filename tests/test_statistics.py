"""Миграция, устойчивость и раздельные показатели статистики."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from app.models import TimerMode
from app.statistics import StatisticsService


class StatisticsServiceTests(unittest.TestCase):
    """Проверяет формат statistics.json версии 2."""

    def test_version_one_migrates_without_losing_data(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "statistics.json"
            old_data = {
                "version": 1,
                "custom_metadata": "сохранить",
                "days": {
                    "2026-08-11": {
                        "work_seconds": 1500,
                        "rest_seconds": 300,
                        "completed_work_periods": 1,
                    },
                },
                "all_time": {
                    "work_seconds": 1500,
                    "rest_seconds": 300,
                    "completed_work_periods": 1,
                    "custom_counter": 7,
                },
            }
            path.write_text(json.dumps(old_data, ensure_ascii=False), encoding="utf-8")

            service = StatisticsService(path)

            self.assertEqual(service.data["version"], 2)
            self.assertEqual(service.data["custom_metadata"], "сохранить")
            self.assertEqual(service.data["all_time"]["work_seconds"], 1500)
            self.assertEqual(service.data["all_time"]["custom_counter"], 7)
            self.assertEqual(service.data["all_time"]["overwork_seconds"], 0)
            old_day = service.data["days"]["2026-08-11"]
            self.assertEqual(old_day["rest_seconds"], 300)
            self.assertEqual(old_day["short_break_overrun_seconds"], 0)

            saved_data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(saved_data["version"], 2)

    def test_partial_and_invalid_values_are_normalized(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "statistics.json"
            path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "days": {"2026-08-12": {"work_seconds": "bad"}},
                        "all_time": {"work_seconds": -10, "rest_seconds": "20"},
                    },
                ),
                encoding="utf-8",
            )

            service = StatisticsService(path)

            self.assertEqual(service.data["all_time"]["work_seconds"], 0)
            self.assertEqual(service.data["all_time"]["rest_seconds"], 20)
            self.assertEqual(service.data["days"]["2026-08-12"]["work_seconds"], 0)
            self.assertEqual(service.data["all_time"]["long_break_overrun_seconds"], 0)

    def test_corrupt_json_is_backed_up_and_does_not_crash(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "statistics.json"
            original = "{not-json"
            path.write_text(original, encoding="utf-8")

            service = StatisticsService(path)

            self.assertEqual(service.data["version"], 2)
            backup = path.with_name("statistics.json.corrupt.bak")
            self.assertTrue(backup.exists())
            self.assertEqual(backup.read_text(encoding="utf-8"), original)
            self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["version"], 2)

    def test_structurally_invalid_json_is_backed_up(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "statistics.json"
            original = {"version": 1, "days": ["bad"], "all_time": {}}
            path.write_text(json.dumps(original), encoding="utf-8")

            service = StatisticsService(path)

            self.assertEqual(service.data["days"], {})
            backup = path.with_name("statistics.json.corrupt.bak")
            self.assertEqual(json.loads(backup.read_text(encoding="utf-8")), original)

    def test_three_overrun_types_are_recorded_separately(self) -> None:
        with TemporaryDirectory() as directory:
            service = StatisticsService(Path(directory) / "statistics.json")

            service.record_overrun(TimerMode.WORK, 11)
            service.record_overrun(TimerMode.SHORT_BREAK, 22)
            service.record_overrun(TimerMode.LONG_BREAK, 33)

            for stats in (service.today_stats(), service.all_time_stats()):
                self.assertEqual(stats["overwork_seconds"], 11)
                self.assertEqual(stats["short_break_overrun_seconds"], 22)
                self.assertEqual(stats["long_break_overrun_seconds"], 33)
                self.assertEqual(stats["work_seconds"], 0)
                self.assertEqual(stats["rest_seconds"], 0)

    def test_zero_overrun_does_not_rewrite_file(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "statistics.json"
            service = StatisticsService(path)
            before = path.stat().st_mtime_ns

            service.record_overrun(TimerMode.WORK, 0)

            self.assertEqual(path.stat().st_mtime_ns, before)


if __name__ == "__main__":
    unittest.main()
