"""Настройки таймера, уведомлений, виджета, профилей, трея и автозапуска."""

from copy import deepcopy
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from app.autostart import (
    AUTOSTART_DISABLED,
    AUTOSTART_ENABLED_CURRENT,
    AUTOSTART_ENABLED_STALE,
)
from app.config import DEFAULT_PROFILE_NAME, PROFILES_FILE, is_frozen_app
from app.models import AppSettings, TimeDisplayFormat
from app.profiles import ProfilesService
from app.theme import (
    APPEARANCE_DARK,
    APPEARANCE_LABELS,
    APPEARANCE_LIGHT,
    THEME_NAMES,
    get_palette,
    normalize_appearance_mode,
    normalize_theme_name,
)
from app.widget_settings import (
    DEFAULT_WIDGET_X,
    DEFAULT_WIDGET_Y,
    MIN_WIDGET_OPACITY,
    WIDGET_SIZES,
    WIDGET_TYPES,
    normalize_widget_layouts,
    set_widget_layout_size,
)


class SettingsView(ttk.Frame):
    """Вкладка настроек с внутренними разделами."""

    def __init__(
        self,
        parent: tk.Widget,
        settings: AppSettings,
        on_save: Callable[[AppSettings, bool], None],
        autostart_status: str = AUTOSTART_DISABLED,
        on_theme_change: Callable[[str, str], None] | None = None,
    ) -> None:
        """Создает вкладку настроек и загружает профили."""
        super().__init__(parent, padding=12)
        self.settings = settings
        self.personal_settings = settings
        self.on_save = on_save
        self.on_theme_change = on_theme_change
        self.autostart_status = autostart_status
        self.profiles = ProfilesService(PROFILES_FILE)

        self.profile_name_var = tk.StringVar(value=settings.active_profile)
        self.work_minutes_var = tk.IntVar(value=settings.work_minutes)
        self.short_break_minutes_var = tk.IntVar(value=settings.short_break_minutes)
        self.long_break_minutes_var = tk.IntVar(value=settings.long_break_minutes)
        self.use_long_break_var = tk.BooleanVar(value=settings.use_long_break)
        self.long_break_interval_var = tk.IntVar(value=settings.long_break_interval)
        self.time_display_format_var = tk.StringVar(value=settings.time_display_format)
        self.minimize_to_tray_on_start_var = tk.BooleanVar(value=settings.minimize_to_tray_on_start)
        self.close_to_tray_var = tk.BooleanVar(value=settings.close_to_tray)
        self.autostart_enabled_var = tk.BooleanVar(value=settings.autostart_enabled)
        self.notifications_enabled_var = tk.BooleanVar(value=settings.notifications_enabled)
        self.notification_sound_enabled_var = tk.BooleanVar(value=settings.notification_sound_enabled)
        self.auto_start_next_period_var = tk.BooleanVar(value=settings.auto_start_next_period)
        self.work_end_message_var = tk.StringVar(value=settings.work_end_message)
        self.short_break_end_message_var = tk.StringVar(value=settings.short_break_end_message)
        self.long_break_end_message_var = tk.StringVar(value=settings.long_break_end_message)
        self.theme_name_var = tk.StringVar(value=settings.theme_name)
        self.appearance_mode_var = tk.StringVar(value=settings.appearance_mode)
        self.widget_type_var = tk.StringVar(value=settings.widget_type)
        self.widget_size_var = tk.StringVar(value=settings.widget_size)
        self.widget_layouts = deepcopy(settings.widget_layouts)
        self.widget_opacity_var = tk.IntVar(value=settings.widget_opacity)
        self.widget_always_on_top_var = tk.BooleanVar(value=settings.widget_always_on_top)
        self.autostart_status_label: ttk.Label | None = None
        self.autostart_checkbutton: ttk.Checkbutton | None = None
        self.autostart_update_button: ttk.Button | None = None
        self.theme_previews: dict[str, tuple[tk.Frame, list[tk.Label]]] = {}

        self._build_ui()
        self._reload_profiles_list()
        self._update_long_break_controls()

    def _build_ui(self) -> None:
        """Создает внутренние вкладки настроек и нижнюю панель сохранения."""
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True)

        theme_tab = ttk.Frame(notebook, padding=18)
        time_tab = ttk.Frame(notebook, padding=16)
        logic_tab = ttk.Frame(notebook, padding=16)
        notifications_tab = ttk.Frame(notebook, padding=16)
        widget_tab = ttk.Frame(notebook, padding=16)
        profiles_tab = ttk.Frame(notebook, padding=16)
        tray_tab = ttk.Frame(notebook, padding=16)

        notebook.add(theme_tab, text="Оформление")
        notebook.add(time_tab, text="Время")
        notebook.add(logic_tab, text="Логика таймера")
        notebook.add(notifications_tab, text="Уведомления")
        notebook.add(widget_tab, text="Виджет")
        notebook.add(profiles_tab, text="Профили")
        notebook.add(tray_tab, text="Трей и автозапуск")

        self._build_theme_settings(theme_tab)
        self._build_time_settings(time_tab)
        self._build_logic_settings(logic_tab)
        self._build_notification_settings(notifications_tab)
        self._build_widget_settings(widget_tab)
        self._build_profiles_settings(profiles_tab)
        self._build_tray_settings(tray_tab)

        footer = ttk.Frame(self)
        footer.pack(fill=tk.X, pady=(12, 0))
        ttk.Button(footer, text="Сохранить настройки", command=self._save).pack(side=tk.RIGHT)

    def _build_theme_settings(self, parent: ttk.Frame) -> None:
        """Создает карточки готовых палитр и переключатель светлого/тёмного режима."""
        ttk.Label(parent, text="Цветовая тема", style="Heading.TLabel").grid(
            row=0,
            column=0,
            columnspan=3,
            sticky=tk.W,
            pady=(0, 12),
        )
        descriptions = {
            "Comet": "Нейтральная и спокойная",
            "Aurora": "Холодная с сине-фиолетовым акцентом",
            "Warm": "Мягкая тёплая палитра",
        }
        for column, theme_name in enumerate(THEME_NAMES):
            card = ttk.LabelFrame(parent, text=theme_name, padding=12)
            card.grid(row=1, column=column, sticky=tk.NSEW, padx=(0, 10), pady=(0, 16))
            ttk.Radiobutton(
                card,
                text="Выбрать",
                value=theme_name,
                variable=self.theme_name_var,
                command=self._on_theme_selection,
                style="Card.TRadiobutton",
            ).pack(anchor=tk.W)
            ttk.Label(
                card,
                text=descriptions[theme_name],
                style="Card.Secondary.TLabel",
                wraplength=180,
            ).pack(anchor=tk.W, pady=(3, 9))
            preview = tk.Frame(card, borderwidth=0, highlightthickness=0)
            preview.pack(fill=tk.X)
            swatches: list[tk.Label] = []
            for _index in range(4):
                swatch = tk.Label(preview, text="", width=4, height=1, borderwidth=0)
                swatch.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 3))
                swatches.append(swatch)
            self.theme_previews[theme_name] = (preview, swatches)
            parent.columnconfigure(column, weight=1)

        mode_card = ttk.Frame(parent, style="Card.TFrame", padding=14)
        mode_card.grid(row=2, column=0, columnspan=3, sticky=tk.EW)
        ttk.Label(mode_card, text="Режим:", style="Card.TLabel").pack(side=tk.LEFT, padx=(0, 12))
        for mode in (APPEARANCE_LIGHT, APPEARANCE_DARK):
            ttk.Radiobutton(
                mode_card,
                text=APPEARANCE_LABELS[mode],
                value=mode,
                variable=self.appearance_mode_var,
                command=self._on_theme_selection,
                style="Card.TRadiobutton",
            ).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(
            parent,
            text="Тема применяется сразу ко всем открытым окнам и не влияет на таймер.",
            style="Secondary.TLabel",
        ).grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=(12, 0))
        self._refresh_theme_previews()

    def _build_time_settings(self, parent: ttk.Frame) -> None:
        """Группа настроек длительности и формата времени."""
        self._add_spinbox(parent, "Работа, минут:", self.work_minutes_var, 0)
        self._add_spinbox(parent, "Короткий отдых, минут:", self.short_break_minutes_var, 1)
        self._add_spinbox(parent, "Длинный отдых, минут:", self.long_break_minutes_var, 2)
        ttk.Label(parent, text="Формат времени:").grid(row=3, column=0, sticky=tk.W, pady=6)
        ttk.Combobox(
            parent,
            values=[format_item.value for format_item in TimeDisplayFormat],
            textvariable=self.time_display_format_var,
            state="readonly",
            width=12,
        ).grid(row=3, column=1, sticky=tk.W, pady=6)
        ttk.Label(
            parent,
            text="Формат применяется в главном окне и в виджете.",
        ).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(8, 0))

    def _build_logic_settings(self, parent: ttk.Frame) -> None:
        """Группа настроек порядка периодов."""
        ttk.Checkbutton(
            parent,
            text="Использовать длинный отдых",
            variable=self.use_long_break_var,
            command=self._update_long_break_controls,
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=6)
        self.interval_label = ttk.Label(parent, text="Рабочих периодов до длинного отдыха:")
        self.interval_label.grid(row=1, column=0, sticky=tk.W, pady=6)
        self.interval_spinbox = ttk.Spinbox(
            parent,
            from_=1,
            to=20,
            width=6,
            textvariable=self.long_break_interval_var,
        )
        self.interval_spinbox.grid(row=1, column=1, sticky=tk.W, pady=6)

    def _build_notification_settings(self, parent: ttk.Frame) -> None:
        """Группа уведомлений и поведения после завершения периода."""
        ttk.Checkbutton(parent, text="Уведомления включены", variable=self.notifications_enabled_var).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=6)
        ttk.Checkbutton(parent, text="Звук включен", variable=self.notification_sound_enabled_var).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=6)
        ttk.Checkbutton(parent, text="Автоматически переходить к следующему периоду", variable=self.auto_start_next_period_var).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=6)
        ttk.Label(
            parent,
            text=(
                "Автопереход сразу запускает следующий период без учета превышения.\n"
                "Ручной переход считает превышение до кнопки «Продолжить» "
                "в уведомлении или главном окне."
            ),
        ).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(4, 12))
        self._add_entry(parent, "Конец работы:", self.work_end_message_var, 4, width=48)
        self._add_entry(parent, "Конец короткого отдыха:", self.short_break_end_message_var, 5, width=48)
        self._add_entry(parent, "Конец длинного отдыха:", self.long_break_end_message_var, 6, width=48)

    def _build_widget_settings(self, parent: ttk.Frame) -> None:
        """Группа настроек плавающего виджета."""
        ttk.Label(parent, text="Тип виджета:").grid(row=0, column=0, sticky=tk.W, pady=6)
        type_box = ttk.Combobox(
            parent,
            values=WIDGET_TYPES,
            textvariable=self.widget_type_var,
            state="readonly",
            width=18,
        )
        type_box.grid(row=0, column=1, sticky=tk.W, pady=6)
        type_box.bind("<<ComboboxSelected>>", self._on_widget_type_selected)
        ttk.Label(parent, text="Размер виджета:").grid(row=1, column=0, sticky=tk.W, pady=6)
        size_box = ttk.Combobox(
            parent,
            values=WIDGET_SIZES,
            textvariable=self.widget_size_var,
            state="readonly",
            width=18,
        )
        size_box.grid(row=1, column=1, sticky=tk.W, pady=6)
        size_box.bind("<<ComboboxSelected>>", self._on_widget_size_selected)
        ttk.Label(parent, text="Прозрачность, %:").grid(row=2, column=0, sticky=tk.W, pady=6)
        ttk.Scale(parent, from_=MIN_WIDGET_OPACITY, to=100, variable=self.widget_opacity_var, orient=tk.HORIZONTAL, length=180).grid(row=2, column=1, sticky=tk.W, pady=6)
        ttk.Checkbutton(parent, text="Поверх всех окон", variable=self.widget_always_on_top_var).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=6)
        ttk.Button(parent, text="Сбросить позицию текущего типа", command=self._reset_widget_position).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(12, 0))
        ttk.Label(
            parent,
            text=(
                "После сохранения вид меняется без перезапуска и сброса таймера.\n"
                "Ручное изменение окна автоматически выбирает размер «Пользовательский»."
            ),
        ).grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(8, 0))
        ttk.Label(
            parent,
            text="Цвета виджета задаются выбранной темой оформления.",
            style="Secondary.TLabel",
        ).grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(8, 0))

    def _build_profiles_settings(self, parent: ttk.Frame) -> None:
        """Группа управления профилями."""
        ttk.Label(parent, text="Имя профиля:").grid(row=0, column=0, sticky=tk.W, pady=6)
        ttk.Entry(parent, textvariable=self.profile_name_var, width=32).grid(row=1, column=0, sticky=tk.EW, pady=(0, 8))
        self.profiles_listbox = tk.Listbox(parent, height=9, width=36, exportselection=False)
        self.profiles_listbox.grid(row=2, column=0, rowspan=5, sticky=tk.NSEW, padx=(0, 12))
        self.profiles_listbox.bind("<<ListboxSelect>>", self._on_profile_selected)
        ttk.Button(parent, text="Сохранить профиль", command=self._save_profile).grid(row=2, column=1, sticky=tk.EW, pady=3)
        ttk.Button(parent, text="Применить профиль", command=self._apply_selected_profile).grid(row=3, column=1, sticky=tk.EW, pady=3)
        ttk.Button(parent, text="Удалить профиль", command=self._delete_selected_profile).grid(row=4, column=1, sticky=tk.EW, pady=3)
        ttk.Button(parent, text="Вернуть настройки по умолчанию", command=self._restore_default_settings).grid(row=5, column=1, sticky=tk.EW, pady=3)
        ttk.Button(parent, text="Вернуть мои настройки", command=self._restore_personal_settings).grid(row=6, column=1, sticky=tk.EW, pady=3)

    def _build_tray_settings(self, parent: ttk.Frame) -> None:
        """Группа настроек трея и автозапуска."""
        ttk.Checkbutton(parent, text="Сворачивать программу после запуска", variable=self.minimize_to_tray_on_start_var).grid(row=0, column=0, sticky=tk.W, pady=6)
        ttk.Checkbutton(parent, text="При закрытии сворачивать в трей", variable=self.close_to_tray_var).grid(row=1, column=0, sticky=tk.W, pady=6)
        self.autostart_checkbutton = ttk.Checkbutton(
            parent,
            text="Включить автозапуск вместе с Windows",
            variable=self.autostart_enabled_var,
        )
        self.autostart_checkbutton.grid(row=2, column=0, sticky=tk.W, pady=6)
        self.autostart_status_label = ttk.Label(parent, text=self._autostart_status_text())
        self.autostart_status_label.grid(row=3, column=0, sticky=tk.W, pady=(8, 0))
        self.autostart_update_button = ttk.Button(
            parent,
            text="Обновить автозапуск",
            command=self._update_autostart,
        )
        self.autostart_update_button.grid(row=4, column=0, sticky=tk.W, pady=(8, 0))
        ttk.Label(
            parent,
            text="Автозапуск создается только для текущего пользователя. В exe-версии он указывает на текущий файл программы.",
        ).grid(row=5, column=0, sticky=tk.W, pady=(8, 0))
        self._sync_autostart_controls()

    def update_autostart_status(self, status: str) -> None:
        """Обновляет подпись автозапуска после сохранения настроек."""
        self.autostart_status = status
        if self.autostart_status_label is not None:
            self.autostart_status_label.config(text=self._autostart_status_text())
        self._sync_autostart_controls()

    def sync_widget_layouts(self, settings: AppSettings) -> None:
        """Принимает отложенно сохраненный ручной размер активного виджета."""
        widget_type = settings.widget_type
        self.widget_layouts[widget_type] = deepcopy(
            settings.widget_layouts[widget_type],
        )
        if self.widget_type_var.get() == widget_type:
            self.widget_size_var.set(settings.widget_size)

    def sync_theme(self, theme_name: str, appearance_mode: str) -> None:
        """Синхронизирует карточки с быстрым переключателем главного окна."""
        self.theme_name_var.set(normalize_theme_name(theme_name))
        self.appearance_mode_var.set(normalize_appearance_mode(appearance_mode))
        self._refresh_theme_previews()

    def _on_theme_selection(self) -> None:
        """Применяет выбор карточки сразу, не ожидая сохранения всей формы."""
        theme_name = normalize_theme_name(self.theme_name_var.get())
        appearance_mode = normalize_appearance_mode(self.appearance_mode_var.get())
        self.theme_name_var.set(theme_name)
        self.appearance_mode_var.set(appearance_mode)
        self._refresh_theme_previews()
        if self.on_theme_change is not None:
            self.on_theme_change(theme_name, appearance_mode)

    def _refresh_theme_previews(self) -> None:
        """Показывает четыре смысловых цвета каждой темы в активном режиме."""
        mode = normalize_appearance_mode(self.appearance_mode_var.get())
        for theme_name, (preview, swatches) in self.theme_previews.items():
            palette = get_palette(theme_name, mode)
            preview.configure(background=palette.card_background)
            colors = (
                palette.background,
                palette.card_background,
                palette.accent,
                palette.text_primary,
            )
            for swatch, color in zip(swatches, colors, strict=True):
                swatch.configure(background=color)

    def _autostart_status_text(self) -> str:
        """Возвращает понятное описание текущего состояния автозапуска."""
        if self.autostart_status == AUTOSTART_ENABLED_CURRENT:
            return "Автозапуск включен и указывает на текущую папку программы."
        if self.autostart_status == AUTOSTART_ENABLED_STALE:
            return "Автозапуск включен, но путь устарел. Сохраните настройку, чтобы обновить ярлык."
        if not is_frozen_app() and self.autostart_status == AUTOSTART_DISABLED:
            return "Сейчас программа запущена из Python. Автозапуск по умолчанию доступен для exe-версии."
        return "Автозапуск выключен."

    def _sync_autostart_controls(self) -> None:
        """Отключает галочку автозапуска при запуске из исходников."""
        if self.autostart_checkbutton is None:
            return
        state = tk.NORMAL if is_frozen_app() else tk.DISABLED
        self.autostart_checkbutton.config(state=state)
        if self.autostart_update_button is not None:
            button_state = tk.NORMAL if is_frozen_app() and self.autostart_status == AUTOSTART_ENABLED_STALE else tk.DISABLED
            self.autostart_update_button.config(state=button_state)

    def _update_autostart(self) -> None:
        """Forces rewriting autostart when the stored exe path is stale."""
        settings = self._settings_from_form(active_profile=self.profile_name_var.get().strip())
        settings.autostart_enabled = True
        self.autostart_enabled_var.set(True)
        self.on_save(settings, True)
        self.settings = settings

    def _add_spinbox(self, parent: ttk.Frame, text: str, variable: tk.IntVar, row: int) -> None:
        """Добавляет строку с числовым полем."""
        ttk.Label(parent, text=text).grid(row=row, column=0, sticky=tk.W, pady=6)
        ttk.Spinbox(parent, from_=1, to=240, width=6, textvariable=variable).grid(row=row, column=1, sticky=tk.W, pady=6)

    def _add_entry(self, parent: ttk.Frame, text: str, variable: tk.StringVar, row: int, width: int = 34) -> None:
        """Добавляет строку с текстовым полем."""
        ttk.Label(parent, text=text).grid(row=row, column=0, sticky=tk.W, pady=6)
        ttk.Entry(parent, textvariable=variable, width=width).grid(row=row, column=1, sticky=tk.W, pady=6)

    def _update_long_break_controls(self) -> None:
        """Включает или отключает поле интервала длинного отдыха."""
        state = tk.NORMAL if self.use_long_break_var.get() else tk.DISABLED
        self.interval_spinbox.config(state=state)
        self.interval_label.config(state=state)

    def _reload_profiles_list(self) -> None:
        """Перечитывает список профилей."""
        self.profiles_listbox.delete(0, tk.END)
        for name in self.profiles.names():
            self.profiles_listbox.insert(tk.END, name)

    def _on_profile_selected(self, _event: tk.Event) -> None:
        """Подставляет имя выбранного профиля в поле ввода."""
        selected_name = self._selected_profile_name()
        if selected_name:
            self.profile_name_var.set(selected_name)

    def _save_profile(self) -> None:
        """Сохраняет текущие значения формы как профиль."""
        profile_name = self.profile_name_var.get().strip()
        if not profile_name:
            messagebox.showwarning("Профиль", "Введите имя профиля.")
            return
        settings = self._settings_from_form(active_profile=profile_name)
        self.profiles.save_profile(profile_name, settings)
        self._reload_profiles_list()
        self._select_profile(profile_name)
        self.on_save(settings, False)
        self.settings = settings
        messagebox.showinfo("Профиль", "Профиль сохранен.")

    def _apply_selected_profile(self) -> None:
        """Применяет выбранный профиль."""
        profile_name = self._selected_profile_name() or self.profile_name_var.get().strip()
        profile = self.profiles.get_profile(profile_name)
        if profile is None:
            messagebox.showwarning("Профиль", "Выберите профиль из списка.")
            return
        settings = self.profiles.settings_from_profile(profile)
        self._preserve_widget_visibility(settings)
        self._load_settings_to_form(settings)
        self.on_save(settings, False)
        self.settings = settings

    def _delete_selected_profile(self) -> None:
        """Удаляет выбранный профиль после подтверждения."""
        profile_name = self._selected_profile_name()
        if not profile_name:
            messagebox.showwarning("Профиль", "Выберите профиль для удаления.")
            return
        if profile_name == DEFAULT_PROFILE_NAME:
            messagebox.showwarning("Профиль", "Стандартный профиль удалить нельзя.")
            return
        if messagebox.askyesno("Удалить профиль", f"Удалить профиль «{profile_name}»?"):
            self.profiles.delete_profile(profile_name)
            self._reload_profiles_list()
            self.profile_name_var.set("")

    def _restore_default_settings(self) -> None:
        """Возвращает стандартный набор настроек."""
        settings = self.profiles.default_settings()
        self._preserve_widget_visibility(settings)
        self._load_settings_to_form(settings)
        self.on_save(settings, False)
        self.settings = settings
        self._select_profile(DEFAULT_PROFILE_NAME)

    def _restore_personal_settings(self) -> None:
        """Возвращает настройки, с которыми пользователь открыл вкладку."""
        settings = self.personal_settings
        self._preserve_widget_visibility(settings)
        self._load_settings_to_form(settings)
        self.on_save(settings, False)
        self.settings = settings
        self._select_profile(self.personal_settings.active_profile)

    def _save(self) -> None:
        """Сохраняет текущие значения формы как активные настройки."""
        settings = self._settings_from_form(active_profile=self.profile_name_var.get().strip())
        autostart_changed = settings.autostart_enabled != self.settings.autostart_enabled
        self.on_save(settings, autostart_changed)
        self.settings = settings

    def _settings_from_form(self, active_profile: str) -> AppSettings:
        """Собирает объект настроек из значений формы."""
        self._remember_widget_size_selection()
        widget_type = self.widget_type_var.get()
        active_layout = self.widget_layouts[widget_type]
        return AppSettings(
            active_profile=active_profile or self.settings.active_profile,
            work_minutes=self._positive_int(self.work_minutes_var, self.settings.work_minutes),
            short_break_minutes=self._positive_int(self.short_break_minutes_var, self.settings.short_break_minutes),
            long_break_minutes=self._positive_int(self.long_break_minutes_var, self.settings.long_break_minutes),
            notifications_enabled=self.notifications_enabled_var.get(),
            notification_sound_enabled=self.notification_sound_enabled_var.get(),
            work_end_message=self.work_end_message_var.get().strip(),
            short_break_end_message=self.short_break_end_message_var.get().strip(),
            long_break_end_message=self.long_break_end_message_var.get().strip(),
            autostart_enabled=self.autostart_enabled_var.get(),
            use_long_break=self.use_long_break_var.get(),
            long_break_interval=self._positive_int(self.long_break_interval_var, self.settings.long_break_interval),
            auto_start_next_period=self.auto_start_next_period_var.get(),
            time_display_format=self.time_display_format_var.get(),
            minimize_to_tray_on_start=self.minimize_to_tray_on_start_var.get(),
            close_to_tray=self.close_to_tray_var.get(),
            theme_name=normalize_theme_name(self.theme_name_var.get()),
            appearance_mode=normalize_appearance_mode(self.appearance_mode_var.get()),
            widget_enabled=self.settings.widget_enabled,
            widget_type=widget_type,
            widget_size=self.widget_size_var.get(),
            widget_layouts=deepcopy(self.widget_layouts),
            widget_background_color=self.settings.widget_background_color,
            widget_text_color=self.settings.widget_text_color,
            widget_opacity=self._bounded_opacity(),
            widget_always_on_top=self.widget_always_on_top_var.get(),
            widget_x=int(active_layout["x"]),
            widget_y=int(active_layout["y"]),
        )

    def _load_settings_to_form(self, settings: AppSettings) -> None:
        """Заполняет поля формы значениями настроек."""
        self.profile_name_var.set(settings.active_profile)
        self.work_minutes_var.set(settings.work_minutes)
        self.short_break_minutes_var.set(settings.short_break_minutes)
        self.long_break_minutes_var.set(settings.long_break_minutes)
        self.use_long_break_var.set(settings.use_long_break)
        self.long_break_interval_var.set(settings.long_break_interval)
        self.auto_start_next_period_var.set(settings.auto_start_next_period)
        self.time_display_format_var.set(settings.time_display_format)
        self.minimize_to_tray_on_start_var.set(settings.minimize_to_tray_on_start)
        self.close_to_tray_var.set(settings.close_to_tray)
        self.autostart_enabled_var.set(settings.autostart_enabled)
        self.notifications_enabled_var.set(settings.notifications_enabled)
        self.notification_sound_enabled_var.set(settings.notification_sound_enabled)
        self.work_end_message_var.set(settings.work_end_message)
        self.short_break_end_message_var.set(settings.short_break_end_message)
        self.long_break_end_message_var.set(settings.long_break_end_message)
        self.theme_name_var.set(settings.theme_name)
        self.appearance_mode_var.set(settings.appearance_mode)
        self.widget_type_var.set(settings.widget_type)
        self.widget_size_var.set(settings.widget_size)
        self.widget_layouts = deepcopy(settings.widget_layouts)
        self.widget_opacity_var.set(settings.widget_opacity)
        self.widget_always_on_top_var.set(settings.widget_always_on_top)
        self._update_long_break_controls()
        self._refresh_theme_previews()

    def _preserve_widget_visibility(self, settings: AppSettings) -> None:
        """Не позволяет профилям подменять состояние кнопки главного окна."""
        settings.widget_enabled = self.settings.widget_enabled

    def _reset_widget_position(self) -> None:
        """Возвращает текущий тип виджета в безопасную область экрана."""
        widget_type = self.widget_type_var.get()
        self.widget_layouts[widget_type]["x"] = DEFAULT_WIDGET_X
        self.widget_layouts[widget_type]["y"] = DEFAULT_WIDGET_Y
        messagebox.showinfo(
            "Виджет",
            "Позиция выбранного типа будет сброшена после сохранения.",
        )

    def _on_widget_type_selected(self, _event: tk.Event) -> None:
        """Восстанавливает сохраненный размер выбранного типа."""
        widget_type = self.widget_type_var.get()
        self.widget_size_var.set(str(self.widget_layouts[widget_type]["size"]))

    def _on_widget_size_selected(self, _event: tk.Event) -> None:
        """Запоминает пресет размера отдельно для текущего типа."""
        self._remember_widget_size_selection()

    def _remember_widget_size_selection(self) -> None:
        """Обновляет локальную копию геометрий до сохранения формы."""
        self.widget_layouts = normalize_widget_layouts(
            self.widget_layouts,
            active_type=self.widget_type_var.get(),
        )
        self.widget_layouts = set_widget_layout_size(
            self.widget_layouts,
            self.widget_type_var.get(),
            self.widget_size_var.get(),
        )

    def _selected_profile_name(self) -> str | None:
        """Возвращает имя профиля, выбранного в списке."""
        selection = self.profiles_listbox.curselection()
        if not selection:
            return None
        return self.profiles_listbox.get(selection[0])

    def _select_profile(self, profile_name: str) -> None:
        """Выделяет профиль в списке по имени."""
        for index, name in enumerate(self.profiles.names()):
            if name == profile_name:
                self.profiles_listbox.selection_clear(0, tk.END)
                self.profiles_listbox.selection_set(index)
                self.profiles_listbox.see(index)
                return

    def _positive_int(self, variable: tk.IntVar, default: int) -> int:
        """Безопасно читает положительное число из поля."""
        try:
            return max(1, int(variable.get()))
        except (tk.TclError, ValueError):
            return default

    def _bounded_opacity(self) -> int:
        """Возвращает прозрачность в безопасном для читаемости диапазоне."""
        try:
            return min(100, max(MIN_WIDGET_OPACITY, int(self.widget_opacity_var.get())))
        except (tk.TclError, ValueError):
            return 100



class SettingsWindow:
    """Отдельное окно настроек для совместимости со старым кодом."""

    def __init__(
        self,
        parent: tk.Tk,
        settings: AppSettings,
        on_save: Callable[[AppSettings, bool], None],
    ) -> None:
        """Создает окно и помещает в него SettingsView."""
        self.window = tk.Toplevel(parent)
        self.window.title("Настройки")
        self.window.geometry("920x560")
        self.window.minsize(820, 480)
        SettingsView(self.window, settings, on_save).pack(fill=tk.BOTH, expand=True)
