"""Отрисовка векторных индикаторов одного кадра без собственных циклов."""

import tkinter as tk

from app.overrun_effects import OverrunVisualFrame, interpolate_color
from app.theme import ThemePalette


def draw_beacon(
    canvas: tk.Canvas,
    frame: OverrunVisualFrame,
    palette: ThemePalette,
    *,
    small: bool = False,
) -> None:
    """Рисует мягкий сигнальный маячок средствами Canvas."""
    canvas.delete("all")
    background = frame.card_background or palette.card_background
    canvas.configure(bg=background)
    if not frame.active or frame.beacon_level <= 0.0 or frame.effect_color is None:
        return
    color = interpolate_color(
        palette.secondary_background,
        frame.effect_color,
        frame.beacon_level,
    )
    padding = 3 if small else 2
    width = max(8, canvas.winfo_width())
    height = max(8, canvas.winfo_height())
    canvas.create_oval(
        padding,
        padding,
        width - padding,
        height - padding,
        fill=color,
        outline="",
    )


def draw_wave(
    canvas: tk.Canvas,
    frame: OverrunVisualFrame,
    palette: ThemePalette,
) -> None:
    """Рисует статичную линию или общий движущийся цветовой сегмент."""
    canvas.delete("all")
    background = frame.card_background or palette.card_background
    canvas.configure(bg=background)
    if not frame.active or frame.wave_position is None or frame.effect_color is None:
        return
    width = max(24, canvas.winfo_width())
    height = max(6, canvas.winfo_height())
    y = height / 2
    margin = 3
    usable = max(1.0, width - (margin * 2))
    canvas.create_line(
        margin,
        y,
        width - margin,
        y,
        fill=palette.border,
        width=1,
    )
    segment = max(12.0, usable * 0.28)
    center = margin + (usable * frame.wave_position)
    start = max(margin, center - (segment / 2))
    finish = min(width - margin, center + (segment / 2))
    canvas.create_line(
        start,
        y,
        finish,
        y,
        fill=frame.effect_color,
        width=3,
        capstyle=tk.ROUND,
    )
