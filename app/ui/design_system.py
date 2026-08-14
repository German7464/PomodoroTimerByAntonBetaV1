"""Единые токены и QSS профессионального интерфейса Pomodoro Timer."""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtGui import QColor
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


def build_stylesheet(p: ThemePalette) -> str:
    """Строит единый QSS для всех стандартных и проектных компонентов."""
    t = TOKENS
    return f"""
    * {{
        font-family: "{t.typography.family}", "{t.typography.fallback}";
        outline: none;
    }}
    QMainWindow, QDialog, QWidget#AppRoot {{
        background: {p.background};
        color: {p.text_primary};
    }}
    QWidget {{ color: {p.text_primary}; }}
    QFrame#Sidebar {{
        background: {p.secondary_background};
        border-right: 1px solid {p.border};
    }}
    QFrame[card="true"], QGroupBox {{
        background: {p.card_background};
        border: 1px solid {p.border};
        border-radius: {t.radii.card}px;
    }}
    QFrame[tone="subtle"] {{
        background: {p.secondary_background};
        border: 1px solid {p.border};
        border-radius: {t.radii.control}px;
    }}
    QLabel[role="pageTitle"] {{
        font-size: {t.typography.headline}px;
        font-weight: 650;
        color: {p.text_primary};
    }}
    QLabel[role="sectionTitle"] {{
        font-size: {t.typography.title}px;
        font-weight: 650;
        color: {p.text_primary};
    }}
    QLabel[role="subtitle"], QLabel[muted="true"] {{
        color: {p.text_secondary};
    }}
    QLabel[role="caption"] {{
        color: {p.text_secondary};
        font-size: {t.typography.caption}px;
    }}
    QLabel[role="timer"] {{
        font-weight: 700;
        color: {p.text_primary};
    }}
    QLabel[role="mode"] {{
        font-weight: 650;
    }}
    QLabel[role="metric"] {{
        font-size: {t.typography.title}px;
        font-weight: 700;
        color: {p.accent};
    }}
    QLabel[role="statusChip"] {{
        background: {p.secondary_background};
        border: 1px solid {p.border};
        border-radius: 12px;
        padding: 4px 10px;
        font-weight: 600;
    }}
    QPushButton {{
        min-height: {t.controls.height}px;
        padding: 0 {t.spacing.md}px;
        background: {p.button_background};
        color: {p.button_text};
        border: 1px solid {p.border};
        border-radius: {t.radii.control}px;
        font-weight: 600;
    }}
    QPushButton:hover {{ background: {p.secondary_background}; border-color: {p.focus}; }}
    QPushButton:pressed {{ background: {p.border}; }}
    QPushButton:focus {{ border: {t.focus_width}px solid {p.focus}; }}
    QPushButton:disabled {{ color: {p.disabled}; background: {p.secondary_background}; border-color: {p.border}; }}
    QPushButton[variant="primary"] {{ background: {p.accent}; color: {p.on_accent}; border-color: {p.accent}; }}
    QPushButton[variant="primary"]:hover {{ background: {p.accent_hover}; border-color: {p.accent_hover}; }}
    QPushButton[variant="ghost"] {{ background: transparent; border-color: transparent; color: {p.text_primary}; }}
    QPushButton[variant="ghost"]:hover {{ background: {p.secondary_background}; border-color: {p.border}; }}
    QPushButton[variant="danger"] {{ background: transparent; color: {p.error}; border-color: {p.error}; }}
    QPushButton[variant="danger"]:hover {{ background: {rgba(p.error, 28)}; }}
    QPushButton[variant="primary"]:disabled,
    QPushButton[variant="ghost"]:disabled,
    QPushButton[variant="danger"]:disabled {{
        color: {p.disabled};
        background: {p.secondary_background};
        border-color: {p.border};
    }}
    QPushButton[nav="true"] {{
        min-height: 44px;
        text-align: left;
        padding-left: {t.spacing.md}px;
        background: transparent;
        border-color: transparent;
        color: {p.text_secondary};
    }}
    QPushButton[nav="true"]:hover {{ background: {p.card_background}; color: {p.text_primary}; }}
    QPushButton[nav="true"]:checked {{ background: {p.card_background}; color: {p.accent}; border-color: {p.border}; }}
    QLineEdit, QSpinBox, QComboBox {{
        min-height: {t.controls.height}px;
        padding: 0 {t.spacing.sm}px;
        background: {p.card_background};
        color: {p.text_primary};
        selection-background-color: {p.accent};
        selection-color: {p.on_accent};
        border: 1px solid {p.border};
        border-radius: {t.radii.control}px;
    }}
    QLineEdit:hover, QSpinBox:hover, QComboBox:hover {{ border-color: {p.focus}; }}
    QLineEdit:focus, QSpinBox:focus, QComboBox:focus {{ border: {t.focus_width}px solid {p.focus}; }}
    QLineEdit:disabled, QSpinBox:disabled, QComboBox:disabled {{ color: {p.disabled}; background: {p.secondary_background}; }}
    QComboBox::drop-down {{ border: none; width: 30px; }}
    QComboBox QAbstractItemView {{
        background: {p.card_background}; color: {p.text_primary};
        border: 1px solid {p.border}; selection-background-color: {p.accent};
        selection-color: {p.on_accent}; padding: 4px;
    }}
    QListWidget, QTextBrowser, QPlainTextEdit {{
        background: {p.card_background};
        color: {p.text_primary};
        border: 1px solid {p.border};
        border-radius: {t.radii.control}px;
        padding: {t.spacing.xs}px;
        selection-background-color: {p.accent};
        selection-color: {p.on_accent};
    }}
    QListWidget::item {{ padding: 9px; border-radius: 7px; }}
    QListWidget::item:hover {{ background: {p.secondary_background}; }}
    QListWidget::item:selected {{ background: {p.accent}; color: {p.on_accent}; }}
    QTabWidget::pane {{ border: none; background: transparent; top: -1px; }}
    QTabBar::tab {{
        min-height: 34px; padding: 0 {t.spacing.md}px; margin-right: 4px;
        color: {p.text_secondary}; background: transparent;
        border: 1px solid transparent; border-radius: {t.radii.small}px;
    }}
    QTabBar::tab:hover {{ background: {p.secondary_background}; color: {p.text_primary}; }}
    QTabBar::tab:selected {{ background: {p.card_background}; color: {p.accent}; border-color: {p.border}; }}
    QSlider::groove:horizontal {{ height: 6px; background: {p.secondary_background}; border-radius: 3px; }}
    QSlider::sub-page:horizontal {{ background: {p.accent}; border-radius: 3px; }}
    QSlider::handle:horizontal {{
        width: 18px; height: 18px; margin: -6px 0;
        background: {p.card_background}; border: 2px solid {p.accent}; border-radius: 9px;
    }}
    QSlider::handle:horizontal:hover {{ border-color: {p.accent_hover}; }}
    QScrollBar:vertical {{ width: 10px; background: transparent; margin: 2px; }}
    QScrollBar::handle:vertical {{ background: {p.border}; border-radius: 5px; min-height: 28px; }}
    QScrollBar::handle:vertical:hover {{ background: {p.text_secondary}; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
    QToolTip {{
        background: {p.text_primary}; color: {p.background}; border: none;
        border-radius: {t.radii.small}px; padding: 6px 9px;
    }}
    """
