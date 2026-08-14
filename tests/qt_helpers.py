"""Изолированные помощники Qt-тестов без доступа к пользовательским JSON."""

from __future__ import annotations

from contextlib import contextmanager
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from app.storage import save_app_settings
from app.ui.qt_app import ensure_application
from tests.test_timer_engine import make_settings


APP = ensure_application([])


@contextmanager
def isolated_main(settings=None):
    """Создаёт настоящий MainWindow, перенаправив все хранилища во временную папку."""
    from app.ui import main_window as main_module
    from app.ui import settings_window as settings_module

    with TemporaryDirectory() as directory:
        root = Path(directory)
        settings_path = root / "settings.json"
        statistics_path = root / "statistics.json"
        profiles_path = root / "profiles.json"
        save_app_settings(settings_path, settings or make_settings())
        with (
            patch.object(main_module, "SETTINGS_FILE", settings_path),
            patch.object(main_module, "STATISTICS_FILE", statistics_path),
            patch.object(settings_module, "PROFILES_FILE", profiles_path),
            patch.object(main_module.QMessageBox, "warning"),
        ):
            window = main_module.MainWindow()
            APP.processEvents()
            try:
                yield window, settings_path, statistics_path
            finally:
                if not window._exiting:
                    window._shutdown(quit_application=False)
                window.deleteLater()
                APP.processEvents()
