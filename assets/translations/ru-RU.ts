<?xml version='1.0' encoding='utf-8'?>
<TS version="2.1" language="ru_RU">
  <context>
    <name>PomodoroTimer</name>
    <message>
      <source>action.apply</source>
      <translation>Применить</translation>
    </message>
    <message>
      <source>action.cancel</source>
      <translation>Отмена</translation>
    </message>
    <message>
      <source>action.choose</source>
      <translation>Выбрать</translation>
    </message>
    <message>
      <source>action.close</source>
      <translation>Закрыть</translation>
    </message>
    <message>
      <source>action.continue</source>
      <translation>Продолжить</translation>
    </message>
    <message>
      <source>action.continue_next_period</source>
      <translation>Продолжить и начать следующий период</translation>
    </message>
    <message>
      <source>action.open</source>
      <translation>Открыть</translation>
    </message>
    <message>
      <source>action.open_main_window</source>
      <translation>Открыть главное окно</translation>
    </message>
    <message>
      <source>action.pause</source>
      <translation>Пауза</translation>
    </message>
    <message>
      <source>action.preview</source>
      <translation>Предпросмотр</translation>
    </message>
    <message>
      <source>action.refresh</source>
      <translation>Обновить</translation>
    </message>
    <message>
      <source>action.reset</source>
      <translation>Сбросить</translation>
    </message>
    <message>
      <source>action.show</source>
      <translation>Показать</translation>
    </message>
    <message>
      <source>action.skip</source>
      <translation>Пропустить</translation>
    </message>
    <message>
      <source>action.start</source>
      <translation>Старт</translation>
    </message>
    <message>
      <source>dialog.color.choose</source>
      <translation>Выберите цвет</translation>
    </message>
    <message>
      <source>dialog.color.invalid_hex</source>
      <translation>Исправьте значения: требуется формат #RRGGBB.</translation>
    </message>
    <message>
      <source>dialog.color.title</source>
      <translation>Цвет</translation>
    </message>
    <message>
      <source>error.autostart.python_unavailable</source>
      <translation>Автозапуск доступен только для собранной exe-версии. При запуске из Python включение автозапуска не выполняется.</translation>
    </message>
    <message>
      <source>error.data.portable_fallback</source>
      <translation>Не удалось записать данные рядом с программой. Настройки временно будут храниться в папке пользователя. Для portable-режима перенесите программу в папку, доступную для записи.</translation>
    </message>
    <message>
      <source>error.data.portable_title</source>
      <translation>Portable-режим</translation>
    </message>
    <message>
      <source>error.data.unavailable</source>
      <translation>Не удалось создать папку для настроек приложения.</translation>
    </message>
    <message>
      <source>error.widget.hide</source>
      <translation>Не удалось скрыть виджет: {error}</translation>
    </message>
    <message>
      <source>error.widget.show</source>
      <translation>Не удалось показать виджет: {error}</translation>
    </message>
    <message>
      <source>error.widget.state_mismatch</source>
      <translation>окно не перешло в запрошенное состояние</translation>
    </message>
    <message>
      <source>help.content</source>
      <translation># Pomodoro Timer

## Быстрый старт

Выберите длительности в настройках, откройте раздел «Таймер» и нажмите
«Старт». В верхней части окна можно мгновенно переключить светлый и тёмный
режим. Все двоичные настройки используют переключатели; обычные действия
остаются кнопками.

## Управление таймером

- **Старт** запускает текущий период.
- **Пауза / Продолжить** замораживает и возобновляет обычный период.
- **Пропустить период** переходит к следующему режиму без зачёта длительности.
- **Сбросить** возвращает остановленную работу и учитывает сброс в статистике.
- **Продолжить и начать следующий период** появляется при ручном переходе,
  сохраняет превышение один раз и сразу запускает следующий период.

При автоматическом переходе следующий период стартует сразу и превышение не
считается. При ручном переходе приложение показывает «Переработка», «Короткий
отдых сверх нормы» или «Длинный отдых сверх нормы» и время со знаком `+`.
Пока идёт превышение, старт, пауза, пропуск и сброс заблокированы, чтобы время
не потерялось.

## Оформление и доступность

Темы Comet, Aurora, Warm и Пользовательская имеют светлый и тёмный режим.
Редактор пользовательской темы хранит режимы раздельно, проверяет `#RRGGBB` и
предупреждает о контрасте ниже 4,5:1. «Отмена» возвращает сохранённые цвета, а
сброс восстанавливает безопасную Comet.

Интерфейс построен на Qt Widgets, масштабируется средствами Windows/Qt и
поддерживает клавиатурный фокус. Переключатели меняются мышью, `Пробелом` или
`Enter`; их состояние видно по положению, цвету и тексту `ВКЛ/ВЫКЛ`.
Командные кнопки также активируются `Пробелом` или `Enter`, дают короткую
анимацию нажатия и показывают контрастную рамку только при клавиатурной
навигации. При отключённом движении нажатие обозначается мгновенной сменой цвета.

