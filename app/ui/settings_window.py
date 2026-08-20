"""Адаптивные настройки Pomodoro Timer на Qt Widgets."""

from __future__ import annotations

from copy import deepcopy
from collections.abc import Callable

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QColorDialog,
    QComboBox,
    QDialog,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QSlider,
    QSpinBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.autostart import AUTOSTART_DISABLED, AUTOSTART_ENABLED_CURRENT, AUTOSTART_ENABLED_STALE
from app.config import DEFAULT_PROFILE_NAME, PROFILES_FILE, is_frozen_app
from app.models import AppSettings, TimerMode, TimeDisplayFormat
from app.i18n import (
    SUPPORTED_LANGUAGES,
    language_native_name,
    localization_manager,
    normalize_language_code,
    tr,
)
from app.overrun_effects import (
    EFFECT_LABEL_KEYS,
    INTENSITY_LABEL_KEYS,
    LONG_BREAK_OVERRUN_KEY,
    OVERWORK_KEY,
    OVERRUN_EFFECTS,
    OVERRUN_INTENSITIES,
    OVERRUN_SCOPES,
    OVERRUN_SPEEDS,
    SCOPE_LABEL_KEYS,
    SPEED_LABEL_KEYS,
    SHORT_BREAK_OVERRUN_KEY,
    normalize_overrun_visual,
    overrun_key,
    resolved_overrun_color,
)
from app.profiles import ProfilesService
from app.theme import (
    APPEARANCE_DARK,
    APPEARANCE_LIGHT,
    CUSTOM_THEME_NAME,
    THEME_NAMES,
    THEME_LABEL_KEYS,
    ThemeManager,
    get_palette,
    is_hex_color,
    mode_color,
    normalize_appearance_mode,
    normalize_theme_name,
)
from app.ui.components import (
    AppButton,
    Card,
    ColorSwatch,
    FlowLayout,
    PageHeader,
    SwitchRow,
    ThemedScrollArea,
)
from app.ui.design_system import TOKENS
from app.ui.qt_app import fit_window_to_available_screen
from app.ui.icons import application_icon
from app.ui.theme_editor import CustomThemeEditor
from app.widget_settings import (
    DEFAULT_WIDGET_X,
    DEFAULT_WIDGET_Y,
    MIN_WIDGET_OPACITY,
    WIDGET_SIZES,
    WIDGET_SIZE_LABEL_KEYS,
    WIDGET_TYPE_DESCRIPTIONS,
    WIDGET_TYPES,
    WIDGET_TYPE_LABEL_KEYS,
    normalize_widget_layouts,
    set_widget_layout_size,
)


