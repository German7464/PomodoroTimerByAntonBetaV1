"""End-to-end contracts for catalogs, persistence and live Qt localization."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from string import Formatter
from tempfile import TemporaryDirectory
import re
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from PySide6.QtCore import QEvent, QTranslator, Qt
from PySide6.QtWidgets import QDialog, QMessageBox, QPushButton

from app.i18n import (
    DEFAULT_LANGUAGE,
    SUPPORTED_LANGUAGES,
    TRANSLATION_CONTEXT,
    localization_manager,
    tr,
    translations_dir,
)
from app.models import TimerMode
from app.storage import load_app_settings, load_json, save_json
from app.ui.help_window import HelpWindow
from app.widget_settings import WIDGET_TYPE_COMPACT
from tests.qt_helpers import APP, isolated_main
from tests.test_timer_engine import make_settings
from tools import build_translations


RUSSIAN_TEXT = re.compile(r"[А-Яа-яЁё]")


def _placeholders(text: str) -> set[str]:
    return {
        field.split(".", 1)[0].split("[", 1)[0]
        for _literal, field, _specification, _conversion in Formatter().parse(text)
        if field
    }


def _catalog(path: Path) -> dict[tuple[str, str], tuple[str, ...]]:
    result: dict[tuple[str, str], tuple[str, ...]] = {}
    for context in ET.parse(path).getroot().findall("context"):
        context_name = context.findtext("name") or ""
        for message in context.findall("message"):
            source = message.findtext("source") or ""
            translation = message.find("translation")
            if translation is None:
                forms = ("",)
            elif message.get("numerus") == "yes":
                forms = tuple("".join(form.itertext()).strip() for form in translation.findall("numerusform"))
            else:
                forms = ("".join(translation.itertext()).strip(),)
            result[(context_name, source)] = forms
    return result


class LanguageChangeProbe(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.language_changes = 0

    def changeEvent(self, event: QEvent) -> None:  # noqa: N802 - Qt API
        if event.type() == QEvent.Type.LanguageChange:
            self.language_changes += 1
        super().changeEvent(event)


class CatalogContractTests(unittest.TestCase):
    def tearDown(self) -> None:
        localization_manager().set_language(DEFAULT_LANGUAGE)
        APP.processEvents()

    def test_all_catalogs_load_and_have_identical_complete_keys(self) -> None:
        reference = _catalog(translations_dir() / "ru-RU.ts")
        self.assertEqual(len(SUPPORTED_LANGUAGES), 11)
        self.assertGreater(len(reference), 250)

        for language in SUPPORTED_LANGUAGES:
            with self.subTest(language=language.code):
                ts_path = translations_dir() / f"{language.code}.ts"
                qm_path = translations_dir() / f"{language.code}.qm"
                self.assertEqual(set(_catalog(ts_path)), set(reference))
                translator = QTranslator()
                self.assertTrue(translator.load(str(qm_path)))

    def test_parameters_plural_forms_and_non_russian_catalogs_are_valid(self) -> None:
        reference = _catalog(translations_dir() / "ru-RU.ts")
        reference_parameters = {
            key: set().union(*(_placeholders(form) for form in forms))
            for key, forms in reference.items()
        }
        for language in SUPPORTED_LANGUAGES:
            catalog = _catalog(translations_dir() / f"{language.code}.ts")
            for key, forms in catalog.items():
                with self.subTest(language=language.code, key=key):
                    self.assertTrue(forms)
                    self.assertTrue(all(form for form in forms))
                    self.assertTrue(all(_placeholders(form) == reference_parameters[key] for form in forms))
                    if language.code != DEFAULT_LANGUAGE:
                        self.assertTrue(all(RUSSIAN_TEXT.search(form) is None for form in forms))

    def test_repository_translation_audit_detects_unused_and_runtime_strings(self) -> None:
        # The project audit additionally checks stable keys, duplicates, unused
        # keys, language-specific plural counts and Russian runtime allowlists.
        build_translations.validate()

    def test_unmapped_qt_strings_fall_back_without_blank_controls(self) -> None:
        for language_code, expected in (("en-US", {"Yes", "No"}), ("hi-IN", {"हाँ", "नहीं"})):
            with self.subTest(language=language_code):
                localization_manager().set_language(language_code)
                message_box = QMessageBox(
                    QMessageBox.Icon.Question,
                    "Title",
                    "Question",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                )
                labels = {
                    button.text().replace("&", "")
                    for button in message_box.findChildren(QPushButton)
                }
                self.assertEqual(labels, expected)

    def test_translation_resources_are_included_in_packaging_spec(self) -> None:
        spec = (Path(__file__).resolve().parents[1] / "PomodoroTimerByAnton.spec").read_text(encoding="utf-8")
        self.assertIn("assets/translations/*.qm", spec)
        self.assertIn("assets/translations/*.ts", spec)


class LocalizationPersistenceTests(unittest.TestCase):
    def test_language_code_is_saved_and_restored(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            settings = make_settings()
            settings.ui_language = "de-DE"
            from app.storage import save_app_settings

            save_app_settings(path, settings)
            self.assertEqual(load_json(path, {})["ui_language"], "de-DE")
            self.assertEqual(load_app_settings(path).ui_language, "de-DE")

    def test_existing_settings_without_language_remain_russian(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            save_json(path, {"work_minutes": 41})
            settings = load_app_settings(path)
            self.assertEqual(settings.ui_language, "ru-RU")
            self.assertEqual(settings.work_minutes, 41)

    def test_new_install_uses_supported_system_language_and_russian_fallback(self) -> None:
        for system_language, expected in (("de-DE", "de-DE"), ("ru-RU", "ru-RU")):
            with self.subTest(system_language=system_language), TemporaryDirectory() as directory:
                path = Path(directory) / "settings.json"
                with patch("app.storage.system_language_code", return_value=system_language):
                    self.assertEqual(load_app_settings(path).ui_language, expected)


class LiveLocalizationTests(unittest.TestCase):
    def tearDown(self) -> None:
        localization_manager().set_language(DEFAULT_LANGUAGE)
        APP.processEvents()

    def test_native_language_names_and_codes_are_never_translated(self) -> None:
        with isolated_main() as (window, _settings_path, _statistics_path):
            expected = [(language.native_name, language.code) for language in SUPPORTED_LANGUAGES]
            actual = [
                (window.settings_view.language_combo.itemText(index), window.settings_view.language_combo.itemData(index))
                for index in range(window.settings_view.language_combo.count())
            ]
            self.assertEqual(actual, expected)
            window.set_interface_language("ja-JP")
            APP.processEvents()
            translated = [
                (window.settings_view.language_combo.itemText(index), window.settings_view.language_combo.itemData(index))
                for index in range(window.settings_view.language_combo.count())
            ]
            self.assertEqual(translated, expected)

    def test_open_windows_widget_tray_editor_notification_update_in_place(self) -> None:
        settings = make_settings()
        settings.widget_enabled = True
        settings.widget_type = WIDGET_TYPE_COMPACT
        with isolated_main(settings) as (window, settings_path, _statistics_path):
            probe = LanguageChangeProbe()
            probe.show()
            help_window = HelpWindow(window)
            help_window.show()
            window.settings_view._open_theme_editor()
            editor = window.settings_view.theme_editor
            self.assertIsNotNone(editor)
            window.notifications._show_popup(
                "Проверка",
                "action.continue",
                None,
                TimerMode.WORK,
                TimerMode.SHORT_BREAK,
            )
            APP.processEvents()

            tray_icon = window.tray.icon
            tray_menu = window.tray.menu
            widget_shell = window.widget_window.window
            widget_view = window.widget_window.view
            timer_engine = window.timer
            old_nav = window.nav_buttons[0].accessibleName()

            window.set_interface_language("en-US")
            APP.processEvents()

            self.assertIs(window.tray.icon, tray_icon)
            self.assertIs(window.tray.menu, tray_menu)
            self.assertIs(window.widget_window.window, widget_shell)
            self.assertIs(window.widget_window.view, widget_view)
            self.assertIs(window.timer, timer_engine)
            self.assertGreater(int(window.property("languageChangeCount") or 0), 0)
            self.assertGreater(probe.language_changes, 0)
            self.assertNotEqual(window.nav_buttons[0].accessibleName(), old_nav)
            self.assertEqual(window.nav_buttons[0].accessibleName(), tr("nav.timer"))
            self.assertEqual(window.tray.actions["tray.show"].text(), tr("tray.show"))
            self.assertEqual(help_window.windowTitle(), tr("help.title"))
            self.assertEqual(editor.windowTitle(), tr("theme_editor.title"))
            self.assertEqual(window.notifications._active_button.text(), tr("action.continue"))
            self.assertEqual(
                window.notifications._active_label.text(),
                window.notifications._build_message(TimerMode.WORK, TimerMode.SHORT_BREAK),
            )
            self.assertEqual(load_app_settings(settings_path).ui_language, "en-US")

            window.notifications.dismiss()
            help_window.close()
            probe.close()
            if editor is not None:
                editor.close()
            APP.processEvents()

    def test_switching_language_preserves_running_timer_statistics_and_user_text(self) -> None:
        settings = make_settings()
        settings.work_end_message = "My private reminder"
        with isolated_main(settings) as (window, _settings_path, _statistics_path):
            window.start()
            timer_state = deepcopy(window.timer.state)
            statistics = deepcopy(window.statistics.data)
            user_text = window.settings_view.work_message.text()

            window.set_interface_language("fr-FR")
            APP.processEvents()

            self.assertTrue(window.timer.state.is_running)
            self.assertEqual(window.timer.state, timer_state)
            self.assertEqual(window.statistics.data, statistics)
            self.assertEqual(window.settings_view.work_message.text(), user_text)

    def test_arabic_is_rtl_only_and_time_remains_ltr(self) -> None:
        settings = make_settings()
        settings.widget_enabled = True
        with isolated_main(settings) as (window, _settings_path, _statistics_path):
            window.set_interface_language("ar-SA")
            APP.processEvents()
            self.assertEqual(APP.layoutDirection(), Qt.LayoutDirection.RightToLeft)
            self.assertEqual(window.layoutDirection(), Qt.LayoutDirection.RightToLeft)
            self.assertEqual(window.timer_visual.time_label.layoutDirection(), Qt.LayoutDirection.LeftToRight)
            self.assertEqual(
                window.widget_window.view.timer_visual.time_label.layoutDirection(),
                Qt.LayoutDirection.LeftToRight,
            )

            window.set_interface_language("ru-RU")
            APP.processEvents()
            self.assertEqual(APP.layoutDirection(), Qt.LayoutDirection.LeftToRight)
            self.assertEqual(window.layoutDirection(), Qt.LayoutDirection.LeftToRight)
            self.assertEqual(window.timer_visual.time_label.layoutDirection(), Qt.LayoutDirection.LeftToRight)


if __name__ == "__main__":
    unittest.main()
