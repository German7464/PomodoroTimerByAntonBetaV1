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
    APPEARANCE_LABEL_KEYS,
    APPEARANCE_LIGHT,
    BUILTIN_THEME_NAMES,
    CustomThemeDraft,
    ThemeManager,
    ThemePalette,
    is_hex_color,
    palette_contrast_warnings,
    palette_from_data,
    THEME_LABEL_KEYS,
)
from app.i18n import localization_manager, tr, trn
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
    ("theme_editor.group.surfaces", (("background", "theme_editor.color.background"), ("card_background", "theme_editor.color.card_background"), ("secondary_background", "theme_editor.color.secondary_background"), ("border", "theme_editor.color.border"))),
    ("theme_editor.group.text_controls", (("text_primary", "theme_editor.color.text_primary"), ("text_secondary", "theme_editor.color.text_secondary"), ("accent", "theme_editor.color.accent"), ("accent_hover", "theme_editor.color.accent_hover"), ("button_background", "theme_editor.color.button_background"), ("button_text", "theme_editor.color.button_text"), ("on_accent", "theme_editor.color.on_accent"), ("focus", "theme_editor.color.focus"), ("disabled", "theme_editor.color.disabled"))),
    ("theme_editor.group.service_states", (("success", "theme_editor.color.success"), ("warning", "theme_editor.color.warning"), ("error", "theme_editor.color.error"))),
    ("theme_editor.group.timer_states", (("work", "timer.mode.work"), ("short_break", "timer.mode.short_break"), ("long_break", "timer.mode.long_break"), ("overwork", "timer.mode.overwork"), ("short_break_overrun", "timer.mode.short_break_overrun"), ("long_break_overrun", "timer.mode.long_break_overrun"))),
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
        self.setWindowTitle(tr("theme_editor.title"))
        self.setWindowIcon(application_icon())
        self._fit_to_available_screen(parent)
        self.setModal(False)
        self._build_ui()
        self._load_mode(self._mode)
        theme_manager.apply_to_window(self)
        localization_manager().language_changed.connect(self._retranslate_ui)
        self.show()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(TOKENS.spacing.lg, TOKENS.spacing.lg, TOKENS.spacing.lg, TOKENS.spacing.lg)
        root.setSpacing(TOKENS.spacing.md)
        root.addWidget(PageHeader("theme_editor.title", "theme_editor.subtitle", self))

        toolbar = Card(self, padding=TOKENS.spacing.md)
        self.toolbar = toolbar
        bar = FlowLayout(horizontal_spacing=TOKENS.spacing.md, vertical_spacing=TOKENS.spacing.sm)
        mode_group = QWidget(toolbar)
        mode_layout = QHBoxLayout(mode_group)
        mode_layout.setContentsMargins(0, 0, 0, 0)
        mode_layout.setSpacing(TOKENS.spacing.xs)
        self.mode_label = QLabel(tr("theme_editor.editing_mode"), mode_group)
        mode_layout.addWidget(self.mode_label)
        self.mode_box = QComboBox(mode_group)
        for mode in (APPEARANCE_LIGHT, APPEARANCE_DARK):
            self.mode_box.addItem(tr(APPEARANCE_LABEL_KEYS[mode]), mode)
        self.mode_box.setCurrentIndex(0 if self._mode == APPEARANCE_LIGHT else 1)
        self.mode_box.currentIndexChanged.connect(self._mode_changed)
        mode_layout.addWidget(self.mode_box)
        bar.addWidget(mode_group)
        base_group = QWidget(toolbar)
        base_layout = QHBoxLayout(base_group)
        base_layout.setContentsMargins(0, 0, 0, 0)
        base_layout.setSpacing(TOKENS.spacing.xs)
        self.base_label = QLabel(tr("theme_editor.create_from"), base_group)
        base_layout.addWidget(self.base_label)
        self.base_box = QComboBox(base_group)
        for theme_name in BUILTIN_THEME_NAMES:
            self.base_box.addItem(tr(THEME_LABEL_KEYS[theme_name]), theme_name)
        base_layout.addWidget(self.base_box)
        self.create_button = AppButton(tr("theme_editor.create_copy"), base_group, theme_manager=self.theme_manager)
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
            heading = QLabel(tr(title), card)
            heading.setProperty("translationKey", title)
            heading.setProperty("role", "sectionTitle")
            card.content_layout.addWidget(heading)
            for key, label in rows:
                row_widget = QWidget(card)
                row_layout = FlowLayout(row_widget, horizontal_spacing=TOKENS.spacing.sm, vertical_spacing=TOKENS.spacing.xs)
                name_label = QLabel(tr(label), row_widget)
                name_label.setProperty("translationKey", label)
                name_label.setMinimumWidth(190)
                row_layout.addWidget(name_label)
                swatch = ColorSwatch("#000000", card)
                swatch.clicked.connect(lambda _checked=False, selected=key: self._choose_color(selected))
                row_layout.addWidget(swatch)
                edit = QLineEdit(card)
                edit.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
                edit.setMinimumWidth(180)
                edit.setMaxLength(7)
                edit.setPlaceholderText("#RRGGBB")
                edit.textChanged.connect(lambda value, selected=key: self._color_text_changed(selected, value))
                row_layout.addWidget(edit)
                choose = AppButton(tr("action.choose"), card, variant="ghost", theme_manager=self.theme_manager)
                choose.setProperty("translationKey", "action.choose")
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
        self.preview_button = AppButton(tr("action.preview"), self.footer_widget, theme_manager=self.theme_manager)
        self.preview_button.clicked.connect(self.preview)
        self.reset_mode_button = AppButton(tr("theme_editor.reset_mode"), self.footer_widget, theme_manager=self.theme_manager)
        self.reset_mode_button.clicked.connect(self._reset_mode)
        self.reset_all_button = AppButton(tr("theme_editor.reset_all"), self.footer_widget, variant="danger", theme_manager=self.theme_manager)
        self.reset_all_button.clicked.connect(self._reset_all)
        self.cancel_button = AppButton(tr("action.cancel"), self.footer_widget, variant="ghost", theme_manager=self.theme_manager)
        self.cancel_button.clicked.connect(self.cancel)
        self.apply_button = AppButton(tr("action.apply"), self.footer_widget, variant="primary", theme_manager=self.theme_manager)
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
        minimum_width = min(
            620,
            max(min(360, available.width()), available.width() - margin),
        )
        minimum_height = min(
            480,
            max(min(360, available.height()), available.height() - margin),
        )
        target_width = min(
            available.width(),
            920,
            max(minimum_width, round(available.width() * 0.72)),
        )
        target_height = min(
            available.height(),
            820,
            max(minimum_height, round(available.height() * 0.82)),
        )
        self.setMaximumSize(available.size())
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
                f"{tr(APPEARANCE_LABEL_KEYS[mode])}: {self._localized_contrast_warning(warning)}"
                for warning in palette_contrast_warnings(self._palette_for_mode(mode))
            )
        if warnings:
            details = "\n".join(f"• {warning}" for warning in warnings[:10])
            answer = QMessageBox.warning(
                self,
                tr("theme_editor.low_contrast.title"),
                tr("theme_editor.low_contrast.confirmation", details=details),
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
                QMessageBox.warning(self, tr("dialog.color.title"), tr("dialog.color.invalid_hex"))
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
        color = QColorDialog.getColor(current, self, tr("dialog.color.choose"))
        if color.isValid():
            self.color_edits[key].setText(color.name().upper())

    def _color_text_changed(self, key: str, value: str) -> None:
        if is_hex_color(value):
            self.swatches[key].set_color(value.upper())

    def _create_from_base(self) -> None:
        self.draft.create_mode_from(self._mode, self.base_box.currentData())
        self._load_mode(self._mode)
        self.preview()

    def _reset_mode(self) -> None:
        self.draft.reset_mode(self._mode)
        self._load_mode(self._mode)
        self.preview()

    def _reset_all(self) -> None:
        answer = QMessageBox.question(
            self,
            tr("theme_editor.reset.title"),
            tr("theme_editor.reset.confirmation"),
        )
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
            self.contrast_label.setText(trn("theme_editor.contrast.warning", len(warnings)))
        else:
            self.contrast_label.setText(tr("theme_editor.contrast.ok"))

    @staticmethod
    def _localized_contrast_warning(warning: str) -> str:
        key, separator, ratio = warning.partition("|")
        return f"{tr(key)}: {ratio}" if separator else warning

    def _retranslate_ui(self, _language_code: str) -> None:
        self.setWindowTitle(tr("theme_editor.title"))
        self.mode_label.setText(tr("theme_editor.editing_mode"))
        self.base_label.setText(tr("theme_editor.create_from"))
        for index, mode in enumerate((APPEARANCE_LIGHT, APPEARANCE_DARK)):
            self.mode_box.setItemText(index, tr(APPEARANCE_LABEL_KEYS[mode]))
        for index, theme_name in enumerate(BUILTIN_THEME_NAMES):
            self.base_box.setItemText(index, tr(THEME_LABEL_KEYS[theme_name]))
        self.create_button.setText(tr("theme_editor.create_copy"))
        for label in self.findChildren(QLabel):
            key = label.property("translationKey")
            if key:
                label.setText(tr(str(key)))
        for button in self.findChildren(AppButton):
            key = button.property("translationKey")
            if key:
                button.setText(tr(str(key)))
        self.preview_button.setText(tr("action.preview"))
        self.reset_mode_button.setText(tr("theme_editor.reset_mode"))
        self.reset_all_button.setText(tr("theme_editor.reset_all"))
        self.cancel_button.setText(tr("action.cancel"))
        self.apply_button.setText(tr("action.apply"))
        self._show_contrast_status(self._palette_for_mode(self._mode))
        self.updateGeometry()
