# Карта проекта

## Назначение и запуск

PomodoroTimerByAnton — portable Windows-приложение Pomodoro на Python 3.14 и PySide6 Qt Widgets. Точка входа `main.py` получает mutex до загрузки GUI, затем создаёт `app.ui.main_window.MainWindow`.

```powershell
python -m pip install -r requirements-dev.txt
python main.py
python tools/build_translations.py --check-only
python -m unittest discover -s tests -v
python tools/generate_app_icons.py
python -m PyInstaller --noconfirm --clean PomodoroTimerByAnton.spec
```

Для headless UI-тестов задаётся `QT_QPA_PLATFORM=offscreen`. Подробности UI: `UI_ARCHITECTURE.md`; решение стека: `UI_TECH_DECISION.md`; parity: `UI_FEATURE_PARITY.md`.

## Структура

- `main.py` — ранняя блокировка и отложенный импорт GUI.
- `app/timer_engine.py`, `models.py` — независимая машина состояния и модели.
- `app/statistics.py`, `storage.py`, `profiles.py` — миграция/сохранение пользовательских данных.
- `app/overrun_effects.py` — чистая математика кадров и единый контроллер.
- `app/window_geometry.py` — первый размер, сохранение и clamp главного окна по мониторам.
- `app/theme.py` — смысловые палитры и Qt ThemeManager.
- `app/i18n.py`, `app/early_i18n.py` — Qt-каталоги, `QTranslator`, plural-формы, RTL и ранние сообщения до импорта Qt.
- `app/notifications.py`, `single_instance.py`, `autostart.py` — уведомления, mutex, HKCU Run.
- `app/ui/` — Qt-окна, дизайн-система, компоненты и семь видов виджета.
- `assets/icons/` — проектные SVG, PNG 16–256, многослойный ICO и лицензия CC0.
- `assets/translations/` — 11 исходных `.ts` и скомпилированных `.qm` каталогов UTF-8.
- `tools/generate_app_icons.py` — воспроизводимая генерация PNG/ICO из `app.svg` средствами PySide6.
- `tools/build_translations.py`, `tools/capture_localization_qa.py` — проверка/сборка каталогов и снимки полной языковой матрицы.
- `tests/` — unittest, включая PySide6 QtTest/offscreen.
- `docs/` — постоянная архитектурная документация.
- `PomodoroTimerByAnton.spec` — onedir-сборка PyInstaller.

`build/`, `dist/`, `.venv/`, `.idea/`, `__pycache__/`, `.pytest_cache/` создаются автоматически и не являются исходным кодом. `data/*.json` — пользовательские данные и не включаются в Git или сборку.

## Связи

`MainWindow` владеет единственным `TimerEngine`. Секундный `QTimer` вызывает `tick()`, затем события завершения передаются `StatisticsService` и `NotificationService`. Главное `TimerVisual` и активный `WidgetView` читают то же состояние. `WidgetActions` направляет команды виджета обратно в методы главного окна. `ThemeManager`, `TranslationManager` и `OverrunVisualController` рассылают палитру, тексты/направление и единый кадр, не меняя ядро.

## Пользовательские JSON

В Python-режиме каталог — `data/` в проекте. В onedir exe каталог `data/` создаётся рядом с exe; если это невозможно, используется `%USERPROFILE%/.pomodoro_timer_by_anton` с предупреждением. Старые данные копируются безопасно и не удаляются.

`settings.json` соответствует полям `AppSettings`: длительности, уведомления, профили, BCP-47 `ui_language`, `theme_name`, `appearance_mode`, две custom-палитры, `overrun_visual`, `widget_enabled`, тип/размер/opacity, `widget_layouts` для семи типов и `main_window_geometry`. Старый файл без `ui_language` получает русский, новая установка — поддерживаемый язык Windows или русский fallback. Отсутствующие/неверные известные поля нормализуются; старые переведённые значения типов/эффектов мигрируют в постоянные ID, старые координаты — в компактный вид, а неверная геометрия главного окна возвращается на доступный монитор.

`profiles.json` хранит именованные срезы настроек. `statistics.json` имеет `version: 2`, блоки `all_time` и `daily`, обычные метрики и три независимых счётчика превышения. Версия 1 дополняется нулями без повторного учёта периодов; структурное повреждение резервируется как `.corrupt*.bak`. Превышение записывается только при «Продолжить» или полном выходе.

## Зависимости и лицензии

Runtime: `PySide6-Essentials==6.11.1`/`shiboken6`, LGPL-3.0 option, динамическая onedir-компоновка. Build: `PyInstaller==6.22.0`, bootloader exception. SVG проекта — CC0-1.0. См. `requirements*.txt`, `THIRD_PARTY_NOTICES.md` и `assets/icons/LICENSE.md`.

## Ограничения

- mutex, автозапуск и целевая сборка ориентированы на Windows 10/11;
- системный title bar остаётся нативным для надёжного DPI, resize и доступности;
- Windows может оставить нативный title bar светлым, даже приняв DWM dark-mode attribute; frameless-замена намеренно не используется;
- секундный тик не компенсирует глубокий сон системы;
- Qt offscreen не подтверждает ClearType, реальный multi-monitor DPI, tray shell и GPU; это ручная релизная матрица;
- very-low widget opacity намеренно может снижать контраст; главный переключатель остаётся способом вернуть окно.
