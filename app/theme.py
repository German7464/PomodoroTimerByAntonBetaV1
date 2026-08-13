"""Централизованные светлые и тёмные палитры интерфейса Tkinter/ttk."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, fields
import tkinter as tk
from tkinter import ttk
from typing import Any, Callable, Final

from app.models import TimerMode


DEFAULT_THEME_NAME: Final = "Comet"
APPEARANCE_LIGHT: Final = "light"
APPEARANCE_DARK: Final = "dark"
DEFAULT_APPEARANCE_MODE: Final = APPEARANCE_LIGHT
CUSTOM_THEME_NAME: Final = "Пользовательская"
BUILTIN_THEME_NAMES: Final = ("Comet", "Aurora", "Warm")
THEME_NAMES: Final = (*BUILTIN_THEME_NAMES, CUSTOM_THEME_NAME)
APPEARANCE_MODES: Final = (APPEARANCE_LIGHT, APPEARANCE_DARK)
APPEARANCE_LABELS: Final = {
    APPEARANCE_LIGHT: "Светлая",
    APPEARANCE_DARK: "Тёмная",
}


@dataclass(frozen=True)
class ThemePalette:
    """Смысловые цвета одного сочетания темы и режима."""

    background: str
    card_background: str
    secondary_background: str
    text_primary: str
    text_secondary: str
    accent: str
    accent_hover: str
    button_background: str
    button_text: str
    border: str
    disabled: str
    focus: str
    success: str
    warning: str
    error: str
    work: str
    short_break: str
    long_break: str
    overwork: str
    short_break_overrun: str
    long_break_overrun: str
    on_accent: str

    def as_dict(self) -> dict[str, str]:
        """Возвращает палитру как словарь для тестов и образцов настроек."""
        return {field.name: getattr(self, field.name) for field in fields(self)}

    @property
    def overrun(self) -> str:
        """Совместимое имя цвета переработки для старых UI-контрактов."""
        return self.overwork


PALETTES: Final[dict[str, dict[str, ThemePalette]]] = {
    "Comet": {
        APPEARANCE_LIGHT: ThemePalette(
            background="#F3F6F5",
            card_background="#FFFFFF",
            secondary_background="#E5ECEA",
            text_primary="#17201E",
            text_secondary="#52615D",
            accent="#0F766E",
            accent_hover="#0B5F59",
            button_background="#E5ECEA",
            button_text="#17201E",
            border="#CBD7D3",
            disabled="#84928E",
            focus="#087E75",
            success="#27754C",
            warning="#805400",
            error="#AA3434",
            work="#0D6F68",
            short_break="#275F9E",
            long_break="#65509A",
            overwork="#9B3651",
            short_break_overrun="#9B3651",
            long_break_overrun="#9B3651",
            on_accent="#FFFFFF",
        ),
        APPEARANCE_DARK: ThemePalette(
            background="#101615",
            card_background="#18211F",
            secondary_background="#22302D",
            text_primary="#F2F7F5",
            text_secondary="#B4C2BE",
            accent="#5BC7B8",
            accent_hover="#78D5C9",
            button_background="#22302D",
            button_text="#F2F7F5",
            border="#344541",
            disabled="#70817D",
            focus="#70D7CA",
            success="#6FD39A",
            warning="#F0BD66",
            error="#FF8A8A",
            work="#62C9BB",
            short_break="#7EB8F0",
            long_break="#B9A0F4",
            overwork="#F18AA2",
            short_break_overrun="#F18AA2",
            long_break_overrun="#F18AA2",
            on_accent="#0E1B18",
        ),
    },
    "Aurora": {
        APPEARANCE_LIGHT: ThemePalette(
            background="#F3F5FC",
            card_background="#FFFFFF",
            secondary_background="#E8ECFA",
            text_primary="#182039",
            text_secondary="#56607E",
            accent="#4F46E5",
            accent_hover="#3F37C7",
            button_background="#E8ECFA",
            button_text="#182039",
            border="#D1D8EE",
            disabled="#8D95AD",
            focus="#6557EF",
            success="#26734D",
            warning="#805400",
            error="#AA344D",
            work="#315E9F",
            short_break="#4B4BB7",
            long_break="#70409A",
            overwork="#A3335E",
            short_break_overrun="#A3335E",
            long_break_overrun="#A3335E",
            on_accent="#FFFFFF",
        ),
        APPEARANCE_DARK: ThemePalette(
            background="#10131E",
            card_background="#181D2B",
            secondary_background="#22283A",
            text_primary="#F4F5FF",
            text_secondary="#B7BDD4",
            accent="#9290FF",
            accent_hover="#AAA8FF",
            button_background="#22283A",
            button_text="#F4F5FF",
            border="#353D55",
            disabled="#747C96",
            focus="#A8A7FF",
            success="#70D29A",
            warning="#F0BD68",
            error="#FF8DA0",
            work="#83B2F0",
            short_break="#9C9AFF",
            long_break="#C2A0F5",
            overwork="#F190B1",
            short_break_overrun="#F190B1",
            long_break_overrun="#F190B1",
            on_accent="#121426",
        ),
    },
    "Warm": {
        APPEARANCE_LIGHT: ThemePalette(
            background="#F7F2EA",
            card_background="#FFFDF9",
            secondary_background="#EEE4D6",
            text_primary="#2E241C",
            text_secondary="#675548",
            accent="#A45127",
            accent_hover="#853F1D",
            button_background="#EEE4D6",
            button_text="#2E241C",
            border="#DCCDBB",
            disabled="#998A7C",
            focus="#B45C30",
            success="#47704A",
            warning="#805000",
            error="#A43B35",
            work="#864A24",
            short_break="#566940",
            long_break="#714D72",
            overwork="#9D3940",
            short_break_overrun="#9D3940",
            long_break_overrun="#9D3940",
            on_accent="#FFFFFF",
        ),
        APPEARANCE_DARK: ThemePalette(
            background="#1B1714",
            card_background="#241E1A",
            secondary_background="#302720",
            text_primary="#FAF5EE",
            text_secondary="#CCBFB2",
            accent="#E99A68",
            accent_hover="#F2B083",
            button_background="#302720",
            button_text="#FAF5EE",
            border="#493C32",
            disabled="#84776C",
            focus="#FFB485",
            success="#86C98D",
            warning="#E8B86A",
            error="#F28E85",
            work="#E7A16F",
            short_break="#AFC287",
            long_break="#C6A1C7",
            overwork="#F08A8E",
            short_break_overrun="#F08A8E",
            long_break_overrun="#F08A8E",
            on_accent="#25140A",
        ),
    },
}


def is_hex_color(value: object) -> bool:
    """Проверяет строгий пользовательский формат #RRGGBB."""
    color = str(value or "").strip()
    if len(color) != 7 or not color.startswith("#"):
        return False
    try:
        int(color[1:], 16)
    except ValueError:
        return False
    return True


