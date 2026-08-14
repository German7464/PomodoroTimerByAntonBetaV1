"""Загрузка и тематическая окраска проектных SVG-иконок."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from PySide6.QtCore import QByteArray, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer


ICON_DIR = Path(__file__).resolve().parents[2] / "assets" / "icons"


@lru_cache(maxsize=128)
def themed_icon(name: str, color: str, size: int = 20) -> QIcon:
    """Возвращает SVG как чёткую QIcon нужного смыслового цвета."""
    path = ICON_DIR / f"{name}.svg"
    try:
        source = path.read_text(encoding="utf-8")
    except OSError:
        return QIcon()
    source = source.replace("#000000", QColor(color).name().upper())
    renderer = QSvgRenderer(QByteArray(source.encode("utf-8")))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap)
