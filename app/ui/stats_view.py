"""Вкладка статистики по Pomodoro-периодам."""

import tkinter as tk
from tkinter import messagebox, ttk

from app.statistics import StatisticsService


class StatsView(ttk.Frame):
    """Показывает статистику за сегодня и за все время."""

    def __init__(self, parent: tk.Widget, statistics: StatisticsService) -> None:
        """Создает вкладку статистики и сразу заполняет ее данными."""
        super().__init__(parent, padding=16)
        self.statistics = statistics
        self.today_labels: dict[str, ttk.Label] = {}
        self.all_time_labels: dict[str, ttk.Label] = {}

        self._build_ui()
        self.refresh()

    def refresh(self) -> None:
        """Обновляет все подписи на вкладке свежими данными."""
        self._fill_labels(self.today_labels, self.statistics.today_stats())
        self._fill_labels(self.all_time_labels, self.statistics.all_time_stats())

    def reset_statistics(self) -> None:
        """Сбрасывает статистику после подтверждения пользователя."""
        confirmed = messagebox.askyesno(
            "Сброс статистики",
            "Вы действительно хотите удалить всю статистику?",
        )
        if not confirmed:
            return

        self.statistics.reset_all()
        self.refresh()

    def _build_ui(self) -> None:
        """Создает две колонки: за сегодня и за все время."""
        buttons = ttk.Frame(self)
        buttons.pack(fill=tk.X, pady=(0, 12))

        ttk.Button(buttons, text="Обновить", command=self.refresh).pack(side=tk.LEFT)
        ttk.Button(
            buttons,
            text="Сбросить статистику",
            command=self.reset_statistics,
        ).pack(side=tk.LEFT, padx=(8, 0))

        columns = ttk.Frame(self)
        columns.pack(fill=tk.BOTH, expand=True)

        today_frame = ttk.LabelFrame(columns, text="Сегодня", padding=12)
        today_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=(0, 8))

        all_time_frame = ttk.LabelFrame(columns, text="За все время", padding=12)
        all_time_frame.grid(row=0, column=1, sticky=tk.NSEW, padx=(8, 0))

        columns.columnconfigure(0, weight=1)
        columns.columnconfigure(1, weight=1)

        self.today_labels = self._create_stats_labels(today_frame)
        self.all_time_labels = self._create_stats_labels(all_time_frame)

    def _create_stats_labels(self, parent: ttk.LabelFrame) -> dict[str, ttk.Label]:
        """Создает строки с названиями показателей и значениями."""
        labels: dict[str, ttk.Label] = {}
        rows = [
            ("work_seconds", "Время работы"),
            ("rest_seconds", "Время отдыха"),
            ("overwork_seconds", "Время переработки"),
            ("short_break_overrun_seconds", "Короткий отдых сверх нормы"),
            ("long_break_overrun_seconds", "Длинный отдых сверх нормы"),
            ("completed_work_periods", "Рабочих периодов завершено"),
            ("completed_short_breaks", "Коротких отдыхов завершено"),
            ("completed_long_breaks", "Длинных отдыхов завершено"),
            ("skipped_periods", "Периодов пропущено"),
            ("timer_resets", "Сбросов таймера"),
            ("completed_pomodoro_cycles", "Полных Pomodoro-циклов"),
        ]

        for row_index, (key, text) in enumerate(rows):
            ttk.Label(parent, text=f"{text}:").grid(
                row=row_index,
                column=0,
                sticky=tk.W,
                pady=2,
            )
            value_label = ttk.Label(parent, text="0")
            value_label.grid(row=row_index, column=1, sticky=tk.E, padx=(16, 0), pady=2)
            labels[key] = value_label

        parent.columnconfigure(0, weight=1)
        return labels

    def _fill_labels(self, labels: dict[str, ttk.Label], stats: dict[str, int]) -> None:
        """Подставляет значения статистики в готовые подписи."""
        for key, label in labels.items():
            value = stats.get(key, 0)
            if key.endswith("_seconds"):
                label.config(text=self._format_seconds(value))
            else:
                label.config(text=str(value))

    def _format_seconds(self, seconds: int) -> str:
        """Форматирует накопленное время как ЧЧ:ММ:СС."""
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