def normalize_palette_data(value: object, fallback: ThemePalette) -> dict[str, str]:
    """Частично восстанавливает палитру, сохраняя каждое корректное поле."""
    raw = value if isinstance(value, dict) else {}
    normalized: dict[str, str] = {}
    for field in fields(ThemePalette):
        candidate = raw.get(field.name)
        normalized[field.name] = (
            str(candidate).strip().upper()
            if is_hex_color(candidate)
            else getattr(fallback, field.name)
        )
    return normalized


def default_custom_theme(base_theme: object = DEFAULT_THEME_NAME) -> dict[str, dict[str, str]]:
    """Создает независимые светлую и тёмную копии безопасной встроенной темы."""
    normalized_base = normalize_builtin_theme_name(base_theme)
    return {
        mode: PALETTES[normalized_base][mode].as_dict()
        for mode in APPEARANCE_MODES
    }


def normalize_custom_theme(value: object) -> dict[str, dict[str, str]]:
    """Восстанавливает оба режима пользовательской темы по полям Comet."""
    raw = value if isinstance(value, dict) else {}
    return {
        mode: normalize_palette_data(
            raw.get(mode),
            PALETTES[DEFAULT_THEME_NAME][mode],
        )
        for mode in APPEARANCE_MODES
    }


def palette_from_data(value: object, fallback: ThemePalette) -> ThemePalette:
    """Создает неизменяемую палитру из безопасно нормализованных данных."""
    return ThemePalette(**normalize_palette_data(value, fallback))


