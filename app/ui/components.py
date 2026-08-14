"""Переиспользуемые Qt-компоненты дизайн-системы приложения."""

from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import (
    Property,
    QEasingCurve,
    QPointF,
    QPropertyAnimation,
    QRectF,
    QSize,
    Qt,
    Signal,
)
from PySide6.QtGui import QColor, QFont, QKeyEvent, QMouseEvent, QPainter, QPen
from PySide6.QtWidgets import (
    QAbstractButton,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.theme import ThemeManager, ThemePalette
from app.ui.design_system import TOKENS, apply_card_shadow
from app.ui.icons import themed_icon


def repolish(widget: QWidget) -> None:
    """Повторно применяет QSS после изменения dynamic property."""
    style = widget.style()
    style.unpolish(widget)
    style.polish(widget)
    widget.update()


class Card(QFrame):
    """Скруглённая поверхность с едиными отступами и необязательной тенью."""

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        padding: int | None = None,
        shadow: bool = False,
        theme_manager: ThemeManager | None = None,
    ) -> None:
        super().__init__(parent)
        self.setProperty("card", True)
        self.content_layout = QVBoxLayout(self)
        inset = TOKENS.spacing.lg if padding is None else padding
        self.content_layout.setContentsMargins(inset, inset, inset, inset)
        self.content_layout.setSpacing(TOKENS.spacing.md)
        self._theme_manager = theme_manager
        if shadow and theme_manager is not None:
            theme_manager.register(self._apply_shadow)

    def _apply_shadow(self, palette: ThemePalette) -> None:
        apply_card_shadow(self, palette)

    def closeEvent(self, event) -> None:  # noqa: N802 - Qt API
        if self._theme_manager is not None:
            self._theme_manager.unregister(self._apply_shadow)
        super().closeEvent(event)


class AppButton(QPushButton):
    """Кнопка с вариантом дизайн-системы и тематической SVG-иконкой."""

    def __init__(
        self,
        text: str,
        parent: QWidget | None = None,
        *,
        variant: str = "secondary",
        icon_name: str | None = None,
        theme_manager: ThemeManager | None = None,
    ) -> None:
        super().__init__(text, parent)
        self.setProperty("variant", variant)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(TOKENS.controls.height)
        self._icon_name = icon_name
        self._theme_manager = theme_manager
        if theme_manager is not None:
            theme_manager.register(self._apply_theme)

    def _apply_theme(self, palette: ThemePalette) -> None:
        if self._icon_name is None:
            return
        variant = str(self.property("variant") or "secondary")
        color = palette.on_accent if variant == "primary" else (
            palette.error if variant == "danger" else palette.text_primary
        )
        self.setIcon(themed_icon(self._icon_name, color, 20))
        self.setIconSize(QSize(20, 20))

    def closeEvent(self, event) -> None:  # noqa: N802 - Qt API
        if self._theme_manager is not None:
            self._theme_manager.unregister(self._apply_theme)
        super().closeEvent(event)


