"""Централизованные светлые и тёмные палитры интерфейса Tkinter/ttk."""

from __future__ import annotations

from dataclasses import dataclass, fields
import tkinter as tk
from tkinter import ttk
from typing import Callable, Final

from app.models import TimerMode


DEFAULT_THEME_NAME: Final = "Comet"
APPEARANCE_LIGHT: Final = "light"
APPEARANCE_DARK: Final = "dark"
DEFAULT_APPEARANCE_MODE: Final = APPEARANCE_LIGHT
THEME_NAMES: Final = ("Comet", "Aurora", "Warm")
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
    border: str
    disabled: str
    focus: str
    success: str
    warning: str
    error: str
    work: str
    short_break: str
    long_break: str
    overrun: str
    on_accent: str

    def as_dict(self) -> dict[str, str]:
        """Возвращает палитру как словарь для тестов и образцов настроек."""
        return {field.name: getattr(self, field.name) for field in fields(self)}


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
            border="#CBD7D3",
            disabled="#84928E",
            focus="#087E75",
            success="#27754C",
            warning="#805400",
            error="#AA3434",
            work="#0D6F68",
            short_break="#275F9E",
            long_break="#65509A",
            overrun="#9B3651",
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
            border="#344541",
            disabled="#70817D",
            focus="#70D7CA",
            success="#6FD39A",
            warning="#F0BD66",
            error="#FF8A8A",
            work="#62C9BB",
            short_break="#7EB8F0",
            long_break="#B9A0F4",
            overrun="#F18AA2",
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
            border="#D1D8EE",
            disabled="#8D95AD",
            focus="#6557EF",
            success="#26734D",
            warning="#805400",
            error="#AA344D",
            work="#315E9F",
            short_break="#4B4BB7",
            long_break="#70409A",
            overrun="#A3335E",
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
            border="#353D55",
            disabled="#747C96",
            focus="#A8A7FF",
            success="#70D29A",
            warning="#F0BD68",
            error="#FF8DA0",
            work="#83B2F0",
            short_break="#9C9AFF",
            long_break="#C2A0F5",
            overrun="#F190B1",
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
            border="#DCCDBB",
            disabled="#998A7C",
            focus="#B45C30",
            success="#47704A",
            warning="#805000",
            error="#A43B35",
            work="#864A24",
            short_break="#566940",
            long_break="#714D72",
            overrun="#9D3940",
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
            border="#493C32",
            disabled="#84776C",
            focus="#FFB485",
            success="#86C98D",
            warning="#E8B86A",
            error="#F28E85",
            work="#E7A16F",
            short_break="#AFC287",
            long_break="#C6A1C7",
            overrun="#F08A8E",
            on_accent="#25140A",
        ),
    },
}


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


def get_palette(theme_name: object, appearance_mode: object) -> ThemePalette:
    """Возвращает нормализованную полноценную палитру."""
    return PALETTES[normalize_theme_name(theme_name)][
        normalize_appearance_mode(appearance_mode)
    ]


def mode_color(
    palette: ThemePalette,
    mode: TimerMode,
    waiting_for_continue: bool = False,
) -> str:
    """Выбирает семантический цвет режима, сохраняя текстовое различие состояний."""
    if waiting_for_continue:
        return palette.overrun
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
        self.palette = get_palette(self.theme_name, self.appearance_mode)
        self._listeners: list[Callable[[ThemePalette], None]] = []

    def register(self, listener: Callable[[ThemePalette], None]) -> None:
        """Регистрирует компонент с обычными tk-элементами и сразу оформляет его."""
        if listener not in self._listeners:
            self._listeners.append(listener)
        listener(self.palette)

    def apply(self, theme_name: object, appearance_mode: object) -> ThemePalette:
        """Мгновенно применяет нормализованную тему без пересоздания окон."""
        self.theme_name = normalize_theme_name(theme_name)
        self.appearance_mode = normalize_appearance_mode(appearance_mode)
        self.palette = get_palette(self.theme_name, self.appearance_mode)
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
            return "Overrun.TimerMode.TLabel"
        if mode == TimerMode.SHORT_BREAK:
            return "ShortBreak.TimerMode.TLabel"
        if mode == TimerMode.LONG_BREAK:
            return "LongBreak.TimerMode.TLabel"
        return "Work.TimerMode.TLabel"

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
            "TimerMode.TLabel",
            background=palette.card_background,
            font=("Segoe UI Semibold", 16),
        )
        for style_name, color in (
            ("Work.TimerMode.TLabel", palette.work),
            ("ShortBreak.TimerMode.TLabel", palette.short_break),
            ("LongBreak.TimerMode.TLabel", palette.long_break),
            ("Overrun.TimerMode.TLabel", palette.overrun),
        ):
            self.style.configure(style_name, background=palette.card_background, foreground=color)

        self._configure_button(
            "TButton",
            palette.secondary_background,
            palette.text_primary,
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
