"""Профессиональная страница статистики Qt Widgets."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QMessageBox, QTabWidget, QVBoxLayout, QWidget

from app.statistics import StatisticsService
from app.i18n import localization_manager, tr, trn
from app.theme import ThemeManager
from app.ui.components import AppButton, MetricCard, PageHeader, ThemedScrollArea
from app.ui.design_system import TOKENS


STAT_ROWS = (
    ("work_seconds", "stats.metric.work_time"),
    ("rest_seconds", "stats.metric.rest_time"),
    ("overwork_seconds", "stats.metric.overwork_time"),
    ("short_break_overrun_seconds", "stats.metric.short_break_overrun"),
    ("long_break_overrun_seconds", "stats.metric.long_break_overrun"),
    ("completed_work_periods", "stats.metric.completed_work_periods"),
    ("completed_short_breaks", "stats.metric.completed_short_breaks"),
    ("completed_long_breaks", "stats.metric.completed_long_breaks"),
    ("skipped_periods", "stats.metric.skipped_periods"),
    ("timer_resets", "stats.metric.timer_resets"),
    ("completed_pomodoro_cycles", "stats.metric.completed_cycles"),
)
COUNT_METRICS = frozenset(key for key, _label in STAT_ROWS if not key.endswith("_seconds"))


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
        localization_manager().language_changed.connect(self._retranslate_ui)

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(TOKENS.spacing.xl, TOKENS.spacing.xl, TOKENS.spacing.xl, TOKENS.spacing.xl)
        layout.setSpacing(TOKENS.spacing.lg)
        header = PageHeader("stats.title", "stats.subtitle", self)
        self.refresh_button = AppButton(tr("action.refresh"), self, variant="ghost", theme_manager=self.theme_manager)
        self.refresh_button.clicked.connect(self.refresh)
        self.reset_button = AppButton(tr("stats.reset.action"), self, variant="danger", theme_manager=self.theme_manager)
        self.reset_button.clicked.connect(self.reset_statistics)
        header.actions.addWidget(self.refresh_button)
        header.actions.addWidget(self.reset_button)
        layout.addWidget(header)

        tabs = QTabWidget(self)
        self.tabs = tabs
        today, self.today_labels = self._stats_page("stats.period.today")
        all_time, self.all_time_labels = self._stats_page("stats.period.all_time")
        tabs.addTab(today, tr("stats.period.today"))
        tabs.addTab(all_time, tr("stats.period.all_time"))
        tabs.currentChanged.connect(
            lambda index: self.theme_manager.refresh_widget_tree(tabs.widget(index), visible_only=False)
            if 0 <= index < tabs.count() else None
        )
        layout.addWidget(tabs, 1)

    def _stats_page(self, accessible_name: str):
        scroll = ThemedScrollArea(self, self.theme_manager)
        content = QWidget(scroll)
        content.setProperty("translationKey", accessible_name)
        content.setAccessibleName(tr(accessible_name))
        grid = QGridLayout(content)
        grid.setContentsMargins(0, TOKENS.spacing.md, 0, TOKENS.spacing.md)
        grid.setHorizontalSpacing(TOKENS.spacing.md)
        grid.setVerticalSpacing(TOKENS.spacing.md)
        labels = {}
        cards = []
        for index, (key, title_key) in enumerate(STAT_ROWS):
            card = MetricCard(title_key, parent=content)
            card.setProperty("metricKey", key)
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
            tr("stats.reset.title"),
            tr("stats.reset.confirmation"),
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
            if key in COUNT_METRICS:
                card = label.parentWidget()
                if isinstance(card, MetricCard):
                    title_key = dict(STAT_ROWS)[key]
                    card.title_label.setText(trn(title_key, value))

    @staticmethod
    def _format_seconds(seconds: int) -> str:
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def _retranslate_ui(self, _language_code: str) -> None:
        self.refresh_button.setText(tr("action.refresh"))
        self.reset_button.setText(tr("stats.reset.action"))
        self.tabs.setTabText(0, tr("stats.period.today"))
        self.tabs.setTabText(1, tr("stats.period.all_time"))
        for index, key in enumerate(("stats.period.today", "stats.period.all_time")):
            self.tabs.widget(index).widget().setAccessibleName(tr(key))
        self.refresh()
        self._reflow_metrics()
