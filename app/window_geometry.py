"""Безопасная нормализация геометрии главного окна без зависимости от Qt."""

from __future__ import annotations

from typing import Iterable


MAIN_WINDOW_MIN_WIDTH = 820
MAIN_WINDOW_MIN_HEIGHT = 560
MAIN_WINDOW_MAX_WIDTH = 1440
MAIN_WINDOW_MAX_HEIGHT = 960
MAIN_WINDOW_SCREEN_RATIO = 0.80


def normalize_main_window_geometry(value: object) -> dict[str, int]:
    """Возвращает полный безопасный прямоугольник либо пустой first-run marker."""
    if not isinstance(value, dict):
        return {}
    try:
        x = int(value["x"])
        y = int(value["y"])
        width = int(value["width"])
        height = int(value["height"])
    except (KeyError, TypeError, ValueError, OverflowError):
        return {}
    if width < 320 or height < 320 or width > 20_000 or height > 20_000:
        return {}
    if not (-100_000 <= x <= 100_000 and -100_000 <= y <= 100_000):
        return {}
    return {"x": x, "y": y, "width": width, "height": height}


def fit_main_window_geometry(
    saved: object,
    screens: Iterable[tuple[int, int, int, int]],
) -> dict[str, int]:
    """Выбирает экран, ограничивает размер и полностью возвращает окно в видимую область."""
    available = [tuple(map(int, screen)) for screen in screens if screen[2] > 0 and screen[3] > 0]
    if not available:
        available = [(0, 0, 1280, 720)]
    normalized = normalize_main_window_geometry(saved)
    if normalized:
        target = max(available, key=lambda screen: _intersection_area(normalized, screen))
        if _intersection_area(normalized, target) == 0:
            target = available[0]
        width = min(target[2], max(MAIN_WINDOW_MIN_WIDTH, normalized["width"]))
        height = min(target[3], max(MAIN_WINDOW_MIN_HEIGHT, normalized["height"]))
        x = min(max(normalized["x"], target[0]), target[0] + target[2] - width)
        y = min(max(normalized["y"], target[1]), target[1] + target[3] - height)
    else:
        target = available[0]
        width = min(
            target[2],
            MAIN_WINDOW_MAX_WIDTH,
            max(MAIN_WINDOW_MIN_WIDTH, round(target[2] * MAIN_WINDOW_SCREEN_RATIO)),
        )
        height = min(
            target[3],
            MAIN_WINDOW_MAX_HEIGHT,
            max(MAIN_WINDOW_MIN_HEIGHT, round(target[3] * MAIN_WINDOW_SCREEN_RATIO)),
        )
        x = target[0] + (target[2] - width) // 2
        y = target[1] + (target[3] - height) // 2
    return {"x": x, "y": y, "width": width, "height": height}


def _intersection_area(rect: dict[str, int], screen: tuple[int, int, int, int]) -> int:
    left = max(rect["x"], screen[0])
    top = max(rect["y"], screen[1])
    right = min(rect["x"] + rect["width"], screen[0] + screen[2])
    bottom = min(rect["y"] + rect["height"], screen[1] + screen[3])
    return max(0, right - left) * max(0, bottom - top)
