"""Редактор светлого и тёмного вариантов пользовательской темы."""

from copy import deepcopy
import tkinter as tk
from tkinter import colorchooser, messagebox, ttk
from typing import Callable

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


COLOR_GROUPS = (
    (
        "Поверхности",
        (
            ("background", "Основной фон"),
            ("card_background", "Фон карточек"),
            ("secondary_background", "Дополнительный фон"),
            ("border", "Границы"),
        ),
    ),
    (
        "Текст и элементы управления",
        (
            ("text_primary", "Основной текст"),
            ("text_secondary", "Вторичный текст"),
            ("accent", "Акцент"),
            ("accent_hover", "Наведение на акцент"),
            ("button_background", "Цвет кнопок"),
            ("button_text", "Текст кнопок"),
            ("on_accent", "Текст акцентных кнопок"),
            ("focus", "Фокус"),
            ("disabled", "Неактивные элементы"),
        ),
    ),
    (
        "Служебные состояния",
        (
            ("success", "Успех"),
            ("warning", "Предупреждение"),
            ("error", "Ошибка"),
        ),
    ),
    (
        "Состояния таймера",
        (
            ("work", "Работа"),
            ("short_break", "Короткий отдых"),
            ("long_break", "Длинный отдых"),
            ("overwork", "Переработка"),
            ("short_break_overrun", "Короткий отдых сверх нормы"),
            ("long_break_overrun", "Длинный отдых сверх нормы"),
        ),
    ),
)


