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
from app.overrun_effects import (
    LONG_BREAK_OVERRUN_KEY,
    OVERWORK_KEY,
    OVERRUN_EFFECTS,
    OVERRUN_INTENSITIES,
    OVERRUN_SCOPES,
    OVERRUN_SPEEDS,
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
    WIDGET_TYPE_DESCRIPTIONS,
    WIDGET_TYPES,
    normalize_widget_layouts,
    set_widget_layout_size,
)


class SettingsView(QWidget):
    """Единая форма настроек с навигацией и совместимыми callbacks."""

    SECTION_NAMES = (
        "Оформление", "Время", "Логика таймера", "Уведомления",
        "Виджет", "Превышение", "Профили", "Трей и автозапуск",
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
        theme_manager: ThemeManager | None = None,
    ) -> None:
        super().__init__(parent)
        if theme_manager is None:
            raise ValueError("SettingsView требует общий ThemeManager")
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
        self._build_ui()
        self._apply_responsive_layout()
        self._load_settings_to_form(settings)
        self._loading_form = False
        self._reload_profiles_list()

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(TOKENS.spacing.xl, TOKENS.spacing.xl, TOKENS.spacing.xl, TOKENS.spacing.lg)
        outer.setSpacing(TOKENS.spacing.lg)
        outer.addWidget(PageHeader("Настройки", "Изменения темы и виджета применяются сразу; остальные — после сохранения.", self))
        self.section_selector = QComboBox(self)
        self.section_selector.addItems(self.SECTION_NAMES)
        self.section_selector.setVisible(False)
        outer.addWidget(self.section_selector)
        body = QHBoxLayout()
        body.setSpacing(TOKENS.spacing.lg)
        self.section_list = QListWidget(self)
        self.section_list.setFixedWidth(210)
        self.section_list.addItems(self.SECTION_NAMES)
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
        save = AppButton("Сохранить настройки", self, variant="primary", theme_manager=self.theme_manager)
        save.clicked.connect(self._save)
        footer.addWidget(save)
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
        heading = QLabel(title, content)
        heading.setProperty("role", "sectionTitle")
        layout.addWidget(heading)
        if subtitle:
            label = QLabel(subtitle, content)
            label.setProperty("role", "subtitle")
            label.setWordWrap(True)
            layout.addWidget(label)
        scroll.setWidget(content)
        return scroll, content, layout

    def _build_theme_page(self) -> QWidget:
        scroll, content, layout = self._page("Оформление", "Полноценные палитры меняют все открытые окна без перезапуска.")
        grid = QGridLayout()
        grid.setSpacing(TOKENS.spacing.md)
        self._theme_grid = grid
        descriptions = {
            "Comet": "Спокойная нейтральная палитра",
            "Aurora": "Холодные синие и фиолетовые акценты",
            "Warm": "Мягкие песочные и тёплые поверхности",
            CUSTOM_THEME_NAME: "Ваши независимые светлая и тёмная палитры",
        }
        for index, name in enumerate(THEME_NAMES):
            button = AppButton(name, content, variant="secondary", theme_manager=self.theme_manager)
            button.setCheckable(True)
            button.clicked.connect(lambda _checked=False, selected=name: self._select_theme(selected))
            card = Card(content, padding=TOKENS.spacing.md)
            card.setMinimumWidth(250)
            card.content_layout.addWidget(button)
            description = QLabel(descriptions[name], card)
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
            "Тёмный режим", self.settings.appearance_mode == APPEARANCE_DARK,
            "ВЫКЛ — светлый режим, ВКЛ — тёмный.", self._appearance_changed,
        )
        layout.addWidget(self.appearance_switch)
        edit = AppButton("Настроить цвета", content, variant="primary", theme_manager=self.theme_manager)
        edit.clicked.connect(self._open_theme_editor)
        layout.addWidget(edit, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addStretch(1)
        return scroll

    def _build_time_page(self) -> QWidget:
        scroll, content, layout = self._page("Время", "Длительности применяются безопасно при сохранении.")
        card = Card(content)
        form = QFormLayout()
        self._configure_form(form)
        form.setSpacing(TOKENS.spacing.sm)
        self.work_minutes = self._spin(1, 240)
        self.short_break_minutes = self._spin(1, 240)
        self.long_break_minutes = self._spin(1, 240)
        self.time_format = QComboBox(card)
        self.time_format.addItems([item.value for item in TimeDisplayFormat])
        form.addRow("Работа, минут", self.work_minutes)
        form.addRow("Короткий отдых, минут", self.short_break_minutes)
        form.addRow("Длинный отдых, минут", self.long_break_minutes)
        form.addRow("Формат времени", self.time_format)
        card.content_layout.addLayout(form)
        layout.addWidget(card)
        layout.addStretch(1)
        return scroll

    def _build_logic_page(self) -> QWidget:
        scroll, content, layout = self._page("Логика таймера", "Порядок работы, короткого и длинного отдыха.")
        card = Card(content)
        self.use_long_break = self._switch("Использовать длинный отдых", True, "После заданного числа рабочих периодов.", self._update_long_break_controls)
        card.content_layout.addWidget(self.use_long_break)
        interval_row = QHBoxLayout()
        self.interval_label = QLabel("Рабочих периодов до длинного отдыха", card)
        self.long_break_interval = self._spin(1, 20)
        interval_row.addWidget(self.interval_label)
        interval_row.addStretch(1)
        interval_row.addWidget(self.long_break_interval)
        card.content_layout.addLayout(interval_row)
        layout.addWidget(card)
        layout.addStretch(1)
        return scroll

    def _build_notifications_page(self) -> QWidget:
        scroll, content, layout = self._page("Уведомления", "Ручной переход всегда можно завершить из главного окна или виджета.")
        card = Card(content)
        self.notifications_enabled = self._switch("Уведомления", True)
        self.notification_sound = self._switch("Звук уведомлений", True)
        self.auto_start = self._switch("Автоматический переход", True, "ВКЛ — следующий период запускается сразу; ВЫКЛ — считается превышение.")
        for row in (self.notifications_enabled, self.notification_sound, self.auto_start):
            card.content_layout.addWidget(row)
        form = QFormLayout()
        self._configure_form(form)
        self.work_message = QLineEdit(card)
        self.short_message = QLineEdit(card)
        self.long_message = QLineEdit(card)
        form.addRow("Конец работы", self.work_message)
        form.addRow("Конец короткого отдыха", self.short_message)
        form.addRow("Конец длинного отдыха", self.long_message)
        card.content_layout.addLayout(form)
        layout.addWidget(card)
        layout.addStretch(1)
        return scroll

    def _build_widget_page(self) -> QWidget:
        scroll, content, layout = self._page("Плавающий виджет", "Видимость управляется переключателем на странице таймера.")
        card = Card(content)
        form = QFormLayout()
        self._configure_form(form)
        self.widget_type = QComboBox(card)
        self.widget_type.addItems(WIDGET_TYPES)
        self.widget_type.currentTextChanged.connect(self._widget_type_changed)
        self.widget_size = QComboBox(card)
        self.widget_size.addItems(WIDGET_SIZES)
        self.widget_size.currentTextChanged.connect(self._widget_size_changed)
        form.addRow("Тип виджета", self.widget_type)
        form.addRow("Размер", self.widget_size)
        card.content_layout.addLayout(form)
        self.widget_description = QLabel("", card)
        self.widget_description.setProperty("role", "caption")
        self.widget_description.setWordWrap(True)
        card.content_layout.addWidget(self.widget_description)
        opacity_row = QHBoxLayout()
        opacity_row.addWidget(QLabel("Непрозрачность виджета", card))
        self.widget_opacity = QSlider(Qt.Orientation.Horizontal, card)
        self.widget_opacity.setRange(MIN_WIDGET_OPACITY, 100)
        self.widget_opacity.valueChanged.connect(self._widget_opacity_changed)
        opacity_row.addWidget(self.widget_opacity, 1)
        self.widget_opacity_label = QLabel("100%", card)
        self.widget_opacity_label.setMinimumWidth(48)
        opacity_row.addWidget(self.widget_opacity_label)
        card.content_layout.addLayout(opacity_row)
        caption = QLabel("Чем ниже значение, тем прозрачнее виджет. Минимум — 5%.", card)
        caption.setProperty("role", "caption")
        card.content_layout.addWidget(caption)
        self.widget_topmost = self._switch("Поверх всех окон", True, callback=lambda _enabled: self._apply_widget_configuration())
        card.content_layout.addWidget(self.widget_topmost)
        reset = AppButton("Сбросить позицию текущего типа", card, theme_manager=self.theme_manager)
        reset.clicked.connect(self._reset_widget_position)
        card.content_layout.addWidget(reset, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(card)
        layout.addStretch(1)
        return scroll

    def _build_overrun_page(self) -> QWidget:
        scroll, content, layout = self._page("Индикация превышения", "Один общий кадр применяется к главному окну и открытому виджету.")
        card = Card(content)
        form = QFormLayout()
        self._configure_form(form)
        self.overrun_effect = self._combo(OVERRUN_EFFECTS)
        self.overrun_scope = self._combo(OVERRUN_SCOPES)
        self.overrun_speed = self._combo(OVERRUN_SPEEDS)
        self.overrun_intensity = self._combo(OVERRUN_INTENSITIES)
        form.addRow("Основной эффект", self.overrun_effect)
        form.addRow("Область изменения цвета", self.overrun_scope)
        form.addRow("Скорость", self.overrun_speed)
        form.addRow("Интенсивность", self.overrun_intensity)
        card.content_layout.addLayout(form)
        self.overrun_color_enabled = self._switch("Изменять цвет таймера", True)
        self.overrun_animations = self._switch("Разрешить движение эффектов", True)
        self.overrun_opaque_widget = self._switch("Делать виджет непрозрачным при превышении", False, callback=self._overrun_opacity_changed)
        for row in (self.overrun_color_enabled, self.overrun_animations, self.overrun_opaque_widget):
            card.content_layout.addWidget(row)
        layout.addWidget(card)

        colors = Card(content)
        colors_title = QLabel("Отдельные цвета", colors)
        colors_title.setProperty("role", "sectionTitle")
        colors.content_layout.addWidget(colors_title)
        self.overrun_color_edits = {}
        self.overrun_color_swatches = {}
        for key, label in ((OVERWORK_KEY, "Переработка"), (SHORT_BREAK_OVERRUN_KEY, "Короткий отдых сверх нормы"), (LONG_BREAK_OVERRUN_KEY, "Длинный отдых сверх нормы")):
            color_row = QWidget(colors)
            color_flow = FlowLayout(color_row, horizontal_spacing=TOKENS.spacing.sm, vertical_spacing=TOKENS.spacing.xs)
            color_label = QLabel(label, color_row)
            color_label.setMinimumWidth(220)
            color_flow.addWidget(color_label)
            swatch = ColorSwatch("#000000", colors)
            swatch.clicked.connect(lambda _checked=False, selected=key: self._choose_overrun_color(selected))
            color_flow.addWidget(swatch)
            edit = QLineEdit(colors)
            edit.setMinimumWidth(140)
            edit.setMaxLength(7)
            edit.textChanged.connect(lambda value, selected=key: self._overrun_color_changed(selected, value))
            color_flow.addWidget(edit)
            choose = AppButton("Выбрать", colors, variant="ghost", theme_manager=self.theme_manager)
            choose.clicked.connect(lambda _checked=False, selected=key: self._choose_overrun_color(selected))
            color_flow.addWidget(choose)
            themed = AppButton("По теме", colors, variant="ghost", theme_manager=self.theme_manager)
            themed.clicked.connect(lambda _checked=False, selected=key: self._reset_overrun_color(selected))
            color_flow.addWidget(themed)
            self.overrun_color_edits[key] = edit
            self.overrun_color_swatches[key] = swatch
            colors.content_layout.addWidget(color_row)
        layout.addWidget(colors)
        preview_card = Card(content, padding=TOKENS.spacing.md)
        preview_row = FlowLayout(horizontal_spacing=TOKENS.spacing.sm)
        preview_row.addWidget(QLabel("Предпросмотр", preview_card))
        self.overrun_preview_mode = self._combo(("Переработка", "Короткий отдых сверх нормы", "Длинный отдых сверх нормы"))
        self.overrun_preview_mode.setMinimumWidth(260)
        preview_row.addWidget(self.overrun_preview_mode)
        preview = AppButton("Показать", preview_card, variant="primary", theme_manager=self.theme_manager)
        preview.clicked.connect(self._preview_overrun)
        preview_row.addWidget(preview)
        preview_card.content_layout.addLayout(preview_row)
        layout.addWidget(preview_card)
        layout.addStretch(1)
        return scroll

    def _build_profiles_page(self) -> QWidget:
        scroll, content, layout = self._page("Профили", "Сохраняйте наборы длительностей, оформления и виджета.")
        card = Card(content)
        self.profile_name = QLineEdit(card)
        self.profile_name.setPlaceholderText("Имя профиля")
        card.content_layout.addWidget(self.profile_name)
        self.profiles_list = QListWidget(card)
        self.profiles_list.currentTextChanged.connect(self.profile_name.setText)
        card.content_layout.addWidget(self.profiles_list, 1)
        buttons = FlowLayout(horizontal_spacing=TOKENS.spacing.sm)
        for text, callback, variant in (
            ("Сохранить профиль", self._save_profile, "primary"),
            ("Применить профиль", self._apply_selected_profile, "secondary"),
            ("Удалить профиль", self._delete_selected_profile, "danger"),
            ("Настройки по умолчанию", self._restore_default_settings, "secondary"),
            ("Вернуть мои настройки", self._restore_personal_settings, "ghost"),
        ):
            button = AppButton(text, card, variant=variant, theme_manager=self.theme_manager)
            button.clicked.connect(callback)
            buttons.addWidget(button)
        card.content_layout.addLayout(buttons)
        layout.addWidget(card)
        layout.addStretch(1)
        return scroll

    def _build_tray_page(self) -> QWidget:
        scroll, content, layout = self._page("Трей и автозапуск", "Системный трей работает в общем GUI-потоке Qt.")
        card = Card(content)
        self.minimize_start = self._switch("Сворачивать программу после запуска", False)
        self.close_to_tray = self._switch("При закрытии сворачивать в трей", True)
        self.autostart_switch = self._switch("Автозапуск вместе с Windows", False, callback=self._autostart_toggled)
        for row in (self.minimize_start, self.close_to_tray, self.autostart_switch):
            card.content_layout.addWidget(row)
        self.autostart_status_label = QLabel("", card)
        self.autostart_status_label.setProperty("role", "caption")
        self.autostart_status_label.setWordWrap(True)
        card.content_layout.addWidget(self.autostart_status_label)
        self.autostart_update_button = AppButton("Обновить путь автозапуска", card, theme_manager=self.theme_manager)
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
            QMessageBox.warning(self, "Пользовательская тема", "Редактор недоступен в этом окне.")
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
        color = QColorDialog.getColor(QColor(self.overrun_color_edits[key].text()), self, "Цвет превышения")
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
            QMessageBox.warning(self, "Индикация превышения", "Некорректные цвета заменены значениями активной темы.")
        self.overrun_visual = normalize_overrun_visual({
            "effect": self.overrun_effect.currentText(),
            "color_enabled": self.overrun_color_enabled.isChecked(),
            "scope": self.overrun_scope.currentText(),
            "speed": self.overrun_speed.currentText(),
            "intensity": self.overrun_intensity.currentText(),
            "animations_enabled": self.overrun_animations.isChecked(),
            "opaque_widget_during_overrun": self.overrun_opaque_widget.isChecked(),
            "colors": self.overrun_color_overrides,
        })
        self._refresh_overrun_colors()
        return deepcopy(self.overrun_visual)

    def _preview_overrun(self) -> None:
        if self.on_overrun_preview is None:
            return
        modes = {"Переработка": TimerMode.WORK, "Короткий отдых сверх нормы": TimerMode.SHORT_BREAK, "Длинный отдых сверх нормы": TimerMode.LONG_BREAK}
        self.on_overrun_preview(modes[self.overrun_preview_mode.currentText()], self._read_overrun_visual(warn=True))

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

    def _widget_type_changed(self, widget_type: str) -> None:
        if widget_type not in self.widget_layouts:
            return
        self.widget_size.blockSignals(True)
        self.widget_size.setCurrentText(str(self.widget_layouts[widget_type]["size"]))
        self.widget_size.blockSignals(False)
        self.widget_description.setText(WIDGET_TYPE_DESCRIPTIONS[widget_type])
        self._apply_widget_configuration()

    def _widget_size_changed(self, _size: str) -> None:
        if hasattr(self, "widget_type"):
            self._remember_widget_size_selection()
            self._apply_widget_configuration()

    def _apply_widget_configuration(self) -> None:
        if self._loading_form or self.on_widget_configuration_change is None:
            return
        widget_type = self.widget_type.currentText()
        if widget_type not in self.widget_layouts:
            return
        self.on_widget_configuration_change(
            widget_type,
            self.widget_size.currentText(),
            deepcopy(self.widget_layouts),
            self.widget_topmost.isChecked(),
        )

    def _remember_widget_size_selection(self) -> None:
        widget_type = self.widget_type.currentText()
        if widget_type not in WIDGET_TYPES:
            return
        self.widget_layouts = normalize_widget_layouts(self.widget_layouts, active_type=widget_type)
        self.widget_layouts = set_widget_layout_size(self.widget_layouts, widget_type, self.widget_size.currentText())

    def _reset_widget_position(self) -> None:
        widget_type = self.widget_type.currentText()
        self.widget_layouts[widget_type]["x"] = DEFAULT_WIDGET_X
        self.widget_layouts[widget_type]["y"] = DEFAULT_WIDGET_Y
        self._apply_widget_configuration()
        QMessageBox.information(self, "Виджет", "Позиция текущего типа сброшена.")

    def sync_widget_layouts(self, settings: AppSettings) -> None:
        self.widget_layouts[settings.widget_type] = deepcopy(settings.widget_layouts[settings.widget_type])
        if self.widget_type.currentText() == settings.widget_type:
            self.widget_size.setCurrentText(settings.widget_size)

    def _update_long_break_controls(self, enabled: bool | None = None) -> None:
        state = self.use_long_break.isChecked() if enabled is None else bool(enabled)
        self.interval_label.setEnabled(state)
        self.long_break_interval.setEnabled(state)

    def _autostart_status_text(self) -> str:
        if self.autostart_status == AUTOSTART_ENABLED_CURRENT:
            return "Автозапуск включён и указывает на текущую папку программы."
        if self.autostart_status == AUTOSTART_ENABLED_STALE:
            return "Путь автозапуска устарел. Обновите его после перемещения программы."
        if not is_frozen_app():
            return "Запуск из Python: включение автозапуска доступно в exe-версии."
        return "Автозапуск выключен."

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
        self.profiles_list.addItems(self.profiles.names())

    def _selected_profile_name(self) -> str | None:
        item = self.profiles_list.currentItem()
        return item.text() if item is not None else None

    def _save_profile(self) -> None:
        name = self.profile_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Профиль", "Введите имя профиля.")
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
            QMessageBox.warning(self, "Профиль", "Выберите профиль из списка.")
            return
        settings = self.profiles.settings_from_profile(profile)
        settings.widget_enabled = self.settings.widget_enabled
        self._load_settings_to_form(settings)
        self.on_save(settings, False)
        self.settings = settings

    def _delete_selected_profile(self) -> None:
        name = self._selected_profile_name()
        if not name:
            return
        if name == DEFAULT_PROFILE_NAME:
            QMessageBox.warning(self, "Профиль", "Стандартный профиль удалить нельзя.")
            return
        if QMessageBox.question(self, "Удалить профиль", f"Удалить профиль «{name}»?") == QMessageBox.StandardButton.Yes:
            self.profiles.delete_profile(name)
            self._reload_profiles_list()

    def _restore_default_settings(self) -> None:
        settings = self.profiles.default_settings()
        settings.widget_enabled = self.settings.widget_enabled
        self._load_settings_to_form(settings)
        self.on_save(settings, False)
        self.settings = settings

    def _restore_personal_settings(self) -> None:
        settings = deepcopy(self.personal_settings)
        settings.widget_enabled = self.settings.widget_enabled
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
        widget_type = self.widget_type.currentText()
        active_layout = self.widget_layouts[widget_type]
        return AppSettings(
            active_profile=active_profile or self.settings.active_profile,
            work_minutes=self.work_minutes.value(), short_break_minutes=self.short_break_minutes.value(), long_break_minutes=self.long_break_minutes.value(),
            notifications_enabled=self.notifications_enabled.isChecked(), notification_sound_enabled=self.notification_sound.isChecked(),
            work_end_message=self.work_message.text().strip(), short_break_end_message=self.short_message.text().strip(), long_break_end_message=self.long_message.text().strip(),
            autostart_enabled=self.autostart_switch.isChecked(), use_long_break=self.use_long_break.isChecked(), long_break_interval=self.long_break_interval.value(),
            auto_start_next_period=self.auto_start.isChecked(), time_display_format=self.time_format.currentText(),
            minimize_to_tray_on_start=self.minimize_start.isChecked(), close_to_tray=self.close_to_tray.isChecked(),
            theme_name=self.current_theme_name, appearance_mode=self.current_appearance_mode,
            custom_theme=deepcopy(self.custom_theme), overrun_visual=self._read_overrun_visual(warn=True),
            widget_enabled=self.settings.widget_enabled, widget_type=widget_type, widget_size=self.widget_size.currentText(), widget_layouts=deepcopy(self.widget_layouts),
            widget_background_color=self.settings.widget_background_color, widget_text_color=self.settings.widget_text_color,
            widget_opacity=self.widget_opacity.value(), widget_always_on_top=self.widget_topmost.isChecked(),
            widget_x=int(active_layout["x"]), widget_y=int(active_layout["y"]),
            main_window_geometry=deepcopy(self.settings.main_window_geometry),
        )

    def _load_settings_to_form(self, settings: AppSettings) -> None:
        self.profile_name.setText(settings.active_profile)
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
        self.work_message.setText(settings.work_end_message)
        self.short_message.setText(settings.short_break_end_message)
        self.long_message.setText(settings.long_break_end_message)
        self.custom_theme = deepcopy(settings.custom_theme)
        self._set_theme_controls(settings.theme_name, settings.appearance_mode)
        self.overrun_visual = normalize_overrun_visual(settings.overrun_visual)
        self.overrun_effect.setCurrentText(str(self.overrun_visual["effect"]))
        self.overrun_color_enabled.setChecked(bool(self.overrun_visual["color_enabled"]))
        self.overrun_scope.setCurrentText(str(self.overrun_visual["scope"]))
        self.overrun_speed.setCurrentText(str(self.overrun_visual["speed"]))
        self.overrun_intensity.setCurrentText(str(self.overrun_visual["intensity"]))
        self.overrun_animations.setChecked(bool(self.overrun_visual["animations_enabled"]))
        self.overrun_opaque_widget.setChecked(bool(self.overrun_visual["opaque_widget_during_overrun"]))
        self.overrun_color_overrides = deepcopy(self.overrun_visual["colors"])
        self.widget_layouts = deepcopy(settings.widget_layouts)
        self.widget_type.setCurrentText(settings.widget_type)
        self.widget_size.setCurrentText(settings.widget_size)
        self.widget_description.setText(WIDGET_TYPE_DESCRIPTIONS[settings.widget_type])
        self.sync_widget_opacity(settings.widget_opacity)
        self.widget_topmost.setChecked(settings.widget_always_on_top)
        self._update_long_break_controls()
        self._refresh_theme_previews()
        self._refresh_overrun_colors()
        self._sync_autostart_controls()


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
        self.setWindowTitle("Настройки")
        self.setWindowIcon(application_icon())
        fit_window_to_available_screen(
            self, parent, preferred=(1040, 700), minimum=(760, 520),
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(SettingsView(self, settings, on_save, theme_manager=theme_manager))
        theme_manager.apply_to_window(self)
