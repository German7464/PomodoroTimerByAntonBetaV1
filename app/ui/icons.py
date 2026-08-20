"""Загрузка и тематическая окраска проектных SVG-иконок."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from PySide6.QtCore import QByteArray, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap, QTransform
from PySide6.QtSvg import QSvgRenderer


ICON_DIR = Path(__file__).resolve().parents[2] / "assets" / "icons"


@lru_cache(maxsize=32)
def _svg_source(name: str) -> str:
    try:
        return (ICON_DIR / f"{name}.svg").read_text(encoding="utf-8")
    except OSError:
        return ""


@lru_cache(maxsize=128)
def themed_icon(name: str, color: str, size: int = 20, mirrored: bool = False) -> QIcon:
    """Возвращает SVG как чёткую QIcon нужного смыслового цвета."""
    source = _svg_source(name)
    if not source:
        return QIcon()
    source = source.replace("#000000", QColor(color).name().upper())
    renderer = QSvgRenderer(QByteArray(source.encode("utf-8")))
    icon = QIcon()
    for scale in (1.0, 1.5, 2.0):
        pixels = max(1, round(size * scale))
        pixmap = QPixmap(pixels, pixels)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        renderer.render(painter)
        painter.end()
        if mirrored:
            pixmap = pixmap.transformed(QTransform().scale(-1, 1))
        pixmap.setDevicePixelRatio(scale)
        icon.addPixmap(pixmap)
    return icon


@lru_cache(maxsize=1)
def application_icon() -> QIcon:
    """Возвращает многослойную Windows-иконку с SVG fallback."""
    ico = ICON_DIR / "app.ico"
    if ico.exists():
        icon = QIcon(str(ico))
        if not icon.isNull():
            return icon
    return QIcon(str(ICON_DIR / "app.svg"))


@lru_cache(maxsize=1)
def tray_icon() -> QIcon:
    """Контрастный малодетальный вариант для системного трея."""
    icon = QIcon(str(ICON_DIR / "tray.svg"))
    return icon if not icon.isNull() else application_icon()
