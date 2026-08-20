"""Общая профессиональная отрисовка таймера и эффектов превышения."""

from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QFontMetrics, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget

from app.models import TimerMode
from app.i18n import localization_manager, timer_mode_text
from app.overrun_effects import INACTIVE_FRAME, OverrunVisualFrame
from app.theme import ThemeManager, ThemePalette, mode_color
from app.ui.design_system import TOKENS


class TimerVisual(QWidget):
    """Текст таймера и векторные эффекты без собственного цикла анимации."""

    def __init__(
        self,
        theme_manager: ThemeManager,
        parent: QWidget | None = None,
        *,
        base_font_size: int = 72,
        mode_font_size: int = 16,
        mono: bool = False,
        show_mode: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("TimerVisual")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._theme_manager = theme_manager
        self._palette = theme_manager.palette
        self._frame = INACTIVE_FRAME
        self._mode = TimerMode.WORK
        self._waiting = False
        self._base_font_size = base_font_size
        self._mode_font_size = mode_font_size
        self._mono = mono
        self._show_mode = show_mode

        self.content_layout = QVBoxLayout(self)
        self.content_layout.setContentsMargins(
            TOKENS.spacing.lg, TOKENS.spacing.md, TOKENS.spacing.lg, TOKENS.spacing.md
        )
        self.content_layout.setSpacing(TOKENS.spacing.xs)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mode_label = QLabel(timer_mode_text(TimerMode.WORK), self)
        self.mode_label.setProperty("role", "mode")
        self.mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mode_label.setWordWrap(True)
        self.mode_label.setVisible(show_mode)
        self.content_layout.addWidget(self.mode_label)
        self.time_label = QLabel("00:25:00", self)
        self.time_label.setProperty("role", "timer")
        self.time_label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._reserve_timer_height()
        self.content_layout.addWidget(self.time_label, 1)
        self.status_label = QLabel("", self)
        self.status_label.setProperty("role", "caption")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.hide()
        self.content_layout.addWidget(self.status_label)
        theme_manager.register(self._apply_theme)
        localization_manager().language_changed.connect(self._retranslate_ui)
        self._apply_fonts(1.0)

    @property
    def visual_frame(self) -> OverrunVisualFrame:
        return self._frame

    def set_base_font_size(self, size: int, mode_size: int | None = None) -> None:
        self._base_font_size = max(12, int(size))
        if mode_size is not None:
            self._mode_font_size = max(9, int(mode_size))
        self._reserve_timer_height()
        self._apply_fonts(self._frame.digit_scale)

    def set_state(
        self,
        mode_name: str,
        formatted_time: str,
        mode: TimerMode,
        waiting_for_continue: bool,
        status: str = "",
    ) -> None:
        self._mode = mode
        self._waiting = bool(waiting_for_continue)
        if not self._frame.preview:
            self.mode_label.setText(mode_name)
            self.time_label.setText(formatted_time)
        self.status_label.setText(status)
        self.status_label.setVisible(bool(status))
        self._apply_fonts(self._frame.digit_scale)
        self._refresh_colors()

    def apply_overrun_frame(self, frame: OverrunVisualFrame, *, short_format: bool = False) -> None:
        self._frame = frame
        if frame.preview and frame.mode is not None:
            self.mode_label.setText(timer_mode_text(frame.mode, True))
            self.time_label.setText("+00:03" if short_format else "+00:00:03")
            self._mode = frame.mode
            self._waiting = True
        self._apply_fonts(frame.digit_scale)
        self._refresh_colors()
        self.update()

    def reset_preview_state(
        self,
        mode_name: str,
        formatted_time: str,
        mode: TimerMode,
        waiting_for_continue: bool,
    ) -> None:
        self._mode = mode
        self._waiting = waiting_for_continue
        self.mode_label.setText(mode_name)
        self.time_label.setText(formatted_time)

    def _apply_fonts(self, scale: float) -> None:
        margin = self._responsive_horizontal_margin()
        self.content_layout.setContentsMargins(
            margin, TOKENS.spacing.md, margin, TOKENS.spacing.md
        )
        family = TOKENS.typography.mono if self._mono else TOKENS.typography.family
        requested_size = max(12, round(self._base_font_size * scale))
        timer_font = QFont(family, requested_size)
        timer_font.setWeight(QFont.Weight.Bold)
        timer_font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        available_width = max(40, self.width() - (margin * 2))
        sample = self.time_label.text() or "+00:00:00"
        while requested_size > 12 and QFontMetrics(timer_font).horizontalAdvance(sample) > available_width:
            requested_size -= 1
            timer_font.setPointSize(requested_size)
        self.time_label.setFont(timer_font)
        mode_font = QFont(TOKENS.typography.family, self._mode_font_size)
        mode_font.setWeight(QFont.Weight.DemiBold)
        self.mode_label.setFont(mode_font)

    def _reserve_timer_height(self) -> None:
        """Резервирует место под максимальный масштаб эффекта без скачка компоновки."""
        family = TOKENS.typography.mono if self._mono else TOKENS.typography.family
        largest = QFont(family, max(12, round(self._base_font_size * 1.15)))
        largest.setWeight(QFont.Weight.Bold)
        self.time_label.setMinimumHeight(QFontMetrics(largest).height() + TOKENS.spacing.xs * 2)

    def _beacon_geometry(self) -> tuple[float, float]:
        """Радиус и отступ маячка уменьшаются раньше, чем читаемая область цифр."""
        radius = max(2.5, min(7.0, self.width() / 70.0))
        inset = max(radius + 3.0, min(13.0, self.width() * 0.04))
        return radius, inset

    def _responsive_horizontal_margin(self) -> int:
        if self.width() < 220:
            margin = TOKENS.spacing.xs
        elif self.width() < 320:
            margin = TOKENS.spacing.sm
        else:
            margin = TOKENS.spacing.lg
        if self._frame.beacon_level > 0:
            radius, inset = self._beacon_geometry()
            margin = max(margin, round(inset + radius + 3))
        return margin

    def resizeEvent(self, event) -> None:  # noqa: N802 - Qt API
        super().resizeEvent(event)
        self._apply_fonts(self._frame.digit_scale)

    def _apply_theme(self, palette: ThemePalette) -> None:
        self._palette = palette
        self._refresh_colors()
        self.update()

    def _retranslate_ui(self, _language_code: str) -> None:
        if self._frame.preview and self._frame.mode is not None:
            self.mode_label.setText(timer_mode_text(self._frame.mode, True))
        self.updateGeometry()

    def _refresh_colors(self) -> None:
        p = self._palette
        frame = self._frame
        background = frame.card_background or p.card_background
        digits = frame.digits_color or p.text_primary
        state_color = mode_color(p, self._mode, self._waiting)
        self.setStyleSheet(
            f"QWidget#TimerVisual {{ background: {background}; border-radius: {TOKENS.radii.card}px; }}"
        )
        self.time_label.setStyleSheet(f"color: {digits}; background: transparent;")
        self.mode_label.setStyleSheet(f"color: {state_color}; background: transparent;")
        self.status_label.setStyleSheet(f"color: {p.text_secondary}; background: transparent;")

    def paintEvent(self, event) -> None:  # noqa: N802 - Qt API
        super().paintEvent(event)
        frame = self._frame
        if not frame.active:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        color = QColor(frame.effect_color or mode_color(self._palette, self._mode, True))
        bounds = QRectF(2, 2, self.width() - 4, self.height() - 4)

        if frame.border_color is not None and frame.border_width > 0:
            border = QColor(frame.border_color)
            border.setAlphaF(max(0.35, min(1.0, 0.55 + frame.phase * 0.35)))
            painter.setPen(QPen(border, frame.border_width))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(bounds, TOKENS.radii.card - 1, TOKENS.radii.card - 1)

        if frame.beacon_level > 0:
            beacon = QColor(color)
            beacon.setAlphaF(min(1.0, max(0.25, frame.beacon_level)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(beacon)
            radius, inset = self._beacon_geometry()
            center_y = self.height() / 2
            painter.drawEllipse(QPointF(inset, center_y), radius, radius)
            painter.drawEllipse(QPointF(self.width() - inset, center_y), radius, radius)

        if frame.wave_position is not None:
            y = self.height() - max(9, TOKENS.spacing.sm)
            left = max(24.0, self.width() * 0.18)
            right = min(self.width() - 24.0, self.width() * 0.82)
            painter.setPen(QPen(QColor(self._palette.border), 2))
            painter.drawLine(round(left), y, round(right), y)
            span = max(18.0, (right - left) * 0.24)
            center = left + (right - left) * frame.wave_position
            path = QPainterPath()
            path.moveTo(max(left, center - span), y)
            path.cubicTo(center - span / 2, y - 4, center + span / 2, y + 4, min(right, center + span), y)
            wave = QColor(color)
            wave.setAlphaF(0.9)
            painter.setPen(QPen(wave, 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            painter.drawPath(path)

    def closeEvent(self, event) -> None:  # noqa: N802 - Qt API
        self._theme_manager.unregister(self._apply_theme)
        super().closeEvent(event)
