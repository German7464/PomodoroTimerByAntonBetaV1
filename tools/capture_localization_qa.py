"""Capture every localized application surface for repeatable visual QA."""

from __future__ import annotations

import argparse
from copy import deepcopy
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QColor, QImage, QPainter
from PySide6.QtWidgets import QMessageBox

from app.i18n import SUPPORTED_LANGUAGES, tr
from app.models import AppSettings, TimerMode
from app.storage import default_settings_data, save_app_settings
from app.ui.qt_app import ensure_application


APP = ensure_application([])


def _capture(widget, path: Path) -> None:
    APP.processEvents()
    image = widget.grab()
    if image.isNull() or not image.save(str(path), "PNG"):
        raise RuntimeError(f"Could not capture {path}")


def _overview(paths: list[Path], destination: Path) -> None:
    columns = 3
    cell_width, cell_height, caption_height = 480, 300, 30
    rows = (len(paths) + columns - 1) // columns
    sheet = QImage(
        columns * cell_width,
        rows * (cell_height + caption_height),
        QImage.Format.Format_ARGB32,
    )
    sheet.fill(QColor("#15171c"))
    painter = QPainter(sheet)
    painter.setPen(QColor("#f5f7fb"))
    for index, path in enumerate(paths):
        image = QImage(str(path))
        row, column = divmod(index, columns)
        x = column * cell_width
        y = row * (cell_height + caption_height)
        target = QRect(x + 4, y + 4, cell_width - 8, cell_height - 8)
        scaled = image.scaled(
            target.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        draw_x = x + (cell_width - scaled.width()) // 2
        draw_y = y + (cell_height - scaled.height()) // 2
        painter.drawImage(draw_x, draw_y, scaled)
        painter.drawText(
            QRect(x + 8, y + cell_height, cell_width - 16, caption_height),
            Qt.AlignmentFlag.AlignCenter,
            path.stem,
        )
    painter.end()
    if not sheet.save(str(destination), "PNG"):
        raise RuntimeError(f"Could not save overview {destination}")


def capture_all(output: Path) -> None:
    from app.ui import main_window as main_module
    from app.ui import settings_window as settings_module

    output.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory() as temporary_directory:
        temporary = Path(temporary_directory)
        settings_path = temporary / "settings.json"
        statistics_path = temporary / "statistics.json"
        profiles_path = temporary / "profiles.json"
        settings_data = default_settings_data("ru-RU")
        settings_data["widget_enabled"] = True
        settings_data["main_window_geometry"] = {
            "x": 30,
            "y": 30,
            "width": 1440,
            "height": 900,
        }
        save_app_settings(settings_path, AppSettings(**settings_data))

        with (
            patch.object(main_module, "SETTINGS_FILE", settings_path),
            patch.object(main_module, "STATISTICS_FILE", statistics_path),
            patch.object(settings_module, "PROFILES_FILE", profiles_path),
            patch.object(main_module.QMessageBox, "warning"),
        ):
            window = main_module.MainWindow()
            window.resize(1440, 900)
            window.show()
            APP.processEvents()
            try:
                for language in SUPPORTED_LANGUAGES:
                    language_dir = output / language.code
                    language_dir.mkdir(parents=True, exist_ok=True)
                    overview_path = language_dir / "overview.png"
                    catalog_path = ROOT / "assets" / "translations" / f"{language.code}.qm"
                    if (
                        overview_path.exists()
                        and overview_path.stat().st_mtime >= catalog_path.stat().st_mtime
                    ):
                        print(f"skipped {language.code}: existing overview", flush=True)
                        continue
                    print(f"capturing {language.code}", flush=True)
                    window.set_interface_language(language.code)
                    APP.processEvents()
                    captured: list[Path] = []

                    for page_index, page_name in (
                        (0, "main_timer"),
                        (1, "statistics"),
                        (3, "help"),
                    ):
                        window.page_stack.setCurrentIndex(page_index)
                        APP.processEvents()
                        path = language_dir / f"{page_name}.png"
                        _capture(window, path)
                        captured.append(path)

                    window.page_stack.setCurrentIndex(2)
                    for section_index, section_key in enumerate(window.settings_view.SECTION_KEYS):
                        window.settings_view.section_list.setCurrentRow(section_index)
                        APP.processEvents()
                        path = language_dir / f"settings_{section_index}_{section_key.rsplit('.', 1)[-1]}.png"
                        _capture(window, path)
                        captured.append(path)

                    window.settings_view._open_theme_editor()
                    editor = window.settings_view.theme_editor
                    if editor is None:
                        raise RuntimeError("Theme editor did not open")
                    APP.processEvents()
                    path = language_dir / "theme_editor.png"
                    _capture(editor, path)
                    captured.append(path)
                    editor.close()
                    APP.processEvents()

                    widget_shell = window.widget_window.window
                    if widget_shell is None:
                        raise RuntimeError("Compact widget did not open")
                    path = language_dir / "compact_widget.png"
                    _capture(widget_shell, path)
                    captured.append(path)

                    window.tray.menu.show()
                    APP.processEvents()
                    path = language_dir / "tray_menu.png"
                    _capture(window.tray.menu, path)
                    captured.append(path)
                    window.tray.menu.hide()

                    window.notifications._show_popup(
                        window.notifications._build_message(TimerMode.WORK, TimerMode.SHORT_BREAK),
                        "action.continue",
                        None,
                        TimerMode.WORK,
                        TimerMode.SHORT_BREAK,
                    )
                    APP.processEvents()
                    notification = window.notifications._active_window
                    if notification is None:
                        raise RuntimeError("Notification did not open")
                    path = language_dir / "notification.png"
                    _capture(notification, path)
                    captured.append(path)
                    window.notifications.dismiss()

                    message_box = QMessageBox(
                        QMessageBox.Icon.Question,
                        tr("stats.reset.title"),
                        tr("stats.reset.confirmation"),
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                        window,
                    )
                    message_box.show()
                    APP.processEvents()
                    path = language_dir / "confirmation_dialog.png"
                    _capture(message_box, path)
                    captured.append(path)
                    message_box.close()

                    original_state = deepcopy(window.timer.state)
                    for mode, page_name in (
                        (TimerMode.WORK, "overwork"),
                        (TimerMode.SHORT_BREAK, "break_overrun"),
                    ):
                        window.timer.state.mode = mode
                        window.timer.state.overrun_mode = mode
                        window.timer.state.waiting_for_continue = True
                        window.timer.state.is_running = False
                        window.timer.state.overrun_seconds = 125
                        window.page_stack.setCurrentIndex(0)
                        window._refresh_labels()
                        APP.processEvents()
                        path = language_dir / f"{page_name}.png"
                        _capture(window, path)
                        captured.append(path)
                    window.timer.state = original_state
                    window._refresh_labels()

                    _overview(captured, overview_path)
                    print(f"captured {language.code}: {len(captured)} surfaces", flush=True)
            finally:
                window._shutdown(quit_application=False)
                window.deleteLater()
                APP.processEvents()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "build" / "localization-qa",
    )
    arguments = parser.parse_args()
    capture_all(arguments.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
