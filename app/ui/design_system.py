"""Единые токены и QSS профессионального интерфейса Pomodoro Timer."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QWidget

from app.theme import ThemePalette


@dataclass(frozen=True)
class Typography:
    """Типографическая шкала в логических пикселях Qt."""

    family: str = "Segoe UI Variable Text"
    fallback: str = "Segoe UI"
    mono: str = "Cascadia Mono"
    caption: int = 12
    body: int = 14
    body_large: int = 16
    title: int = 20
    headline: int = 28
    timer: int = 72


@dataclass(frozen=True)
class Spacing:
    xxs: int = 4
    xs: int = 8
    sm: int = 12
    md: int = 16
    lg: int = 24
    xl: int = 32
    xxl: int = 48


@dataclass(frozen=True)
class Radii:
    small: int = 8
    control: int = 10
    card: int = 16
    large: int = 22
    pill: int = 999


@dataclass(frozen=True)
class ControlSizes:
    height: int = 42
    compact_height: int = 34
    touch_target: int = 40
    toggle_width: int = 64
    toggle_height: int = 32
    sidebar_width: int = 220
    content_max_width: int = 1080


@dataclass(frozen=True)
class Motion:
    fast_ms: int = 120
    normal_ms: int = 170
    slow_ms: int = 240
    easing: str = "out-cubic"
    overrun_frame_ms: int = 80


@dataclass(frozen=True)
class DesignSystem:
    typography: Typography = Typography()
    spacing: Spacing = Spacing()
    radii: Radii = Radii()
    controls: ControlSizes = ControlSizes()
    motion: Motion = Motion()
    border_width: int = 1
    focus_width: int = 2
    shadow_blur: int = 28
    shadow_y: int = 8
    shadow_alpha: int = 36


TOKENS = DesignSystem()


def rgba(color: str, alpha: int) -> str:
    """Возвращает QSS rgba из смыслового HEX-цвета."""
    value = QColor(color)
    return f"rgba({value.red()}, {value.green()}, {value.blue()}, {alpha})"


def apply_card_shadow(widget: QWidget, palette: ThemePalette) -> None:
    """Добавляет одну мягкую тему-зависимую тень карточке."""
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(TOKENS.shadow_blur)
    shadow.setOffset(0, TOKENS.shadow_y)
    color = QColor(palette.text_primary)
    color.setAlpha(TOKENS.shadow_alpha)
    shadow.setColor(color)
    widget.setGraphicsEffect(shadow)


def build_application_palette(p: ThemePalette) -> QPalette:
    """Отображает смысловые цвета темы на стандартные роли Qt."""
    palette = QPalette()
    roles = {
        QPalette.ColorRole.Window: p.background,
        QPalette.ColorRole.WindowText: p.text_primary,
        QPalette.ColorRole.Base: p.card_background,
        QPalette.ColorRole.AlternateBase: p.secondary_background,
        QPalette.ColorRole.Text: p.text_primary,
        QPalette.ColorRole.Button: p.button_background,
        QPalette.ColorRole.ButtonText: p.button_text,
        QPalette.ColorRole.Highlight: p.accent,
        QPalette.ColorRole.HighlightedText: p.on_accent,
        QPalette.ColorRole.PlaceholderText: p.text_secondary,
        QPalette.ColorRole.ToolTipBase: p.text_primary,
        QPalette.ColorRole.ToolTipText: p.background,
        QPalette.ColorRole.Mid: p.border,
        QPalette.ColorRole.Dark: p.border,
        QPalette.ColorRole.Light: p.secondary_background,
        QPalette.ColorRole.Link: p.error,
        QPalette.ColorRole.LinkVisited: p.warning,
    }
    accent_role = getattr(QPalette.ColorRole, "Accent", None)
    if accent_role is not None:
        roles[accent_role] = p.accent
    for role, color in roles.items():
        palette.setColor(role, QColor(color))
    for group in (QPalette.ColorGroup.Disabled, QPalette.ColorGroup.Inactive):
        for role in (
            QPalette.ColorRole.WindowText,
            QPalette.ColorRole.Text,
            QPalette.ColorRole.ButtonText,
            QPalette.ColorRole.PlaceholderText,
        ):
            palette.setColor(group, role, QColor(p.disabled))
    return palette


@lru_cache(maxsize=1)
def build_stylesheet() -> str:
    """Возвращает один QSS, который получает цвета через текущий QPalette."""
    t = TOKENS
    return f"""
    * {{
        font-family: "{t.typography.family}", "{t.typography.fallback}", "Microsoft YaHei UI", "Nirmala UI", "Yu Gothic UI", "Meiryo UI", "Malgun Gothic", "Arial";
        outline: none;
    }}
    QMainWindow, QDialog, QWidget#AppRoot {{
        background: palette(window);
        color: palette(window-text);
    }}
    QWidget {{ color: palette(window-text); }}
    QScrollArea, QAbstractScrollArea, QStackedWidget,
    QWidget#qt_scrollarea_viewport, QWidget[pageSurface="true"] {{
        background: palette(window);
        border: none;
    }}
    QFrame#Sidebar {{
        background: palette(alternate-base);
        border-right: 1px solid palette(mid);
    }}
    QFrame[card="true"], QGroupBox {{
        background: palette(base);
        border: 1px solid palette(mid);
        border-radius: {t.radii.card}px;
    }}
    QFrame[tone="subtle"] {{
        background: palette(alternate-base);
        border: 1px solid palette(mid);
        border-radius: {t.radii.control}px;
    }}
    QLabel[role="pageTitle"] {{
        font-size: {t.typography.headline}px;
        font-weight: 650;
        color: palette(window-text);
    }}
    QLabel[role="sectionTitle"] {{
        font-size: {t.typography.title}px;
        font-weight: 650;
        color: palette(window-text);
    }}
    QLabel[role="subtitle"], QLabel[muted="true"] {{
        color: palette(placeholder-text);
    }}
    QLabel[role="caption"] {{
        color: palette(placeholder-text);
        font-size: {t.typography.caption}px;
    }}
    QLabel[role="timer"] {{
        font-weight: 700;
        color: palette(window-text);
    }}
    QLabel[role="mode"] {{
        font-weight: 650;
    }}
    QLabel[role="metric"] {{
        font-size: {t.typography.title}px;
        font-weight: 700;
        color: palette(highlight);
    }}
    QLabel[role="statusChip"] {{
        background: palette(alternate-base);
        border: 1px solid palette(mid);
        border-radius: 12px;
        padding: 4px 10px;
        font-weight: 600;
    }}
    QPushButton {{
        min-height: {t.controls.height}px;
        padding: 0 {t.spacing.md}px;
        background: palette(button);
        color: palette(button-text);
        border: 1px solid palette(mid);
        border-radius: {t.radii.control}px;
        font-weight: 600;
    }}
    QPushButton:hover {{ background: palette(alternate-base); border-color: palette(highlight); }}
    QPushButton:pressed {{ background: palette(mid); }}
    QPushButton:disabled {{ color: palette(placeholder-text); background: palette(alternate-base); border-color: palette(mid); }}
    QPushButton[variant="primary"] {{ background: palette(highlight); color: palette(highlighted-text); border-color: palette(highlight); }}
    QPushButton[variant="primary"]:hover {{ background: palette(highlight); border-color: palette(highlight); }}
    QPushButton[variant="ghost"] {{ background: transparent; border-color: transparent; color: palette(window-text); }}
    QPushButton[variant="ghost"]:hover {{ background: palette(alternate-base); border-color: palette(mid); }}
    QPushButton[variant="danger"] {{ background: transparent; color: palette(link); border-color: palette(link); }}
    QPushButton[variant="danger"]:hover {{ background: palette(alternate-base); }}
    QPushButton[variant="primary"]:disabled,
    QPushButton[variant="ghost"]:disabled,
    QPushButton[variant="danger"]:disabled {{
        color: palette(placeholder-text);
        background: palette(alternate-base);
        border-color: palette(mid);
    }}
    QPushButton[nav="true"] {{
        min-height: 44px;
        text-align: left;
        padding-left: {t.spacing.md}px;
        background: transparent;
        border-color: transparent;
        color: palette(placeholder-text);
    }}
    QPushButton[nav="true"]:hover {{ background: palette(base); color: palette(window-text); }}
    QPushButton[nav="true"]:checked {{ background: palette(base); color: palette(highlight); border-color: palette(mid); }}
    QLineEdit, QSpinBox, QComboBox {{
        min-height: {t.controls.height}px;
        padding: 0 {t.spacing.sm}px;
        background: palette(base);
        color: palette(text);
        selection-background-color: palette(highlight);
        selection-color: palette(highlighted-text);
        border: 1px solid palette(mid);
        border-radius: {t.radii.control}px;
    }}
    QLineEdit:hover, QSpinBox:hover, QComboBox:hover {{ border-color: palette(highlight); }}
    QLineEdit:focus, QSpinBox:focus, QComboBox:focus {{ border: {t.focus_width}px solid palette(highlight); }}
    QLineEdit[invalid="true"] {{ border: {t.focus_width}px solid palette(link); }}
    QLineEdit:disabled, QSpinBox:disabled, QComboBox:disabled {{ color: palette(placeholder-text); background: palette(alternate-base); }}
    QComboBox::drop-down {{ border: none; width: 30px; }}
    QComboBox QAbstractItemView {{
        background: palette(base); color: palette(text);
        border: 1px solid palette(mid); selection-background-color: palette(highlight);
        selection-color: palette(highlighted-text); padding: 4px;
    }}
    QListWidget, QTextBrowser, QPlainTextEdit {{
        background: palette(base);
        color: palette(text);
        border: 1px solid palette(mid);
        border-radius: {t.radii.control}px;
        padding: {t.spacing.xs}px;
        selection-background-color: palette(highlight);
        selection-color: palette(highlighted-text);
    }}
    QListWidget::item {{ padding: 9px; border-radius: 7px; }}
    QListWidget::item:hover {{ background: palette(alternate-base); }}
    QListWidget::item:selected {{ background: palette(highlight); color: palette(highlighted-text); }}
    QTabWidget::pane {{ border: none; background: transparent; top: -1px; }}
    QTabBar::tab {{
        min-height: 34px; padding: 0 {t.spacing.md}px; margin-right: 4px;
        color: palette(placeholder-text); background: transparent;
        border: 1px solid transparent; border-radius: {t.radii.small}px;
    }}
    QTabBar::tab:hover {{ background: palette(alternate-base); color: palette(window-text); }}
    QTabBar::tab:selected {{ background: palette(base); color: palette(highlight); border-color: palette(mid); }}
    QSlider::groove:horizontal {{ height: 6px; background: palette(alternate-base); border-radius: 3px; }}
    QSlider::sub-page:horizontal {{ background: palette(highlight); border-radius: 3px; }}
    QSlider::handle:horizontal {{
        width: 18px; height: 18px; margin: -6px 0;
        background: palette(base); border: 2px solid palette(highlight); border-radius: 9px;
    }}
    QSlider::handle:horizontal:hover {{ border-color: palette(highlight); }}
    QScrollBar:vertical {{ width: 10px; background: transparent; margin: 2px; }}
    QScrollBar::handle:vertical {{ background: palette(mid); border-radius: 5px; min-height: 28px; }}
    QScrollBar::handle:vertical:hover {{ background: palette(placeholder-text); }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
    QToolTip {{
        background: palette(tool-tip-base); color: palette(tool-tip-text); border: none;
        border-radius: {t.radii.small}px; padding: 6px 9px;
    }}
    QMenu {{
        background: palette(base); color: palette(text);
        border: 1px solid palette(mid); border-radius: {t.radii.control}px;
        padding: {t.spacing.xs}px;
    }}
    QMenu::item {{ padding: 8px 28px 8px 12px; border-radius: {t.radii.small}px; }}
    QMenu::item:selected {{ background: palette(highlight); color: palette(highlighted-text); }}
    QMenu::item:disabled {{ color: palette(placeholder-text); }}
    QMenu::separator {{ height: 1px; background: palette(mid); margin: 6px 8px; }}
    """


@lru_cache(maxsize=16)
def build_menu_stylesheet(p: ThemePalette) -> str:
    """Явный QSS контекстного меню трея на базе его QPalette."""
    t = TOKENS
    return f"""
    QMenu {{
        background: {p.card_background}; color: {p.text_primary};
        border: 1px solid {p.border}; border-radius: {t.radii.control}px;
        padding: {t.spacing.xs}px;
    }}
    QMenu::item {{ padding: 8px 28px 8px 12px; border-radius: {t.radii.small}px; }}
    QMenu::item:selected {{ background: {p.accent}; color: {p.on_accent}; }}
    QMenu::item:disabled {{ color: {p.disabled}; }}
    QMenu::separator {{ height: 1px; background: {p.border}; margin: 6px 8px; }}
    """
