"""Константы приложения и пути к локальным файлам данных."""

from pathlib import Path
import shutil
import sys


APP_NAME = "Pomodoro Timer"
DATA_FILE_NAMES = ("settings.json", "profiles.json", "statistics.json")

PROJECT_DIR = Path(__file__).resolve().parent.parent
USER_DATA_DIR = Path.home() / ".pomodoro_timer_by_anton"


def is_frozen_app() -> bool:
    """Возвращает True, если программа запущена как собранный PyInstaller exe."""
    return bool(getattr(sys, "frozen", False))


def get_app_base_dir() -> Path:
    """Возвращает папку приложения: папку exe для сборки или корень проекта для Python."""
    if is_frozen_app():
        return Path(sys.executable).resolve().parent
    return PROJECT_DIR


BASE_DIR = get_app_base_dir()


def get_data_dir() -> tuple[Path, str]:
    """Выбирает папку данных и возвращает предупреждение, если пришлось включить fallback."""
    portable_data_dir = get_app_base_dir() / "data"
    warning = ""

    if _ensure_writable_directory(portable_data_dir):
        _migrate_legacy_user_data(portable_data_dir)
        return portable_data_dir, warning

    # Если запись рядом с exe запрещена, не падаем: используем старую папку пользователя.
    warning = (
        "Не удалось записать данные рядом с программой. "
        "Настройки временно будут храниться в папке пользователя. "
        "Для portable-режима перенесите программу в папку, доступную для записи."
    )
    if _ensure_writable_directory(USER_DATA_DIR):
        return USER_DATA_DIR, warning

    raise RuntimeError("Не удалось создать папку для настроек приложения.")


def _ensure_writable_directory(path: Path) -> bool:
    """Создает папку и проверяет, можно ли записать в нее небольшой временный файл."""
    try:
        path.mkdir(parents=True, exist_ok=True)
        test_file = path / ".write_test"
        test_file.write_text("ok", encoding="utf-8")
        test_file.unlink(missing_ok=True)
        return True
    except OSError:
        return False


def _migrate_legacy_user_data(target_dir: Path) -> None:
    """Копирует старые пользовательские JSON в portable-папку, если она еще пустая.

    Старые файлы не удаляются: это безопаснее, если пользователь захочет вернуться
    к предыдущей версии программы или проверить данные вручную.
    """
    if target_dir.resolve() == USER_DATA_DIR.resolve():
        return

    has_portable_json = any((target_dir / name).exists() for name in DATA_FILE_NAMES)
    if has_portable_json:
        return

    for file_name in DATA_FILE_NAMES:
        old_file = USER_DATA_DIR / file_name
        new_file = target_dir / file_name
        if old_file.exists() and not new_file.exists():
            shutil.copy2(old_file, new_file)


DATA_DIR, DATA_DIR_WARNING = get_data_dir()

SETTINGS_FILE = DATA_DIR / "settings.json"
PROFILES_FILE = DATA_DIR / "profiles.json"
STATISTICS_FILE = DATA_DIR / "statistics.json"

DEFAULT_WORK_MINUTES = 25
DEFAULT_SHORT_BREAK_MINUTES = 5
DEFAULT_LONG_BREAK_MINUTES = 15
DEFAULT_CYCLES_BEFORE_LONG_BREAK = 4
DEFAULT_PROFILE_NAME = "Стандартный"

DEFAULT_USE_LONG_BREAK = True
DEFAULT_AUTO_START_NEXT_PERIOD = True
DEFAULT_TIME_DISPLAY_FORMAT = "HH:MM:SS"
DEFAULT_MINIMIZE_TO_TRAY_ON_START = False
