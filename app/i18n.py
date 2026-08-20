"""Qt localization infrastructure with stable keys and a Russian fallback."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Final

from PySide6.QtCore import (
    QCoreApplication,
    QEvent,
    QLibraryInfo,
    QLocale,
    QObject,
    QTranslator,
    Qt,
    Signal,
)
from PySide6.QtWidgets import QApplication

from app.models import TimerMode


TRANSLATION_CONTEXT: Final = "PomodoroTimer"
DEFAULT_LANGUAGE: Final = "ru-RU"
RTL_LANGUAGES: Final = frozenset({"ar-SA"})


@dataclass(frozen=True)
class Language:
    code: str
    native_name: str
    qt_catalog: str


SUPPORTED_LANGUAGES: Final = (
    Language("ru-RU", "Русский", "ru"),
    Language("en-US", "English", "en"),
    Language("es-ES", "Español", "es"),
    Language("de-DE", "Deutsch", "de"),
    Language("fr-FR", "Français", "fr"),
    Language("pt-BR", "Português (Brasil)", "pt_BR"),
    Language("zh-CN", "中文（简体）", "zh_CN"),
    Language("hi-IN", "हिन्दी", "hi"),
    Language("ar-SA", "العربية", "ar"),
    Language("ja-JP", "日本語", "ja"),
    Language("ko-KR", "한국어", "ko"),
)
SUPPORTED_LANGUAGE_CODES: Final = tuple(language.code for language in SUPPORTED_LANGUAGES)
LANGUAGE_BY_CODE: Final = {language.code: language for language in SUPPORTED_LANGUAGES}


def normalize_language_code(value: object, default: str = DEFAULT_LANGUAGE) -> str:
    """Return a supported BCP 47 code without accepting translated labels."""
    candidate = str(value or "").strip().replace("_", "-")
    if candidate in LANGUAGE_BY_CODE:
        return candidate
    casefolded = candidate.casefold()
    for code in SUPPORTED_LANGUAGE_CODES:
        if casefolded == code.casefold():
            return code
    return default if default in LANGUAGE_BY_CODE else DEFAULT_LANGUAGE


def system_language_code() -> str:
    """Use the Windows/Qt locale for a new installation, otherwise Russian."""
    system_name = QLocale.system().name().replace("_", "-")
    if system_name in LANGUAGE_BY_CODE:
        return system_name
    # Qt may report an explicit script (for example zh-Hans-CN).
    if system_name.casefold() in {"zh-hans-cn", "zh-hans"}:
        return "zh-CN"
    return DEFAULT_LANGUAGE


def translations_dir() -> Path:
    resource_root = Path(
        getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[1])
    )
    return resource_root / "assets" / "translations"


class _CompositeTranslator(QTranslator):
    """One installed translator that atomically switches app and Qt catalogs."""

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.current: QTranslator | None = None
        self.fallback: QTranslator | None = None
        self.qt_current: QTranslator | None = None

    def translate(
        self,
        context: str,
        source_text: str,
        disambiguation: str | None = None,
        n: int = -1,
    ) -> str | None:
        for translator in (self.current, self.fallback, self.qt_current):
            if translator is None:
                continue
            translated = translator.translate(context, source_text, disambiguation, n)
            if translated:
                return translated
        # PySide must return a null QString here. An empty Python string is an
        # explicit empty translation and makes unmapped Qt controls blank.
        return None


class TranslationManager(QObject):
    """Load each catalog once and update open Qt objects without recreating them."""

    language_changed = Signal(str)

    def __init__(self, application: QApplication, language_code: object) -> None:
        super().__init__(application)
        self.application = application
        self._catalog_cache: dict[str, QTranslator] = {}
        self._qt_catalog_cache: dict[str, QTranslator | None] = {}
        self._translator = _CompositeTranslator(self)
        self._translator.fallback = self._load_catalog(DEFAULT_LANGUAGE)
        self.application.installTranslator(self._translator)
        self._language_code = DEFAULT_LANGUAGE
        self.set_language(language_code, notify=False)

    @property
    def language_code(self) -> str:
        return self._language_code

    @property
    def is_rtl(self) -> bool:
        return self._language_code in RTL_LANGUAGES

    @property
    def loaded_language_codes(self) -> tuple[str, ...]:
        return tuple(self._catalog_cache)

    def set_language(self, language_code: object, *, notify: bool = True) -> bool:
        normalized = normalize_language_code(language_code)
        if normalized == self._language_code and notify:
            return False
        selected = None if normalized == DEFAULT_LANGUAGE else self._load_catalog(normalized)
        self._translator.current = selected
        self._translator.qt_current = self._load_qt_catalog(normalized)
        self._language_code = normalized
        locale = QLocale(normalized.replace("-", "_"))
        QLocale.setDefault(locale)
        self.application.setLayoutDirection(
            Qt.LayoutDirection.RightToLeft
            if normalized in RTL_LANGUAGES
            else Qt.LayoutDirection.LeftToRight
        )
        if notify:
            event = QEvent(QEvent.Type.LanguageChange)
            for widget in tuple(self.application.topLevelWidgets()):
                QCoreApplication.sendEvent(widget, event)
            self.language_changed.emit(normalized)
        return True

    def _load_catalog(self, language_code: str) -> QTranslator:
        cached = self._catalog_cache.get(language_code)
        if cached is not None:
            return cached
        path = translations_dir() / f"{language_code}.qm"
        translator = QTranslator(self)
        if not translator.load(str(path)):
            raise FileNotFoundError(f"Translation catalog is missing or invalid: {path}")
        self._catalog_cache[language_code] = translator
        return translator

    def _load_qt_catalog(self, language_code: str) -> QTranslator | None:
        if language_code in self._qt_catalog_cache:
            return self._qt_catalog_cache[language_code]
        catalog_name = LANGUAGE_BY_CODE[language_code].qt_catalog
        path = Path(QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)) / f"qtbase_{catalog_name}.qm"
        translator = QTranslator(self)
        loaded = translator.load(str(path))
        result = translator if loaded else None
        self._qt_catalog_cache[language_code] = result
        return result


_MANAGER: TranslationManager | None = None


def initialize_localization(application: QApplication, language_code: object) -> TranslationManager:
    global _MANAGER
    if _MANAGER is None or _MANAGER.application is not application:
        _MANAGER = TranslationManager(application, language_code)
    else:
        _MANAGER.set_language(language_code)
    return _MANAGER


def localization_manager() -> TranslationManager:
    if _MANAGER is None:
        raise RuntimeError("Localization has not been initialized")
    return _MANAGER


def tr(key: str, **parameters: object) -> str:
    """Translate a stable key and substitute named parameters."""
    text = QCoreApplication.translate(TRANSLATION_CONTEXT, key)
    if not text:
        text = key
    return text.format_map(parameters) if parameters else text


def trn(key: str, count: int, **parameters: object) -> str:
    """Select the locale-specific plural form and use a named count parameter."""
    number = int(count)
    text = QCoreApplication.translate(TRANSLATION_CONTEXT, key, None, number)
    if not text:
        text = key
    values = {"count": number, **parameters}
    return text.format_map(values)


def timer_mode_text(mode: TimerMode, waiting_for_continue: bool = False) -> str:
    if waiting_for_continue:
        keys = {
            TimerMode.WORK: "timer.mode.overwork",
            TimerMode.SHORT_BREAK: "timer.mode.short_break_overrun",
            TimerMode.LONG_BREAK: "timer.mode.long_break_overrun",
        }
    else:
        keys = {
            TimerMode.WORK: "timer.mode.work",
            TimerMode.SHORT_BREAK: "timer.mode.short_break",
            TimerMode.LONG_BREAK: "timer.mode.long_break",
        }
    return tr(keys[mode])


def language_native_name(code: object) -> str:
    return LANGUAGE_BY_CODE[normalize_language_code(code)].native_name
