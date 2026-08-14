"""Редактор светлого и тёмного вариантов пользовательской темы Qt."""

from __future__ import annotations

from copy import deepcopy
from collections.abc import Callable

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QColorDialog,
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QApplication,
    QVBoxLayout,
    QWidget,
)

from app.theme import (
    APPEARANCE_DARK,
    APPEARANCE_LABELS,
    APPEARANCE_LIGHT,
    BUILTIN_THEME_NAMES,
    CustomThemeDraft,
    ThemeManager,
    ThemePalette,
    is_hex_color,
    palette_contrast_warnings,
    palette_from_data,
)
from app.ui.components import (
    AppButton,
    Card,
    ColorSwatch,
    FlowLayout,
    PageHeader,
    ThemedScrollArea,
    repolish,
)
from app.ui.design_system import TOKENS
from app.ui.icons import application_icon


COLOR_GROUPS = (
    ("Поверхности", (("background", "Основной фон"), ("card_background", "Фон карточек"), ("secondary_background", "Дополнительный фон"), ("border", "Границы"))),
    ("Текст и управление", (("text_primary", "Основной текст"), ("text_secondary", "Вторичный текст"), ("accent", "Акцент"), ("accent_hover", "Наведение"), ("button_background", "Цвет кнопок"), ("button_text", "Текст кнопок"), ("on_accent", "Текст акцентных кнопок"), ("focus", "Фокус"), ("disabled", "Неактивные элементы"))),
    ("Служебные состояния", (("success", "Успех"), ("warning", "Предупреждение"), ("error", "Ошибка"))),
    ("Состояния таймера", (("work", "Работа"), ("short_break", "Короткий отдых"), ("long_break", "Длинный отдых"), ("overwork", "Переработка"), ("short_break_overrun", "Короткий отдых сверх нормы"), ("long_break_overrun", "Длинный отдых сверх нормы"))),
)


