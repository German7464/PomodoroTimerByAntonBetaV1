# Соответствие функций интерфейса

| Функция до миграции | Где находится в Qt | Подтверждение | Ограничения |
|---|---|---|---|
| Старт, пауза, пропуск, сброс | `MainWindow`, страница «Таймер» | `test_timer_engine`, `test_ui_contracts` | Точность тика зависит от GUI event loop |
| Автоматический/ручной переход | `TimerEngine`, общие Qt-команды | `test_timer_engine`, `test_ui_contracts` | Нет |
| Переработка и два превышения отдыха | `TimerVisual`, `OverrunVisualController` | `test_overrun_effects`, `test_ui_contracts` | Частота эффекта около 12,5 кадров/с |
| Кнопка «Продолжить» | главное окно, уведомление, каждый виджет → один метод | `test_ui_contracts` | Нет |
| Статистика сегодня/всё время | `StatsView` с карточками | `test_statistics`, `test_ui_contracts` | Графиков пока нет |
| Настройки и профили | `SettingsView`, восемь разделов | тесты storage/theme/widget | Автозапуск меняется только в exe |
| Comet/Aurora/Warm/custom, light/dark | `ThemeManager`, QPalette, карточки темы, редактор | `test_theme`, `test_adaptive_ui` | DWM dark title имеет системный fallback |
| Двоичные настройки | единый `ToggleSwitch` | `test_toggle_switch` + QtTest | Считывается также текстом ВКЛ/ВЫКЛ |
| Шесть эффектов | общий `TimerVisual` и кадр | `test_overrun_effects` | Движение можно отключить |
| Семь макетов виджета | фабрика `VIEW_CLASSES` в одном `WidgetShell` | `test_widget_settings`, `test_widget_visibility` | Кольцо остаётся прямоугольным системным окном |
| Размер/позиция каждого виджета | `widget_layouts`, Qt move/resize | `test_widget_settings`, `test_widget_visibility` | Реальные multi-monitor DPI требуют ручной QA |
| Прозрачность 5–100% и временные 100% | `setWindowOpacity()` | `test_widget_opacity` | Очень малая alpha снижает читаемость по выбору пользователя |
| Уведомления | немодальный тематизированный `QDialog` | `test_ui_contracts` | Нативный Windows toast не используется |
| Трей | `QSystemTrayIcon`, прямой тематический `QMenu` | `test_adaptive_ui`, exe smoke | Наличие трея зависит от оболочки Windows |
| Единственный экземпляр | ранний Windows mutex | `test_single_instance`, exe smoke | Windows-only по проектному решению |
| Миграция JSON | прежние storage/statistics/services | тесты migration/statistics/theme/widget | Неизвестные поля сохраняются только там, где поддерживал прежний формат |

## Ручная визуальная матрица

Перед релизом на реальном рабочем столе следует проверить шесть сочетаний встроенных тем/режимов, пользовательскую тему, паузу и три превышения; затем семь видов виджета при Windows DPI 100%, 125% и 150%, несколько мониторов, alpha 5% и временную alpha 100%. Автоматические offscreen-снимки подтверждают разметку и отсутствие падения, но не заменяют проверку системных заголовков, ClearType и разных видеодрайверов.