def relative_luminance(color: str) -> float:
    """Вычисляет относительную яркость цвета по формуле WCAG."""
    channels = []
    for offset in (1, 3, 5):
        channel = int(color[offset : offset + 2], 16) / 255
        channels.append(
            channel / 12.92
            if channel <= 0.04045
            else ((channel + 0.055) / 1.055) ** 2.4,
        )
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast_ratio(first: str, second: str) -> float:
    """Возвращает WCAG contrast ratio двух корректных HEX-цветов."""
    first_luminance = relative_luminance(first)
    second_luminance = relative_luminance(second)
    lighter = max(first_luminance, second_luminance)
    darker = min(first_luminance, second_luminance)
    return (lighter + 0.05) / (darker + 0.05)


def palette_contrast_warnings(palette: ThemePalette) -> list[str]:
    """Возвращает понятные предупреждения для сочетаний ниже 4,5:1."""
    pairs = (
        ("Основной текст / карточка", palette.text_primary, palette.card_background),
        ("Вторичный текст / карточка", palette.text_secondary, palette.card_background),
        ("Текст кнопок / кнопка", palette.button_text, palette.button_background),
        ("Текст акцента / акцент", palette.on_accent, palette.accent),
        ("Работа / карточка", palette.work, palette.card_background),
        ("Короткий отдых / карточка", palette.short_break, palette.card_background),
        ("Длинный отдых / карточка", palette.long_break, palette.card_background),
        ("Переработка / карточка", palette.overwork, palette.card_background),
        (
            "Короткий отдых сверх нормы / карточка",
            palette.short_break_overrun,
            palette.card_background,
        ),
        (
            "Длинный отдых сверх нормы / карточка",
            palette.long_break_overrun,
            palette.card_background,
        ),
    )
    return [
        f"{label}: {contrast_ratio(foreground, background):.2f}:1"
        for label, foreground, background in pairs
        if contrast_ratio(foreground, background) < 4.5
    ]


def normalize_builtin_theme_name(value: object) -> str:
    """Возвращает имя встроенной темы, пригодной как основа копии."""
    candidate = str(value or "").strip().casefold()
    for name in BUILTIN_THEME_NAMES:
        if candidate == name.casefold():
            return name
    return DEFAULT_THEME_NAME


class CustomThemeDraft:
    """Черновик редактора, отделяющий предпросмотр и отмену от сохранённых цветов."""

    def __init__(self, custom_theme: object) -> None:
        self.saved = normalize_custom_theme(custom_theme)
        self.value = deepcopy(self.saved)

    def set_mode(self, mode: object, palette_data: object) -> None:
        """Сохраняет в черновик только нормализованный выбранный режим."""
        normalized_mode = normalize_appearance_mode(mode)
        self.value[normalized_mode] = normalize_palette_data(
            palette_data,
            PALETTES[DEFAULT_THEME_NAME][normalized_mode],
        )

    def create_mode_from(self, mode: object, base_theme: object) -> None:
        """Заменяет режим независимой копией одной встроенной палитры."""
        normalized_mode = normalize_appearance_mode(mode)
        normalized_base = normalize_builtin_theme_name(base_theme)
        self.value[normalized_mode] = PALETTES[normalized_base][normalized_mode].as_dict()

    def reset_mode(self, mode: object) -> None:
        """Возвращает выбранный режим к безопасной Comet."""
        self.create_mode_from(mode, DEFAULT_THEME_NAME)

    def reset_all(self) -> None:
        """Возвращает оба режима к безопасной Comet."""
        self.value = default_custom_theme()

    def cancel(self) -> dict[str, dict[str, str]]:
        """Возвращает сохранённую до открытия редактора палитру."""
        return deepcopy(self.saved)

    def applied(self) -> dict[str, dict[str, str]]:
        """Возвращает независимую нормализованную копию результата."""
        return normalize_custom_theme(self.value)