class CustomThemeEditor(QDialog):
    """Модальный редактор с отдельным черновиком и безопасной отменой."""

    def __init__(
        self,
        parent: QWidget,
        custom_theme: object,
        initial_mode: str,
        on_preview: Callable[[dict[str, dict[str, str]], str], None],
        on_apply: Callable[[dict[str, dict[str, str]], str], None],
        on_cancel: Callable[[], None],
        theme_manager: ThemeManager,
    ) -> None:
        super().__init__(parent)
        self.window = self
        self.on_preview = on_preview
        self.on_apply = on_apply
        self.on_cancel = on_cancel
        self.theme_manager = theme_manager
        self.draft = CustomThemeDraft(custom_theme)
        self._mode = initial_mode if initial_mode in (APPEARANCE_LIGHT, APPEARANCE_DARK) else APPEARANCE_LIGHT
        self._closed = False
        self.color_edits: dict[str, QLineEdit] = {}
        self.swatches: dict[str, ColorSwatch] = {}
        self.setWindowTitle("Пользовательская тема")
        self.setWindowIcon(application_icon())
        self._fit_to_available_screen(parent)
        self.setModal(False)
        self._build_ui()
        self._load_mode(self._mode)
        theme_manager.apply_to_window(self)
        self.show()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(TOKENS.spacing.lg, TOKENS.spacing.lg, TOKENS.spacing.lg, TOKENS.spacing.lg)
        root.setSpacing(TOKENS.spacing.md)
        root.addWidget(PageHeader("Пользовательская тема", "Редактируйте светлый и тёмный режимы независимо.", self))

        toolbar = Card(self, padding=TOKENS.spacing.md)
        self.toolbar = toolbar
        bar = FlowLayout(horizontal_spacing=TOKENS.spacing.md, vertical_spacing=TOKENS.spacing.sm)
        mode_group = QWidget(toolbar)
        mode_layout = QHBoxLayout(mode_group)
        mode_layout.setContentsMargins(0, 0, 0, 0)
        mode_layout.setSpacing(TOKENS.spacing.xs)
        mode_layout.addWidget(QLabel("Редактируемый режим", mode_group))
        self.mode_box = QComboBox(mode_group)
        for mode in (APPEARANCE_LIGHT, APPEARANCE_DARK):
            self.mode_box.addItem(APPEARANCE_LABELS[mode], mode)
        self.mode_box.setCurrentIndex(0 if self._mode == APPEARANCE_LIGHT else 1)
        self.mode_box.currentIndexChanged.connect(self._mode_changed)
        mode_layout.addWidget(self.mode_box)
        bar.addWidget(mode_group)
        base_group = QWidget(toolbar)
        base_layout = QHBoxLayout(base_group)
        base_layout.setContentsMargins(0, 0, 0, 0)
        base_layout.setSpacing(TOKENS.spacing.xs)
        base_layout.addWidget(QLabel("Создать на основе", base_group))
        self.base_box = QComboBox(base_group)
        self.base_box.addItems(BUILTIN_THEME_NAMES)
        base_layout.addWidget(self.base_box)
        self.create_button = AppButton("Создать копию", base_group, theme_manager=self.theme_manager)
        self.create_button.clicked.connect(self._create_from_base)
        base_layout.addWidget(self.create_button)
        bar.addWidget(base_group)
        toolbar.content_layout.addLayout(bar)
        root.addWidget(toolbar)

        scroll = ThemedScrollArea(self, self.theme_manager)
        self.scroll = scroll
        content = QWidget(scroll)
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, TOKENS.spacing.xs, 0)
        content_layout.setSpacing(TOKENS.spacing.md)
        for title, rows in COLOR_GROUPS:
            card = Card(content, padding=TOKENS.spacing.md)
            heading = QLabel(title, card)
            heading.setProperty("role", "sectionTitle")
            card.content_layout.addWidget(heading)
            for key, label in rows:
                row_widget = QWidget(card)
                row_layout = FlowLayout(row_widget, horizontal_spacing=TOKENS.spacing.sm, vertical_spacing=TOKENS.spacing.xs)
                name_label = QLabel(label, row_widget)
                name_label.setMinimumWidth(190)
                row_layout.addWidget(name_label)
                swatch = ColorSwatch("#000000", card)
                swatch.clicked.connect(lambda _checked=False, selected=key: self._choose_color(selected))
                row_layout.addWidget(swatch)
                edit = QLineEdit(card)
                edit.setMinimumWidth(180)
                edit.setMaxLength(7)
                edit.setPlaceholderText("#RRGGBB")
                edit.textChanged.connect(lambda value, selected=key: self._color_text_changed(selected, value))
                row_layout.addWidget(edit)
                choose = AppButton("Выбрать", card, variant="ghost", theme_manager=self.theme_manager)
                choose.clicked.connect(lambda _checked=False, selected=key: self._choose_color(selected))
                row_layout.addWidget(choose)
                self.color_edits[key] = edit
                self.swatches[key] = swatch
                card.content_layout.addWidget(row_widget)
            content_layout.addWidget(card)
        content_layout.addStretch(1)
        scroll.setWidget(content)
        root.addWidget(scroll, 1)

        self.contrast_label = QLabel("", self)
        self.contrast_label.setProperty("role", "caption")
        self.contrast_label.setWordWrap(True)
        root.addWidget(self.contrast_label)
        self.footer_widget = QWidget(self)
        footer = FlowLayout(self.footer_widget, horizontal_spacing=TOKENS.spacing.sm, vertical_spacing=TOKENS.spacing.xs)
        self.preview_button = AppButton("Предпросмотр", self.footer_widget, theme_manager=self.theme_manager)
        self.preview_button.clicked.connect(self.preview)
        self.reset_mode_button = AppButton("Сбросить текущий режим", self.footer_widget, theme_manager=self.theme_manager)
        self.reset_mode_button.clicked.connect(self._reset_mode)
        self.reset_all_button = AppButton("Сбросить всю тему", self.footer_widget, variant="danger", theme_manager=self.theme_manager)
        self.reset_all_button.clicked.connect(self._reset_all)
        self.cancel_button = AppButton("Отмена", self.footer_widget, variant="ghost", theme_manager=self.theme_manager)
        self.cancel_button.clicked.connect(self.cancel)
        self.apply_button = AppButton("Применить", self.footer_widget, variant="primary", theme_manager=self.theme_manager)
        self.apply_button.clicked.connect(self.apply)
        for button in (
            self.preview_button,
            self.reset_mode_button,
            self.reset_all_button,
            self.cancel_button,
            self.apply_button,
        ):
            footer.addWidget(button)
        root.addWidget(self.footer_widget)

    def _fit_to_available_screen(self, parent: QWidget) -> None:
        screen = parent.screen() or QApplication.primaryScreen()
        if screen is None:
            self.resize(820, 720)
            self.setMinimumSize(620, 480)
            return
        available = screen.availableGeometry()
        margin = 32
        minimum_width = min(620, max(480, available.width() - margin))
        minimum_height = min(480, max(420, available.height() - margin))
        target_width = min(920, max(minimum_width, round(available.width() * 0.72)))
        target_height = min(820, max(minimum_height, round(available.height() * 0.82)))
        self.setMinimumSize(minimum_width, minimum_height)
        self.resize(target_width, target_height)

    def is_open(self) -> bool:
        return not self._closed and self.isVisible()

    def focus(self) -> None:
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def preview(self) -> bool:
        if not self._store_form(self._mode, warn=True):
            return False
        self.on_preview(deepcopy(self.draft.value), self._mode)
        self._show_contrast_status(self._palette_for_mode(self._mode))
        return True

    def apply(self) -> bool:
        if not self._store_form(self._mode, warn=True):
            return False
        warnings = []
        for mode in (APPEARANCE_LIGHT, APPEARANCE_DARK):
            warnings.extend(
                f"{APPEARANCE_LABELS[mode]}: {warning}"
                for warning in palette_contrast_warnings(self._palette_for_mode(mode))
            )
        if warnings:
            details = "\n".join(f"• {warning}" for warning in warnings[:10])
            answer = QMessageBox.warning(
                self,
                "Низкий контраст",
                "Некоторые сочетания ниже 4,5:1:\n\n" + details + "\n\nСохранить осознанно?",
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Cancel,
            )
            if answer != QMessageBox.StandardButton.Save:
                return False
        self.on_apply(self.draft.applied(), self._mode)
        self._closed = True
        self.accept()
        return True

    def cancel(self) -> None:
        if self._closed:
            return
        self._closed = True
        self.on_cancel()
        self.reject()

    def reject(self) -> None:
        if not self._closed:
            self._closed = True
            self.on_cancel()
        super().reject()

    def _mode_changed(self, _index: int) -> None:
        new_mode = str(self.mode_box.currentData())
        if not self._store_form(self._mode, warn=True):
            self.mode_box.blockSignals(True)
            self.mode_box.setCurrentIndex(0 if self._mode == APPEARANCE_LIGHT else 1)
            self.mode_box.blockSignals(False)
            return
        self._mode = new_mode
        self._load_mode(new_mode)

    def _store_form(self, mode: str, *, warn: bool) -> bool:
        data = {}
        invalid = []
        for key, edit in self.color_edits.items():
            value = edit.text().strip().upper()
            if not is_hex_color(value):
                invalid.append(key)
                edit.setProperty("invalid", True)
                repolish(edit)
            else:
                edit.setProperty("invalid", False)
                repolish(edit)
                data[key] = value
        if invalid:
            if warn:
                QMessageBox.warning(self, "Цвет", "Исправьте значения: требуется формат #RRGGBB.")
            return False
        self.draft.set_mode(mode, data)
        return True

    def _load_mode(self, mode: str) -> None:
        palette = self.draft.value[mode]
        for key, edit in self.color_edits.items():
            edit.blockSignals(True)
            edit.setText(palette[key])
            edit.setProperty("invalid", False)
            repolish(edit)
            edit.blockSignals(False)
            self.swatches[key].set_color(palette[key])
        self._show_contrast_status(self._palette_for_mode(mode))

    def _choose_color(self, key: str) -> None:
        current = QColor(self.color_edits[key].text())
        color = QColorDialog.getColor(current, self, "Выберите цвет")
        if color.isValid():
            self.color_edits[key].setText(color.name().upper())

    def _color_text_changed(self, key: str, value: str) -> None:
        if is_hex_color(value):
            self.swatches[key].set_color(value.upper())

    def _create_from_base(self) -> None:
        self.draft.create_mode_from(self._mode, self.base_box.currentText())
        self._load_mode(self._mode)
        self.preview()

    def _reset_mode(self) -> None:
        self.draft.reset_mode(self._mode)
        self._load_mode(self._mode)
        self.preview()

    def _reset_all(self) -> None:
        answer = QMessageBox.question(self, "Сброс темы", "Сбросить оба режима к безопасной теме Comet?")
        if answer != QMessageBox.StandardButton.Yes:
            return
        self.draft.reset_all()
        self._load_mode(self._mode)
        self.preview()

    def _palette_for_mode(self, mode: str) -> ThemePalette:
        fallback = self.theme_manager.palette
        return palette_from_data(self.draft.value[mode], fallback)

    def _show_contrast_status(self, palette: ThemePalette) -> None:
        warnings = palette_contrast_warnings(palette)
        if warnings:
            self.contrast_label.setText(f"Проверка контраста: {len(warnings)} сочетаний ниже 4,5:1. При применении потребуется подтверждение.")
        else:
            self.contrast_label.setText("Проверка контраста: основные сочетания соответствуют ориентиру 4,5:1.")
