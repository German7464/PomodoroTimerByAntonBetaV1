"""Validate Qt TS catalogs and compile them to deployable QM files."""

from __future__ import annotations

import argparse
import ast
from collections import defaultdict
from pathlib import Path
import re
import shutil
from string import Formatter
import subprocess
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SOURCE_DIR = ROOT / "app"
TRANSLATION_DIR = ROOT / "assets" / "translations"
LANGUAGE_CODES = (
    "ru-RU", "en-US", "es-ES", "de-DE", "fr-FR", "pt-BR",
    "zh-CN", "hi-IN", "ar-SA", "ja-JP", "ko-KR",
)
PLURAL_FORM_COUNTS = {
    "ru-RU": 3, "en-US": 2, "es-ES": 2, "de-DE": 2, "fr-FR": 2,
    "pt-BR": 2, "zh-CN": 1, "hi-IN": 2, "ar-SA": 6, "ja-JP": 1, "ko-KR": 1,
}
APP_CONTEXT = "PomodoroTimer"
KEY_PATTERN = re.compile(r"^[a-z][a-z0-9_]*(?:\.[a-z0-9_]+)+$")
KEY_PREFIXES = {
    "action", "dialog", "error", "help", "main", "nav", "notification",
    "overrun", "settings", "startup", "stats", "theme", "theme_editor",
    "timer", "toggle", "tray", "widget",
}
RUSSIAN_PATTERN = re.compile(r"[А-Яа-яЁё]")

# Migration values, the native language label, and compatibility-only public
# strings retained for older integrations are justified runtime exceptions.
RUSSIAN_RUNTIME_ALLOWLIST = {
    "Русский",
    "Минималистичный", "Компактный", "Расширенный", "Микро", "Строка", "Кольцо", "Табло",
    "Маленький", "Средний", "Большой", "Пользовательский",
    "Без анимации", "Пульсация", "Увеличение цифр", "Сигнальные маячки", "Акцентная рамка", "Волна-индикатор",
    "Без дополнительного эффекта", "Изменение цвета", "Цвет и пульсация",
    "Только цифры таймера", "Карточка таймера", "Цифры и карточка",
    "Медленно", "Обычно", "Быстро", "Слабо", "Средне", "Сильно",
    "Пользовательская", "пользовательская", "Тёмная", "Темная", "Светлая", "тёмная", "темная", "светлая",
    "Стандартный",
    "Рабочий период завершен. Время отдохнуть.",
    "Короткий отдых завершен. Пора вернуться к работе.",
    "Длинный отдых завершен. Пора начать новый рабочий период.",
    "Pomodoro Timer уже запускается или уже запущен. Дождитесь открытия окна либо используйте уже открытое приложение.",
    "Работа", "Короткий отдых", "Длинный отдых", "Переработка",
    "Короткий отдых сверх нормы", "Длинный отдых сверх нормы",
}


def placeholders(text: str) -> set[str]:
    return {
        field_name.split(".", 1)[0].split("[", 1)[0]
        for _literal, field_name, _format_spec, _conversion in Formatter().parse(text)
        if field_name
    }


def parse_catalog(path: Path) -> dict[str, dict[str, tuple[str, ...]]]:
    root = ET.parse(path).getroot()
    contexts: dict[str, dict[str, tuple[str, ...]]] = {}
    for context in root.findall("context"):
        name = context.findtext("name") or ""
        messages: dict[str, tuple[str, ...]] = {}
        for message in context.findall("message"):
            source = message.findtext("source") or ""
            if source in messages:
                raise ValueError(f"{path.name}: duplicate key {name}/{source}")
            translation = message.find("translation")
            if translation is None:
                forms = ("",)
            elif message.get("numerus") == "yes":
                forms = tuple("".join(item.itertext()).strip() for item in translation.findall("numerusform"))
            else:
                forms = ("".join(translation.itertext()).strip(),)
            messages[source] = forms
        contexts[name] = messages
    return contexts


def code_translation_keys() -> set[str]:
    keys: set[str] = set()
    for path in SOURCE_DIR.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if (
                    KEY_PATTERN.fullmatch(node.value)
                    and node.value.split(".", 1)[0] in KEY_PREFIXES
                    and not node.value.endswith((".json", ".svg", ".ico", ".qm", ".ts"))
                ):
                    keys.add(node.value)
    from app.overrun_effects import EFFECT_LABEL_KEYS, INTENSITY_LABEL_KEYS, SCOPE_LABEL_KEYS, SPEED_LABEL_KEYS
    from app.theme import APPEARANCE_LABEL_KEYS, THEME_LABEL_KEYS
    from app.widget_settings import WIDGET_SIZE_LABEL_KEYS, WIDGET_TYPE_DESCRIPTIONS, WIDGET_TYPE_LABEL_KEYS

    for mapping in (
        EFFECT_LABEL_KEYS, INTENSITY_LABEL_KEYS, SCOPE_LABEL_KEYS, SPEED_LABEL_KEYS,
        APPEARANCE_LABEL_KEYS, THEME_LABEL_KEYS, WIDGET_SIZE_LABEL_KEYS,
        WIDGET_TYPE_DESCRIPTIONS, WIDGET_TYPE_LABEL_KEYS,
    ):
        keys.update(mapping.values())
    return keys


