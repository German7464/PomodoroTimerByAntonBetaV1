"""Переиспользуемые Qt-компоненты дизайн-системы приложения."""

from __future__ import annotations

from collections.abc import Callable
import ctypes
import os

from PySide6.QtCore import (
    Property,
    QEasingCurve,
    QPointF,
    QPropertyAnimation,
    QRect,
    QRectF,
    QSize,
    Qt,
    Signal,
)
from PySide6.QtGui import (
    QColor,
    QFocusEvent,
    QFont,
    QFontMetrics,
    QKeyEvent,
    QMouseEvent,
    QPaintEvent,
    QPainter,
    QPen,
)
from PySide6.QtWidgets import (
    QAbstractButton,
    QApplication,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLayout,
    QLayoutItem,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStyle,
    QStyleOptionButton,
    QStylePainter,
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


def interface_animations_enabled() -> bool:
    """Учитывает настройку приложения и системное уменьшение движения Windows."""
    application = QApplication.instance()
    if application is not None and application.property("animationsEnabled") is False:
        return False
    if os.name != "nt":
        return True
    try:
        enabled = ctypes.c_int(1)
        # SPI_GETCLIENTAREAANIMATION — документированная настройка анимаций UI Windows.
        result = ctypes.windll.user32.SystemParametersInfoW(
            0x1042,
            0,
            ctypes.byref(enabled),
            0,
        )
    except (AttributeError, OSError):
        return True
    return bool(enabled.value) if result else True


class FlowLayout(QLayout):
    """Компактная flow-компоновка: переносит целые элементы без обрезания текста."""

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        horizontal_spacing: int | None = None,
        vertical_spacing: int | None = None,
    ) -> None:
        super().__init__(parent)
        self._items: list[QLayoutItem] = []
        self._horizontal_spacing = TOKENS.spacing.sm if horizontal_spacing is None else horizontal_spacing
        self._vertical_spacing = TOKENS.spacing.sm if vertical_spacing is None else vertical_spacing
        self.setContentsMargins(0, 0, 0, 0)

    def addItem(self, item: QLayoutItem) -> None:  # noqa: N802 - Qt API
        self._items.append(item)

    def count(self) -> int:
        return len(self._items)

    def itemAt(self, index: int) -> QLayoutItem | None:  # noqa: N802 - Qt API
        return self._items[index] if 0 <= index < len(self._items) else None

    def takeAt(self, index: int) -> QLayoutItem | None:  # noqa: N802 - Qt API
        return self._items.pop(index) if 0 <= index < len(self._items) else None

    def expandingDirections(self) -> Qt.Orientations:  # noqa: N802 - Qt API
        return Qt.Orientations()

    def hasHeightForWidth(self) -> bool:  # noqa: N802 - Qt API
        return True

    def heightForWidth(self, width: int) -> int:  # noqa: N802 - Qt API
        return self._do_layout(QRect(0, 0, max(0, width), 0), test_only=True)

    def setGeometry(self, rect: QRect) -> None:  # noqa: N802 - Qt API
        super().setGeometry(rect)
        self._do_layout(rect, test_only=False)

    def sizeHint(self) -> QSize:  # noqa: N802 - Qt API
        return self.minimumSize()

    def minimumSize(self) -> QSize:  # noqa: N802 - Qt API
        size = QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        margins = self.contentsMargins()
        return size + QSize(margins.left() + margins.right(), margins.top() + margins.bottom())

    def _do_layout(self, rect: QRect, *, test_only: bool) -> int:
        margins = self.contentsMargins()
        effective = rect.adjusted(margins.left(), margins.top(), -margins.right(), -margins.bottom())
        x = effective.x()
        y = effective.y()
        line_height = 0
        for item in self._items:
            hint = item.sizeHint().expandedTo(item.minimumSize())
            next_x = x + hint.width() + self._horizontal_spacing
            if line_height and next_x - self._horizontal_spacing > effective.right() + 1:
                x = effective.x()
                y += line_height + self._vertical_spacing
                next_x = x + hint.width() + self._horizontal_spacing
                line_height = 0
            if not test_only:
                item.setGeometry(QRect(QPointF(x, y).toPoint(), hint))
            x = next_x
            line_height = max(line_height, hint.height())
        return y + line_height - rect.y() + margins.bottom()


