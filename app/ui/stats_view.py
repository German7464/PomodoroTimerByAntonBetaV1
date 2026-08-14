"""Профессиональная страница статистики Qt Widgets."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QMessageBox, QTabWidget, QVBoxLayout, QWidget

from app.statistics import StatisticsService
from app.theme import ThemeManager
from app.ui.components import AppButton, MetricCard, PageHeader, ThemedScrollArea
from app.ui.design_system import TOKENS


STAT_ROWS = (
    ("work_seconds", "Время работы"),
    ("rest_seconds", "Время отдыха"),
    ("overwork_seconds", "Время переработки"),
    ("short_break_overrun_seconds", "Короткий отдых сверх нормы"),
    ("long_break_overrun_seconds", "Длинный отдых сверх нормы"),
    ("completed_work_periods", "Рабочих периодов"),
    ("completed_short_breaks", "Коротких отдыхов"),
    ("completed_long_breaks", "Длинных отдыхов"),
    ("skipped_periods", "Пропущено периодов"),
    ("timer_resets", "Сбросов таймера"),
    ("completed_pomodoro_cycles", "Полных циклов"),
)


class StatsView(QWidget):
    """Показывает независимые метрики за сегодня и за всё время."""

    def __init__(
        self,
        parent: QWidget | None,
        statistics: StatisticsService,
        theme_manager: ThemeManager,
    ) -> None:
        super().__init__(parent)
        self.statistics = statistics
        self.theme_manager = theme_manager
        self.today_labels = {}
        self.all_time_labels = {}
        self._responsive_pages = []
        self._build_ui()
        self._reflow_metrics()
        self.refresh()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(TOKENS.spacing.xl, TOKENS.spacing.xl, TOKENS.spacing.xl, TOKENS.spacing.xl)
        layout.setSpacing(TOKENS.spacing.lg)
        header = PageHeader("Статистика", "Обычное время и превышения учитываются раздельно.", self)
        refresh_button = AppButton("Обновить", self, variant="ghost", theme_manager=self.theme_manager)
        refresh_button.clicked.connect(self.refresh)
        reset_button = AppButton("Сбросить статистику", self, variant="danger", theme_manager=self.theme_manager)
        reset_button.clicked.connect(self.reset_statistics)
        header.actions.addWidget(refresh_button)
        header.actions.addWidget(reset_button)
        layout.addWidget(header)

        tabs = QTabWidget(self)
        self.tabs = tabs
        today, self.today_labels = self._stats_page("Сегодня")
        all_time, self.all_time_labels = self._stats_page("За всё время")
        tabs.addTab(today, "Сегодня")
        tabs.addTab(all_time, "За всё время")
        tabs.currentChanged.connect(
            lambda index: self.theme_manager.refresh_widget_tree(tabs.widget(index), visible_only=False)
            if 0 <= index < tabs.count() else None
        )
        layout.addWidget(tabs, 1)

    def _stats_page(self, accessible_name: str):
        scroll = ThemedScrollArea(self, self.theme_manager)
        content = QWidget(scroll)
        content.setAccessibleName(accessible_name)
        grid = QGridLayout(content)
        grid.setContentsMargins(0, TOKENS.spacing.md, 0, TOKENS.spacing.md)
        grid.setHorizontalSpacing(TOKENS.spacing.md)
        grid.setVerticalSpacing(TOKENS.spacing.md)
        labels = {}
        cards = []
        for index, (key, title) in enumerate(STAT_ROWS):
            card = MetricCard(title, parent=content)
            card.setMinimumWidth(220)
            grid.addWidget(card, index // 2, index % 2)
            cards.append(card)
            labels[key] = card.value_label
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        scroll.setWidget(content)
        self._responsive_pages.append([scroll, grid, cards, None])
        return scroll, labels

    def resizeEvent(self, event) -> None:  # noqa: N802 - Qt API
        super().resizeEvent(event)
        self._reflow_metrics()

    def _reflow_metrics(self) -> None:
        for page in self._responsive_pages:
            scroll, grid, cards, previous_columns = page
            columns = 1 if scroll.viewport().width() < 560 else 2
            if columns == previous_columns:
                continue
            page[3] = columns
            for card in cards:
                grid.removeWidget(card)
            for index, card in enumerate(cards):
                grid.addWidget(card, index // columns, index % columns)
            for column in range(2):
                grid.setColumnStretch(column, 1 if column < columns else 0)

    def refresh(self) -> None:
        self._fill_labels(self.today_labels, self.statistics.today_stats())
        self._fill_labels(self.all_time_labels, self.statistics.all_time_stats())

    def reset_statistics(self) -> None:
        answer = QMessageBox.question(
            self,
            "Сброс статистики",
            "Вы действительно хотите удалить всю статистику?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        self.statistics.reset_all()
        self.refresh()

    def _fill_labels(self, labels, stats: dict[str, int]) -> None:
        for key, label in labels.items():
            value = stats.get(key, 0)
            label.setText(self._format_seconds(value) if key.endswith("_seconds") else str(value))

    @staticmethod
    def _format_seconds(seconds: int) -> str:
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
