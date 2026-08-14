"""Генерирует PNG-набор и многослойный Windows ICO из assets/icons/app.svg."""

from __future__ import annotations

from pathlib import Path
import struct

from PySide6.QtCore import QByteArray, QBuffer, QIODevice, QRectF
from PySide6.QtGui import QImage, QPainter
from PySide6.QtSvg import QSvgRenderer


ROOT = Path(__file__).resolve().parents[1]
ICON_DIR = ROOT / "assets" / "icons"
SIZES = (16, 20, 24, 32, 48, 64, 128, 256)


def render_png(renderer: QSvgRenderer, size: int) -> bytes:
    image = QImage(size, size, QImage.Format.Format_ARGB32_Premultiplied)
    image.fill(0)
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    renderer.render(painter, QRectF(0, 0, size, size))
    painter.end()
    data = QByteArray()
    buffer = QBuffer(data)
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    if not image.save(buffer, "PNG"):
        raise RuntimeError(f"Qt не смог сохранить PNG {size}x{size}")
    return bytes(data)


def write_ico(path: Path, images: list[tuple[int, bytes]]) -> None:
    header_size = 6 + 16 * len(images)
    offset = header_size
    entries = []
    payload = []
    for size, png in images:
        dimension = 0 if size == 256 else size
        entries.append(
            struct.pack(
                "<BBBBHHII",
                dimension,
                dimension,
                0,
                0,
                1,
                32,
                len(png),
                offset,
            )
        )
        payload.append(png)
        offset += len(png)
    path.write_bytes(
        struct.pack("<HHH", 0, 1, len(images)) + b"".join(entries) + b"".join(payload)
    )


def main() -> None:
    source = ICON_DIR / "app.svg"
    renderer = QSvgRenderer(str(source))
    if not renderer.isValid():
        raise RuntimeError(f"Некорректный SVG: {source}")
    images = []
    for size in SIZES:
        png = render_png(renderer, size)
        (ICON_DIR / f"app-{size}.png").write_bytes(png)
        images.append((size, png))
    write_ico(ICON_DIR / "app.ico", images)
    print(f"Созданы {len(images)} PNG и ICO с {len(images)} размерами в {ICON_DIR}")


if __name__ == "__main__":
    main()