class ThemedScrollArea(QScrollArea):
    """Scroll area с явно тематизированными рамкой, viewport и содержимым."""

    def __init__(self, parent: QWidget | None, theme_manager: ThemeManager) -> None:
        super().__init__(parent)
        self._theme_manager = theme_manager
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setProperty("pageSurface", True)
        self.viewport().setObjectName("qt_scrollarea_viewport")
        self.viewport().setAutoFillBackground(True)
        theme_manager.register(self._apply_theme)

    def setWidget(self, widget: QWidget) -> None:  # noqa: N802 - Qt API
        widget.setProperty("pageSurface", True)
        widget.setAutoFillBackground(True)
        super().setWidget(widget)
        self._apply_theme(self._theme_manager.palette)

    def _apply_theme(self, palette: ThemePalette) -> None:
        for widget in (self, self.viewport(), self.widget()):
            if widget is None:
                continue
            qt_palette = widget.palette()
            qt_palette.setColor(qt_palette.ColorRole.Window, QColor(palette.background))
            qt_palette.setColor(qt_palette.ColorRole.Base, QColor(palette.background))
            widget.setPalette(qt_palette)
            widget.update()

    def closeEvent(self, event) -> None:  # noqa: N802 - Qt API
        self._theme_manager.unregister(self._apply_theme)
        super().closeEvent(event)


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
        reserved_texts: tuple[str, ...] = (),
        animations_enabled: Callable[[], bool] | None = None,
    ) -> None:
        super().__init__(text, parent)
        self.setProperty("variant", variant)
        self.setProperty("keyboardFocus", False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMinimumHeight(TOKENS.controls.height)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self._icon_name = icon_name
        self._theme_manager = theme_manager
        self._reserved_texts = tuple(str(value) for value in reserved_texts)
        self._animations_enabled = animations_enabled
        self._press_progress = 0.0
        self._press_animation = QPropertyAnimation(self, b"pressProgress", self)
        self._press_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.pressed.connect(self._animate_press_in)
        self.released.connect(self._animate_press_out)
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

    def sizeHint(self) -> QSize:  # noqa: N802 - Qt API
        base = super().sizeHint()
        width = max(
            self.width_for_text(value)
            for value in (self.text(), *self._reserved_texts)
        )
        return QSize(max(base.width(), width), max(base.height(), TOKENS.controls.height))

    def minimumSizeHint(self) -> QSize:  # noqa: N802 - Qt API
        return self.sizeHint()

    def width_for_text(self, text: str) -> int:
        """Ширина подписи с реальными font metrics, иконкой и безопасными полями."""
        metrics = QFontMetrics(self.font())
        current_text_width = metrics.horizontalAdvance(self.text())
        # Qt/QSS уже учитывает рамку, внутренние поля и иконку в штатном sizeHint.
        # Выделяем эту «обвязку», чтобы другая (в том числе локализованная) подпись
        # получила те же поля при любом DPI и стиле платформы.
        chrome_width = max(
            TOKENS.spacing.md * 2,
            super().sizeHint().width() - current_text_width,
        )
        return metrics.horizontalAdvance(str(text)) + chrome_width

    def activate_from_keyboard(self) -> bool:
        """Визуально нажимает кнопку и запускает тот же clicked-handler, что мышь."""
        if not self.isEnabled() or not self.isVisible():
            return False
        self._set_keyboard_focus(True)
        self.setFocus(Qt.FocusReason.ShortcutFocusReason)
        self.animateClick()
        return True

    def _motion_enabled(self) -> bool:
        return interface_animations_enabled() and (
            self._animations_enabled is None or bool(self._animations_enabled())
        )

    def _animate_press_in(self) -> None:
        self._animate_press_to(1.0, max(60, TOKENS.motion.fast_ms // 2))

    def _animate_press_out(self) -> None:
        self._animate_press_to(0.0, TOKENS.motion.fast_ms)

    def _animate_press_to(self, target: float, duration_ms: int) -> None:
        self._press_animation.stop()
        if not self._motion_enabled():
            self._set_press_progress(0.0)
            return
        self._press_animation.setDuration(max(1, int(duration_ms)))
        self._press_animation.setStartValue(self._press_progress)
        self._press_animation.setEndValue(max(0.0, min(1.0, float(target))))
        self._press_animation.start()

    def _get_press_progress(self) -> float:
        return self._press_progress

    def _set_press_progress(self, value: float) -> None:
        normalized = max(0.0, min(1.0, float(value)))
        if abs(normalized - self._press_progress) < 0.001:
            return
        self._press_progress = normalized
        self.update()

    pressProgress = Property(float, _get_press_progress, _set_press_progress)

    @property
    def press_progress(self) -> float:
        """Диагностическое состояние для Qt-тестов без привязки к таймеру."""
        return self._press_progress

    def _set_keyboard_focus(self, visible: bool) -> None:
        normalized = bool(visible)
        if bool(self.property("keyboardFocus")) == normalized:
            return
        self.setProperty("keyboardFocus", normalized)
        # Рамка рисуется поверх кнопки: QSS-repolish здесь сбрасывал локальный
        # размер шрифта виджета и менял компоновку в момент нажатия Space.
        self.update()

    def focusInEvent(self, event: QFocusEvent) -> None:  # noqa: N802 - Qt API
        keyboard_reasons = {
            Qt.FocusReason.TabFocusReason,
            Qt.FocusReason.BacktabFocusReason,
            Qt.FocusReason.ShortcutFocusReason,
        }
        self._set_keyboard_focus(event.reason() in keyboard_reasons)
        super().focusInEvent(event)

    def focusOutEvent(self, event: QFocusEvent) -> None:  # noqa: N802 - Qt API
        self._set_keyboard_focus(False)
        super().focusOutEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802 - Qt API
        self._set_keyboard_focus(False)
        super().mousePressEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802 - Qt API
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter) and not event.isAutoRepeat():
            if self.activate_from_keyboard():
                event.accept()
            return
        if event.key() == Qt.Key.Key_Space:
            self._set_keyboard_focus(True)
        super().keyPressEvent(event)

    def paintEvent(self, _event: QPaintEvent) -> None:  # noqa: N802 - Qt API
        option = QStyleOptionButton()
        self.initStyleOption(option)
        if self._press_progress > 0.001:
            option.state |= QStyle.StateFlag.State_Sunken
        painter = QStylePainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.save()
        scale = 1.0 - (0.025 * self._press_progress)
        center = self.rect().center()
        painter.translate(center)
        painter.scale(scale, scale)
        painter.translate(-center)
        painter.setOpacity(1.0 - (0.06 * self._press_progress))
        painter.drawControl(QStyle.ControlElement.CE_PushButton, option)
        painter.restore()
        if bool(self.property("keyboardFocus")) and self.isEnabled():
            painter.setOpacity(1.0)
            focus_color = QColor(
                self._theme_manager.palette.focus
                if self._theme_manager is not None
                else self.palette().highlight().color()
            )
            painter.setPen(QPen(focus_color, TOKENS.focus_width + 1))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            inset = (TOKENS.focus_width + 1) / 2 + 1
            focus_rect = QRectF(self.rect()).adjusted(inset, inset, -inset, -inset)
            radius = max(2, TOKENS.radii.control - 1)
            painter.drawRoundedRect(focus_rect, radius, radius)
            contrast_color = QColor(
                self._theme_manager.palette.on_accent
                if self._theme_manager is not None and self.property("variant") == "primary"
                else (
                    self._theme_manager.palette.text_primary
                    if self._theme_manager is not None
                    else self.palette().windowText().color()
                )
            )
            inner = focus_rect.adjusted(2.5, 2.5, -2.5, -2.5)
            painter.setPen(QPen(contrast_color, 1))
            painter.drawRoundedRect(inner, max(2, radius - 2), max(2, radius - 2))

    def closeEvent(self, event) -> None:  # noqa: N802 - Qt API
        self._press_animation.stop()
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
        self._grid = QGridLayout(self)
        self._grid.setContentsMargins(0, 0, 0, 0)
        self._grid.setHorizontalSpacing(TOKENS.spacing.md)
        self._grid.setVerticalSpacing(TOKENS.spacing.sm)
        self._text_container = QWidget(self)
        text_layout = QVBoxLayout(self._text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(TOKENS.spacing.xxs)
        self.title_label = QLabel(title, self._text_container)
        self.title_label.setProperty("role", "pageTitle")
        text_layout.addWidget(self.title_label)
        self.subtitle_label = QLabel(subtitle, self._text_container)
        self.subtitle_label.setProperty("role", "subtitle")
        self.subtitle_label.setWordWrap(True)
        self.subtitle_label.setVisible(bool(subtitle))
        text_layout.addWidget(self.subtitle_label)
        self._grid.addWidget(self._text_container, 0, 0)
        self._grid.setColumnStretch(0, 1)
        self.actions_container = QWidget(self)
        self.actions = QHBoxLayout(self.actions_container)
        self.actions.setContentsMargins(0, 0, 0, 0)
        self.actions.setSpacing(TOKENS.spacing.xs)
        self._grid.addWidget(self.actions_container, 0, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self._compact = False

    def resizeEvent(self, event) -> None:  # noqa: N802 - Qt API
        compact = event.size().width() < 720
        if compact != self._compact:
            self._compact = compact
            self._grid.removeWidget(self.actions_container)
            if compact:
                self._grid.addWidget(self.actions_container, 1, 0, 1, 2, Qt.AlignmentFlag.AlignLeft)
            else:
                self._grid.addWidget(self.actions_container, 0, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        super().resizeEvent(event)


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


class ColorSwatch(QAbstractButton):
    """Доступный образец цвета, не хранящий случайные цвета интерфейса."""

    def __init__(self, color: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._color = color
        self.setFixedSize(44, 32)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setToolTip(color)

    @property
    def color(self) -> str:
        return self._color

    def set_color(self, color: str) -> None:
        self._color = color
        self.setToolTip(color)
        self.update()

    def paintEvent(self, _event) -> None:  # noqa: N802 - Qt API
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        border = self.palette().color(self.palette().ColorRole.Highlight if self.hasFocus() else self.palette().ColorRole.Mid)
        painter.setPen(QPen(border, 2 if self.hasFocus() else 1))
        painter.setBrush(QColor(self._color))
        painter.drawRoundedRect(QRectF(1, 1, self.width() - 2, self.height() - 2), 8, 8)