class CustomThemeEditor:
    """Модальное окно, сохраняющее черновик только после явного применения."""

    def __init__(
        self,
        parent: tk.Widget,
        custom_theme: object,
        initial_mode: str,
        on_preview: Callable[[dict[str, dict[str, str]], str], None],
        on_apply: Callable[[dict[str, dict[str, str]], str], None],
        on_cancel: Callable[[], None],
        theme_manager: ThemeManager,
    ) -> None:
        self.on_preview = on_preview
        self.on_apply = on_apply
        self.on_cancel = on_cancel
        self.theme_manager = theme_manager
        self.draft = CustomThemeDraft(custom_theme)
        self.mode_var = tk.StringVar(value=initial_mode)
        self.base_var = tk.StringVar(value=BUILTIN_THEME_NAMES[0])
        self.color_vars: dict[str, tk.StringVar] = {}
        self.swatches: dict[str, tk.Label] = {}
        self._last_mode = initial_mode
        self._closed = False

        self.window = tk.Toplevel(parent)
        self.window.title("Пользовательская тема")
        self.window.geometry("760x700")
        self.window.minsize(680, 560)
        self.window.transient(parent.winfo_toplevel())
        self.window.protocol("WM_DELETE_WINDOW", self.cancel)
        self.window.bind("<Escape>", lambda _event: self.cancel())
        self._build_ui()
        self._load_mode(initial_mode)
        self.theme_manager.apply_to_window(self.window)
        self.window.lift()
        self.window.focus_set()

    def is_open(self) -> bool:
        """Сообщает, существует ли единственное окно редактора."""
        try:
            return not self._closed and bool(self.window.winfo_exists())
        except tk.TclError:
            return False

    def focus(self) -> None:
        """Поднимает уже открытый редактор вместо создания второго."""
        if self.is_open():
            self.window.deiconify()
            self.window.lift()
            self.window.focus_force()

    def preview(self) -> bool:
        """Временно применяет текущий черновик без записи настроек."""
        if not self._store_form(self._last_mode):
            return False
        mode = self.mode_var.get()
        self.on_preview(deepcopy(self.draft.value), mode)
        self._show_contrast_status(self._palette_for_mode(mode))
        return True

    def apply(self) -> bool:
        """Проверяет оба режима, подтверждает низкий контраст и сохраняет результат."""
        if not self._store_form(self._last_mode):
            return False
        warnings: list[str] = []
        for mode in (APPEARANCE_LIGHT, APPEARANCE_DARK):
            for warning in palette_contrast_warnings(self._palette_for_mode(mode)):
                warnings.append(f"{APPEARANCE_LABELS[mode]}: {warning}")
        if warnings:
            details = "\n".join(f"• {warning}" for warning in warnings[:10])
            if len(warnings) > 10:
                details += f"\n• …и ещё {len(warnings) - 10}"
            confirmed = messagebox.askyesno(
                "Низкий контраст",
                "Некоторые сочетания имеют контраст ниже 4,5:1:\n\n"
                f"{details}\n\nСохранить палитру осознанно?",
                parent=self.window,
            )
            if not confirmed:
                return False
        result = self.draft.applied()
        mode = self.mode_var.get()
        self.on_apply(result, mode)
        self._destroy()
        return True

    def cancel(self) -> None:
        """Отменяет весь черновик и восстанавливает ранее сохранённое оформление."""
        if self._closed:
            return
        self.draft.cancel()
        self.on_cancel()
        self._destroy()

    def reset_current_mode(self) -> None:
        """Возвращает редактируемый режим к соответствующей Comet."""
        self.draft.reset_mode(self._last_mode)
        self._load_mode(self._last_mode)
        self.preview()

    def reset_all(self) -> None:
        """Возвращает светлую и тёмную копии к безопасной Comet."""
        if not messagebox.askyesno(
            "Сброс пользовательской темы",
            "Сбросить светлый и тёмный режимы к палитре Comet?",
            parent=self.window,
        ):
            return
        self.draft.reset_all()
        self._load_mode(self._last_mode)
        self.preview()

    def _build_ui(self) -> None:
        header = ttk.Frame(self.window, padding=(18, 16, 18, 10))
        header.pack(fill=tk.X)
        ttk.Label(header, text="Пользовательская тема", style="Heading.TLabel").pack(
            side=tk.LEFT,
        )

        mode_card = ttk.Frame(self.window, style="Card.TFrame", padding=12)
        mode_card.pack(fill=tk.X, padx=18, pady=(0, 10))
        ttk.Label(mode_card, text="Редактировать:", style="Card.TLabel").pack(
            side=tk.LEFT,
            padx=(0, 10),
        )
        for mode in (APPEARANCE_LIGHT, APPEARANCE_DARK):
            ttk.Radiobutton(
                mode_card,
                text=APPEARANCE_LABELS[mode],
                value=mode,
                variable=self.mode_var,
                command=self._switch_mode,
                style="Card.TRadiobutton",
            ).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Combobox(
            mode_card,
            textvariable=self.base_var,
            values=BUILTIN_THEME_NAMES,
            state="readonly",
            width=10,
        ).pack(side=tk.LEFT, padx=(16, 6))
        ttk.Button(
            mode_card,
            text="Создать на основе",
            command=self._create_from_base,
        ).pack(side=tk.LEFT)

        canvas_frame = ttk.Frame(self.window)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=18)
        canvas = tk.Canvas(canvas_frame, highlightthickness=0, borderwidth=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
        content = ttk.Frame(canvas, padding=(0, 0, 8, 0))
        content_id = canvas.create_window((0, 0), window=content, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        content.bind(
            "<Configure>",
            lambda _event: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(content_id, width=event.width),
        )

        for group_name, color_fields in COLOR_GROUPS:
            group = ttk.LabelFrame(content, text=group_name, padding=12)
            group.pack(fill=tk.X, pady=(0, 10))
            group.columnconfigure(1, weight=1)
            for row, (field_name, label) in enumerate(color_fields):
                variable = tk.StringVar()
                self.color_vars[field_name] = variable
                ttk.Label(group, text=label, style="Card.TLabel").grid(
                    row=row,
                    column=0,
                    sticky=tk.W,
                    pady=3,
                )
                swatch = tk.Label(group, width=5, relief=tk.FLAT, borderwidth=0)
                swatch.grid(row=row, column=1, sticky=tk.E, padx=(12, 8), pady=3)
                self.swatches[field_name] = swatch
                entry = ttk.Entry(group, textvariable=variable, width=10)
                entry.grid(row=row, column=2, padx=(0, 8), pady=3)
                entry.bind(
                    "<FocusOut>",
                    lambda _event, name=field_name: self._refresh_swatch(name),
                )
                ttk.Button(
                    group,
                    text="Выбрать…",
                    command=lambda name=field_name: self._choose_color(name),
                ).grid(row=row, column=3, pady=3)

        self.contrast_label = ttk.Label(
            self.window,
            text="",
            style="Secondary.TLabel",
        )
        self.contrast_label.pack(fill=tk.X, padx=18, pady=(8, 4))

        footer = ttk.Frame(self.window, padding=(18, 8, 18, 16))
        footer.pack(fill=tk.X)
        ttk.Button(
            footer,
            text="Сбросить всю пользовательскую тему",
            command=self.reset_all,
        ).pack(side=tk.LEFT)
        ttk.Button(
            footer,
            text="Сбросить текущий режим",
            command=self.reset_current_mode,
        ).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(footer, text="Отмена", command=self.cancel).pack(side=tk.RIGHT)
        ttk.Button(
            footer,
            text="Применить",
            command=self.apply,
            style="Accent.TButton",
        ).pack(side=tk.RIGHT, padx=(0, 8))
        ttk.Button(footer, text="Предпросмотр", command=self.preview).pack(
            side=tk.RIGHT,
            padx=(0, 8),
        )

    def _switch_mode(self) -> None:
        requested_mode = self.mode_var.get()
        if not self._store_form(self._last_mode):
            self.mode_var.set(self._last_mode)
            return
        self._last_mode = requested_mode
        self._load_mode(requested_mode)

    def _create_from_base(self) -> None:
        if not self._store_form(self._last_mode):
            return
        self.draft.create_mode_from(self._last_mode, self.base_var.get())
        self._load_mode(self._last_mode)
        self.preview()

    def _load_mode(self, mode: str) -> None:
        self._last_mode = mode
        self.mode_var.set(mode)
        palette_data = self.draft.value[mode]
        for field_name, variable in self.color_vars.items():
            variable.set(palette_data[field_name])
            self._refresh_swatch(field_name)
        self._show_contrast_status(self._palette_for_mode(mode))

    def _store_form(self, mode: str) -> bool:
        invalid = [
            field_name
            for field_name, variable in self.color_vars.items()
            if not is_hex_color(variable.get())
        ]
        if invalid:
            first_name = invalid[0]
            messagebox.showwarning(
                "Некорректный цвет",
                "Используйте формат #RRGGBB. "
                f"Исправьте поле «{self._field_label(first_name)}».",
                parent=self.window,
            )
            return False
        self.draft.set_mode(
            mode,
            {name: variable.get() for name, variable in self.color_vars.items()},
        )
        return True

    def _choose_color(self, field_name: str) -> None:
        current = self.color_vars[field_name].get()
        initial = current if is_hex_color(current) else "#FFFFFF"
        _rgb, selected = colorchooser.askcolor(
            color=initial,
            title=self._field_label(field_name),
            parent=self.window,
        )
        if selected:
            self.color_vars[field_name].set(selected.upper())
            self._refresh_swatch(field_name)

    def _refresh_swatch(self, field_name: str) -> None:
        color = self.color_vars[field_name].get().strip()
        self.swatches[field_name].configure(
            background=color if is_hex_color(color) else "#FF00FF",
        )

    def _palette_for_mode(self, mode: str) -> ThemePalette:
        fallback = ThemePalette(**self.draft.value[mode])
        return palette_from_data(self.draft.value[mode], fallback)

    def _show_contrast_status(self, palette: ThemePalette) -> None:
        warnings = palette_contrast_warnings(palette)
        if warnings:
            self.contrast_label.configure(
                text=f"Контраст ниже 4,5:1 в сочетаниях: {len(warnings)}. "
                "Сохранение потребует подтверждения.",
            )
        else:
            self.contrast_label.configure(text="Контраст основных сочетаний: не ниже 4,5:1.")

    def _field_label(self, field_name: str) -> str:
        for _group, color_fields in COLOR_GROUPS:
            for name, label in color_fields:
                if name == field_name:
                    return label
        return field_name

    def _destroy(self) -> None:
        self._closed = True
        try:
            self.window.destroy()
        except tk.TclError:
            pass