class ToggleSwitch(QAbstractButton):
    """Округлый доступный переключатель для одного логического значения."""

    valueChanged = Signal(bool)

    def __init__(
        self,
        checked: bool = False,
        parent: QWidget | None = None,
        *,
        theme_manager: ThemeManager,
        animations_enabled: Callable[[], bool] | None = None,
        accessible_name: str = "Переключатель",
    ) -> None:
        super().__init__(parent)
        self.setCheckable(True)
        self.setChecked(bool(checked))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAccessibleName(accessible_name)
        self.setAccessibleDescription("ВКЛ — включено, ВЫКЛ — выключено")
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self._theme_manager = theme_manager
        self._palette = theme_manager.palette
        self._animations_enabled = animations_enabled or (lambda: True)
        self._position = 1.0 if checked else 0.0
        self._hovered = False
        self._pressed = False
        self._animation = QPropertyAnimation(self, b"thumbPosition", self)
        self._animation.setDuration(TOKENS.motion.normal_ms)
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.clicked.connect(self._handle_clicked)
        theme_manager.register(self._apply_theme)

    def sizeHint(self) -> QSize:  # noqa: N802 - Qt API
        return QSize(112, TOKENS.controls.toggle_height)

    def minimumSizeHint(self) -> QSize:  # noqa: N802 - Qt API
        return self.sizeHint()

    @property
    def value(self) -> bool:
        return self.isChecked()

    @property
    def state_text(self) -> str:
        return "ВКЛ" if self.isChecked() else "ВЫКЛ"

    @property
    def thumb_fraction(self) -> float:
        return self._position

    @property
    def animation_active(self) -> bool:
        return self._animation.state() == QPropertyAnimation.State.Running

    def set(self, value: bool) -> None:
        """Совместимый явный способ синхронизации внешнего состояния."""
        self.set_value(value, animate=False, emit=False)

    def get_thumb_position(self) -> float:
        return self._position

    def set_thumb_position(self, value: float) -> None:
        self._position = min(1.0, max(0.0, float(value)))
        self.update()

    thumbPosition = Property(float, get_thumb_position, set_thumb_position)

    def set_value(self, checked: bool, *, animate: bool = False, emit: bool = False) -> None:
        """Синхронизирует внешний источник без противоположной записи."""
        normalized = bool(checked)
        changed = self.isChecked() != normalized
        if changed:
            self.blockSignals(not emit)
            QAbstractButton.setChecked(self, normalized)
            self.blockSignals(False)
        self._move_thumb(normalized, animate=animate)
        self.setAccessibleDescription(
            f"{'ВКЛ, включено' if normalized else 'ВЫКЛ, выключено'}"
        )
        if changed and emit:
            self.valueChanged.emit(normalized)

    def _handle_clicked(self, checked: bool) -> None:
        self._move_thumb(checked, animate=True)
        self.setAccessibleDescription(
            f"{'ВКЛ, включено' if checked else 'ВЫКЛ, выключено'}"
        )
        self.valueChanged.emit(bool(checked))

    def _move_thumb(self, checked: bool, *, animate: bool) -> None:
        target = 1.0 if checked else 0.0
        self._animation.stop()
        if not animate or not self._animations_enabled():
            self.set_thumb_position(target)
            return
        self._animation.setStartValue(self._position)
        self._animation.setEndValue(target)
        self._animation.start()

    def _apply_theme(self, palette: ThemePalette) -> None:
        self._palette = palette
        self.update()

    def paintEvent(self, _event) -> None:  # noqa: N802 - Qt API
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        p = self._palette
        status_width = 42.0
        track = QRectF(status_width + 4, 2, 64, 28)
        track_color = p.accent if self.isChecked() else p.secondary_background
        if not self.isEnabled():
            track_color = p.disabled
        elif self._hovered:
            track_color = p.accent_hover if self.isChecked() else p.border
        painter.setPen(QPen(QColor(p.focus if self.hasFocus() else p.border), 2 if self.hasFocus() else 1))
        painter.setBrush(QColor(track_color))
        painter.drawRoundedRect(track, 14, 14)

        thumb_size = 22.0
        start_x = track.left() + 3
        end_x = track.right() - thumb_size - 3
        thumb_x = start_x + (end_x - start_x) * self._position
        thumb = QRectF(thumb_x, track.top() + 3, thumb_size, thumb_size)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(p.on_accent if self.isChecked() else p.card_background))
        painter.drawEllipse(thumb)

        font = QFont("Segoe UI Variable Text", 9)
        font.setWeight(QFont.Weight.DemiBold)
        painter.setFont(font)
        painter.setPen(QColor(p.disabled if not self.isEnabled() else p.text_secondary))
        painter.drawText(QRectF(0, 0, status_width, self.height()), Qt.AlignmentFlag.AlignCenter, self.state_text)

    def enterEvent(self, event) -> None:  # noqa: N802 - Qt API
        self._hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:  # noqa: N802 - Qt API
        self._hovered = False
        self._pressed = False
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802 - Qt API
        self._pressed = True
        self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802 - Qt API
        self._pressed = False
        self.update()
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802 - Qt API
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.click()
            event.accept()
            return
        super().keyPressEvent(event)

    def closeEvent(self, event) -> None:  # noqa: N802 - Qt API
        self._animation.stop()
        self._theme_manager.unregister(self._apply_theme)
        super().closeEvent(event)


