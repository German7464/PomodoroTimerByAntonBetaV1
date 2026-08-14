# Карта проекта

## Назначение и запуск

PomodoroTimerByAnton — portable Windows-приложение Pomodoro на Python 3.14 и PySide6 Qt Widgets. Точка входа `main.py` получает mutex до загрузки GUI, затем создаёт `app.ui.main_window.MainWindow`.

```powershell
python -m pip install -r requirements-dev.txt
python main.py
python -m unittest discover -s tests -v
python -m PyInstaller --noconfirm --clean PomodoroTimerByAnton.spec
```

Для headless UI-тестов задаётся `QT_QPA_PLATFORM=offscreen`. Подробности UI: `UI_ARCHITECTURE.md`; решение стека: `UI_TECH_DECISION.md`; parity: `UI_FEATURE_PARITY.md`.

## Структура

- `main.py` — ранняя блокировка и отложенный импорт GUI.
- `app/timer_engine.py`, `models.py` — независимая машина состояния и модели.
- `app/statistics.py`, `storage.py`, `profiles.py` — миграция/сохранение пользовательских данных.
- `app/overrun_effects.py` — чистая математика кадров и единый контроллер.
- `app/theme.py` — смысловые палитры и Qt ThemeManager.
- `app/notifications.py`, `single_instance.py`, `autostart.py` — уведомления, mutex, HKCU Run.
- `app/ui/` — Qt-окна, дизайн-система, компоненты и семь видов виджета.
- `assets/icons/` — проектные SVG и лицензия.
- `tests/` — unittest, включая PySide6 QtTest/offscreen.
- `docs/` — постоянная архитектурная документация.
- `PomodoroTimerByAnton.spec` — onedir-сборка PyInstaller.

`build/`, `dist/`, `.venv/`, `.idea/`, `__pycache__/`, `.pytest_cache/` создаются автоматически и не являются исходным кодом. `data/*.json` — пользовательские данные и не включаются в Git или сборку.

## Связи

`MainWindow` владеет единственным `TimerEngine`. Секундный `QTimer` вызывает `tick()`, затем события завершения передаются `StatisticsService` и `NotificationService`. Главное `TimerVisual` и активный `WidgetView` читают то же состояние. `WidgetActions` направляет команды виджета обратно в методы главного окна. `ThemeManager` и `OverrunVisualController` рассылают палитру и единый кадр, не меняя ядро.

## Пользовательские JSON

В Python-режиме каталог — `data/` в проекте. В onedir exe каталог `data/` создаётся рядом с exe; если это невозможно, используется `%USERPROFILE%/.pomodoro_timer_by_anton` с предупреждением. Старые данные копируются безопасно и не удаляются.

`settings.json` соответствует полям `AppSettings`: длительности, уведомления, профили, `theme_name`, `appearance_mode`, две custom-палитры, `overrun_visual`, `widget_enabled`, тип/размер/opacity и `widget_layouts` для семи типов. Отсутствующие/неверные известные поля нормализуются; старые координаты мигрируют в компактный вид.

`profiles.json` хранит именованные срезы настроек. `statistics.json` имеет `version: 2`, блоки `all_time` и `daily`, обычные метрики и три независимых счётчика превышения. Версия 1 дополняется нулями без повторного учёта периодов; структурное повреждение резервируется как `.corrupt*.bak`. Превышение записывается только при «Продолжить» или полном выходе.

## Зависимости и лицензии

Runtime: `PySide6-Essentials==6.11.1`/`shiboken6`, LGPL-3.0 option, динамическая onedir-компоновка. Build: `PyInstaller==6.22.0`, bootloader exception. SVG проекта — CC0-1.0. См. `requirements*.txt`, `THIRD_PARTY_NOTICES.md` и `assets/icons/LICENSE.md`.

## Ограничения

- mutex, автозапуск и целевая сборка ориентированы на Windows 10/11;
- системный title bar остаётся нативным для надёжного DPI, resize и доступности;
- секундный тик не компенсирует глубокий сон системы;
- Qt offscreen не подтверждает ClearType, реальный multi-monitor DPI, tray shell и GPU; это ручная релизная матрица;
- very-low widget opacity намеренно может снижать контраст; главный переключатель остаётся способом вернуть окно.
