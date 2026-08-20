"""Адаптивность подписей кнопок и единая обратная связь мыши/клавиатуры."""

from __future__ import annotations

import unittest

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics
from PySide6.QtTest import QTest

from app.theme import (
    APPEARANCE_DARK,
    APPEARANCE_MODES,
    THEME_NAMES,
    ThemeManager,
    contrast_ratio,
)
from app.ui.components import AppButton
from app.ui.design_system import TOKENS
from app.ui.widget_window import ExpandedWidgetView, MinimalWidgetView
from app.widget_settings import (
    WIDGET_SIZE_CUSTOM,
    WIDGET_TYPE_EXPANDED,
    WIDGET_TYPE_MINIMAL,
    default_widget_layouts,
)
from tests.qt_helpers import APP, isolated_main
from tests.test_timer_engine import finish_current_period, make_settings


class AppButtonFeedbackTests(unittest.TestCase):
    def tearDown(self) -> None:
        for widget in tuple(APP.topLevelWidgets()):
            if isinstance(widget, AppButton):
                widget.close()
                widget.deleteLater()
        APP.processEvents()

    def test_reserved_label_width_uses_font_metrics_and_padding(self) -> None:
        button = AppButton(
            "Старт",
            reserved_texts=("Старт", "Пауза", "Продолжить"),
        )
        button.show()
        APP.processEvents()
        start_width = button.sizeHint().width()
        required = QFontMetrics(button.font()).horizontalAdvance("Продолжить") + TOKENS.spacing.md * 2

        self.assertGreaterEqual(start_width, required)
        button.setText("Продолжить")
        self.assertEqual(button.sizeHint().width(), start_width)

    def test_mouse_enter_and_space_emit_the_same_clicked_signal_once(self) -> None:
        button = AppButton("Действие")
        activations: list[str] = []
        button.clicked.connect(lambda: activations.append("clicked"))
        button.show()
        button.setFocus()
        APP.processEvents()

        QTest.mouseClick(button, Qt.MouseButton.LeftButton)
        self.assertEqual(len(activations), 1)
        QTest.keyClick(button, Qt.Key.Key_Return)
        QTest.qWait(130)
        self.assertEqual(len(activations), 2)
        QTest.keyClick(button, Qt.Key.Key_Space)
        self.assertEqual(len(activations), 3)

    def test_keyboard_focus_is_visible_but_mouse_focus_is_not_persistent(self) -> None:
        button = AppButton("Действие")
        button.show()
        button.setFocus()
        QTest.keyClick(button, Qt.Key.Key_Space)
        self.assertTrue(button.property("keyboardFocus"))

        QTest.mouseClick(button, Qt.MouseButton.LeftButton)
        self.assertFalse(button.property("keyboardFocus"))

    def test_disabled_button_cannot_be_activated_from_keyboard(self) -> None:
        button = AppButton("Недоступно")
        activations: list[bool] = []
        button.clicked.connect(lambda: activations.append(True))
        button.show()
        button.setEnabled(False)

        self.assertFalse(button.activate_from_keyboard())
        QTest.keyClick(button, Qt.Key.Key_Return)
        self.assertEqual(activations, [])

    def test_reduced_motion_keeps_click_but_skips_scale_animation(self) -> None:
        button = AppButton("Без движения", animations_enabled=lambda: False)
        activations: list[bool] = []
        button.clicked.connect(lambda: activations.append(True))
        button.show()
        APP.processEvents()

        QTest.mouseClick(button, Qt.MouseButton.LeftButton)

        self.assertEqual(activations, [True])
        self.assertEqual(button.press_progress, 0.0)

    def test_focus_colors_are_readable_in_every_theme_and_mode(self) -> None:
        manager = ThemeManager()
        button = AppButton("Действие", variant="primary", theme_manager=manager)
        for theme_name in THEME_NAMES:
            for appearance_mode in APPEARANCE_MODES:
                with self.subTest(theme=theme_name, mode=appearance_mode):
                    palette = manager.apply(theme_name, appearance_mode)
                    self.assertGreaterEqual(
                        contrast_ratio(palette.focus, palette.card_background),
                        4.5,
                    )
                    self.assertGreaterEqual(
                        contrast_ratio(palette.on_accent, palette.accent),
                        4.5,
                    )
        button.close()


class ExpandedWidgetActionLayoutTests(unittest.TestCase):
    @staticmethod
    def _expanded_settings(width: int = 330, height: int = 245):
        settings = make_settings()
        settings.widget_enabled = True
        settings.widget_type = WIDGET_TYPE_EXPANDED
        settings.widget_size = WIDGET_SIZE_CUSTOM
        settings.widget_layouts = default_widget_layouts()
        settings.widget_layouts[WIDGET_TYPE_EXPANDED].update(
            size=WIDGET_SIZE_CUSTOM,
            width=width,
            height=height,
        )
        return settings

    def test_all_actions_fit_at_minimum_width_without_clipped_text(self) -> None:
        with isolated_main(self._expanded_settings()) as (window, _settings, _statistics):
            view = window.widget_window.view
            self.assertIsInstance(view, ExpandedWidgetView)
            APP.processEvents()

            buttons = (view.primary_button, view.skip_button, view.reset_button, view.open_button)
            for button in buttons:
                with self.subTest(button=button.accessibleName() or button.text()):
                    self.assertGreaterEqual(button.width(), button.minimumSizeHint().width())
                    self.assertTrue(view.action_panel.rect().contains(button.geometry()))
            self.assertEqual(view.primary_button.text(), "Старт")
            self.assertEqual(view.open_button.text(), "")
            self.assertEqual(view.open_button.accessibleName(), "Открыть главное окно")

    def test_overrun_keeps_window_geometry_and_full_continue_label(self) -> None:
        with isolated_main(self._expanded_settings()) as (window, _settings, _statistics):
            view = window.widget_window.view
            APP.processEvents()
            shell_size = window.widget_window.window.size()
            normal_width = view.primary_button.width()

            finish_current_period(window.timer)
            window._refresh_labels()
            APP.processEvents()

            self.assertEqual(view.primary_button.text(), "Продолжить")
            self.assertEqual(window.widget_window.window.size(), shell_size)
            self.assertGreaterEqual(view.primary_button.width(), normal_width)
            self.assertGreaterEqual(
                view.primary_button.width(),
                view.primary_button.width_for_text("Продолжить"),
            )
            self.assertTrue(view.action_panel.rect().contains(view.primary_button.geometry()))

    def test_theme_switch_does_not_resize_widget(self) -> None:
        with isolated_main(self._expanded_settings(400, 245)) as (window, _settings, _statistics):
            before = window.widget_window.window.size()

            window.theme_manager.apply("Aurora", APPEARANCE_DARK, window.settings.custom_theme)
            APP.processEvents()

            self.assertEqual(window.widget_window.window.size(), before)

    def test_hidden_action_is_removed_from_keyboard_focus(self) -> None:
        settings = make_settings()
        settings.widget_enabled = True
        settings.widget_type = WIDGET_TYPE_MINIMAL
        with isolated_main(settings) as (window, _settings, _statistics):
            view = window.widget_window.view
            self.assertIsInstance(view, MinimalWidgetView)
            APP.processEvents()

            self.assertFalse(view.primary_button.isVisible())
            self.assertEqual(view.primary_button.focusPolicy(), Qt.FocusPolicy.NoFocus)
            self.assertFalse(view.primary_button.activate_from_keyboard())


if __name__ == "__main__":
    unittest.main()