class ClickableLabel(QLabel):
    clicked = Signal()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802 - Qt API
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mouseReleaseEvent(event)


class SwitchRow(QWidget):
    """Подпись слева и единый ToggleSwitch справа."""

    valueChanged = Signal(bool)

    def __init__(
        self,
        text: str,
        checked: bool,
        parent: QWidget | None = None,
        *,
        theme_manager: ThemeManager,
        animations_enabled: Callable[[], bool] | None = None,
        description: str = "",
    ) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, TOKENS.spacing.xs, 0, TOKENS.spacing.xs)
        layout.setSpacing(TOKENS.spacing.md)
        text_box = QVBoxLayout()
        text_box.setSpacing(TOKENS.spacing.xxs)
        self.label = ClickableLabel(text, self)
        self.label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.label.setWordWrap(True)
        text_box.addWidget(self.label)
        if description:
            caption = QLabel(description, self)
            caption.setProperty("role", "caption")
            caption.setWordWrap(True)
            text_box.addWidget(caption)
        layout.addLayout(text_box, 1)
        self.switch = ToggleSwitch(
            checked,
            self,
            theme_manager=theme_manager,
            animations_enabled=animations_enabled,
            accessible_name=text,
        )
        layout.addWidget(self.switch, 0, Qt.AlignmentFlag.AlignVCenter)
        self.label.clicked.connect(self.switch.click)
        self.switch.valueChanged.connect(self.valueChanged)

    def isChecked(self) -> bool:  # noqa: N802 - Qt API convention
        return self.switch.isChecked()

    def setChecked(self, value: bool, *, animate: bool = False) -> None:  # noqa: N802
        self.switch.set_value(value, animate=animate, emit=False)

    def setEnabled(self, enabled: bool) -> None:  # noqa: N802
        super().setEnabled(enabled)
        self.label.setEnabled(enabled)
        self.switch.setEnabled(enabled)


class PageHeader(QWidget):
    """Заголовок страницы с пояснением и областью действий."""

    def __init__(
        self,
        title: str,
        subtitle: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(TOKENS.spacing.md)
        text_layout = QVBoxLayout()
        text_layout.setSpacing(TOKENS.spacing.xxs)
        self.title_label = QLabel(title, self)
        self.title_label.setProperty("role", "pageTitle")
        text_layout.addWidget(self.title_label)
        self.subtitle_label = QLabel(subtitle, self)
        self.subtitle_label.setProperty("role", "subtitle")
        self.subtitle_label.setWordWrap(True)
        self.subtitle_label.setVisible(bool(subtitle))
        text_layout.addWidget(self.subtitle_label)
        layout.addLayout(text_layout, 1)
        self.actions = QHBoxLayout()
        self.actions.setSpacing(TOKENS.spacing.xs)
        layout.addLayout(self.actions)


class MetricCard(Card):
    """Карточка одного числового показателя статистики."""

    def __init__(self, title: str, value: str = "0", parent: QWidget | None = None) -> None:
        super().__init__(parent, padding=TOKENS.spacing.md)
        self.title_label = QLabel(title, self)
        self.title_label.setProperty("role", "caption")
        self.title_label.setWordWrap(True)
        self.value_label = QLabel(value, self)
        self.value_label.setProperty("role", "metric")
        self.content_layout.addWidget(self.title_label)
        self.content_layout.addWidget(self.value_label)


class ColorSwatch(QPushButton):
    """Доступный образец цвета, не хранящий случайные цвета интерфейса."""

    def __init__(self, color: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._color = color
        self.setFixedSize(44, 32)
        self.setToolTip(color)
        self._refresh()

    @property
    def color(self) -> str:
        return self._color

    def set_color(self, color: str) -> None:
        self._color = color
        self.setToolTip(color)
        self._refresh()

    def _refresh(self) -> None:
        self.setStyleSheet(
            f"QPushButton {{ background: {self._color}; border: 1px solid rgba(127,127,127,0.65); border-radius: 8px; min-height: 30px; padding: 0; }}"
        )