class SettingsView(QWidget):
    """Единая форма настроек с навигацией и совместимыми callbacks."""

    SECTION_KEYS = (
        "settings.section.appearance", "settings.section.time",
        "settings.section.logic", "settings.section.notifications",
        "settings.section.widget", "settings.section.overrun",
        "settings.section.profiles", "settings.section.tray",
    )

    def __init__(
        self,
        parent: QWidget | None,
        settings: AppSettings,
        on_save: Callable[[AppSettings, bool], None],
        autostart_status: str = AUTOSTART_DISABLED,
        on_theme_change: Callable[[str, str], None] | None = None,
        on_custom_theme_preview: Callable[[dict[str, dict[str, str]], str], None] | None = None,
        on_custom_theme_apply: Callable[[dict[str, dict[str, str]], str], None] | None = None,
        on_theme_preview_cancel: Callable[[], None] | None = None,
        on_overrun_preview: Callable[[TimerMode, dict[str, object]], None] | None = None,
        on_widget_opacity_change: Callable[[int], None] | None = None,
        on_overrun_opacity_change: Callable[[bool], None] | None = None,
        on_widget_configuration_change: Callable[[str, str, dict, bool], None] | None = None,
        on_language_change: Callable[[str], None] | None = None,
        theme_manager: ThemeManager | None = None,
    ) -> None:
        super().__init__(parent)
        if theme_manager is None:
            raise ValueError("SettingsView requires the shared ThemeManager")
        self.settings = settings
        self.personal_settings = deepcopy(settings)
        self.on_save = on_save
        self.on_theme_change = on_theme_change
        self.on_custom_theme_preview = on_custom_theme_preview
        self.on_custom_theme_apply = on_custom_theme_apply
        self.on_theme_preview_cancel = on_theme_preview_cancel
        self.on_overrun_preview = on_overrun_preview
        self.on_widget_opacity_change = on_widget_opacity_change
        self.on_overrun_opacity_change = on_overrun_opacity_change
        self.on_widget_configuration_change = on_widget_configuration_change
        self.on_language_change = on_language_change
        self.theme_manager = theme_manager
        self.autostart_status = autostart_status
        self.profiles = ProfilesService(PROFILES_FILE)
        self.theme_editor: CustomThemeEditor | None = None
        self.custom_theme = deepcopy(settings.custom_theme)
        self.overrun_visual = normalize_overrun_visual(settings.overrun_visual)
        self.overrun_color_overrides = deepcopy(self.overrun_visual["colors"])
        self.widget_layouts = deepcopy(settings.widget_layouts)
        self.toggle_switches: list[SwitchRow] = []
        self._theme_buttons = {}
        self._loading_form = True
        self._compact_layout: bool | None = None
        self._theme_columns: int | None = None
        self._theme_cards: list[Card] = []
        self._message_sources: dict[QLineEdit, str | None] = {}
        self._build_ui()
        self._apply_responsive_layout()
        self._load_settings_to_form(settings)
        self._loading_form = False
        self._reload_profiles_list()
        localization_manager().language_changed.connect(self._retranslate_ui)

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(TOKENS.spacing.xl, TOKENS.spacing.xl, TOKENS.spacing.xl, TOKENS.spacing.lg)
        outer.setSpacing(TOKENS.spacing.lg)
        outer.addWidget(PageHeader("settings.title", "settings.subtitle", self))
        self.section_selector = QComboBox(self)
        for key in self.SECTION_KEYS:
            self.section_selector.addItem(tr(key), key)
        self.section_selector.setVisible(False)
        outer.addWidget(self.section_selector)
        body = QHBoxLayout()
        body.setSpacing(TOKENS.spacing.lg)
        self.section_list = QListWidget(self)
        self.section_list.setFixedWidth(210)
        for key in self.SECTION_KEYS:
            item = QListWidgetItem(tr(key))
            item.setData(Qt.ItemDataRole.UserRole, key)
            self.section_list.addItem(item)
        self.section_list.setCurrentRow(0)
        self.section_list.currentRowChanged.connect(self._section_changed)
        body.addWidget(self.section_list)
        self.stack = QStackedWidget(self)
        self.section_selector.currentIndexChanged.connect(self._section_changed)
        body.addWidget(self.stack, 1)
        outer.addLayout(body, 1)
        builders = (
            self._build_theme_page, self._build_time_page, self._build_logic_page,
            self._build_notifications_page, self._build_widget_page,
            self._build_overrun_page, self._build_profiles_page, self._build_tray_page,
        )
        for builder in builders:
            self.stack.addWidget(builder())
        footer = QHBoxLayout()
        footer.addStretch(1)
        self.save_button = AppButton(tr("settings.save"), self, variant="primary", theme_manager=self.theme_manager)
        self.save_button.clicked.connect(self._save)
        footer.addWidget(self.save_button)
        outer.addLayout(footer)

    def _section_changed(self, index: int) -> None:
        if 0 <= index < self.stack.count():
            self.stack.setCurrentIndex(index)
            self.theme_manager.refresh_widget_tree(self.stack.widget(index), visible_only=False)
            self.section_list.blockSignals(True)
            self.section_list.setCurrentRow(index)
            self.section_list.blockSignals(False)
            self.section_selector.blockSignals(True)
            self.section_selector.setCurrentIndex(index)
            self.section_selector.blockSignals(False)

    def resizeEvent(self, event) -> None:  # noqa: N802 - Qt API
        super().resizeEvent(event)
        self._apply_responsive_layout()

    def _apply_responsive_layout(self) -> None:
        compact = self.width() < 820
        if compact != self._compact_layout:
            self._compact_layout = compact
            self.section_list.setVisible(not compact)
            self.section_selector.setVisible(compact)
        if not hasattr(self, "_theme_grid"):
            return
        columns = 1 if self.stack.width() < 660 else 2
        if columns == self._theme_columns:
            return
        self._theme_columns = columns
        for card in self._theme_cards:
            self._theme_grid.removeWidget(card)
        for index, card in enumerate(self._theme_cards):
            self._theme_grid.addWidget(card, index // columns, index % columns)
        for column in range(2):
            self._theme_grid.setColumnStretch(column, 1 if column < columns else 0)

    def _page(self, title: str, subtitle: str):
        scroll = ThemedScrollArea(self, self.theme_manager)
        content = QWidget(scroll)
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, TOKENS.spacing.xs, TOKENS.spacing.lg)
        layout.setSpacing(TOKENS.spacing.md)
        heading = QLabel(tr(title), content)
        heading.setProperty("translationKey", title)
        heading.setProperty("role", "sectionTitle")
        layout.addWidget(heading)
        if subtitle:
            label = QLabel(tr(subtitle), content)
            label.setProperty("translationKey", subtitle)
            label.setProperty("role", "subtitle")
            label.setWordWrap(True)
            layout.addWidget(label)
        scroll.setWidget(content)
        return scroll, content, layout

    def _build_theme_page(self) -> QWidget:
        scroll, content, layout = self._page("settings.appearance.title", "settings.appearance.subtitle")
        language_card = Card(content, padding=TOKENS.spacing.md)
        language_row = QHBoxLayout()
        self.language_label = QLabel(tr("settings.appearance.language"), language_card)
        self.language_label.setProperty("translationKey", "settings.appearance.language")
        language_row.addWidget(self.language_label)
        language_row.addStretch(1)
        self.language_combo = QComboBox(language_card)
        for language in SUPPORTED_LANGUAGES:
            self.language_combo.addItem(language.native_name, language.code)
        self.language_combo.currentIndexChanged.connect(self._language_changed)
        language_row.addWidget(self.language_combo)
        language_card.content_layout.addLayout(language_row)
        layout.addWidget(language_card)
        grid = QGridLayout()
        grid.setSpacing(TOKENS.spacing.md)
        self._theme_grid = grid
        descriptions = {
            "Comet": "theme.description.comet",
            "Aurora": "theme.description.aurora",
            "Warm": "theme.description.warm",
            CUSTOM_THEME_NAME: "theme.description.custom",
        }
        for index, name in enumerate(THEME_NAMES):
            button = AppButton(tr(THEME_LABEL_KEYS[name]), content, variant="secondary", theme_manager=self.theme_manager)
            button.setCheckable(True)
            button.clicked.connect(lambda _checked=False, selected=name: self._select_theme(selected))
            card = Card(content, padding=TOKENS.spacing.md)
            card.setMinimumWidth(250)
            card.content_layout.addWidget(button)
            description = QLabel(tr(descriptions[name]), card)
            description.setProperty("translationKey", descriptions[name])
            description.setProperty("role", "caption")
            description.setWordWrap(True)
            card.content_layout.addWidget(description)
            swatches = QHBoxLayout()
            preview_items = []
            for _ in range(4):
                swatch = ColorSwatch("#000000", card)
                swatch.setEnabled(False)
                preview_items.append(swatch)
                swatches.addWidget(swatch)
            swatches.addStretch(1)
            card.content_layout.addLayout(swatches)
            grid.addWidget(card, index // 2, index % 2)
            self._theme_cards.append(card)
            self._theme_buttons[name] = (button, preview_items)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        layout.addLayout(grid)
        self.appearance_switch = self._switch(
            "settings.appearance.dark_mode", self.settings.appearance_mode == APPEARANCE_DARK,
            "settings.appearance.dark_mode.description", self._appearance_changed,
        )
        layout.addWidget(self.appearance_switch)
        self.edit_theme_button = AppButton(tr("settings.appearance.edit_colors"), content, variant="primary", theme_manager=self.theme_manager)
        self.edit_theme_button.clicked.connect(self._open_theme_editor)
        layout.addWidget(self.edit_theme_button, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addStretch(1)
        return scroll

    def _build_time_page(self) -> QWidget:
        scroll, content, layout = self._page("settings.time.title", "settings.time.subtitle")
        card = Card(content)
        form = QFormLayout()
        self._configure_form(form)
        form.setSpacing(TOKENS.spacing.sm)
        self.work_minutes = self._spin(1, 240)
        self.short_break_minutes = self._spin(1, 240)
        self.long_break_minutes = self._spin(1, 240)
        self.time_format = QComboBox(card)
        self.time_format.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.time_format.addItems([item.value for item in TimeDisplayFormat])
        self._add_form_row(form, "settings.time.work_minutes", self.work_minutes, card)
        self._add_form_row(form, "settings.time.short_break_minutes", self.short_break_minutes, card)
        self._add_form_row(form, "settings.time.long_break_minutes", self.long_break_minutes, card)
        self._add_form_row(form, "settings.time.format", self.time_format, card)
        card.content_layout.addLayout(form)
        layout.addWidget(card)
        layout.addStretch(1)
        return scroll

    def _build_logic_page(self) -> QWidget:
        scroll, content, layout = self._page("settings.logic.title", "settings.logic.subtitle")
        card = Card(content)
        self.use_long_break = self._switch("settings.logic.use_long_break", True, "settings.logic.use_long_break.description", self._update_long_break_controls)
        card.content_layout.addWidget(self.use_long_break)
        interval_row = QHBoxLayout()
        self.interval_label = QLabel(tr("settings.logic.long_break_interval"), card)
        self.interval_label.setProperty("translationKey", "settings.logic.long_break_interval")
        self.long_break_interval = self._spin(1, 20)
        interval_row.addWidget(self.interval_label)
        interval_row.addStretch(1)
        interval_row.addWidget(self.long_break_interval)
        card.content_layout.addLayout(interval_row)
        layout.addWidget(card)
        layout.addStretch(1)
        return scroll

    def _build_notifications_page(self) -> QWidget:
        scroll, content, layout = self._page("settings.notifications.title", "settings.notifications.subtitle")
        card = Card(content)
        self.notifications_enabled = self._switch("settings.notifications.enabled", True)
        self.notification_sound = self._switch("settings.notifications.sound", True)
        self.auto_start = self._switch("settings.notifications.auto_transition", True, "settings.notifications.auto_transition.description")
        for row in (self.notifications_enabled, self.notification_sound, self.auto_start):
            card.content_layout.addWidget(row)
        form = QFormLayout()
        self._configure_form(form)
        self.work_message = QLineEdit(card)
        self.short_message = QLineEdit(card)
        self.long_message = QLineEdit(card)
        for edit in (self.work_message, self.short_message, self.long_message):
            edit.textEdited.connect(lambda _text, target=edit: self._message_sources.__setitem__(target, None))
        self._add_form_row(form, "settings.notifications.work_end", self.work_message, card)
        self._add_form_row(form, "settings.notifications.short_break_end", self.short_message, card)
        self._add_form_row(form, "settings.notifications.long_break_end", self.long_message, card)
        card.content_layout.addLayout(form)
        layout.addWidget(card)
        layout.addStretch(1)
        return scroll

    def _build_widget_page(self) -> QWidget:
        scroll, content, layout = self._page("settings.widget.title", "settings.widget.subtitle")
        card = Card(content)
        form = QFormLayout()
        self._configure_form(form)
        self.widget_type = QComboBox(card)
        for widget_type in WIDGET_TYPES:
            self.widget_type.addItem(tr(WIDGET_TYPE_LABEL_KEYS[widget_type]), widget_type)
        self.widget_type.currentIndexChanged.connect(self._widget_type_changed)
        self.widget_size = QComboBox(card)
        for widget_size in WIDGET_SIZES:
            self.widget_size.addItem(tr(WIDGET_SIZE_LABEL_KEYS[widget_size]), widget_size)
        self.widget_size.currentIndexChanged.connect(self._widget_size_changed)
        self._add_form_row(form, "settings.widget.type", self.widget_type, card)
        self._add_form_row(form, "settings.widget.size", self.widget_size, card)
        card.content_layout.addLayout(form)
        self.widget_description = QLabel("", card)
        self.widget_description.setProperty("role", "caption")
        self.widget_description.setWordWrap(True)
        card.content_layout.addWidget(self.widget_description)
        opacity_row = QHBoxLayout()
        opacity_label = QLabel(tr("settings.widget.opacity"), card)
        opacity_label.setProperty("translationKey", "settings.widget.opacity")
        opacity_row.addWidget(opacity_label)
        self.widget_opacity = QSlider(Qt.Orientation.Horizontal, card)
        self.widget_opacity.setRange(MIN_WIDGET_OPACITY, 100)
        self.widget_opacity.valueChanged.connect(self._widget_opacity_changed)
        opacity_row.addWidget(self.widget_opacity, 1)
        self.widget_opacity_label = QLabel("100%", card)
        self.widget_opacity_label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.widget_opacity_label.setMinimumWidth(48)
        opacity_row.addWidget(self.widget_opacity_label)
        card.content_layout.addLayout(opacity_row)
        caption = QLabel(tr("settings.widget.opacity.description"), card)
        caption.setProperty("translationKey", "settings.widget.opacity.description")
        caption.setProperty("role", "caption")
        card.content_layout.addWidget(caption)
        self.widget_topmost = self._switch("settings.widget.always_on_top", True, callback=lambda _enabled: self._apply_widget_configuration())
        card.content_layout.addWidget(self.widget_topmost)
        self.reset_widget_button = AppButton(tr("settings.widget.reset_position"), card, theme_manager=self.theme_manager)
        self.reset_widget_button.clicked.connect(self._reset_widget_position)
        card.content_layout.addWidget(self.reset_widget_button, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(card)
        layout.addStretch(1)
        return scroll

    def _build_overrun_page(self) -> QWidget:
        scroll, content, layout = self._page("settings.overrun.title", "settings.overrun.subtitle")
        card = Card(content)
        form = QFormLayout()
        self._configure_form(form)
        self.overrun_effect = self._localized_combo(OVERRUN_EFFECTS, EFFECT_LABEL_KEYS)
        self.overrun_scope = self._localized_combo(OVERRUN_SCOPES, SCOPE_LABEL_KEYS)
        self.overrun_speed = self._localized_combo(OVERRUN_SPEEDS, SPEED_LABEL_KEYS)
        self.overrun_intensity = self._localized_combo(OVERRUN_INTENSITIES, INTENSITY_LABEL_KEYS)
        self._add_form_row(form, "settings.overrun.effect", self.overrun_effect, card)
        self._add_form_row(form, "settings.overrun.scope", self.overrun_scope, card)
        self._add_form_row(form, "settings.overrun.speed", self.overrun_speed, card)
        self._add_form_row(form, "settings.overrun.intensity", self.overrun_intensity, card)
        card.content_layout.addLayout(form)
        self.overrun_color_enabled = self._switch("settings.overrun.change_color", True)
        self.overrun_animations = self._switch("settings.overrun.allow_motion", True)
        self.overrun_opaque_widget = self._switch("settings.overrun.opaque_widget", False, callback=self._overrun_opacity_changed)
        for row in (self.overrun_color_enabled, self.overrun_animations, self.overrun_opaque_widget):
            card.content_layout.addWidget(row)
        layout.addWidget(card)

        colors = Card(content)
        colors_title = QLabel(tr("settings.overrun.separate_colors"), colors)
        colors_title.setProperty("translationKey", "settings.overrun.separate_colors")
        colors_title.setProperty("role", "sectionTitle")
        colors.content_layout.addWidget(colors_title)
        self.overrun_color_edits = {}
        self.overrun_color_swatches = {}
        for key, label_key in ((OVERWORK_KEY, "timer.mode.overwork"), (SHORT_BREAK_OVERRUN_KEY, "timer.mode.short_break_overrun"), (LONG_BREAK_OVERRUN_KEY, "timer.mode.long_break_overrun")):
            color_row = QWidget(colors)
            color_flow = FlowLayout(color_row, horizontal_spacing=TOKENS.spacing.sm, vertical_spacing=TOKENS.spacing.xs)
            color_label = QLabel(tr(label_key), color_row)
            color_label.setProperty("translationKey", label_key)
            color_label.setMinimumWidth(220)
            color_flow.addWidget(color_label)
            swatch = ColorSwatch("#000000", colors)
            swatch.clicked.connect(lambda _checked=False, selected=key: self._choose_overrun_color(selected))
            color_flow.addWidget(swatch)
            edit = QLineEdit(colors)
            edit.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
            edit.setMinimumWidth(140)
            edit.setMaxLength(7)
            edit.textChanged.connect(lambda value, selected=key: self._overrun_color_changed(selected, value))
            color_flow.addWidget(edit)
            choose = AppButton(tr("action.choose"), colors, variant="ghost", theme_manager=self.theme_manager)
            choose.setProperty("translationKey", "action.choose")
            choose.clicked.connect(lambda _checked=False, selected=key: self._choose_overrun_color(selected))
            color_flow.addWidget(choose)
            themed = AppButton(tr("settings.overrun.use_theme_color"), colors, variant="ghost", theme_manager=self.theme_manager)
            themed.setProperty("translationKey", "settings.overrun.use_theme_color")
            themed.clicked.connect(lambda _checked=False, selected=key: self._reset_overrun_color(selected))
            color_flow.addWidget(themed)
            self.overrun_color_edits[key] = edit
            self.overrun_color_swatches[key] = swatch
            colors.content_layout.addWidget(color_row)
        layout.addWidget(colors)
        preview_card = Card(content, padding=TOKENS.spacing.md)
        preview_row = FlowLayout(horizontal_spacing=TOKENS.spacing.sm)
        preview_label = QLabel(tr("action.preview"), preview_card)
        preview_label.setProperty("translationKey", "action.preview")
        preview_row.addWidget(preview_label)
        self.overrun_preview_mode = QComboBox(preview_card)
        for mode, key in ((TimerMode.WORK, "timer.mode.overwork"), (TimerMode.SHORT_BREAK, "timer.mode.short_break_overrun"), (TimerMode.LONG_BREAK, "timer.mode.long_break_overrun")):
            self.overrun_preview_mode.addItem(tr(key), mode)
        self.overrun_preview_mode.setProperty("translationKeys", "timer.mode.overwork|timer.mode.short_break_overrun|timer.mode.long_break_overrun")
        self.overrun_preview_mode.setMinimumWidth(260)
        preview_row.addWidget(self.overrun_preview_mode)
        self.overrun_preview_button = AppButton(tr("action.show"), preview_card, variant="primary", theme_manager=self.theme_manager)
        self.overrun_preview_button.clicked.connect(self._preview_overrun)
        preview_row.addWidget(self.overrun_preview_button)
        preview_card.content_layout.addLayout(preview_row)
        layout.addWidget(preview_card)
        layout.addStretch(1)
        return scroll

    def _build_profiles_page(self) -> QWidget:
        scroll, content, layout = self._page("settings.profiles.title", "settings.profiles.subtitle")
        card = Card(content)
        self.profile_name = QLineEdit(card)
        self.profile_name.setPlaceholderText(tr("settings.profiles.name_placeholder"))
        card.content_layout.addWidget(self.profile_name)
        self.profiles_list = QListWidget(card)
        self.profiles_list.currentTextChanged.connect(self.profile_name.setText)
        card.content_layout.addWidget(self.profiles_list, 1)
        buttons = FlowLayout(horizontal_spacing=TOKENS.spacing.sm)
        self.profile_buttons = []
        for key, callback, variant in (
            ("settings.profiles.save", self._save_profile, "primary"),
            ("settings.profiles.apply", self._apply_selected_profile, "secondary"),
            ("settings.profiles.delete", self._delete_selected_profile, "danger"),
            ("settings.profiles.defaults", self._restore_default_settings, "secondary"),
            ("settings.profiles.restore_personal", self._restore_personal_settings, "ghost"),
        ):
            button = AppButton(tr(key), card, variant=variant, theme_manager=self.theme_manager)
            button.setProperty("translationKey", key)
            button.clicked.connect(callback)
            buttons.addWidget(button)
            self.profile_buttons.append(button)
        card.content_layout.addLayout(buttons)
        layout.addWidget(card)
        layout.addStretch(1)
        return scroll

    def _build_tray_page(self) -> QWidget:
        scroll, content, layout = self._page("settings.tray.title", "settings.tray.subtitle")
        card = Card(content)
        self.minimize_start = self._switch("settings.tray.minimize_on_start", False)
        self.close_to_tray = self._switch("settings.tray.close_to_tray", True)
        self.autostart_switch = self._switch("settings.tray.autostart", False, callback=self._autostart_toggled)
        for row in (self.minimize_start, self.close_to_tray, self.autostart_switch):
            card.content_layout.addWidget(row)
        self.autostart_status_label = QLabel("", card)
        self.autostart_status_label.setProperty("role", "caption")
        self.autostart_status_label.setWordWrap(True)
        card.content_layout.addWidget(self.autostart_status_label)
        self.autostart_update_button = AppButton(tr("settings.tray.update_autostart"), card, theme_manager=self.theme_manager)
        self.autostart_update_button.clicked.connect(self._update_autostart)
        card.content_layout.addWidget(self.autostart_update_button, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(card)
        layout.addStretch(1)
        return scroll

    def _switch(self, text: str, checked: bool, description: str = "", callback: Callable[[bool], None] | None = None) -> SwitchRow:
        switch = SwitchRow(
            text, checked, self, theme_manager=self.theme_manager,
            animations_enabled=lambda: self.overrun_animations.isChecked() if hasattr(self, "overrun_animations") else True,
            description=description,
        )
        if callback is not None:
            switch.valueChanged.connect(callback)
        self.toggle_switches.append(switch)
        return switch

    @staticmethod
    def _spin(minimum: int, maximum: int) -> QSpinBox:
        spin = QSpinBox()
        spin.setRange(minimum, maximum)
        return spin

    @staticmethod
    def _combo(values) -> QComboBox:
        combo = QComboBox()
        combo.addItems(list(values))
        return combo

    @staticmethod
    def _localized_combo(values, label_keys) -> QComboBox:
        combo = QComboBox()
        for value in values:
            combo.addItem(tr(label_keys[value]), value)
        combo.setProperty("translationKeys", "|".join(label_keys[value] for value in values))
        return combo

    @staticmethod
    def _add_form_row(form: QFormLayout, key: str, field: QWidget, parent: QWidget) -> None:
        label = QLabel(tr(key), parent)
        label.setProperty("translationKey", key)
        label.setWordWrap(True)
        form.addRow(label, field)

    @staticmethod
    def _configure_form(form: QFormLayout) -> None:
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

    def sync_theme(self, theme_name: str, appearance_mode: str) -> None:
        self._set_theme_controls(theme_name, appearance_mode)
        self._refresh_theme_previews()
        self._refresh_overrun_colors()

    def _set_theme_controls(self, theme_name: str, appearance_mode: str) -> None:
        self.current_theme_name = normalize_theme_name(theme_name)
        self.current_appearance_mode = normalize_appearance_mode(appearance_mode)
        for name, (button, _swatches) in self._theme_buttons.items():
            button.blockSignals(True)
            button.setChecked(name == self.current_theme_name)
            button.blockSignals(False)
        self.appearance_switch.setChecked(self.current_appearance_mode == APPEARANCE_DARK)

    def _select_theme(self, name: str) -> None:
        self.current_theme_name = normalize_theme_name(name)
        self._set_theme_controls(self.current_theme_name, self.current_appearance_mode)
        self._theme_selection_changed()

    def _appearance_changed(self, dark: bool) -> None:
        self.current_appearance_mode = APPEARANCE_DARK if dark else APPEARANCE_LIGHT
        self._theme_selection_changed()

    def _theme_selection_changed(self) -> None:
        self._refresh_theme_previews()
        self._refresh_overrun_colors()
        if self.on_theme_change is not None:
            self.on_theme_change(self.current_theme_name, self.current_appearance_mode)

    def _refresh_theme_previews(self) -> None:
        for name, (_button, swatches) in self._theme_buttons.items():
            palette = get_palette(name, self.current_appearance_mode, self.custom_theme)
            for swatch, color in zip(swatches, (palette.background, palette.card_background, palette.accent, palette.text_primary), strict=True):
                swatch.set_color(color)

    def _open_theme_editor(self) -> None:
        if self.theme_editor is not None and self.theme_editor.is_open():
            self.theme_editor.focus()
            return
        if None in (self.on_custom_theme_preview, self.on_custom_theme_apply, self.on_theme_preview_cancel):
            QMessageBox.warning(
                self,
                tr("theme.name.custom"),
                tr("settings.appearance.editor_unavailable"),
            )
            return
        self.theme_editor = CustomThemeEditor(
            self, self.custom_theme, self.current_appearance_mode,
            self.on_custom_theme_preview, self._apply_custom_theme_from_editor,
            self.on_theme_preview_cancel, self.theme_manager,
        )

    def _apply_custom_theme_from_editor(self, custom_theme, appearance_mode: str) -> None:
        self.custom_theme = deepcopy(custom_theme)
        self.current_theme_name = CUSTOM_THEME_NAME
        self.current_appearance_mode = appearance_mode
        self._set_theme_controls(CUSTOM_THEME_NAME, appearance_mode)
        if self.on_custom_theme_apply is not None:
            self.on_custom_theme_apply(custom_theme, appearance_mode)
        self._refresh_theme_previews()
        self._refresh_overrun_colors()

    def _active_form_palette(self):
        return get_palette(self.current_theme_name, self.current_appearance_mode, self.custom_theme)

    def _refresh_overrun_colors(self) -> None:
        if not hasattr(self, "overrun_color_edits"):
            return
        palette = self._active_form_palette()
        visual = normalize_overrun_visual({**self.overrun_visual, "colors": self.overrun_color_overrides})
        for mode in TimerMode:
            key = overrun_key(mode)
            color = self.overrun_color_overrides.get(key) or resolved_overrun_color(visual, palette, mode)
            edit = self.overrun_color_edits[key]
            edit.blockSignals(True)
            edit.setText(color)
            edit.blockSignals(False)
            self.overrun_color_swatches[key].set_color(color)

    def _choose_overrun_color(self, key: str) -> None:
        color = QColorDialog.getColor(
            QColor(self.overrun_color_edits[key].text()),
            self,
            tr("settings.overrun.color_dialog"),
        )
        if color.isValid():
            value = color.name().upper()
            self.overrun_color_overrides[key] = value
            self.overrun_color_edits[key].setText(value)

    def _reset_overrun_color(self, key: str) -> None:
        self.overrun_color_overrides[key] = None
        self._refresh_overrun_colors()

    def _overrun_color_changed(self, key: str, value: str) -> None:
        if is_hex_color(value):
            self.overrun_color_swatches[key].set_color(value.upper())

    def _read_overrun_visual(self, *, warn: bool) -> dict[str, object]:
        palette = self._active_form_palette()
        invalid = []
        for mode in TimerMode:
            key = overrun_key(mode)
            value = self.overrun_color_edits[key].text().strip().upper()
            themed = mode_color(palette, mode, waiting_for_continue=True)
            if not is_hex_color(value):
                invalid.append(key)
                self.overrun_color_overrides[key] = None
            elif self.overrun_color_overrides.get(key) is None and value == themed.upper():
                self.overrun_color_overrides[key] = None
            else:
                self.overrun_color_overrides[key] = value
        if invalid and warn:
            QMessageBox.warning(
                self,
                tr("settings.overrun.title"),
                tr("settings.overrun.invalid_colors"),
            )
        self.overrun_visual = normalize_overrun_visual({
            "effect": self.overrun_effect.currentData(),
            "color_enabled": self.overrun_color_enabled.isChecked(),
            "scope": self.overrun_scope.currentData(),
            "speed": self.overrun_speed.currentData(),
            "intensity": self.overrun_intensity.currentData(),
            "animations_enabled": self.overrun_animations.isChecked(),
            "opaque_widget_during_overrun": self.overrun_opaque_widget.isChecked(),
            "colors": self.overrun_color_overrides,
        })
        self._refresh_overrun_colors()
        return deepcopy(self.overrun_visual)

    def _preview_overrun(self) -> None:
        if self.on_overrun_preview is None:
            return
        self.on_overrun_preview(
            self.overrun_preview_mode.currentData(),
            self._read_overrun_visual(warn=True),
        )

    def _overrun_opacity_changed(self, enabled: bool) -> None:
        if self.on_overrun_opacity_change is not None:
            self.on_overrun_opacity_change(enabled)

    def sync_overrun_widget_opacity(self, enabled: bool) -> None:
        self.overrun_opaque_widget.setChecked(enabled)

    def _widget_opacity_changed(self, value: int) -> None:
        self.widget_opacity_label.setText(f"{value}%")
        if self.on_widget_opacity_change is not None:
            self.on_widget_opacity_change(value)

    def sync_widget_opacity(self, opacity: int) -> None:
        value = min(100, max(MIN_WIDGET_OPACITY, int(opacity)))
        self.widget_opacity.blockSignals(True)
        self.widget_opacity.setValue(value)
        self.widget_opacity.blockSignals(False)
        self.widget_opacity_label.setText(f"{value}%")

    def _widget_type_changed(self, _index: int) -> None:
        widget_type = str(self.widget_type.currentData() or "")
        if widget_type not in self.widget_layouts:
            return
        self.widget_size.blockSignals(True)
        self._set_combo_data(self.widget_size, str(self.widget_layouts[widget_type]["size"]))
        self.widget_size.blockSignals(False)
        self.widget_description.setText(tr(WIDGET_TYPE_DESCRIPTIONS[widget_type]))
        self._apply_widget_configuration()

    def _widget_size_changed(self, _index: int) -> None:
        if hasattr(self, "widget_type"):
            self._remember_widget_size_selection()
            self._apply_widget_configuration()

    def _apply_widget_configuration(self) -> None:
        if self._loading_form or self.on_widget_configuration_change is None:
            return
        widget_type = str(self.widget_type.currentData() or "")
        if widget_type not in self.widget_layouts:
            return
        self.on_widget_configuration_change(
            widget_type,
            str(self.widget_size.currentData() or ""),
            deepcopy(self.widget_layouts),
            self.widget_topmost.isChecked(),
        )

    def _remember_widget_size_selection(self) -> None:
        widget_type = str(self.widget_type.currentData() or "")
        if widget_type not in WIDGET_TYPES:
            return
        self.widget_layouts = normalize_widget_layouts(self.widget_layouts, active_type=widget_type)
        self.widget_layouts = set_widget_layout_size(
            self.widget_layouts,
            widget_type,
            str(self.widget_size.currentData() or ""),
        )

    def _reset_widget_position(self) -> None:
        widget_type = str(self.widget_type.currentData() or "")
        self.widget_layouts[widget_type]["x"] = DEFAULT_WIDGET_X
        self.widget_layouts[widget_type]["y"] = DEFAULT_WIDGET_Y
        self._apply_widget_configuration()
        QMessageBox.information(
            self,
            tr("settings.widget.dialog_title"),
            tr("settings.widget.position_reset"),
        )

    def sync_widget_layouts(self, settings: AppSettings) -> None:
        self.widget_layouts[settings.widget_type] = deepcopy(settings.widget_layouts[settings.widget_type])
        if self.widget_type.currentData() == settings.widget_type:
            self._set_combo_data(self.widget_size, settings.widget_size)

    def _update_long_break_controls(self, enabled: bool | None = None) -> None:
        state = self.use_long_break.isChecked() if enabled is None else bool(enabled)
        self.interval_label.setEnabled(state)
        self.long_break_interval.setEnabled(state)

    def _autostart_status_text(self) -> str:
        if self.autostart_status == AUTOSTART_ENABLED_CURRENT:
            return tr("settings.tray.autostart_current")
        if self.autostart_status == AUTOSTART_ENABLED_STALE:
            return tr("settings.tray.autostart_stale")
        if not is_frozen_app():
            return tr("settings.tray.autostart_python")
        return tr("settings.tray.autostart_disabled")

    def _sync_autostart_controls(self) -> None:
        self.autostart_status_label.setText(self._autostart_status_text())
        self.autostart_switch.setEnabled(is_frozen_app())
        self.autostart_update_button.setEnabled(is_frozen_app() and self.autostart_status == AUTOSTART_ENABLED_STALE)

    def _autostart_toggled(self, _enabled: bool) -> None:
        pass

    def _update_autostart(self) -> None:
        self.autostart_switch.setChecked(True)
        settings = self._settings_from_form(self.profile_name.text().strip())
        settings.autostart_enabled = True
        self.on_save(settings, True)
        self.settings = settings

    def update_autostart_status(self, status: str) -> None:
        self.autostart_status = status
        self._sync_autostart_controls()

    def _reload_profiles_list(self) -> None:
        self.profiles_list.clear()
        for name in self.profiles.names():
            item = QListWidgetItem(
                tr("settings.profiles.default_name") if name == DEFAULT_PROFILE_NAME else name
            )
            item.setData(Qt.ItemDataRole.UserRole, name)
            self.profiles_list.addItem(item)

    def _selected_profile_name(self) -> str | None:
        item = self.profiles_list.currentItem()
        return str(item.data(Qt.ItemDataRole.UserRole)) if item is not None else None

    def _save_profile(self) -> None:
        name = self.profile_name.text().strip()
        if name == tr("settings.profiles.default_name"):
            name = DEFAULT_PROFILE_NAME
        if not name:
            QMessageBox.warning(
                self,
                tr("settings.profiles.dialog_title"),
                tr("settings.profiles.enter_name"),
            )
            return
        settings = self._settings_from_form(name)
        self.profiles.save_profile(name, settings)
        self._reload_profiles_list()
        self.on_save(settings, False)
        self.settings = settings

    def _apply_selected_profile(self) -> None:
        name = self._selected_profile_name() or self.profile_name.text().strip()
        profile = self.profiles.get_profile(name)
        if profile is None:
            QMessageBox.warning(
                self,
                tr("settings.profiles.dialog_title"),
                tr("settings.profiles.select_profile"),
            )
            return
        settings = self.profiles.settings_from_profile(profile)
        settings.widget_enabled = self.settings.widget_enabled
        settings.ui_language = self.settings.ui_language
        self._load_settings_to_form(settings)
        self.on_save(settings, False)
        self.settings = settings

    def _delete_selected_profile(self) -> None:
        name = self._selected_profile_name()
        if not name:
            return
        if name == DEFAULT_PROFILE_NAME:
            QMessageBox.warning(
                self,
                tr("settings.profiles.dialog_title"),
                tr("settings.profiles.default_cannot_delete"),
            )
            return
        if QMessageBox.question(
            self,
            tr("settings.profiles.delete_title"),
            tr("settings.profiles.delete_confirmation", profile_name=name),
        ) == QMessageBox.StandardButton.Yes:
            self.profiles.delete_profile(name)
            self._reload_profiles_list()

    def _restore_default_settings(self) -> None:
        settings = self.profiles.default_settings()
        settings.widget_enabled = self.settings.widget_enabled
        settings.ui_language = self.settings.ui_language
        self._load_settings_to_form(settings)
        self.on_save(settings, False)
        self.settings = settings

    def _restore_personal_settings(self) -> None:
        settings = deepcopy(self.personal_settings)
        settings.widget_enabled = self.settings.widget_enabled
        settings.ui_language = self.settings.ui_language
        self._load_settings_to_form(settings)
        self.on_save(settings, False)
        self.settings = settings

    def _save(self) -> None:
        settings = self._settings_from_form(self.profile_name.text().strip())
        autostart_changed = settings.autostart_enabled != self.settings.autostart_enabled
        self.on_save(settings, autostart_changed)
        self.settings = settings

    def _settings_from_form(self, active_profile: str) -> AppSettings:
        self._remember_widget_size_selection()
        widget_type = str(self.widget_type.currentData() or "")
        active_layout = self.widget_layouts[widget_type]
        normalized_profile = (
            DEFAULT_PROFILE_NAME
            if active_profile == tr("settings.profiles.default_name")
            else active_profile
        )
        return AppSettings(
            active_profile=normalized_profile or self.settings.active_profile,
            work_minutes=self.work_minutes.value(), short_break_minutes=self.short_break_minutes.value(), long_break_minutes=self.long_break_minutes.value(),
            notifications_enabled=self.notifications_enabled.isChecked(), notification_sound_enabled=self.notification_sound.isChecked(),
            work_end_message=self._stored_message(self.work_message), short_break_end_message=self._stored_message(self.short_message), long_break_end_message=self._stored_message(self.long_message),
            autostart_enabled=self.autostart_switch.isChecked(), use_long_break=self.use_long_break.isChecked(), long_break_interval=self.long_break_interval.value(),
            auto_start_next_period=self.auto_start.isChecked(), time_display_format=self.time_format.currentText(),
            minimize_to_tray_on_start=self.minimize_start.isChecked(), close_to_tray=self.close_to_tray.isChecked(),
            theme_name=self.current_theme_name, appearance_mode=self.current_appearance_mode,
            custom_theme=deepcopy(self.custom_theme), overrun_visual=self._read_overrun_visual(warn=True),
            widget_enabled=self.settings.widget_enabled, widget_type=widget_type, widget_size=str(self.widget_size.currentData() or ""), widget_layouts=deepcopy(self.widget_layouts),
            widget_background_color=self.settings.widget_background_color, widget_text_color=self.settings.widget_text_color,
            widget_opacity=self.widget_opacity.value(), widget_always_on_top=self.widget_topmost.isChecked(),
            widget_x=int(active_layout["x"]), widget_y=int(active_layout["y"]),
            main_window_geometry=deepcopy(self.settings.main_window_geometry),
            ui_language=normalize_language_code(self.language_combo.currentData()),
        )

    def _load_settings_to_form(self, settings: AppSettings) -> None:
        self.profile_name.setText(
            tr("settings.profiles.default_name")
            if settings.active_profile == DEFAULT_PROFILE_NAME
            else settings.active_profile
        )
        self.work_minutes.setValue(settings.work_minutes)
        self.short_break_minutes.setValue(settings.short_break_minutes)
        self.long_break_minutes.setValue(settings.long_break_minutes)
        self.use_long_break.setChecked(settings.use_long_break)
        self.long_break_interval.setValue(settings.long_break_interval)
        self.auto_start.setChecked(settings.auto_start_next_period)
        self.time_format.setCurrentText(settings.time_display_format)
        self.minimize_start.setChecked(settings.minimize_to_tray_on_start)
        self.close_to_tray.setChecked(settings.close_to_tray)
        self.autostart_switch.setChecked(settings.autostart_enabled)
        self.notifications_enabled.setChecked(settings.notifications_enabled)
        self.notification_sound.setChecked(settings.notification_sound_enabled)
        for edit, value in (
            (self.work_message, settings.work_end_message),
            (self.short_message, settings.short_break_end_message),
            (self.long_message, settings.long_break_end_message),
        ):
            source = value if str(value).startswith("notification.default.") else None
            self._message_sources[edit] = source
            edit.setText(tr(source) if source else str(value))
        self.custom_theme = deepcopy(settings.custom_theme)
        self._set_theme_controls(settings.theme_name, settings.appearance_mode)
        self.overrun_visual = normalize_overrun_visual(settings.overrun_visual)
        self._set_combo_data(self.overrun_effect, str(self.overrun_visual["effect"]))
        self.overrun_color_enabled.setChecked(bool(self.overrun_visual["color_enabled"]))
        self._set_combo_data(self.overrun_scope, str(self.overrun_visual["scope"]))
        self._set_combo_data(self.overrun_speed, str(self.overrun_visual["speed"]))
        self._set_combo_data(self.overrun_intensity, str(self.overrun_visual["intensity"]))
        self.overrun_animations.setChecked(bool(self.overrun_visual["animations_enabled"]))
        self.overrun_opaque_widget.setChecked(bool(self.overrun_visual["opaque_widget_during_overrun"]))
        self.overrun_color_overrides = deepcopy(self.overrun_visual["colors"])
        self.widget_layouts = deepcopy(settings.widget_layouts)
        self._set_combo_data(self.widget_type, settings.widget_type)
        self._set_combo_data(self.widget_size, settings.widget_size)
        self.widget_description.setText(tr(WIDGET_TYPE_DESCRIPTIONS[settings.widget_type]))
        self.sync_widget_opacity(settings.widget_opacity)
        self.widget_topmost.setChecked(settings.widget_always_on_top)
        self._set_combo_data(self.language_combo, settings.ui_language)
        self._update_long_break_controls()
        self._refresh_theme_previews()
        self._refresh_overrun_colors()
        self._sync_autostart_controls()

    def _stored_message(self, edit: QLineEdit) -> str:
        value = edit.text().strip()
        source = self._message_sources.get(edit)
        return source if source and value == tr(source) else value

    @staticmethod
    def _set_combo_data(combo: QComboBox, value: object) -> None:
        index = combo.findData(value)
        if index >= 0:
            combo.setCurrentIndex(index)

    def _language_changed(self, _index: int) -> None:
        if self._loading_form or self.on_language_change is None:
            return
        language_code = normalize_language_code(self.language_combo.currentData())
        self.settings.ui_language = language_code
        self.on_language_change(language_code)

    def sync_language(self, language_code: str) -> None:
        self.language_combo.blockSignals(True)
        self._set_combo_data(self.language_combo, normalize_language_code(language_code))
        self.language_combo.blockSignals(False)

    def _retranslate_ui(self, _language_code: str) -> None:
        current_section = self.stack.currentIndex()
        for index, key in enumerate(self.SECTION_KEYS):
            self.section_selector.setItemText(index, tr(key))
            self.section_list.item(index).setText(tr(key))
        self.section_selector.setCurrentIndex(current_section)
        self.section_list.setCurrentRow(current_section)
        for label in self.findChildren(QLabel):
            key = label.property("translationKey")
            if key:
                label.setText(tr(str(key)))
        for button in self.findChildren(AppButton):
            key = button.property("translationKey")
            if key:
                button.setText(tr(str(key)))
        for name, (button, _swatches) in self._theme_buttons.items():
            button.setText(tr(THEME_LABEL_KEYS[name]))
        self.save_button.setText(tr("settings.save"))
        self.edit_theme_button.setText(tr("settings.appearance.edit_colors"))
        self.reset_widget_button.setText(tr("settings.widget.reset_position"))
        self.overrun_preview_button.setText(tr("action.show"))
        self.autostart_update_button.setText(tr("settings.tray.update_autostart"))
        self.profile_name.setPlaceholderText(tr("settings.profiles.name_placeholder"))
        self._retranslate_combo(self.widget_type, WIDGET_TYPES, WIDGET_TYPE_LABEL_KEYS)
        self._retranslate_combo(self.widget_size, WIDGET_SIZES, WIDGET_SIZE_LABEL_KEYS)
        self._retranslate_combo(self.overrun_effect, OVERRUN_EFFECTS, EFFECT_LABEL_KEYS)
        self._retranslate_combo(self.overrun_scope, OVERRUN_SCOPES, SCOPE_LABEL_KEYS)
        self._retranslate_combo(self.overrun_speed, OVERRUN_SPEEDS, SPEED_LABEL_KEYS)
        self._retranslate_combo(self.overrun_intensity, OVERRUN_INTENSITIES, INTENSITY_LABEL_KEYS)
        preview_keys = (
            "timer.mode.overwork",
            "timer.mode.short_break_overrun",
            "timer.mode.long_break_overrun",
        )
        for index, key in enumerate(preview_keys):
            self.overrun_preview_mode.setItemText(index, tr(key))
        for edit, source in self._message_sources.items():
            if source:
                edit.setText(tr(source))
        selected_profile = self._selected_profile_name()
        self._reload_profiles_list()
        if selected_profile is not None:
            for row in range(self.profiles_list.count()):
                if self.profiles_list.item(row).data(Qt.ItemDataRole.UserRole) == selected_profile:
                    self.profiles_list.setCurrentRow(row)
                    break
        if self.settings.active_profile == DEFAULT_PROFILE_NAME:
            self.profile_name.setText(tr("settings.profiles.default_name"))
        self.widget_description.setText(
            tr(WIDGET_TYPE_DESCRIPTIONS[str(self.widget_type.currentData())])
        )
        self._sync_autostart_controls()
        self._apply_responsive_layout()
        self.updateGeometry()

    @staticmethod
    def _retranslate_combo(combo: QComboBox, values, label_keys) -> None:
        current = combo.currentData()
        combo.blockSignals(True)
        for index, value in enumerate(values):
            combo.setItemText(index, tr(label_keys[value]))
        combo.setCurrentIndex(combo.findData(current))
        combo.blockSignals(False)


class SettingsWindow(QDialog):
    """Отдельное окно настроек для внешних вызовов."""

    def __init__(
        self,
        parent: QWidget,
        settings: AppSettings,
        on_save: Callable[[AppSettings, bool], None],
        theme_manager: ThemeManager,
    ) -> None:
        super().__init__(parent)
        self.window = self
        self.setWindowTitle(tr("settings.title"))
        self.setWindowIcon(application_icon())
        fit_window_to_available_screen(
            self, parent, preferred=(1040, 700), minimum=(760, 520),
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(SettingsView(self, settings, on_save, theme_manager=theme_manager))
        theme_manager.apply_to_window(self)
        localization_manager().language_changed.connect(self._retranslate_ui)

    def _retranslate_ui(self, _language_code: str) -> None:
        self.setWindowTitle(tr("settings.title"))
    SCOPE_LABEL_KEYS,
    SPEED_LABEL_KEYS,
