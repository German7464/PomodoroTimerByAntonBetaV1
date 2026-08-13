"""Переиспользуемый тематизированный переключатель двоичных настроек."""

from __future__ import annotations

from collections.abc import Callable
import time
import tkinter as tk
from typing import Final

from app.theme import ThemeManager, ThemePalette


TOGGLE_ANIMATION_MS: Final = 150
TOGGLE_FRAME_MS: Final = 15
TOGGLE_BASE_WIDTH: Final = 60
TOGGLE_BASE_HEIGHT: Final = 30


def _interpolate_color(first: str, second: str, fraction: float) -> str:
    """Смешивает два цвета #RRGGBB для короткой анимации основы."""
    amount = min(1.0, max(0.0, float(fraction)))
    channels = []
    for offset in (1, 3, 5):
        start = int(first[offset : offset + 2], 16)
        end = int(second[offset : offset + 2], 16)
        channels.append(round(start + (end - start) * amount))
    return "#" + "".join(f"{channel:02X}" for channel in channels)


class ToggleSwitch(tk.Frame):
    """Строка «название — ВКЛ/ВЫКЛ — ползунок» для одного BooleanVar."""

    def __init__(
        self,
        parent: tk.Misc,
        *,
        text: str,
        variable: tk.BooleanVar,
        command: Callable[[bool], None] | None = None,
        theme_manager: ThemeManager,
        enabled: bool = True,
        animations_enabled: bool | Callable[[], bool] = True,
        surface: str = "background",
    ) -> None:
        super().__init__(parent, borderwidth=0, highlightthickness=0, takefocus=0)
        self.variable = variable
        self.command = command
        self.theme_manager = theme_manager
        self._enabled = bool(enabled)
        self._animations_enabled = animations_enabled
        self._surface = surface
        self._palette = theme_manager.palette
        self._hovered = False
        self._pressed = False
        self._focused = False
        self._animation_id: str | None = None
        self._animation_started = 0.0
        initial_fraction = 1.0 if bool(variable.get()) else 0.0
        self._thumb_fraction = initial_fraction
        self._animation_from = initial_fraction
        self._animation_to = initial_fraction
        self._target_value = bool(variable.get())

        scaling = self._display_scaling()
        self._track_width = round(TOGGLE_BASE_WIDTH * scaling)
        self._track_height = round(TOGGLE_BASE_HEIGHT * scaling)

        self.columnconfigure(0, weight=1)
        self.label = tk.Label(
            self,
            text=text,
            anchor=tk.W,
            borderwidth=0,
            padx=0,
            pady=0,
            font=("Segoe UI", 10),
        )
        self.label.grid(row=0, column=0, sticky=tk.EW, padx=(0, 16))
        self.state_label = tk.Label(
            self,
            width=5,
            anchor=tk.E,
            borderwidth=0,
            padx=0,
            pady=0,
            font=("Segoe UI Semibold", 9),
        )
        self.state_label.grid(row=0, column=1, padx=(0, 8))
        self.canvas = tk.Canvas(
            self,
            width=self._track_width,
            height=self._track_height,
            borderwidth=0,
            highlightthickness=max(1, round(2 * scaling)),
            takefocus=1,
        )
        self.canvas.grid(row=0, column=2)

        for widget in (self.label, self.state_label, self.canvas):
            widget.bind("<Enter>", self._on_enter, add="+")
            widget.bind("<Leave>", self._on_leave, add="+")
            widget.bind("<ButtonPress-1>", self._on_press, add="+")
            widget.bind("<ButtonRelease-1>", self._on_release, add="+")
        self.canvas.bind("<FocusIn>", self._on_focus_in, add="+")
        self.canvas.bind("<FocusOut>", self._on_focus_out, add="+")
        self.canvas.bind("<KeyPress-space>", self._on_key, add="+")
        self.canvas.bind("<KeyPress-Return>", self._on_key, add="+")
        self.canvas.bind("<KeyPress-KP_Enter>", self._on_key, add="+")

        self._variable_trace = self.variable.trace_add("write", self._on_variable_changed)
        self.theme_manager.register(self.apply_theme)

    @property
    def value(self) -> bool:
        """Возвращает фактическое логическое значение связанной настройки."""
        return bool(self.variable.get())

    @property
    def state_text(self) -> str:
        """Возвращает доступную текстовую индикацию состояния."""
        return "ВКЛ" if self.value else "ВЫКЛ"

    @property
    def thumb_fraction(self) -> float:
        """Положение ползунка: 0 слева, 1 справа (полезно для UI-тестов)."""
        return self._thumb_fraction

    @property
    def animation_active(self) -> bool:
        return self._animation_id is not None

    def set(self, value: bool, *, invoke: bool = False) -> bool:
        """Синхронизирует внешний источник и при необходимости вызывает handler."""
        normalized = bool(value)
        if self.value == normalized:
            return False
        self.variable.set(normalized)
        if invoke and self.command is not None:
            self.command(normalized)
        return True

    def toggle(self) -> bool:
        """Меняет значение ровно один раз, если управление доступно."""
        if not self._enabled:
            return False
        return self.set(not self.value, invoke=True)

    def set_enabled(self, enabled: bool) -> None:
        """Включает или отключает мышь и клавиатуру без изменения значения."""
        self._enabled = bool(enabled)
        if not self._enabled:
            self._pressed = False
        self._apply_cursor()
        self._draw()

    def focus_set(self) -> None:
        """Передает клавиатурный фокус интерактивной части компонента."""
        self.canvas.focus_set()

    def apply_theme(self, palette: ThemePalette) -> None:
        """Применяет все цвета из смысловых токенов активной палитры."""
        self._palette = palette
        background = self._surface_color()
        self.configure(background=background)
        self.label.configure(background=background)
        self.state_label.configure(background=background)
        self.canvas.configure(background=background)
        self._apply_cursor()
        self._draw()

    def destroy(self) -> None:
        """Отменяет конечную анимацию и отсоединяет наблюдателей."""
        self._cancel_animation()
        try:
            self.variable.trace_remove("write", self._variable_trace)
        except (tk.TclError, AttributeError):
            pass
        self.theme_manager.unregister(self.apply_theme)
        super().destroy()

    def _display_scaling(self) -> float:
        try:
            # Tk scaling == 96/72 при масштабе Windows 100%.
            scaling = float(self.tk.call("tk", "scaling")) / (96 / 72)
        except (tk.TclError, TypeError, ValueError):
            scaling = 1.0
        return min(2.0, max(0.85, scaling))

    def _surface_color(self) -> str:
        if self._surface == "card_background":
            return self._palette.card_background
        if self._surface == "secondary_background":
            return self._palette.secondary_background
        return self._palette.background

    def _animations_are_enabled(self) -> bool:
        if callable(self._animations_enabled):
            try:
                return bool(self._animations_enabled())
            except (tk.TclError, RuntimeError):
                return False
        return bool(self._animations_enabled)

    def _on_variable_changed(self, *_args: str) -> None:
        target = bool(self.variable.get())
        if target == self._target_value:
            self._draw()
            return
        self._target_value = target
        self._animate_to(1.0 if target else 0.0)

    def _animate_to(self, target: float) -> None:
        self._cancel_animation()
        if not self._animations_are_enabled():
            self._thumb_fraction = target
            self._animation_from = target
            self._animation_to = target
            self._draw()
            return
        self._animation_from = self._thumb_fraction
        self._animation_to = target
        self._animation_started = time.monotonic()
        self._animation_id = self.after(0, self._animation_step)

    def _animation_step(self) -> None:
        self._animation_id = None
        elapsed_ms = (time.monotonic() - self._animation_started) * 1000
        progress = min(1.0, elapsed_ms / TOGGLE_ANIMATION_MS)
        eased = progress * progress * (3 - 2 * progress)
        self._thumb_fraction = self._animation_from + (
            self._animation_to - self._animation_from
        ) * eased
        self._draw()
        if progress < 1.0:
            self._animation_id = self.after(TOGGLE_FRAME_MS, self._animation_step)
        else:
            self._thumb_fraction = self._animation_to
            self._draw()

    def _cancel_animation(self) -> None:
        after_id = self._animation_id
        self._animation_id = None
        if after_id is None:
            return
        try:
            self.after_cancel(after_id)
        except tk.TclError:
            pass

    def _draw(self) -> None:
        if not self.winfo_exists():
            return
        palette = self._palette
        background = self._surface_color()
        self.label.configure(
            foreground=palette.text_primary if self._enabled else palette.disabled,
        )
        self.state_label.configure(
            text=self.state_text,
            foreground=(
                palette.accent
                if self._enabled and self.value
                else palette.text_secondary
                if self._enabled
                else palette.disabled
            ),
        )
        self.canvas.configure(
            highlightbackground=palette.focus if self._focused else background,
            highlightcolor=palette.focus,
        )
        self.canvas.delete("all")

        fraction = min(1.0, max(0.0, self._thumb_fraction))
        off_color = palette.secondary_background
        on_color = palette.accent_hover if self._hovered else palette.accent
        if not self._enabled:
            track_color = palette.secondary_background
        else:
            track_color = _interpolate_color(off_color, on_color, fraction)
        border_color = palette.focus if self._focused else palette.border
        if self._pressed and self._enabled:
            border_color = palette.accent_hover

        scale = self._track_height / TOGGLE_BASE_HEIGHT
        outer_padding = max(1, round(2 * scale))
        border = max(1, round(1 * scale))
        self._rounded_bar(
            outer_padding,
            outer_padding,
            self._track_width - outer_padding,
            self._track_height - outer_padding,
            border_color,
        )
        self._rounded_bar(
            outer_padding + border,
            outer_padding + border,
            self._track_width - outer_padding - border,
            self._track_height - outer_padding - border,
            track_color,
        )

        thumb_padding = max(3, round(4 * scale))
        diameter = self._track_height - 2 * thumb_padding
        left_center = thumb_padding + diameter / 2
        right_center = self._track_width - thumb_padding - diameter / 2
        center_x = left_center + (right_center - left_center) * fraction
        center_y = self._track_height / 2
        thumb_color = (
            palette.disabled
            if not self._enabled
            else _interpolate_color(palette.card_background, palette.on_accent, fraction)
        )
        self.canvas.create_oval(
            center_x - diameter / 2,
            center_y - diameter / 2,
            center_x + diameter / 2,
            center_y + diameter / 2,
            fill=thumb_color,
            outline="",
            tags=("thumb",),
        )

    def _rounded_bar(
        self,
        left: float,
        top: float,
        right: float,
        bottom: float,
        color: str,
    ) -> None:
        radius = (bottom - top) / 2
        self.canvas.create_rectangle(
            left + radius,
            top,
            right - radius,
            bottom,
            fill=color,
            outline="",
        )
        self.canvas.create_oval(
            left,
            top,
            left + 2 * radius,
            bottom,
            fill=color,
            outline="",
        )
        self.canvas.create_oval(
            right - 2 * radius,
            top,
            right,
            bottom,
            fill=color,
            outline="",
        )

    def _apply_cursor(self) -> None:
        cursor = "hand2" if self._enabled else "arrow"
        for widget in (self.label, self.state_label, self.canvas):
            widget.configure(cursor=cursor)

    def _on_enter(self, _event: tk.Event) -> None:
        self._hovered = True
        self._draw()

    def _on_leave(self, _event: tk.Event) -> None:
        self._hovered = False
        self._pressed = False
        self._draw()

    def _on_press(self, _event: tk.Event) -> str:
        if not self._enabled:
            return "break"
        self.canvas.focus_set()
        self._pressed = True
        self._draw()
        return "break"

    def _on_release(self, _event: tk.Event) -> str:
        if not self._enabled or not self._pressed:
            return "break"
        self._pressed = False
        self.toggle()
        self._draw()
        return "break"

    def _on_key(self, _event: tk.Event) -> str:
        self.toggle()
        return "break"

    def _on_focus_in(self, _event: tk.Event) -> None:
        self._focused = True
        self._draw()

    def _on_focus_out(self, _event: tk.Event) -> None:
        self._focused = False
        self._pressed = False
        self._draw()
