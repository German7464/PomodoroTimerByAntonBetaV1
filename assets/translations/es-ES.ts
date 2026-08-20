<?xml version='1.0' encoding='utf-8'?>
<TS version="2.1" language="es_ES">
  <context>
    <name>PomodoroTimer</name>
    <message>
      <source>action.apply</source>
      <translation>Aplicar</translation>
    </message>
    <message>
      <source>action.cancel</source>
      <translation>Cancelar</translation>
    </message>
    <message>
      <source>action.choose</source>
      <translation>Elegir</translation>
    </message>
    <message>
      <source>action.close</source>
      <translation>Cerrar</translation>
    </message>
    <message>
      <source>action.continue</source>
      <translation>Continuar</translation>
    </message>
    <message>
      <source>action.continue_next_period</source>
      <translation>Continuar e iniciar el siguiente período</translation>
    </message>
    <message>
      <source>action.open</source>
      <translation>Abrir</translation>
    </message>
    <message>
      <source>action.open_main_window</source>
      <translation>Abrir la ventana principal</translation>
    </message>
    <message>
      <source>action.pause</source>
      <translation>Pausar</translation>
    </message>
    <message>
      <source>action.preview</source>
      <translation>Vista previa</translation>
    </message>
    <message>
      <source>action.refresh</source>
      <translation>Actualizar</translation>
    </message>
    <message>
      <source>action.reset</source>
      <translation>Restablecer</translation>
    </message>
    <message>
      <source>action.show</source>
      <translation>Mostrar</translation>
    </message>
    <message>
      <source>action.skip</source>
      <translation>Omitir</translation>
    </message>
    <message>
      <source>action.start</source>
      <translation>Iniciar</translation>
    </message>
    <message>
      <source>dialog.color.choose</source>
      <translation>Elige un color</translation>
    </message>
    <message>
      <source>dialog.color.invalid_hex</source>
      <translation>Corrige los valores: se requiere el formato #RRGGBB.</translation>
    </message>
    <message>
      <source>dialog.color.title</source>
      <translation>Color</translation>
    </message>
    <message>
      <source>error.autostart.python_unavailable</source>
      <translation>El inicio automático solo está disponible en el EXE compilado. No se puede activar al ejecutar desde Python.</translation>
    </message>
    <message>
      <source>error.data.portable_fallback</source>
      <translation>No se pudieron guardar los datos junto a la aplicación. La configuración se almacenará temporalmente en tu carpeta de usuario. Para el modo portátil, mueve la aplicación a una carpeta con permisos de escritura.</translation>
    </message>
    <message>
      <source>error.data.portable_title</source>
      <translation>Modo portátil</translation>
    </message>
    <message>
      <source>error.data.unavailable</source>
      <translation>No se pudo crear la carpeta de configuración de la aplicación.</translation>
    </message>
    <message>
      <source>error.widget.hide</source>
      <translation>No se pudo ocultar el widget: {error}</translation>
    </message>
    <message>
      <source>error.widget.show</source>
      <translation>No se pudo mostrar el widget: {error}</translation>
    </message>
    <message>
      <source>error.widget.state_mismatch</source>
      <translation>la ventana no pasó al estado solicitado</translation>
    </message>
    <message>
      <source>help.content</source>
      <translation># Pomodoro Timer

## Inicio rápido

Elige las duraciones en Configuración, abre Temporizador y pulsa **Iniciar**. El interruptor superior cambia al instante entre los modos claro y oscuro. Las opciones binarias usan interruptores; las acciones normales siguen siendo botones.

## Control del temporizador

**Iniciar** comienza el período actual. **Pausar / Continuar** detiene y reanuda un período normal. **Omitir** pasa al siguiente modo sin registrar la duración. **Restablecer** vuelve a Trabajo detenido y registra el reinicio. **Continuar e iniciar el siguiente período** aparece en una transición manual, guarda el exceso una sola vez e inicia inmediatamente el período siguiente.

Con la transición automática, el período siguiente comienza de inmediato y no se cuenta exceso. Con la transición manual se muestra Trabajo adicional, Exceso de descanso corto o Exceso de descanso largo, y el tiempo lleva el signo `+`. Durante el exceso se bloquean iniciar, pausar, omitir y restablecer para no perder tiempo.

## Apariencia y accesibilidad

Comet, Aurora, Warm y Personalizado tienen modos claro y oscuro. El editor guarda ambos por separado, valida `#RRGGBB` y avisa si el contraste es inferior a 4,5:1. Cancelar restaura los colores guardados y restablecer recupera la paleta segura Comet.

La interfaz Qt Widgets respeta el escalado de Windows/Qt y el foco de teclado. Los interruptores funcionan con ratón, `Espacio` o `Enter`; los botones de acción también admiten teclado. Si el movimiento está desactivado, una variación inmediata de color sustituye la animación.