Главное окно при первом запуске занимает около 80% доступной области экрана,
запоминает размер и положение и возвращается на видимый монитор после смены
разрешения. На среднем и узком окне навигация сворачивается до иконок с
подсказками, группы кнопок переносятся строками, а содержимое настроек
прокручивается без обрезания закреплённых действий.

Тёмная тема оформляет viewport, меню трея и, если Windows поддерживает DWM
dark title, системный заголовок. Оригинальная иконка с помидором и дугой
таймера используется окном, панелью задач, треем и собранным EXE.

## Индикация превышения

Доступны пульсация, увеличение цифр, сигнальные маячки, акцентная рамка,
волна-индикатор и режим без анимации. Изменение цвета, область, скорость,
интенсивность и три цвета настраиваются отдельно. Предпросмотр не меняет
таймер, статистику, уведомления или прозрачность.

Главное окно и виджет получают один кадр эффекта. После «Продолжить» или выхода
обычные цвета и размеры сразу восстанавливаются. При отключённом движении
остаётся статичная доступная индикация, название состояния и знак `+`.

## Плавающий виджет

Переключатель «Отображать виджет» на странице таймера показывает и скрывает
одно и то же окно. Доступны семь видов: Минималистичный, Компактный,
Расширенный, Микро, Строка, Кольцо и Табло. Все читают один `TimerEngine`.

Тип, размер и положение хранятся отдельно для каждого вида. Ручное изменение
создаёт пользовательский размер. Непрозрачность регулируется от 5 до 100%,
а при превышении виджет по желанию временно становится полностью
непрозрачным и затем возвращает точное постоянное значение.

В расширенном виде узкая панель переносит действия целиком. Надпись
«Продолжить» не сокращается; при минимальной ширине только «Открыть» может
стать иконкой с подсказкой, а остальные команды переходят на следующую строку.

## Уведомления, статистика и трей

Информационное уведомление автоматического перехода можно закрыть. Ручное
уведомление содержит «Продолжить»; крестик закрывает только окно и не теряет
превышение. Та же команда всегда доступна в главном окне и виджете.

Статистика отдельно показывает обычную работу, обычный отдых и три вида
превышения за сегодня и всё время. Закрытие главного окна может свернуть
программу в трей. При полном штатном выходе накопленное превышение сохраняется.

Для текущего пользователя Windows работает один экземпляр программы. Второй
запуск показывает системное сообщение и не создаёт интерфейс.
</translation>
    </message>
    <message>
      <source>help.subtitle</source>
      <translation>Функции и безопасное поведение приложения.</translation>
    </message>
    <message>
      <source>help.title</source>
      <translation>Справка</translation>
    </message>
    <message>
      <source>main.brand_subtitle</source>
      <translation>Спокойный ритм работы</translation>
    </message>
    <message>
      <source>nav.help</source>
      <translation>Справка</translation>
    </message>
    <message>
      <source>nav.settings</source>
      <translation>Настройки</translation>
    </message>
    <message>
      <source>nav.statistics</source>
      <translation>Статистика</translation>
    </message>
    <message>
      <source>nav.timer</source>
      <translation>Таймер</translation>
    </message>
    <message>
      <source>notification.auto_transition</source>
      <translation>{completed}

Следующий период уже запущен: {next_period}.</translation>
    </message>
    <message>
      <source>notification.completed.long_break</source>
      <translation>Длинный отдых завершён.</translation>
    </message>
    <message>
      <source>notification.completed.short_break</source>
      <translation>Короткий отдых завершён.</translation>
    </message>
    <message>
      <source>notification.completed.work</source>
      <translation>Рабочий период завершён.</translation>
    </message>
    <message>
      <source>notification.default.long_break_end</source>
      <translation>Длинный отдых завершен. Пора начать новый рабочий период.</translation>
    </message>
    <message>
      <source>notification.default.short_break_end</source>
      <translation>Короткий отдых завершен. Пора вернуться к работе.</translation>
    </message>
    <message>
      <source>notification.default.work_end</source>
      <translation>Рабочий период завершен. Время отдохнуть.</translation>
    </message>
    <message>
      <source>notification.manual_transition</source>
      <translation>{completed}