def normalize_theme_name(value: object) -> str:
    """Возвращает известную тему либо безопасную Comet."""
    candidate = str(value or "").strip().casefold()
    for name in THEME_NAMES:
        if candidate == name.casefold():
            return name
    return DEFAULT_THEME_NAME


def normalize_appearance_mode(value: object) -> str:
    """Возвращает light/dark либо безопасный светлый режим."""
    candidate = str(value or "").strip().casefold()
    if candidate in {APPEARANCE_DARK, "тёмная", "темная", "dark mode"}:
        return APPEARANCE_DARK
    if candidate in {APPEARANCE_LIGHT, "светлая", "light mode"}:
        return APPEARANCE_LIGHT
    return DEFAULT_APPEARANCE_MODE


def get_palette(
    theme_name: object,
    appearance_mode: object,
    custom_theme: object = None,
) -> ThemePalette:
    """Возвращает нормализованную полноценную палитру."""
    normalized_theme = normalize_theme_name(theme_name)
    normalized_mode = normalize_appearance_mode(appearance_mode)
    if normalized_theme == CUSTOM_THEME_NAME:
        normalized_custom = normalize_custom_theme(custom_theme)
        return palette_from_data(
            normalized_custom[normalized_mode],
            PALETTES[DEFAULT_THEME_NAME][normalized_mode],
        )
    return PALETTES[normalized_theme][normalized_mode]


def mode_color(
    palette: ThemePalette,
    mode: TimerMode,
    waiting_for_continue: bool = False,
) -> str:
    """Выбирает семантический цвет режима, сохраняя текстовое различие состояний."""
    if waiting_for_continue:
        if mode == TimerMode.SHORT_BREAK:
            return palette.short_break_overrun
        if mode == TimerMode.LONG_BREAK:
            return palette.long_break_overrun
        return palette.overwork
    if mode == TimerMode.SHORT_BREAK:
        return palette.short_break
    if mode == TimerMode.LONG_BREAK:
        return palette.long_break
    return palette.work