La ventana principal ocupa cerca del 80% de la pantalla en el primer inicio, recuerda su geometría y vuelve a un monitor visible tras cambios de resolución. En anchos reducidos, la navegación pasa a iconos con ayudas, los botones se distribuyen en varias filas y Configuración se desplaza sin recortar acciones.

## Indicación de tiempo excedido

Puedes elegir pulsación, dígitos ampliados, balizas, borde de énfasis, onda o ninguna animación. El color, el área, la velocidad, la intensidad y tres colores se configuran por separado. La vista previa no modifica el temporizador, las estadísticas, las notificaciones ni la opacidad.

La ventana principal y el widget comparten el mismo fotograma. Continuar o salir restaura de inmediato los colores y tamaños normales; sin movimiento permanecen la indicación estática, el estado y el signo `+`.

## Widget flotante

**Mostrar widget** muestra y oculta la misma ventana. Hay siete diseños: Minimalista, Compacto, Ampliado, Micro, Fila, Anillo y Marcador; todos comparten un `TimerEngine`. Tipo, tamaño y posición se guardan por diseño. La opacidad va del 5 al 100% y puede pasar temporalmente al 100% durante un exceso.

En el diseño Ampliado, las acciones completas se ajustan a otra fila. Continuar nunca se abrevia; con el ancho mínimo solo Abrir puede convertirse en un icono con ayuda.

## Notificaciones, estadísticas y bandeja

Una notificación automática puede cerrarse. La manual incluye Continuar; cerrarla no pierde el exceso. La misma acción permanece en la ventana principal y el widget. Las estadísticas separan trabajo, descansos y los tres excesos para hoy y para todo el tiempo. Al salir normalmente se guarda el exceso acumulado. Solo se ejecuta una instancia por usuario de Windows.
</translation>
    </message>
    <message>
      <source>help.subtitle</source>
      <translation>Funciones y comportamiento seguro de la aplicación.</translation>
    </message>
    <message>
      <source>help.title</source>
      <translation>Ayuda</translation>
    </message>
    <message>
      <source>main.brand_subtitle</source>
      <translation>Un ritmo de trabajo tranquilo</translation>
    </message>
    <message>
      <source>nav.help</source>
      <translation>Ayuda</translation>
    </message>
    <message>
      <source>nav.settings</source>
      <translation>Configuración</translation>
    </message>
    <message>
      <source>nav.statistics</source>
      <translation>Estadísticas</translation>
    </message>
    <message>
      <source>nav.timer</source>
      <translation>Temporizador</translation>
    </message>
    <message>
      <source>notification.auto_transition</source>
      <translation>{completed}

El siguiente período ya ha comenzado: {next_period}.</translation>
    </message>
    <message>
      <source>notification.completed.long_break</source>
      <translation>Descanso largo completado.</translation>
    </message>
    <message>
      <source>notification.completed.short_break</source>
      <translation>Descanso corto completado.</translation>
    </message>
    <message>
      <source>notification.completed.work</source>
      <translation>Período de trabajo completado.</translation>
    </message>
    <message>
      <source>notification.default.long_break_end</source>
      <translation>Descanso largo completado. Es hora de iniciar un nuevo período de trabajo.</translation>
    </message>
    <message>
      <source>notification.default.short_break_end</source>
      <translation>Descanso corto completado. Es hora de volver al trabajo.</translation>
    </message>
    <message>
      <source>notification.default.work_end</source>
      <translation>Período de trabajo completado. Es hora de descansar.</translation>
    </message>
    <message>
      <source>notification.manual_transition</source>
      <translation>{completed}

