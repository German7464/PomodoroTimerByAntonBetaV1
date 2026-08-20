"""Смысловые палитры и менеджер оформления интерфейса Qt Widgets."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, fields
from typing import Callable, Final
import weakref

from PySide6.QtCore import QObject, Qt, QTimer, Signal
from PySide6.QtWidgets import QApplication, QWidget

from app.models import TimerMode


DEFAULT_THEME_NAME: Final = "Comet"
APPEARANCE_LIGHT: Final = "light"
APPEARANCE_DARK: Final = "dark"
DEFAULT_APPEARANCE_MODE: Final = APPEARANCE_LIGHT
CUSTOM_THEME_NAME: Final = "custom"
BUILTIN_THEME_NAMES: Final = ("Comet", "Aurora", "Warm")
THEME_NAMES: Final = (*BUILTIN_THEME_NAMES, CUSTOM_THEME_NAME)
APPEARANCE_MODES: Final = (APPEARANCE_LIGHT, APPEARANCE_DARK)
THEME_LABEL_KEYS: Final = {
    "Comet": "theme.name.comet",
    "Aurora": "theme.name.aurora",
    "Warm": "theme.name.warm",
    CUSTOM_THEME_NAME: "theme.name.custom",
}
APPEARANCE_LABEL_KEYS: Final = {
    APPEARANCE_LIGHT: "theme.appearance.light",
    APPEARANCE_DARK: "theme.appearance.dark",
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
        return {field.name: getattr(self, field.name) for field in fields(self)}

    @property
    def overrun(self) -> str:
        return self.overwork


PALETTES: Final[dict[str, dict[str, ThemePalette]]] = {
    "Comet": {
        APPEARANCE_LIGHT: ThemePalette(
            background="#F3F6F5", card_background="#FFFFFF",
            secondary_background="#E5ECEA", text_primary="#17201E",
            text_secondary="#52615D", accent="#0F766E",
            accent_hover="#0B5F59", button_background="#E5ECEA",
            button_text="#17201E", border="#CBD7D3", disabled="#66736F",
            focus="#087E75", success="#27754C", warning="#805400",
            error="#AA3434", work="#0D6F68", short_break="#275F9E",
            long_break="#65509A", overwork="#9B3651",
            short_break_overrun="#9B3651", long_break_overrun="#9B3651",
            on_accent="#FFFFFF",
        ),
        APPEARANCE_DARK: ThemePalette(
            background="#101615", card_background="#18211F",
            secondary_background="#22302D", text_primary="#F2F7F5",
            text_secondary="#B4C2BE", accent="#5BC7B8",
            accent_hover="#78D5C9", button_background="#22302D",
            button_text="#F2F7F5", border="#344541", disabled="#84938F",
            focus="#70D7CA", success="#6FD39A", warning="#F0BD66",
            error="#FF8A8A", work="#62C9BB", short_break="#7EB8F0",
            long_break="#B9A0F4", overwork="#F18AA2",
            short_break_overrun="#F18AA2", long_break_overrun="#F18AA2",
            on_accent="#0E1B18",
        ),
    },
    "Aurora": {
        APPEARANCE_LIGHT: ThemePalette(
            background="#F3F5FC", card_background="#FFFFFF",
            secondary_background="#E8ECFA", text_primary="#182039",
            text_secondary="#56607E", accent="#4F46E5",
            accent_hover="#3F37C7", button_background="#E8ECFA",
            button_text="#182039", border="#D1D8EE", disabled="#687089",
            focus="#6557EF", success="#26734D", warning="#805400",
            error="#AA344D", work="#315E9F", short_break="#4B4BB7",
            long_break="#70409A", overwork="#A3335E",
            short_break_overrun="#A3335E", long_break_overrun="#A3335E",
            on_accent="#FFFFFF",
        ),
        APPEARANCE_DARK: ThemePalette(
            background="#10131E", card_background="#181D2B",
            secondary_background="#22283A", text_primary="#F4F5FF",
            text_secondary="#B7BDD4", accent="#9290FF",
            accent_hover="#AAA8FF", button_background="#22283A",
            button_text="#F4F5FF", border="#353D55", disabled="#8A92AD",
            focus="#A8A7FF", success="#70D29A", warning="#F0BD68",
            error="#FF8DA0", work="#83B2F0", short_break="#9C9AFF",
            long_break="#C2A0F5", overwork="#F190B1",
            short_break_overrun="#F190B1", long_break_overrun="#F190B1",
            on_accent="#121426",
        ),
    },
    "Warm": {
        APPEARANCE_LIGHT: ThemePalette(
            background="#F7F2EA", card_background="#FFFDF9",
            secondary_background="#EEE4D6", text_primary="#2E241C",
            text_secondary="#675548", accent="#A45127",
            accent_hover="#853F1D", button_background="#EEE4D6",
            button_text="#2E241C", border="#DCCDBB", disabled="#76685D",
            focus="#B45C30", success="#47704A", warning="#805000",
            error="#A43B35", work="#864A24", short_break="#566940",
            long_break="#714D72", overwork="#9D3940",
            short_break_overrun="#9D3940", long_break_overrun="#9D3940",
            on_accent="#FFFFFF",
        ),
        APPEARANCE_DARK: ThemePalette(
            background="#1B1714", card_background="#241E1A",
            secondary_background="#302720", text_primary="#FAF5EE",
            text_secondary="#CCBFB2", accent="#E99A68",
            accent_hover="#F2B083", button_background="#302720",
            button_text="#FAF5EE", border="#493C32", disabled="#97887B",
            focus="#FFB485", success="#86C98D", warning="#E8B86A",
            error="#F28E85", work="#E7A16F", short_break="#AFC287",
            long_break="#C6A1C7", overwork="#F08A8E",
            short_break_overrun="#F08A8E", long_break_overrun="#F08A8E",
            on_accent="#25140A",
        ),
    },
}


def is_hex_color(value: object) -> bool:
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


def normalize_builtin_theme_name(value: object) -> str:
    candidate = str(value or "").strip().casefold()
    for name in BUILTIN_THEME_NAMES:
        if candidate == name.casefold():
            return name
    return DEFAULT_THEME_NAME


def default_custom_theme(base_theme: object = DEFAULT_THEME_NAME) -> dict[str, dict[str, str]]:
    normalized_base = normalize_builtin_theme_name(base_theme)
    return {
        mode: PALETTES[normalized_base][mode].as_dict()
        for mode in APPEARANCE_MODES
    }


def normalize_custom_theme(value: object) -> dict[str, dict[str, str]]:
    raw = value if isinstance(value, dict) else {}
    return {
        mode: normalize_palette_data(raw.get(mode), PALETTES[DEFAULT_THEME_NAME][mode])
        for mode in APPEARANCE_MODES
    }


def palette_from_data(value: object, fallback: ThemePalette) -> ThemePalette:
    return ThemePalette(**normalize_palette_data(value, fallback))


def relative_luminance(color: str) -> float:
    channels = []
    for offset in (1, 3, 5):
        channel = int(color[offset: offset + 2], 16) / 255
        channels.append(
            channel / 12.92
            if channel <= 0.04045
            else ((channel + 0.055) / 1.055) ** 2.4
        )
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast_ratio(first: str, second: str) -> float:
    first_luminance = relative_luminance(first)
    second_luminance = relative_luminance(second)
    lighter = max(first_luminance, second_luminance)
    darker = min(first_luminance, second_luminance)
    return (lighter + 0.05) / (darker + 0.05)


def palette_contrast_warnings(palette: ThemePalette) -> list[str]:
    pairs = (
        ("theme.contrast.primary_card", palette.text_primary, palette.card_background),
        ("theme.contrast.secondary_card", palette.text_secondary, palette.card_background),
        ("theme.contrast.button", palette.button_text, palette.button_background),
        ("theme.contrast.accent", palette.on_accent, palette.accent),
        ("theme.contrast.work", palette.work, palette.card_background),
        ("theme.contrast.short_break", palette.short_break, palette.card_background),
        ("theme.contrast.long_break", palette.long_break, palette.card_background),
        ("theme.contrast.overwork", palette.overwork, palette.card_background),
        ("theme.contrast.short_break_overrun", palette.short_break_overrun, palette.card_background),
        ("theme.contrast.long_break_overrun", palette.long_break_overrun, palette.card_background),
    )
    return [
        f"{label}|{contrast_ratio(foreground, background):.2f}:1"
        for label, foreground, background in pairs
        if contrast_ratio(foreground, background) < 4.5
    ]


class CustomThemeDraft:
    """Черновик редактора, отделяющий предпросмотр от сохранённой темы."""

    def __init__(self, custom_theme: object) -> None:
        self.saved = normalize_custom_theme(custom_theme)
        self.value = deepcopy(self.saved)

    def set_mode(self, mode: object, palette_data: object) -> None:
        normalized_mode = normalize_appearance_mode(mode)
        self.value[normalized_mode] = normalize_palette_data(
            palette_data, PALETTES[DEFAULT_THEME_NAME][normalized_mode]
        )

    def create_mode_from(self, mode: object, base_theme: object) -> None:
        normalized_mode = normalize_appearance_mode(mode)
        normalized_base = normalize_builtin_theme_name(base_theme)
        self.value[normalized_mode] = PALETTES[normalized_base][normalized_mode].as_dict()

    def reset_mode(self, mode: object) -> None:
        self.create_mode_from(mode, DEFAULT_THEME_NAME)

    def reset_all(self) -> None:
        self.value = default_custom_theme()

    def cancel(self) -> dict[str, dict[str, str]]:
        return deepcopy(self.saved)

    def applied(self) -> dict[str, dict[str, str]]:
        return normalize_custom_theme(self.value)


def normalize_theme_name(value: object) -> str:
    candidate = str(value or "").strip().casefold()
    if candidate == "пользовательская":
        return CUSTOM_THEME_NAME
    for name in THEME_NAMES:
        if candidate == name.casefold():
            return name
    return DEFAULT_THEME_NAME


def normalize_appearance_mode(value: object) -> str:
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


class ThemeManager(QObject):
    """Применяет одну QSS-палитру и уведомляет открытые custom-компоненты."""

    changed = Signal(object)

    def __init__(self, root: QWidget | QApplication | None = None) -> None:
        super().__init__()
        self.root = root
        self.theme_name = DEFAULT_THEME_NAME
        self.appearance_mode = DEFAULT_APPEARANCE_MODE
        self.custom_theme = default_custom_theme()
        self.palette = get_palette(self.theme_name, self.appearance_mode, self.custom_theme)
        self._listeners: list[Callable[[ThemePalette], None] | weakref.WeakMethod] = []
        self._applied_signature: tuple[str, str, tuple[tuple[str, str], ...]] | None = None
        self._stylesheet_install_count = 0

    def register(self, listener: Callable[[ThemePalette], None]) -> None:
        if any(self._resolve_listener(item) == listener for item in self._listeners):
            listener(self.palette)
            return
        owner = getattr(listener, "__self__", None)
        self._listeners.append(weakref.WeakMethod(listener) if owner is not None else listener)
        listener(self.palette)

    @property
    def stylesheet_install_count(self) -> int:
        """Диагностический счётчик: глобальный QSS не должен ставиться на каждую тему."""
        return self._stylesheet_install_count

    def unregister(self, listener: Callable[[ThemePalette], None]) -> None:
        self._listeners = [
            item for item in self._listeners
            if self._resolve_listener(item) not in (None, listener)
        ]

    @staticmethod
    def _resolve_listener(
        listener: Callable[[ThemePalette], None] | weakref.WeakMethod,
    ) -> Callable[[ThemePalette], None] | None:
        return listener() if isinstance(listener, weakref.WeakMethod) else listener

    def apply(
        self,
        theme_name: object,
        appearance_mode: object,
        custom_theme: object = None,
    ) -> ThemePalette:
        normalized_theme = normalize_theme_name(theme_name)
        normalized_mode = normalize_appearance_mode(appearance_mode)
        if custom_theme is not None:
            self.custom_theme = normalize_custom_theme(custom_theme)
        palette = get_palette(normalized_theme, normalized_mode, self.custom_theme)
        signature = (normalized_theme, normalized_mode, tuple(sorted(palette.as_dict().items())))
        if self._applied_signature == signature:
            return self.palette

        self.theme_name = normalized_theme
        self.appearance_mode = normalized_mode
        self.palette = palette
        self._applied_signature = signature
        from app.ui.design_system import build_application_palette, build_stylesheet

        application = QApplication.instance()
        if application is not None:
            application.setPalette(build_application_palette(self.palette))
            stylesheet = build_stylesheet()
            if application.styleSheet() != stylesheet:
                application.setStyleSheet(stylesheet)
                self._stylesheet_install_count += 1
            else:
                # QSS palette(...) вычисляется при polish. Один контролируемый
                # проход заметно дешевле повторного QApplication.setStyleSheet().
                for widget in application.allWidgets():
                    if widget.isVisible():
                        self._repolish(widget)
            for window in application.topLevelWidgets():
                if window.windowType() not in (
                    Qt.WindowType.Popup,
                    Qt.WindowType.ToolTip,
                ):
                    self.apply_to_window(window)
        elif isinstance(self.root, QWidget):
            self.apply_to_window(self.root)
        live_listeners = []
        for reference in tuple(self._listeners):
            listener = self._resolve_listener(reference)
            if listener is None:
                continue
            try:
                listener(self.palette)
            except RuntimeError:
                # Qt-объект мог быть удалён через deleteLater между кадрами.
                continue
            live_listeners.append(reference)
        self._listeners = live_listeners
        self.changed.emit(self.palette)
        return self.palette

    def apply_to_window(self, window: QWidget) -> None:
        window.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        from app.ui.qt_app import apply_windows_title_bar

        dark = self.appearance_mode == APPEARANCE_DARK
        apply_windows_title_bar(window, dark)

        # Windows применяет собственную тему non-client area в момент первого показа
        # HWND и может перезаписать слишком ранний вызов DWM. Повтор в следующем
        # обороте GUI-цикла оставляет системную рамку нативной и не создаёт таймер.
        def refresh_native_frame() -> None:
            try:
                apply_windows_title_bar(window, self.appearance_mode == APPEARANCE_DARK)
            except RuntimeError:
                # Окно могло быть закрыто через deleteLater до выполнения singleShot.
                return

        QTimer.singleShot(0, refresh_native_frame)
        window.update()

    def refresh_widget_tree(self, root: QWidget, *, visible_only: bool = True) -> None:
        """Обновляет страницу при показе; скрытые страницы не замедляют смену темы."""
        for widget in (root, *root.findChildren(QWidget)):
            if not visible_only or widget.isVisible():
                self._repolish(widget)

    @staticmethod
    def _repolish(widget: QWidget) -> None:
        style = widget.style()
        style.unpolish(widget)
        style.polish(widget)
        widget.update()

    def mode_style(self, mode: TimerMode, waiting_for_continue: bool) -> str:
        """Совместимый семантический результат для простых UI-адаптеров."""
        return mode_color(self.palette, mode, waiting_for_continue)

    def apply_timer_effect(self, _digits_color: str | None, _card_background: str | None) -> None:
        """Эффект теперь применяется целевым TimerVisual, а не глобальным QSS."""


class Tooltip:
    """Совместимый адаптер к нативной доступной подсказке Qt."""

    def __init__(self, widget: QWidget, text: str, _theme_manager: ThemeManager) -> None:
        widget.setToolTip(text)