class ThemeManager:
    """Применяет одну палитру ко всему дереву Tk/ttk и слушателям виджета."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.style = ttk.Style(root)
        self.theme_name = DEFAULT_THEME_NAME
        self.appearance_mode = DEFAULT_APPEARANCE_MODE
        self.custom_theme = default_custom_theme()
        self.palette = get_palette(
            self.theme_name,
            self.appearance_mode,
            self.custom_theme,
        )
        self._listeners: list[Callable[[ThemePalette], None]] = []

    def register(self, listener: Callable[[ThemePalette], None]) -> None:
        """Регистрирует компонент с обычными tk-элементами и сразу оформляет его."""
        if listener not in self._listeners:
            self._listeners.append(listener)
        listener(self.palette)

    def apply(
        self,
        theme_name: object,
        appearance_mode: object,
        custom_theme: object = None,
    ) -> ThemePalette:
        """Мгновенно применяет нормализованную тему без пересоздания окон."""
        self.theme_name = normalize_theme_name(theme_name)
        self.appearance_mode = normalize_appearance_mode(appearance_mode)
        if custom_theme is not None:
            self.custom_theme = normalize_custom_theme(custom_theme)
        self.palette = get_palette(
            self.theme_name,
            self.appearance_mode,
            self.custom_theme,
        )
        self._configure_ttk_styles()
        self.apply_to_window(self.root)
        for listener in tuple(self._listeners):
            listener(self.palette)
        return self.palette

    def apply_to_window(self, window: tk.Misc) -> None:
        """Оформляет новое окно и обычные tk.Text/Listbox внутри него."""
        palette = self.palette
        try:
            window.configure(background=palette.background)
        except (tk.TclError, TypeError):
            pass
        self._apply_native_tree(window)

    def mode_style(self, mode: TimerMode, waiting_for_continue: bool) -> str:
        """Возвращает ttk-стиль цветовой метки режима таймера."""
        if waiting_for_continue:
            if mode == TimerMode.SHORT_BREAK:
                return "ShortBreakOverrun.TimerMode.TLabel"
            if mode == TimerMode.LONG_BREAK:
                return "LongBreakOverrun.TimerMode.TLabel"
            return "Overwork.TimerMode.TLabel"
        if mode == TimerMode.SHORT_BREAK:
            return "ShortBreak.TimerMode.TLabel"
        if mode == TimerMode.LONG_BREAK:
            return "LongBreak.TimerMode.TLabel"
        return "Work.TimerMode.TLabel"

    def apply_timer_effect(
        self,
        digits_color: str | None,
        card_background: str | None,
    ) -> None:
        """Применяет один кадр только к карточке таймера, не затрагивая вкладки."""
        palette = self.palette
        background = card_background or palette.card_background
        foreground = digits_color or palette.text_primary
        self.style.configure("TimerCard.TFrame", background=background)
        self.style.configure(
            "TimerCard.Timer.TLabel",
            background=background,
            foreground=foreground,
        )
        self.style.configure(
            "TimerCard.Secondary.TLabel",
            background=background,
            foreground=palette.text_secondary,
        )
        for style_name in (
            "Work.TimerMode.TLabel",
            "ShortBreak.TimerMode.TLabel",
            "LongBreak.TimerMode.TLabel",
            "Overwork.TimerMode.TLabel",
            "ShortBreakOverrun.TimerMode.TLabel",
            "LongBreakOverrun.TimerMode.TLabel",
            "Overrun.TimerMode.TLabel",
        ):
            self.style.configure(style_name, background=background)

    def _configure_ttk_styles(self) -> None:
        palette = self.palette
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.root.option_add("*Font", "{Segoe UI} 10")
        self.root.option_add("*TCombobox*Listbox.background", palette.card_background)
        self.root.option_add("*TCombobox*Listbox.foreground", palette.text_primary)
        self.root.option_add("*TCombobox*Listbox.selectBackground", palette.accent)
        self.root.option_add("*TCombobox*Listbox.selectForeground", palette.on_accent)

        self.style.configure(".", background=palette.background, foreground=palette.text_primary)
        self.style.configure("TFrame", background=palette.background)
        self.style.configure("Card.TFrame", background=palette.card_background)
        self.style.configure("TimerCard.TFrame", background=palette.card_background)
        self.style.configure("Toolbar.TFrame", background=palette.background)
        self.style.configure(
            "TLabel",
            background=palette.background,
            foreground=palette.text_primary,
            font=("Segoe UI", 10),
        )
        self.style.configure(
            "Secondary.TLabel",
            background=palette.background,
            foreground=palette.text_secondary,
        )
        self.style.configure(
            "Heading.TLabel",
            background=palette.background,
            foreground=palette.text_primary,
            font=("Segoe UI Semibold", 18),
        )
        self.style.configure(
            "Card.TLabel",
            background=palette.card_background,
            foreground=palette.text_primary,
        )
        self.style.configure(
            "Card.Secondary.TLabel",
            background=palette.card_background,
            foreground=palette.text_secondary,
        )
        self.style.configure(
            "Card.StatValue.TLabel",
            background=palette.card_background,
            foreground=palette.accent,
            font=("Segoe UI Semibold", 10),
        )
        self.style.configure(
            "Card.Timer.TLabel",
            background=palette.card_background,
            foreground=palette.text_primary,
            font=("Segoe UI Semibold", 52),
        )
        self.style.configure(
            "TimerCard.Timer.TLabel",
            background=palette.card_background,
            foreground=palette.text_primary,
            font=("Segoe UI Semibold", 52),
        )
        self.style.configure(
            "TimerCard.Secondary.TLabel",
            background=palette.card_background,
            foreground=palette.text_secondary,
        )
        self.style.configure(
            "TimerMode.TLabel",
            background=palette.card_background,
            font=("Segoe UI Semibold", 16),
        )
        for style_name, color in (
            ("Work.TimerMode.TLabel", palette.work),
            ("ShortBreak.TimerMode.TLabel", palette.short_break),
            ("LongBreak.TimerMode.TLabel", palette.long_break),
            ("Overwork.TimerMode.TLabel", palette.overwork),
            ("ShortBreakOverrun.TimerMode.TLabel", palette.short_break_overrun),
            ("LongBreakOverrun.TimerMode.TLabel", palette.long_break_overrun),
            ("Overrun.TimerMode.TLabel", palette.overwork),
        ):
            self.style.configure(style_name, background=palette.card_background, foreground=color)

        self._configure_button(
            "TButton",
            palette.button_background,
            palette.button_text,
            palette.border,
        )
        self._configure_button("Accent.TButton", palette.accent, palette.on_accent, palette.accent_hover)
        self._configure_button("Ghost.TButton", palette.card_background, palette.text_primary, palette.secondary_background)
        self.style.configure("TButton", padding=(14, 8), borderwidth=1, relief="flat")
        self.style.configure("Accent.TButton", padding=(16, 9), borderwidth=1, relief="flat")
        self.style.configure("Ghost.TButton", padding=(12, 7), borderwidth=1, relief="flat")

        for control in ("TEntry", "TSpinbox", "TCombobox"):
            self.style.configure(
                control,
                fieldbackground=palette.card_background,
                background=palette.card_background,
                foreground=palette.text_primary,
                bordercolor=palette.border,
                lightcolor=palette.border,
                darkcolor=palette.border,
                insertcolor=palette.text_primary,
                arrowcolor=palette.text_secondary,
                padding=7,
            )
            self.style.map(
                control,
                fieldbackground=[("readonly", palette.card_background), ("disabled", palette.secondary_background)],
                foreground=[("disabled", palette.disabled), ("readonly", palette.text_primary)],
                bordercolor=[("focus", palette.focus)],
                lightcolor=[("focus", palette.focus)],
                darkcolor=[("focus", palette.focus)],
            )

        for control in ("TCheckbutton", "TRadiobutton"):
            self.style.configure(
                control,
                background=palette.background,
                foreground=palette.text_primary,
                focuscolor=palette.focus,
                padding=(4, 5),
            )
            self.style.map(
                control,
                background=[("active", palette.secondary_background)],
                foreground=[("disabled", palette.disabled)],
                indicatorcolor=[("selected", palette.accent), ("!selected", palette.card_background)],
            )
        for control in ("Card.TCheckbutton", "Card.TRadiobutton"):
            self.style.configure(
                control,
                background=palette.card_background,
                foreground=palette.text_primary,
                focuscolor=palette.focus,
                padding=(4, 5),
            )
            self.style.map(
                control,
                background=[("active", palette.secondary_background)],
                foreground=[("disabled", palette.disabled)],
                indicatorcolor=[("selected", palette.accent), ("!selected", palette.card_background)],
            )

        self.style.configure("TNotebook", background=palette.background, borderwidth=0, tabmargins=(0, 0, 0, 8))
        self.style.configure(
            "TNotebook.Tab",
            background=palette.secondary_background,
            foreground=palette.text_secondary,
            borderwidth=0,
            padding=(16, 9),
            font=("Segoe UI Semibold", 9),
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", palette.card_background), ("active", palette.card_background)],
            foreground=[("selected", palette.text_primary), ("active", palette.text_primary)],
            focuscolor=[("focus", palette.focus)],
        )
        self.style.configure(
            "TLabelframe",
            background=palette.card_background,
            bordercolor=palette.border,
            lightcolor=palette.border,
            darkcolor=palette.border,
            borderwidth=1,
            relief="solid",
        )
        self.style.configure(
            "TLabelframe.Label",
            background=palette.card_background,
            foreground=palette.text_primary,
            font=("Segoe UI Semibold", 11),
        )
        self.style.configure(
            "Vertical.TScrollbar",
            background=palette.secondary_background,
            troughcolor=palette.background,
            bordercolor=palette.background,
            arrowcolor=palette.text_secondary,
        )
        self.style.map("Vertical.TScrollbar", background=[("active", palette.accent)])
        self.style.configure(
            "Horizontal.TScale",
            background=palette.background,
            troughcolor=palette.secondary_background,
        )
        self.style.configure(
            "Tooltip.TLabel",
            background=palette.text_primary,
            foreground=palette.background,
            borderwidth=0,
            padding=(9, 6),
            font=("Segoe UI", 9),
        )

    def _configure_button(self, style_name: str, background: str, foreground: str, hover: str) -> None:
        palette = self.palette
        self.style.configure(
            style_name,
            background=background,
            foreground=foreground,
            bordercolor=palette.border,
            focuscolor=palette.focus,
            font=("Segoe UI Semibold", 10),
        )
        self.style.map(
            style_name,
            background=[("pressed", hover), ("active", hover), ("disabled", palette.secondary_background)],
            foreground=[("disabled", palette.disabled)],
            bordercolor=[("focus", palette.focus)],
        )

    def _apply_native_tree(self, widget: tk.Misc) -> None:
        palette = self.palette
        try:
            children = widget.winfo_children()
        except tk.TclError:
            return
        for child in children:
            try:
                if isinstance(child, tk.Text):
                    child.configure(
                        background=palette.card_background,
                        foreground=palette.text_primary,
                        insertbackground=palette.text_primary,
                        selectbackground=palette.accent,
                        selectforeground=palette.on_accent,
                        highlightbackground=palette.border,
                        highlightcolor=palette.focus,
                        relief=tk.FLAT,
                        borderwidth=0,
                        highlightthickness=1,
                    )
                elif isinstance(child, tk.Listbox):
                    child.configure(
                        background=palette.card_background,
                        foreground=palette.text_primary,
                        selectbackground=palette.accent,
                        selectforeground=palette.on_accent,
                        disabledforeground=palette.disabled,
                        highlightbackground=palette.border,
                        highlightcolor=palette.focus,
                        relief=tk.FLAT,
                        borderwidth=0,
                        highlightthickness=1,
                    )
                elif isinstance(child, tk.Canvas):
                    child.configure(
                        background=palette.background,
                        highlightbackground=palette.border,
                        highlightcolor=palette.focus,
                    )
                elif isinstance(child, tk.Toplevel):
                    child.configure(background=palette.background)
            except tk.TclError:
                pass
            self._apply_native_tree(child)


class Tooltip:
    """Короткая текстовая подсказка для компактных кнопок."""

    def __init__(self, widget: tk.Widget, text: str, theme_manager: ThemeManager) -> None:
        self.widget = widget
        self.text = text
        self.theme_manager = theme_manager
        self._window: tk.Toplevel | None = None
        widget.bind("<Enter>", self._show, add="+")
        widget.bind("<Leave>", self._hide, add="+")
        widget.bind("<ButtonPress>", self._hide, add="+")

    def _show(self, _event: tk.Event) -> None:
        if self._window is not None:
            return
        x = self.widget.winfo_rootx()
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 6
        window = tk.Toplevel(self.widget)
        self._window = window
        window.wm_overrideredirect(True)
        window.wm_geometry(f"+{x}+{y}")
        ttk.Label(window, text=self.text, style="Tooltip.TLabel").pack()
        self.theme_manager.apply_to_window(window)

    def _hide(self, _event: tk.Event | None = None) -> None:
        if self._window is None:
            return
        try:
            self._window.destroy()
        except tk.TclError:
            pass
        self._window = None