Pulsa Continuar para iniciar {next_period}.</translation>
    </message>
    <message>
      <source>overrun.effect.beacons</source>
      <translation>Balizas de señal</translation>
    </message>
    <message>
      <source>overrun.effect.border</source>
      <translation>Borde de énfasis</translation>
    </message>
    <message>
      <source>overrun.effect.none</source>
      <translation>Sin animación</translation>
    </message>
    <message>
      <source>overrun.effect.pulse</source>
      <translation>Pulsación</translation>
    </message>
    <message>
      <source>overrun.effect.scale</source>
      <translation>Ampliar dígitos</translation>
    </message>
    <message>
      <source>overrun.effect.wave</source>
      <translation>Indicador de onda</translation>
    </message>
    <message>
      <source>overrun.intensity.medium</source>
      <translation>Media</translation>
    </message>
    <message>
      <source>overrun.intensity.strong</source>
      <translation>Alta</translation>
    </message>
    <message>
      <source>overrun.intensity.weak</source>
      <translation>Baja</translation>
    </message>
    <message>
      <source>overrun.scope.both</source>
      <translation>Dígitos y tarjeta</translation>
    </message>
    <message>
      <source>overrun.scope.card</source>
      <translation>Tarjeta del temporizador</translation>
    </message>
    <message>
      <source>overrun.scope.digits</source>
      <translation>Solo los dígitos</translation>
    </message>
    <message>
      <source>overrun.speed.fast</source>
      <translation>Rápida</translation>
    </message>
    <message>
      <source>overrun.speed.normal</source>
      <translation>Normal</translation>
    </message>
    <message>
      <source>overrun.speed.slow</source>
      <translation>Lenta</translation>
    </message>
    <message>
      <source>settings.appearance.dark_mode</source>
      <translation>Modo oscuro</translation>
    </message>
    <message>
      <source>settings.appearance.dark_mode.description</source>
      <translation>DESACTIVADO: modo claro; ACTIVADO: modo oscuro.</translation>
    </message>
    <message>
      <source>settings.appearance.edit_colors</source>
      <translation>Personalizar colores</translation>
    </message>
    <message>
      <source>settings.appearance.editor_unavailable</source>
      <translation>El editor no está disponible en esta ventana.</translation>
    </message>
    <message>
      <source>settings.appearance.language</source>
      <translation>Idioma de la interfaz</translation>
    </message>
    <message>
      <source>settings.appearance.subtitle</source>
      <translation>Las paletas completas actualizan todas las ventanas abiertas sin reiniciar.</translation>
    </message>
    <message>
      <source>settings.appearance.title</source>
      <translation>Apariencia</translation>
    </message>
    <message>
      <source>settings.logic.long_break_interval</source>
      <translation>Períodos de trabajo antes del descanso largo</translation>
    </message>
    <message>
      <source>settings.logic.subtitle</source>
      <translation>Orden del trabajo y los descansos corto y largo.</translation>
    </message>
    <message>
      <source>settings.logic.title</source>
      <translation>Comportamiento del temporizador</translation>
    </message>
    <message>
      <source>settings.logic.use_long_break</source>
      <translation>Usar descansos largos</translation>
    </message>
    <message>
      <source>settings.logic.use_long_break.description</source>
      <translation>Después del número indicado de períodos de trabajo.</translation>
    </message>
    <message>
      <source>settings.notifications.auto_transition</source>
      <translation>Transición automática</translation>
    </message>
    <message>
      <source>settings.notifications.auto_transition.description</source>
      <translation>ACTIVADO: el siguiente período comienza de inmediato; DESACTIVADO: se cuenta el tiempo excedido.</translation>
    </message>
    <message>
      <source>settings.notifications.enabled</source>
      <translation>Notificaciones</translation>
    </message>
    <message>
      <source>settings.notifications.long_break_end</source>
      <translation>Fin del descanso largo</translation>
    </message>
    <message>
      <source>settings.notifications.short_break_end</source>
      <translation>Fin del descanso corto</translation>
    </message>
    <message>
      <source>settings.notifications.sound</source>
      <translation>Sonido de notificación</translation>
    </message>
    <message>
      <source>settings.notifications.subtitle</source>
      <translation>Una transición manual siempre puede completarse desde la ventana principal o el widget.</translation>
    </message>
    <message>
      <source>settings.notifications.title</source>
      <translation>Notificaciones</translation>
    </message>
    <message>
      <source>settings.notifications.work_end</source>
      <translation>Fin del trabajo</translation>
    </message>
    <message>
      <source>settings.overrun.allow_motion</source>
      <translation>Permitir movimiento de los efectos</translation>
    </message>
    <message>
      <source>settings.overrun.change_color</source>
      <translation>Cambiar el color del temporizador</translation>
    </message>
    <message>
      <source>settings.overrun.color_dialog</source>
      <translation>Color del tiempo excedido</translation>
    </message>
    <message>
      <source>settings.overrun.effect</source>
      <translation>Efecto principal</translation>
    </message>
    <message>
      <source>settings.overrun.intensity</source>
      <translation>Intensidad</translation>
    </message>
    <message>
      <source>settings.overrun.invalid_colors</source>
      <translation>Los colores no válidos se sustituyeron por valores del tema activo.</translation>
    </message>
    <message>
      <source>settings.overrun.opaque_widget</source>
      <translation>Hacer opaco el widget durante el tiempo excedido</translation>
    </message>
    <message>
      <source>settings.overrun.scope</source>
      <translation>Área del cambio de color</translation>
    </message>
    <message>
      <source>settings.overrun.separate_colors</source>
      <translation>Colores independientes</translation>
    </message>
    <message>
      <source>settings.overrun.speed</source>
      <translation>Velocidad</translation>
    </message>
    <message>
      <source>settings.overrun.subtitle</source>
      <translation>Se aplica un único fotograma compartido a la ventana principal y al widget abierto.</translation>
    </message>
    <message>
      <source>settings.overrun.title</source>
      <translation>Indicación de tiempo excedido</translation>
    </message>
    <message>
      <source>settings.overrun.use_theme_color</source>
      <translation>Usar color del tema</translation>
    </message>
    <message>
      <source>settings.profiles.apply</source>
      <translation>Aplicar perfil</translation>
    </message>
    <message>
      <source>settings.profiles.default_cannot_delete</source>
      <translation>No se puede eliminar el perfil predeterminado.</translation>
    </message>
    <message>
      <source>settings.profiles.default_name</source>
      <translation>Predeterminado</translation>
    </message>
    <message>
      <source>settings.profiles.defaults</source>
      <translation>Configuración predeterminada</translation>
    </message>
    <message>
      <source>settings.profiles.delete</source>
      <translation>Eliminar perfil</translation>
    </message>
    <message>
      <source>settings.profiles.delete_confirmation</source>
      <translation>¿Eliminar el perfil «{profile_name}»?</translation>
    </message>
    <message>
      <source>settings.profiles.delete_title</source>
      <translation>Eliminar perfil</translation>
    </message>
    <message>
      <source>settings.profiles.dialog_title</source>
      <translation>Perfil</translation>
    </message>
    <message>
      <source>settings.profiles.enter_name</source>
      <translation>Introduce un nombre de perfil.</translation>
    </message>
    <message>
      <source>settings.profiles.name_placeholder</source>
      <translation>Nombre del perfil</translation>
    </message>
    <message>
      <source>settings.profiles.restore_personal</source>
      <translation>Restaurar mi configuración</translation>
    </message>
    <message>
      <source>settings.profiles.save</source>
      <translation>Guardar perfil</translation>
    </message>
    <message>
      <source>settings.profiles.select_profile</source>
      <translation>Selecciona un perfil de la lista.</translation>
    </message>
    <message>
      <source>settings.profiles.subtitle</source>
      <translation>Guarda conjuntos de duraciones, apariencia y opciones del widget.</translation>
    </message>
    <message>
      <source>settings.profiles.title</source>
      <translation>Perfiles</translation>
    </message>
    <message>
      <source>settings.save</source>
      <translation>Guardar configuración</translation>
    </message>
    <message>
      <source>settings.section.appearance</source>
      <translation>Apariencia</translation>
    </message>
    <message>
      <source>settings.section.logic</source>
      <translation>Comportamiento</translation>
    </message>
    <message>
      <source>settings.section.notifications</source>
      <translation>Notificaciones</translation>
    </message>
    <message>
      <source>settings.section.overrun</source>
      <translation>Tiempo excedido</translation>
    </message>
    <message>
      <source>settings.section.profiles</source>
      <translation>Perfiles</translation>
    </message>
    <message>
      <source>settings.section.time</source>
      <translation>Tiempo</translation>
    </message>
    <message>
      <source>settings.section.tray</source>
      <translation>Bandeja e inicio automático</translation>
    </message>
    <message>
      <source>settings.section.widget</source>
      <translation>Widget</translation>
    </message>
    <message>
      <source>settings.subtitle</source>
      <translation>Los cambios de tema y widget se aplican de inmediato; los demás, al guardar.</translation>
    </message>
    <message>
      <source>settings.time.format</source>
      <translation>Formato de tiempo</translation>
    </message>
    <message>
      <source>settings.time.long_break_minutes</source>
      <translation>Descanso largo, minutos</translation>
    </message>
    <message>
      <source>settings.time.short_break_minutes</source>
      <translation>Descanso corto, minutos</translation>
    </message>
    <message>
      <source>settings.time.subtitle</source>
      <translation>Las duraciones se aplican de forma segura al guardar.</translation>
    </message>
    <message>
      <source>settings.time.title</source>
      <translation>Tiempo</translation>
    </message>
    <message>
      <source>settings.time.work_minutes</source>
      <translation>Trabajo, minutos</translation>
    </message>
    <message>
      <source>settings.title</source>
      <translation>Configuración</translation>
    </message>
    <message>
      <source>settings.tray.autostart</source>
      <translation>Iniciar con Windows</translation>
    </message>
    <message>
      <source>settings.tray.autostart_current</source>
      <translation>El inicio automático está activado y apunta a la carpeta actual de la aplicación.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_disabled</source>
      <translation>El inicio automático está desactivado.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_python</source>
      <translation>Ejecución desde Python: el inicio automático puede activarse en la versión EXE.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_stale</source>
      <translation>La ruta de inicio automático está desactualizada. Actualízala después de mover la aplicación.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_title</source>
      <translation>Inicio automático</translation>
    </message>
    <message>
      <source>settings.tray.close_to_tray</source>
      <translation>Minimizar a la bandeja al cerrar</translation>
    </message>
    <message>
      <source>settings.tray.minimize_on_start</source>
      <translation>Minimizar la aplicación después de iniciarla</translation>
    </message>
    <message>
      <source>settings.tray.subtitle</source>
      <translation>La bandeja del sistema usa el hilo gráfico compartido de Qt.</translation>
    </message>
    <message>
      <source>settings.tray.title</source>
      <translation>Bandeja e inicio automático</translation>
    </message>
    <message>
      <source>settings.tray.update_autostart</source>
      <translation>Actualizar ruta de inicio automático</translation>
    </message>
    <message>
      <source>settings.widget.always_on_top</source>
      <translation>Siempre visible</translation>
    </message>
    <message>
      <source>settings.widget.dialog_title</source>
      <translation>Widget</translation>
    </message>
    <message>
      <source>settings.widget.opacity</source>
      <translation>Opacidad del widget</translation>
    </message>
    <message>
      <source>settings.widget.opacity.description</source>
      <translation>Los valores bajos hacen el widget más transparente. Mínimo: 5%.</translation>
    </message>
    <message>
      <source>settings.widget.position_reset</source>
      <translation>Se restableció la posición del tipo actual.</translation>
    </message>
    <message>
      <source>settings.widget.reset_position</source>
      <translation>Restablecer posición del tipo actual</translation>
    </message>
    <message>
      <source>settings.widget.size</source>
      <translation>Tamaño</translation>
    </message>
    <message>
      <source>settings.widget.subtitle</source>
      <translation>La visibilidad se controla con el interruptor de la página Temporizador.</translation>
    </message>
    <message>
      <source>settings.widget.title</source>
      <translation>Widget flotante</translation>
    </message>
    <message>
      <source>settings.widget.type</source>
      <translation>Tipo de widget</translation>
    </message>
    <message>
      <source>startup.already_running</source>
      <translation>Pomodoro Timer se está iniciando o ya está en ejecución. Espera a que se abra la ventana o usa la aplicación que ya está abierta.</translation>
    </message>
    <message>
      <source>startup.lock.already_running</source>
      <translation>Ya se está ejecutando otra instancia de la aplicación.</translation>
    </message>
    <message>
      <source>startup.lock.create_failed</source>
      <translation>No se pudo crear el bloqueo del sistema (WinError {error_code}).</translation>
    </message>
    <message>
      <source>startup.lock.release_failed</source>
      <translation>No se pudo liberar el bloqueo del sistema (WinError {error_code}).</translation>
    </message>
    <message>
      <source>startup.lock.secondary_close_failed</source>
      <translation>Ya hay otra instancia en ejecución, pero no se pudo cerrar su identificador secundario (WinError {error_code}).</translation>
    </message>
    <message>
      <source>startup.lock.unsupported</source>
      <translation>El bloqueo de instancia única solo es compatible con Windows.</translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_cycles</source>
      <translation>
        <numerusform>Ciclo completo</numerusform>
        <numerusform>Ciclos completos</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_long_breaks</source>
      <translation>
        <numerusform>Descanso largo</numerusform>
        <numerusform>Descansos largos</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_short_breaks</source>
      <translation>
        <numerusform>Descanso corto</numerusform>
        <numerusform>Descansos cortos</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_work_periods</source>
      <translation>
        <numerusform>Período de trabajo</numerusform>
        <numerusform>Períodos de trabajo</numerusform>
      </translation>
    </message>
    <message>
      <source>stats.metric.long_break_overrun</source>
      <translation>Exceso de descanso largo</translation>
    </message>
    <message>
      <source>stats.metric.overwork_time</source>
      <translation>Tiempo de trabajo adicional</translation>
    </message>
    <message>
      <source>stats.metric.rest_time</source>
      <translation>Tiempo de descanso</translation>
    </message>
    <message>
      <source>stats.metric.short_break_overrun</source>
      <translation>Exceso de descanso corto</translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.skipped_periods</source>
      <translation>
        <numerusform>Período omitido</numerusform>
        <numerusform>Períodos omitidos</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.timer_resets</source>
      <translation>
        <numerusform>Reinicio del temporizador</numerusform>
        <numerusform>Reinicios del temporizador</numerusform>
      </translation>
    </message>
    <message>
      <source>stats.metric.work_time</source>
      <translation>Tiempo de trabajo</translation>
    </message>
    <message>
      <source>stats.period.all_time</source>
      <translation>Todo el tiempo</translation>
    </message>
    <message>
      <source>stats.period.today</source>
      <translation>Hoy</translation>
    </message>
    <message>
      <source>stats.reset.action</source>
      <translation>Restablecer estadísticas</translation>
    </message>
    <message>
      <source>stats.reset.confirmation</source>
      <translation>¿Seguro que quieres eliminar todas las estadísticas?</translation>
    </message>
    <message>
      <source>stats.reset.title</source>
      <translation>Restablecer estadísticas</translation>
    </message>
    <message>
      <source>stats.subtitle</source>
      <translation>El tiempo normal y los excesos se registran por separado.</translation>
    </message>
    <message>
      <source>stats.title</source>
      <translation>Estadísticas</translation>
    </message>
    <message>
      <source>theme.appearance.dark</source>
      <translation>Oscuro</translation>
    </message>
    <message>
      <source>theme.appearance.light</source>
      <translation>Claro</translation>
    </message>
    <message>
      <source>theme.contrast.accent</source>
      <translation>Texto de énfasis / énfasis</translation>
    </message>
    <message>
      <source>theme.contrast.button</source>
      <translation>Texto del botón / botón</translation>
    </message>
    <message>
      <source>theme.contrast.long_break</source>
      <translation>Descanso largo / tarjeta</translation>
    </message>
    <message>
      <source>theme.contrast.long_break_overrun</source>
      <translation>Exceso de descanso largo / tarjeta</translation>
    </message>
    <message>
      <source>theme.contrast.overwork</source>
      <translation>Trabajo adicional / tarjeta</translation>
    </message>
    <message>
      <source>theme.contrast.primary_card</source>
      <translation>Texto principal / tarjeta</translation>
    </message>
    <message>
      <source>theme.contrast.secondary_card</source>
      <translation>Texto secundario / tarjeta</translation>
    </message>
    <message>
      <source>theme.contrast.short_break</source>
      <translation>Descanso corto / tarjeta</translation>
    </message>
    <message>
      <source>theme.contrast.short_break_overrun</source>
      <translation>Exceso de descanso corto / tarjeta</translation>
    </message>
    <message>
      <source>theme.contrast.work</source>
      <translation>Trabajo / tarjeta</translation>
    </message>
    <message>
      <source>theme.description.aurora</source>
      <translation>Acentos fríos azules y violetas</translation>
    </message>
    <message>
      <source>theme.description.comet</source>
      <translation>Paleta neutra y tranquila</translation>
    </message>
    <message>
      <source>theme.description.custom</source>
      <translation>Tus paletas clara y oscura independientes</translation>
    </message>
    <message>
      <source>theme.description.warm</source>
      <translation>Superficies suaves, cálidas y arenosas</translation>
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
      <translation>Personalizado</translation>
    </message>
    <message>
      <source>theme.name.warm</source>
      <translation>Warm</translation>
    </message>
    <message>
      <source>theme_editor.color.accent</source>
      <translation>Énfasis</translation>
    </message>
    <message>
      <source>theme_editor.color.accent_hover</source>
      <translation>Al pasar el puntero</translation>
    </message>
    <message>
      <source>theme_editor.color.background</source>
      <translation>Fondo principal</translation>
    </message>
    <message>
      <source>theme_editor.color.border</source>
      <translation>Bordes</translation>
    </message>
    <message>
      <source>theme_editor.color.button_background</source>
      <translation>Color de botones</translation>
    </message>
    <message>
      <source>theme_editor.color.button_text</source>
      <translation>Texto de botones</translation>
    </message>
    <message>
      <source>theme_editor.color.card_background</source>
      <translation>Fondo de tarjetas</translation>
    </message>
    <message>
      <source>theme_editor.color.disabled</source>
      <translation>Elementos desactivados</translation>
    </message>
    <message>
      <source>theme_editor.color.error</source>
      <translation>Error</translation>
    </message>
    <message>
      <source>theme_editor.color.focus</source>
      <translation>Foco</translation>
    </message>
    <message>
      <source>theme_editor.color.on_accent</source>
      <translation>Texto de botones de énfasis</translation>
    </message>
    <message>
      <source>theme_editor.color.secondary_background</source>
      <translation>Fondo secundario</translation>
    </message>
    <message>
      <source>theme_editor.color.success</source>
      <translation>Éxito</translation>
    </message>
    <message>
      <source>theme_editor.color.text_primary</source>
      <translation>Texto principal</translation>
    </message>
    <message>
      <source>theme_editor.color.text_secondary</source>
      <translation>Texto secundario</translation>
    </message>
    <message>
      <source>theme_editor.color.warning</source>
      <translation>Advertencia</translation>
    </message>
    <message>
      <source>theme_editor.contrast.ok</source>
      <translation>Comprobación de contraste: las combinaciones principales cumplen la referencia 4,5:1.</translation>
    </message>
    <message numerus="yes">
      <source>theme_editor.contrast.warning</source>
      <translation>
        <numerusform>Comprobación de contraste: {count} combinación está por debajo de 4,5:1. Se pedirá confirmación al aplicar.</numerusform>
        <numerusform>Comprobación de contraste: {count} combinaciones están por debajo de 4,5:1. Se pedirá confirmación al aplicar.</numerusform>
      </translation>
    </message>
    <message>
      <source>theme_editor.create_copy</source>
      <translation>Crear copia</translation>
    </message>
    <message>
      <source>theme_editor.create_from</source>
      <translation>Crear a partir de</translation>
    </message>
    <message>
      <source>theme_editor.editing_mode</source>
      <translation>Modo en edición</translation>
    </message>
    <message>
      <source>theme_editor.group.service_states</source>
      <translation>Colores de estado</translation>
    </message>
    <message>
      <source>theme_editor.group.surfaces</source>
      <translation>Superficies</translation>
    </message>
    <message>
      <source>theme_editor.group.text_controls</source>
      <translation>Texto y controles</translation>
    </message>
    <message>
      <source>theme_editor.group.timer_states</source>
      <translation>Estados del temporizador</translation>
    </message>
    <message>
      <source>theme_editor.low_contrast.confirmation</source>
      <translation>Algunas combinaciones están por debajo de 4,5:1:

{details}

¿Guardar de todos modos?</translation>
    </message>
    <message>
      <source>theme_editor.low_contrast.title</source>
      <translation>Contraste bajo</translation>
    </message>
    <message>
      <source>theme_editor.reset.confirmation</source>
      <translation>¿Restablecer ambos modos al tema seguro Comet?</translation>
    </message>
    <message>
      <source>theme_editor.reset.title</source>
      <translation>Restablecer tema</translation>
    </message>
    <message>
      <source>theme_editor.reset_all</source>
      <translation>Restablecer todo el tema</translation>
    </message>
    <message>
      <source>theme_editor.reset_mode</source>
      <translation>Restablecer modo actual</translation>
    </message>
    <message>
      <source>theme_editor.subtitle</source>
      <translation>Edita los modos claro y oscuro de forma independiente.</translation>
    </message>
    <message>
      <source>theme_editor.title</source>
      <translation>Tema personalizado</translation>
    </message>
    <message>
      <source>timer.mode.long_break</source>
      <translation>Descanso largo</translation>
    </message>
    <message>
      <source>timer.mode.long_break_overrun</source>
      <translation>Exceso de descanso largo</translation>
    </message>
    <message>
      <source>timer.mode.overwork</source>
      <translation>Trabajo adicional</translation>
    </message>
    <message>
      <source>timer.mode.short_break</source>
      <translation>Descanso corto</translation>
    </message>
    <message>
      <source>timer.mode.short_break_overrun</source>
      <translation>Exceso de descanso corto</translation>
    </message>
    <message>
      <source>timer.mode.work</source>
      <translation>Trabajo</translation>
    </message>
    <message>
      <source>timer.overrun.waiting_status</source>
      <translation>Período completado: el exceso se cuenta hasta que continúes</translation>
    </message>
    <message>
      <source>timer.page.subtitle</source>
      <translation>Un temporizador para la ventana principal, las notificaciones y el widget.</translation>
    </message>
    <message>
      <source>timer.page.title</source>
      <translation>Sesión de concentración</translation>
    </message>
    <message>
      <source>timer.status.accessible_name</source>
      <translation>Estado del temporizador</translation>
    </message>
    <message>
      <source>timer.status.overrun</source>
      <translation>Se está contabilizando el tiempo adicional</translation>
    </message>
    <message>
      <source>timer.status.paused</source>
      <translation>Temporizador en pausa</translation>
    </message>
    <message>
      <source>timer.status.running</source>
      <translation>Temporizador en marcha</translation>
    </message>
    <message>
      <source>timer.status.stopped</source>
      <translation>Temporizador detenido</translation>
    </message>
    <message>
      <source>timer.widget.show</source>
      <translation>Mostrar widget</translation>
    </message>
    <message>
      <source>timer.widget.show.description</source>
      <translation>La posición, el tamaño, el tipo y la opacidad se guardan por separado.</translation>
    </message>
    <message>
      <source>toggle.accessible_description</source>
      <translation>ACTIVADO: habilitado; DESACTIVADO: deshabilitado</translation>
    </message>
    <message>
      <source>toggle.accessible_name</source>
      <translation>Interruptor</translation>
    </message>
    <message>
      <source>toggle.off</source>
      <translation>DESACT.</translation>
    </message>
    <message>
      <source>toggle.on</source>
      <translation>ACTIV.</translation>
    </message>
    <message>
      <source>toggle.state.off</source>
      <translation>DESACTIVADO, deshabilitado</translation>
    </message>
    <message>
      <source>toggle.state.on</source>
      <translation>ACTIVADO, habilitado</translation>
    </message>
    <message>
      <source>tray.exit</source>
      <translation>Salir</translation>
    </message>
    <message>
      <source>tray.hide</source>
      <translation>Ocultar ventana</translation>
    </message>
    <message>
      <source>tray.reset</source>
      <translation>Restablecer</translation>
    </message>
    <message>
      <source>tray.show</source>
      <translation>Mostrar ventana</translation>
    </message>
    <message>
      <source>tray.start_pause</source>
      <translation>Iniciar / Pausar</translation>
    </message>
    <message numerus="yes">
      <source>widget.completed_work_periods</source>
      <translation>
        <numerusform>Período de trabajo completado: {count}</numerusform>
        <numerusform>Períodos de trabajo completados: {count}</numerusform>
      </translation>
    </message>
    <message>
      <source>widget.size.custom</source>
      <translation>Personalizado</translation>
    </message>
    <message>
      <source>widget.size.large</source>
      <translation>Grande</translation>
    </message>
    <message>
      <source>widget.size.medium</source>
      <translation>Mediano</translation>
    </message>
    <message>
      <source>widget.size.small</source>
      <translation>Pequeño</translation>
    </message>
    <message>
      <source>widget.type.compact</source>
      <translation>Compacto</translation>
    </message>
    <message>
      <source>widget.type.compact.description</source>
      <translation>Una tarjeta compacta clásica con la acción principal.</translation>
    </message>
    <message>
      <source>widget.type.expanded</source>
      <translation>Ampliado</translation>
    </message>
    <message>
      <source>widget.type.expanded.description</source>
      <translation>Información del ciclo y todas las acciones principales del temporizador.</translation>
    </message>
    <message>
      <source>widget.type.micro</source>
      <translation>Micro</translation>
    </message>
    <message>
      <source>widget.type.micro.description</source>
      <translation>La ventana más pequeña: normalmente solo muestra el tiempo.</translation>
    </message>
    <message>
      <source>widget.type.minimal</source>
      <translation>Minimalista</translation>
    </message>
    <message>
      <source>widget.type.minimal.description</source>
      <translation>Tiempo grande, nombre del estado y pocos detalles.</translation>
    </message>
    <message>
      <source>widget.type.ring</source>
      <translation>Anillo</translation>
    </message>
    <message>
      <source>widget.type.ring.description</source>
      <translation>Tiempo dentro de un indicador circular del período.</translation>
    </message>
    <message>
      <source>widget.type.row</source>
      <translation>Fila</translation>
    </message>
    <message>
      <source>widget.type.row.description</source>
      <translation>Una fila horizontal para el borde de la pantalla.</translation>
    </message>
    <message>
      <source>widget.type.scoreboard</source>
      <translation>Marcador</translation>
    </message>
    <message>
      <source>widget.type.scoreboard.description</source>
      <translation>Dígitos monoespaciados grandes con un estilo de marcador discreto.</translation>
    </message>
    <message>
      <source>widget.window_title</source>
      <translation>Widget Pomodoro</translation>
    </message>
  </context>
  <context>
    <name>QPlatformTheme</name>
    <message>
      <source>OK</source>
      <translation>Aceptar</translation>
    </message>
    <message>
      <source>Save</source>
      <translation>Guardar</translation>
    </message>
    <message>
      <source>Save All</source>
      <translation>Guardar todo</translation>
    </message>
    <message>
      <source>Open</source>
      <translation>Abrir</translation>
    </message>
    <message>
      <source>&amp;Yes</source>
      <translation>&amp;Sí</translation>
    </message>
    <message>
      <source>Yes to &amp;All</source>
      <translation>Sí a &amp;todo</translation>
    </message>
    <message>
      <source>&amp;No</source>
      <translation>&amp;No</translation>
    </message>
    <message>
      <source>N&amp;o to All</source>
      <translation>No a t&amp;odo</translation>
    </message>
    <message>
      <source>Abort</source>
      <translation>Anular</translation>
    </message>
    <message>
      <source>Retry</source>
      <translation>Reintentar</translation>
    </message>
    <message>
      <source>Ignore</source>
      <translation>Ignorar</translation>
    </message>
    <message>
      <source>Close</source>
      <translation>Cerrar</translation>
    </message>
    <message>
      <source>Cancel</source>
      <translation>Cancelar</translation>
    </message>
    <message>
      <source>Discard</source>
      <translation>Descartar</translation>
    </message>
    <message>
      <source>Help</source>
      <translation>Ayuda</translation>
    </message>
    <message>
      <source>Apply</source>
      <translation>Aplicar</translation>
    </message>
    <message>
      <source>Reset</source>
      <translation>Restablecer</translation>
    </message>
    <message>
      <source>Restore Defaults</source>
      <translation>Restaurar valores predeterminados</translation>
    </message>
  </context>
</TS>