def runtime_russian_strings() -> list[str]:
    offenders: list[str] = []
    for path in SOURCE_DIR.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        docstring_nodes = set()
        for owner in (tree, *(node for node in ast.walk(tree) if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)))):
            if owner.body and isinstance(owner.body[0], ast.Expr):
                docstring_nodes.add(id(owner.body[0].value))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
                continue
            if id(node) in docstring_nodes or not RUSSIAN_PATTERN.search(node.value):
                continue
            if node.value not in RUSSIAN_RUNTIME_ALLOWLIST:
                offenders.append(f"{path.relative_to(ROOT)}:{node.lineno}: {node.value!r}")
    return offenders


def validate() -> None:
    catalogs = {}
    errors: list[str] = []
    for code in LANGUAGE_CODES:
        path = TRANSLATION_DIR / f"{code}.ts"
        if not path.exists():
            errors.append(f"missing catalog: {path}")
            continue
        try:
            catalogs[code] = parse_catalog(path)
        except (ET.ParseError, ValueError) as error:
            errors.append(str(error))
    if errors:
        raise SystemExit("\n".join(errors))

    reference = catalogs["ru-RU"]
    reference_shape = {context: set(messages) for context, messages in reference.items()}
    for code, contexts in catalogs.items():
        shape = {context: set(messages) for context, messages in contexts.items()}
        if shape != reference_shape:
            errors.append(f"{code}: context/key set differs from ru-RU")
        for context, messages in contexts.items():
            for key, forms in messages.items():
                if context == APP_CONTEXT and not KEY_PATTERN.fullmatch(key):
                    errors.append(f"{code}: source is not a stable key: {key!r}")
                if not forms or any(not form for form in forms):
                    errors.append(f"{code}: empty translation: {context}/{key}")
                    continue
                reference_forms = reference.get(context, {}).get(key, ())
                is_plural = len(reference_forms) > 1
                if is_plural and len(forms) != PLURAL_FORM_COUNTS[code]:
                    errors.append(f"{code}: wrong plural form count: {context}/{key}")
                expected = set().union(*(placeholders(form) for form in reference_forms))
                for form in forms:
                    if placeholders(form) != expected:
                        errors.append(f"{code}: placeholder mismatch: {context}/{key}")
                if code != "ru-RU" and any(RUSSIAN_PATTERN.search(form) for form in forms):
                    errors.append(f"{code}: Russian text remains: {context}/{key}")

    used = code_translation_keys()
    catalog_keys = set(reference.get(APP_CONTEXT, {}))
    missing = sorted(used - catalog_keys)
    unused = sorted(catalog_keys - used)
    if missing:
        errors.append("keys used by code but missing from catalog: " + ", ".join(missing))
    if unused:
        errors.append("unused catalog keys: " + ", ".join(unused))
    russian_offenders = runtime_russian_strings()
    if russian_offenders:
        errors.append("unjustified Russian runtime strings:\n" + "\n".join(russian_offenders))
    if errors:
        raise SystemExit("\n".join(errors))


def lrelease_command() -> str:
    executable = shutil.which("pyside6-lrelease")
    if executable:
        return executable
    candidate = Path(sys.executable).resolve().parent / "pyside6-lrelease.exe"
    if candidate.exists():
        return str(candidate)
    raise SystemExit("pyside6-lrelease was not found")


def compile_catalogs() -> None:
    executable = lrelease_command()
    for code in LANGUAGE_CODES:
        source = TRANSLATION_DIR / f"{code}.ts"
        target = TRANSLATION_DIR / f"{code}.qm"
        subprocess.run([executable, str(source), "-qm", str(target)], check=True)
    from PySide6.QtCore import QTranslator

    for code in LANGUAGE_CODES:
        path = TRANSLATION_DIR / f"{code}.qm"
        if not QTranslator().load(str(path)):
            raise SystemExit(f"compiled catalog does not load: {path}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    arguments = parser.parse_args()
    validate()
    if not arguments.check_only:
        compile_catalogs()
    print(f"translations: {len(LANGUAGE_CODES)} catalogs valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