Нажмите «Продолжить», чтобы начать {next_period}.</translation>
    </message>
    <message>
      <source>overrun.effect.beacons</source>
      <translation>Сигнальные маячки</translation>
    </message>
    <message>
      <source>overrun.effect.border</source>
      <translation>Акцентная рамка</translation>
    </message>
    <message>
      <source>overrun.effect.none</source>
      <translation>Без анимации</translation>
    </message>
    <message>
      <source>overrun.effect.pulse</source>
      <translation>Пульсация</translation>
    </message>
    <message>
      <source>overrun.effect.scale</source>
      <translation>Увеличение цифр</translation>
    </message>
    <message>
      <source>overrun.effect.wave</source>
      <translation>Волна-индикатор</translation>
    </message>
    <message>
      <source>overrun.intensity.medium</source>
      <translation>Средне</translation>
    </message>
    <message>
      <source>overrun.intensity.strong</source>
      <translation>Сильно</translation>
    </message>
    <message>
      <source>overrun.intensity.weak</source>
      <translation>Слабо</translation>
    </message>
    <message>
      <source>overrun.scope.both</source>
      <translation>Цифры и карточка</translation>
    </message>
    <message>
      <source>overrun.scope.card</source>
      <translation>Карточка таймера</translation>
    </message>
    <message>
      <source>overrun.scope.digits</source>
      <translation>Только цифры таймера</translation>
    </message>
    <message>
      <source>overrun.speed.fast</source>
      <translation>Быстро</translation>
    </message>
    <message>
      <source>overrun.speed.normal</source>
      <translation>Обычно</translation>
    </message>
    <message>
      <source>overrun.speed.slow</source>
      <translation>Медленно</translation>
    </message>
    <message>
      <source>settings.appearance.dark_mode</source>
      <translation>Тёмный режим</translation>
    </message>
    <message>
      <source>settings.appearance.dark_mode.description</source>
      <translation>ВЫКЛ — светлый режим, ВКЛ — тёмный.</translation>
    </message>
    <message>
      <source>settings.appearance.edit_colors</source>
      <translation>Настроить цвета</translation>
    </message>
    <message>
      <source>settings.appearance.editor_unavailable</source>
      <translation>Редактор недоступен в этом окне.</translation>
    </message>
    <message>
      <source>settings.appearance.language</source>
      <translation>Язык интерфейса</translation>
    </message>
    <message>
      <source>settings.appearance.subtitle</source>
      <translation>Полноценные палитры меняют все открытые окна без перезапуска.</translation>
    </message>
    <message>
      <source>settings.appearance.title</source>
      <translation>Оформление</translation>
    </message>
    <message>
      <source>settings.logic.long_break_interval</source>
      <translation>Рабочих периодов до длинного отдыха</translation>
    </message>
    <message>
      <source>settings.logic.subtitle</source>
      <translation>Порядок работы, короткого и длинного отдыха.</translation>
    </message>
    <message>
      <source>settings.logic.title</source>
      <translation>Логика таймера</translation>
    </message>
    <message>
      <source>settings.logic.use_long_break</source>
      <translation>Использовать длинный отдых</translation>
    </message>
    <message>
      <source>settings.logic.use_long_break.description</source>
      <translation>После заданного числа рабочих периодов.</translation>
    </message>
    <message>
      <source>settings.notifications.auto_transition</source>
      <translation>Автоматический переход</translation>
    </message>
    <message>
      <source>settings.notifications.auto_transition.description</source>
      <translation>ВКЛ — следующий период запускается сразу; ВЫКЛ — считается превышение.</translation>
    </message>
    <message>
      <source>settings.notifications.enabled</source>
      <translation>Уведомления</translation>
    </message>
    <message>
      <source>settings.notifications.long_break_end</source>
      <translation>Конец длинного отдыха</translation>
    </message>
    <message>
      <source>settings.notifications.short_break_end</source>
      <translation>Конец короткого отдыха</translation>
    </message>
    <message>
      <source>settings.notifications.sound</source>
      <translation>Звук уведомлений</translation>
    </message>
    <message>
      <source>settings.notifications.subtitle</source>
      <translation>Ручной переход всегда можно завершить из главного окна или виджета.</translation>
    </message>
    <message>
      <source>settings.notifications.title</source>
      <translation>Уведомления</translation>
    </message>
    <message>
      <source>settings.notifications.work_end</source>
      <translation>Конец работы</translation>
    </message>
    <message>
      <source>settings.overrun.allow_motion</source>
      <translation>Разрешить движение эффектов</translation>
    </message>
    <message>
      <source>settings.overrun.change_color</source>
      <translation>Изменять цвет таймера</translation>
    </message>
    <message>
      <source>settings.overrun.color_dialog</source>
      <translation>Цвет превышения</translation>
    </message>
    <message>
      <source>settings.overrun.effect</source>
      <translation>Основной эффект</translation>
    </message>
    <message>
      <source>settings.overrun.intensity</source>
      <translation>Интенсивность</translation>
    </message>
    <message>
      <source>settings.overrun.invalid_colors</source>
      <translation>Некорректные цвета заменены значениями активной темы.</translation>
    </message>
    <message>
      <source>settings.overrun.opaque_widget</source>
      <translation>Делать виджет непрозрачным при превышении</translation>
    </message>
    <message>
      <source>settings.overrun.scope</source>
      <translation>Область изменения цвета</translation>
    </message>
    <message>
      <source>settings.overrun.separate_colors</source>
      <translation>Отдельные цвета</translation>
    </message>
    <message>
      <source>settings.overrun.speed</source>
      <translation>Скорость</translation>
    </message>
    <message>
      <source>settings.overrun.subtitle</source>
      <translation>Один общий кадр применяется к главному окну и открытому виджету.</translation>
    </message>
    <message>
      <source>settings.overrun.title</source>
      <translation>Индикация превышения</translation>
    </message>
    <message>
      <source>settings.overrun.use_theme_color</source>
      <translation>По теме</translation>
    </message>
    <message>
      <source>settings.profiles.apply</source>
      <translation>Применить профиль</translation>
    </message>
    <message>
      <source>settings.profiles.default_cannot_delete</source>
      <translation>Стандартный профиль удалить нельзя.</translation>
    </message>
    <message>
      <source>settings.profiles.default_name</source>
      <translation>Стандартный</translation>
    </message>
    <message>
      <source>settings.profiles.defaults</source>
      <translation>Настройки по умолчанию</translation>
    </message>
    <message>
      <source>settings.profiles.delete</source>
      <translation>Удалить профиль</translation>
    </message>
    <message>
      <source>settings.profiles.delete_confirmation</source>
      <translation>Удалить профиль «{profile_name}»?</translation>
    </message>
    <message>
      <source>settings.profiles.delete_title</source>
      <translation>Удалить профиль</translation>
    </message>
    <message>
      <source>settings.profiles.dialog_title</source>
      <translation>Профиль</translation>
    </message>
    <message>
      <source>settings.profiles.enter_name</source>
      <translation>Введите имя профиля.</translation>
    </message>
    <message>
      <source>settings.profiles.name_placeholder</source>
      <translation>Имя профиля</translation>
    </message>
    <message>
      <source>settings.profiles.restore_personal</source>
      <translation>Вернуть мои настройки</translation>
    </message>
    <message>
      <source>settings.profiles.save</source>
      <translation>Сохранить профиль</translation>
    </message>
    <message>
      <source>settings.profiles.select_profile</source>
      <translation>Выберите профиль из списка.</translation>
    </message>
    <message>
      <source>settings.profiles.subtitle</source>
      <translation>Сохраняйте наборы длительностей, оформления и виджета.</translation>
    </message>
    <message>
      <source>settings.profiles.title</source>
      <translation>Профили</translation>
    </message>
    <message>
      <source>settings.save</source>
      <translation>Сохранить настройки</translation>
    </message>
    <message>
      <source>settings.section.appearance</source>
      <translation>Оформление</translation>
    </message>
    <message>
      <source>settings.section.logic</source>
      <translation>Логика таймера</translation>
    </message>
    <message>
      <source>settings.section.notifications</source>
      <translation>Уведомления</translation>
    </message>
    <message>
      <source>settings.section.overrun</source>
      <translation>Превышение</translation>
    </message>
    <message>
      <source>settings.section.profiles</source>
      <translation>Профили</translation>
    </message>
    <message>
      <source>settings.section.time</source>
      <translation>Время</translation>
    </message>
    <message>
      <source>settings.section.tray</source>
      <translation>Трей и автозапуск</translation>
    </message>
    <message>
      <source>settings.section.widget</source>
      <translation>Виджет</translation>
    </message>
    <message>
      <source>settings.subtitle</source>
      <translation>Изменения темы и виджета применяются сразу; остальные — после сохранения.</translation>
    </message>
    <message>
      <source>settings.time.format</source>
      <translation>Формат времени</translation>
    </message>
    <message>
      <source>settings.time.long_break_minutes</source>
      <translation>Длинный отдых, минут</translation>
    </message>
    <message>
      <source>settings.time.short_break_minutes</source>
      <translation>Короткий отдых, минут</translation>
    </message>
    <message>
      <source>settings.time.subtitle</source>
      <translation>Длительности применяются безопасно при сохранении.</translation>
    </message>
    <message>
      <source>settings.time.title</source>
      <translation>Время</translation>
    </message>
    <message>
      <source>settings.time.work_minutes</source>
      <translation>Работа, минут</translation>
    </message>
    <message>
      <source>settings.title</source>
      <translation>Настройки</translation>
    </message>
    <message>
      <source>settings.tray.autostart</source>
      <translation>Автозапуск вместе с Windows</translation>
    </message>
    <message>
      <source>settings.tray.autostart_current</source>
      <translation>Автозапуск включён и указывает на текущую папку программы.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_disabled</source>
      <translation>Автозапуск выключен.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_python</source>
      <translation>Запуск из Python: включение автозапуска доступно в exe-версии.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_stale</source>
      <translation>Путь автозапуска устарел. Обновите его после перемещения программы.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_title</source>
      <translation>Автозапуск</translation>
    </message>
    <message>
      <source>settings.tray.close_to_tray</source>
      <translation>При закрытии сворачивать в трей</translation>
    </message>
    <message>
      <source>settings.tray.minimize_on_start</source>
      <translation>Сворачивать программу после запуска</translation>
    </message>
    <message>
      <source>settings.tray.subtitle</source>
      <translation>Системный трей работает в общем GUI-потоке Qt.</translation>
    </message>
    <message>
      <source>settings.tray.title</source>
      <translation>Трей и автозапуск</translation>
    </message>
    <message>
      <source>settings.tray.update_autostart</source>
      <translation>Обновить путь автозапуска</translation>
    </message>
    <message>
      <source>settings.widget.always_on_top</source>
      <translation>Поверх всех окон</translation>
    </message>
    <message>
      <source>settings.widget.dialog_title</source>
      <translation>Виджет</translation>
    </message>
    <message>
      <source>settings.widget.opacity</source>
      <translation>Непрозрачность виджета</translation>
    </message>
    <message>
      <source>settings.widget.opacity.description</source>
      <translation>Чем ниже значение, тем прозрачнее виджет. Минимум — 5%.</translation>
    </message>
    <message>
      <source>settings.widget.position_reset</source>
      <translation>Позиция текущего типа сброшена.</translation>
    </message>
    <message>
      <source>settings.widget.reset_position</source>
      <translation>Сбросить позицию текущего типа</translation>
    </message>
    <message>
      <source>settings.widget.size</source>
      <translation>Размер</translation>
    </message>
    <message>
      <source>settings.widget.subtitle</source>
      <translation>Видимость управляется переключателем на странице таймера.</translation>
    </message>
    <message>
      <source>settings.widget.title</source>
      <translation>Плавающий виджет</translation>
    </message>
    <message>
      <source>settings.widget.type</source>
      <translation>Тип виджета</translation>
    </message>
    <message>
      <source>startup.already_running</source>
      <translation>Pomodoro Timer уже запускается или уже запущен. Дождитесь открытия окна либо используйте уже открытое приложение.</translation>
    </message>
    <message>
      <source>startup.lock.already_running</source>
      <translation>Другой экземпляр приложения уже работает.</translation>
    </message>
    <message>
      <source>startup.lock.create_failed</source>
      <translation>Не удалось создать системную блокировку (WinError {error_code}).</translation>
    </message>
    <message>
      <source>startup.lock.release_failed</source>
      <translation>Не удалось освободить системную блокировку (WinError {error_code}).</translation>
    </message>
    <message>
      <source>startup.lock.secondary_close_failed</source>
      <translation>Другой экземпляр уже запущен, но не удалось закрыть вторичный handle (WinError {error_code}).</translation>
    </message>
    <message>
      <source>startup.lock.unsupported</source>
      <translation>Системная блокировка одного экземпляра поддерживается только в Windows.</translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_cycles</source>
      <translation>
        <numerusform>Полных циклов</numerusform>
        <numerusform>Полных циклов</numerusform>
        <numerusform>Полных циклов</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_long_breaks</source>
      <translation>
        <numerusform>Длинных отдыхов</numerusform>
        <numerusform>Длинных отдыхов</numerusform>
        <numerusform>Длинных отдыхов</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_short_breaks</source>
      <translation>
        <numerusform>Коротких отдыхов</numerusform>
        <numerusform>Коротких отдыхов</numerusform>
        <numerusform>Коротких отдыхов</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_work_periods</source>
      <translation>
        <numerusform>Рабочих периодов</numerusform>
        <numerusform>Рабочих периодов</numerusform>
        <numerusform>Рабочих периодов</numerusform>
      </translation>
    </message>
    <message>
      <source>stats.metric.long_break_overrun</source>
      <translation>Длинный отдых сверх нормы</translation>
    </message>
    <message>
      <source>stats.metric.overwork_time</source>
      <translation>Время переработки</translation>
    </message>
    <message>
      <source>stats.metric.rest_time</source>
      <translation>Время отдыха</translation>
    </message>
    <message>
      <source>stats.metric.short_break_overrun</source>
      <translation>Короткий отдых сверх нормы</translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.skipped_periods</source>
      <translation>
        <numerusform>Пропущено периодов</numerusform>
        <numerusform>Пропущено периодов</numerusform>
        <numerusform>Пропущено периодов</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.timer_resets</source>
      <translation>
        <numerusform>Сбросов таймера</numerusform>
        <numerusform>Сбросов таймера</numerusform>
        <numerusform>Сбросов таймера</numerusform>
      </translation>
    </message>
    <message>
      <source>stats.metric.work_time</source>
      <translation>Время работы</translation>
    </message>
    <message>
      <source>stats.period.all_time</source>
      <translation>За всё время</translation>
    </message>
    <message>
      <source>stats.period.today</source>
      <translation>Сегодня</translation>
    </message>
    <message>
      <source>stats.reset.action</source>
      <translation>Сбросить статистику</translation>
    </message>
    <message>
      <source>stats.reset.confirmation</source>
      <translation>Вы действительно хотите удалить всю статистику?</translation>
    </message>
    <message>
      <source>stats.reset.title</source>
      <translation>Сброс статистики</translation>
    </message>
    <message>
      <source>stats.subtitle</source>
      <translation>Обычное время и превышения учитываются раздельно.</translation>
    </message>
    <message>
      <source>stats.title</source>
      <translation>Статистика</translation>
    </message>
    <message>
      <source>theme.appearance.dark</source>
      <translation>Тёмная</translation>
    </message>
    <message>
      <source>theme.appearance.light</source>
      <translation>Светлая</translation>
    </message>
    <message>
      <source>theme.contrast.accent</source>
      <translation>Текст акцента / акцент</translation>
    </message>
    <message>
      <source>theme.contrast.button</source>
      <translation>Текст кнопок / кнопка</translation>
    </message>
    <message>
      <source>theme.contrast.long_break</source>
      <translation>Длинный отдых / карточка</translation>
    </message>
    <message>
      <source>theme.contrast.long_break_overrun</source>
      <translation>Длинный отдых сверх нормы / карточка</translation>
    </message>
    <message>
      <source>theme.contrast.overwork</source>
      <translation>Переработка / карточка</translation>
    </message>
    <message>
      <source>theme.contrast.primary_card</source>
      <translation>Основной текст / карточка</translation>
    </message>
    <message>
      <source>theme.contrast.secondary_card</source>
      <translation>Вторичный текст / карточка</translation>
    </message>
    <message>
      <source>theme.contrast.short_break</source>
      <translation>Короткий отдых / карточка</translation>
    </message>
    <message>
      <source>theme.contrast.short_break_overrun</source>
      <translation>Короткий отдых сверх нормы / карточка</translation>
    </message>
    <message>
      <source>theme.contrast.work</source>
      <translation>Работа / карточка</translation>
    </message>
    <message>
      <source>theme.description.aurora</source>
      <translation>Холодные синие и фиолетовые акценты</translation>
    </message>
    <message>
      <source>theme.description.comet</source>
      <translation>Спокойная нейтральная палитра</translation>
    </message>
    <message>
      <source>theme.description.custom</source>
      <translation>Ваши независимые светлая и тёмная палитры</translation>
    </message>
    <message>
      <source>theme.description.warm</source>
      <translation>Мягкие песочные и тёплые поверхности</translation>
    </message>
    <message>
      <source>theme.name.aurora</source>
      <translation>Aurora</translation>
    </message>
    <message>
      <source>theme.name.comet</source>
      <translation>Comet</translation>
    </message>
    <message>
      <source>theme.name.custom</source>
      <translation>Пользовательская</translation>
    </message>
    <message>
      <source>theme.name.warm</source>
      <translation>Warm</translation>
    </message>
    <message>
      <source>theme_editor.color.accent</source>
      <translation>Акцент</translation>
    </message>
    <message>
      <source>theme_editor.color.accent_hover</source>
      <translation>Наведение</translation>
    </message>
    <message>
      <source>theme_editor.color.background</source>
      <translation>Основной фон</translation>
    </message>
    <message>
      <source>theme_editor.color.border</source>
      <translation>Границы</translation>
    </message>
    <message>
      <source>theme_editor.color.button_background</source>
      <translation>Цвет кнопок</translation>
    </message>
    <message>
      <source>theme_editor.color.button_text</source>
      <translation>Текст кнопок</translation>
    </message>
    <message>
      <source>theme_editor.color.card_background</source>
      <translation>Фон карточек</translation>
    </message>
    <message>
      <source>theme_editor.color.disabled</source>
      <translation>Неактивные элементы</translation>
    </message>
    <message>
      <source>theme_editor.color.error</source>
      <translation>Ошибка</translation>
    </message>
    <message>
      <source>theme_editor.color.focus</source>
      <translation>Фокус</translation>
    </message>
    <message>
      <source>theme_editor.color.on_accent</source>
      <translation>Текст акцентных кнопок</translation>
    </message>
    <message>
      <source>theme_editor.color.secondary_background</source>
      <translation>Дополнительный фон</translation>
    </message>
    <message>
      <source>theme_editor.color.success</source>
      <translation>Успех</translation>
    </message>
    <message>
      <source>theme_editor.color.text_primary</source>
      <translation>Основной текст</translation>
    </message>
    <message>
      <source>theme_editor.color.text_secondary</source>
      <translation>Вторичный текст</translation>
    </message>
    <message>
      <source>theme_editor.color.warning</source>
      <translation>Предупреждение</translation>
    </message>
    <message>
      <source>theme_editor.contrast.ok</source>
      <translation>Проверка контраста: основные сочетания соответствуют ориентиру 4,5:1.</translation>
    </message>
    <message numerus="yes">
      <source>theme_editor.contrast.warning</source>
      <translation>
        <numerusform>Проверка контраста: {count} сочетаний ниже 4,5:1. При применении потребуется подтверждение.</numerusform>
        <numerusform>Проверка контраста: {count} сочетаний ниже 4,5:1. При применении потребуется подтверждение.</numerusform>
        <numerusform>Проверка контраста: {count} сочетаний ниже 4,5:1. При применении потребуется подтверждение.</numerusform>
      </translation>
    </message>
    <message>
      <source>theme_editor.create_copy</source>
      <translation>Создать копию</translation>
    </message>
    <message>
      <source>theme_editor.create_from</source>
      <translation>Создать на основе</translation>
    </message>
    <message>
      <source>theme_editor.editing_mode</source>
      <translation>Редактируемый режим</translation>
    </message>
    <message>
      <source>theme_editor.group.service_states</source>
      <translation>Служебные состояния</translation>
    </message>
    <message>
      <source>theme_editor.group.surfaces</source>
      <translation>Поверхности</translation>
    </message>
    <message>
      <source>theme_editor.group.text_controls</source>
      <translation>Текст и управление</translation>
    </message>
    <message>
      <source>theme_editor.group.timer_states</source>
      <translation>Состояния таймера</translation>
    </message>
    <message>
      <source>theme_editor.low_contrast.confirmation</source>
      <translation>Некоторые сочетания ниже 4,5:1:

{details}

Сохранить осознанно?</translation>
    </message>
    <message>
      <source>theme_editor.low_contrast.title</source>
      <translation>Низкий контраст</translation>
    </message>
    <message>
      <source>theme_editor.reset.confirmation</source>
      <translation>Сбросить оба режима к безопасной теме Comet?</translation>
    </message>
    <message>
      <source>theme_editor.reset.title</source>
      <translation>Сброс темы</translation>
    </message>
    <message>
      <source>theme_editor.reset_all</source>
      <translation>Сбросить всю тему</translation>
    </message>
    <message>
      <source>theme_editor.reset_mode</source>
      <translation>Сбросить текущий режим</translation>
    </message>
    <message>
      <source>theme_editor.subtitle</source>
      <translation>Редактируйте светлый и тёмный режимы независимо.</translation>
    </message>
    <message>
      <source>theme_editor.title</source>
      <translation>Пользовательская тема</translation>
    </message>
    <message>
      <source>timer.mode.long_break</source>
      <translation>Длинный отдых</translation>
    </message>
    <message>
      <source>timer.mode.long_break_overrun</source>
      <translation>Длинный отдых сверх нормы</translation>
    </message>
    <message>
      <source>timer.mode.overwork</source>
      <translation>Переработка</translation>
    </message>
    <message>
      <source>timer.mode.short_break</source>
      <translation>Короткий отдых</translation>
    </message>
    <message>
      <source>timer.mode.short_break_overrun</source>
      <translation>Короткий отдых сверх нормы</translation>
    </message>
    <message>
      <source>timer.mode.work</source>
      <translation>Работа</translation>
    </message>
    <message>
      <source>timer.overrun.waiting_status</source>
      <translation>Период завершён — превышение считается до продолжения</translation>
    </message>
    <message>
      <source>timer.page.subtitle</source>
      <translation>Один таймер для главного окна, уведомления и виджета.</translation>
    </message>
    <message>
      <source>timer.page.title</source>
      <translation>Фокус-сессия</translation>
    </message>
    <message>
      <source>timer.status.accessible_name</source>
      <translation>Состояние таймера</translation>
    </message>
    <message>
      <source>timer.status.overrun</source>
      <translation>Превышение учитывается</translation>
    </message>
    <message>
      <source>timer.status.paused</source>
      <translation>Таймер на паузе</translation>
    </message>
    <message>
      <source>timer.status.running</source>
      <translation>Таймер запущен</translation>
    </message>
    <message>
      <source>timer.status.stopped</source>
      <translation>Таймер остановлен</translation>
    </message>
    <message>
      <source>timer.widget.show</source>
      <translation>Отображать виджет</translation>
    </message>
    <message>
      <source>timer.widget.show.description</source>
      <translation>Положение, размер, тип и прозрачность сохраняются отдельно.</translation>
    </message>
    <message>
      <source>toggle.accessible_description</source>
      <translation>ВКЛ — включено, ВЫКЛ — выключено</translation>
    </message>
    <message>
      <source>toggle.accessible_name</source>
      <translation>Переключатель</translation>
    </message>
    <message>
      <source>toggle.off</source>
      <translation>ВЫКЛ</translation>
    </message>
    <message>
      <source>toggle.on</source>
      <translation>ВКЛ</translation>
    </message>
    <message>
      <source>toggle.state.off</source>
      <translation>ВЫКЛ, выключено</translation>
    </message>
    <message>
      <source>toggle.state.on</source>
      <translation>ВКЛ, включено</translation>
    </message>
    <message>
      <source>tray.exit</source>
      <translation>Выход</translation>
    </message>
    <message>
      <source>tray.hide</source>
      <translation>Скрыть окно</translation>
    </message>
    <message>
      <source>tray.reset</source>
      <translation>Сброс</translation>
    </message>
    <message>
      <source>tray.show</source>
      <translation>Показать окно</translation>
    </message>
    <message>
      <source>tray.start_pause</source>
      <translation>Старт / Пауза</translation>
    </message>
    <message numerus="yes">
      <source>widget.completed_work_periods</source>
      <translation>
        <numerusform>Завершено рабочих периодов: {count}</numerusform>
        <numerusform>Завершено рабочих периодов: {count}</numerusform>
        <numerusform>Завершено рабочих периодов: {count}</numerusform>
      </translation>
    </message>
    <message>
      <source>widget.size.custom</source>
      <translation>Пользовательский</translation>
    </message>
    <message>
      <source>widget.size.large</source>
      <translation>Большой</translation>
    </message>
    <message>
      <source>widget.size.medium</source>
      <translation>Средний</translation>
    </message>
    <message>
      <source>widget.size.small</source>
      <translation>Маленький</translation>
    </message>
    <message>
      <source>widget.type.compact</source>
      <translation>Компактный</translation>
    </message>
    <message>
      <source>widget.type.compact.description</source>
      <translation>Классическая компактная карточка с основной кнопкой.</translation>
    </message>
    <message>
      <source>widget.type.expanded</source>
      <translation>Расширенный</translation>
    </message>
    <message>
      <source>widget.type.expanded.description</source>
      <translation>Цикл и полный набор основных команд таймера.</translation>
    </message>
    <message>
      <source>widget.type.micro</source>
      <translation>Микро</translation>
    </message>
    <message>
      <source>widget.type.micro.description</source>
      <translation>Самое маленькое окно: обычно только время.</translation>
    </message>
    <message>
      <source>widget.type.minimal</source>
      <translation>Минималистичный</translation>
    </message>
    <message>
      <source>widget.type.minimal.description</source>
      <translation>Крупное время, название состояния и минимум деталей.</translation>
    </message>
    <message>
      <source>widget.type.ring</source>
      <translation>Кольцо</translation>
    </message>
    <message>
      <source>widget.type.ring.description</source>
      <translation>Время внутри кольцевого индикатора периода.</translation>
    </message>
    <message>
      <source>widget.type.row</source>
      <translation>Строка</translation>
    </message>
    <message>
      <source>widget.type.row.description</source>
      <translation>Горизонтальная строка для края экрана.</translation>
    </message>
    <message>
      <source>widget.type.scoreboard</source>
      <translation>Табло</translation>
    </message>
    <message>
      <source>widget.type.scoreboard.description</source>
      <translation>Крупные моноширинные цифры в стиле спокойного табло.</translation>
    </message>
    <message>
      <source>widget.window_title</source>
      <translation>Виджет Pomodoro</translation>
    </message>
  </context>
  <context>
    <name>QPlatformTheme</name>
    <message>
      <source>OK</source>
      <translation>OK</translation>
    </message>
    <message>
      <source>Save</source>
      <translation>Сохранить</translation>
    </message>
    <message>
      <source>Save All</source>
      <translation>Сохранить всё</translation>
    </message>
    <message>
      <source>Open</source>
      <translation>Открыть</translation>
    </message>
    <message>
      <source>&amp;Yes</source>
      <translation>&amp;Да</translation>
    </message>
    <message>
      <source>Yes to &amp;All</source>
      <translation>Да для &amp;всех</translation>
    </message>
    <message>
      <source>&amp;No</source>
      <translation>&amp;Нет</translation>
    </message>
    <message>
      <source>N&amp;o to All</source>
      <translation>Нет для в&amp;сех</translation>
    </message>
    <message>
      <source>Abort</source>
      <translation>Прервать</translation>
    </message>
    <message>
      <source>Retry</source>
      <translation>Повторить</translation>
    </message>
    <message>
      <source>Ignore</source>
      <translation>Игнорировать</translation>
    </message>
    <message>
      <source>Close</source>
      <translation>Закрыть</translation>
    </message>
    <message>
      <source>Cancel</source>
      <translation>Отмена</translation>
    </message>
    <message>
      <source>Discard</source>
      <translation>Не сохранять</translation>
    </message>
    <message>
      <source>Help</source>
      <translation>Справка</translation>
    </message>
    <message>
      <source>Apply</source>
      <translation>Применить</translation>
    </message>
    <message>
      <source>Reset</source>
      <translation>Сбросить</translation>
    </message>
    <message>
      <source>Restore Defaults</source>
      <translation>Восстановить значения по умолчанию</translation>
    </message>
  </context>
</TS>
