"""Tiny TS reader for native startup messages shown before importing Qt."""

from __future__ import annotations

import ctypes
from functools import lru_cache
import json
import locale
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


DEFAULT_LANGUAGE = "ru-RU"
SUPPORTED_LANGUAGE_CODES = (
    "ru-RU", "en-US", "es-ES", "de-DE", "fr-FR", "pt-BR",
    "zh-CN", "hi-IN", "ar-SA", "ja-JP", "ko-KR",
)


def _base_dir() -> Path:
    if bool(getattr(sys, "frozen", False)):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[1]


def _translations_dir() -> Path:
    resource_root = Path(getattr(sys, "_MEIPASS", _base_dir()))
    return resource_root / "assets" / "translations"


def _settings_candidates() -> tuple[Path, ...]:
    return (
        _base_dir() / "data" / "settings.json",
        Path.home() / ".pomodoro_timer_by_anton" / "settings.json",
    )


def selected_language_code() -> str:
    for path in _settings_candidates():
        try:
            value = json.loads(path.read_text(encoding="utf-8")).get("ui_language")
        except (OSError, ValueError, AttributeError):
            continue
        if value in SUPPORTED_LANGUAGE_CODES:
            return value
        # A settings file without the new field belongs to an existing Russian user.
        return DEFAULT_LANGUAGE
    return _system_language_code()


def _system_language_code() -> str:
    name = ""
    if sys.platform == "win32":
        try:
            buffer = ctypes.create_unicode_buffer(85)
            if ctypes.windll.kernel32.GetUserDefaultLocaleName(buffer, len(buffer)):
                name = buffer.value
        except (AttributeError, OSError):
            name = ""
    if not name:
        name = (locale.getlocale()[0] or "").replace("_", "-")
    if name in SUPPORTED_LANGUAGE_CODES:
        return name
    if name.casefold() in {"zh-hans-cn", "zh-hans"}:
        return "zh-CN"
    return DEFAULT_LANGUAGE


@lru_cache(maxsize=11)
def _catalog(language_code: str) -> dict[str, str]:
    path = _translations_dir() / f"{language_code}.ts"
    try:
        root = ET.parse(path).getroot()
    except (OSError, ET.ParseError):
        return {}
    result: dict[str, str] = {}
    for context in root.findall("context"):
        if context.findtext("name") != "PomodoroTimer":
            continue
        for message in context.findall("message"):
            source = message.findtext("source") or ""
            translation = message.find("translation")
            if translation is None or message.get("numerus") == "yes":
                continue
            text = "".join(translation.itertext()).strip()
            if source and text:
                result[source] = text
    return result


def early_tr(key: str, **parameters: object) -> str:
    selected = _catalog(selected_language_code()).get(key)
    fallback = _catalog(DEFAULT_LANGUAGE).get(key)
    text = selected or fallback or key
    return text.format_map(parameters) if parameters else text
