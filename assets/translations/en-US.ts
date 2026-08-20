<?xml version='1.0' encoding='utf-8'?>
<TS version="2.1" language="en_US">
  <context>
    <name>PomodoroTimer</name>
    <message>
      <source>action.apply</source>
      <translation>Apply</translation>
    </message>
    <message>
      <source>action.cancel</source>
      <translation>Cancel</translation>
    </message>
    <message>
      <source>action.choose</source>
      <translation>Choose</translation>
    </message>
    <message>
      <source>action.close</source>
      <translation>Close</translation>
    </message>
    <message>
      <source>action.continue</source>
      <translation>Continue</translation>
    </message>
    <message>
      <source>action.continue_next_period</source>
      <translation>Continue and start the next period</translation>
    </message>
    <message>
      <source>action.open</source>
      <translation>Open</translation>
    </message>
    <message>
      <source>action.open_main_window</source>
      <translation>Open main window</translation>
    </message>
    <message>
      <source>action.pause</source>
      <translation>Pause</translation>
    </message>
    <message>
      <source>action.preview</source>
      <translation>Preview</translation>
    </message>
    <message>
      <source>action.refresh</source>
      <translation>Refresh</translation>
    </message>
    <message>
      <source>action.reset</source>
      <translation>Reset</translation>
    </message>
    <message>
      <source>action.show</source>
      <translation>Show</translation>
    </message>
    <message>
      <source>action.skip</source>
      <translation>Skip</translation>
    </message>
    <message>
      <source>action.start</source>
      <translation>Start</translation>
    </message>
    <message>
      <source>dialog.color.choose</source>
      <translation>Choose a color</translation>
    </message>
    <message>
      <source>dialog.color.invalid_hex</source>
      <translation>Correct the values: #RRGGBB format is required.</translation>
    </message>
    <message>
      <source>dialog.color.title</source>
      <translation>Color</translation>
    </message>
    <message>
      <source>error.autostart.python_unavailable</source>
      <translation>Autostart is available only in the packaged EXE. It cannot be enabled when running from Python.</translation>
    </message>
    <message>
      <source>error.data.portable_fallback</source>
      <translation>Data could not be written next to the application. Settings will temporarily be stored in your user folder. For portable mode, move the application to a writable folder.</translation>
    </message>
    <message>
      <source>error.data.portable_title</source>
      <translation>Portable mode</translation>
    </message>
    <message>
      <source>error.data.unavailable</source>
      <translation>The application settings folder could not be created.</translation>
    </message>
    <message>
      <source>error.widget.hide</source>
      <translation>Could not hide the widget: {error}</translation>
    </message>
    <message>
      <source>error.widget.show</source>
      <translation>Could not show the widget: {error}</translation>
    </message>
    <message>
      <source>error.widget.state_mismatch</source>
      <translation>the window did not enter the requested state</translation>
    </message>
    <message>
      <source>help.content</source>
      <translation># Pomodoro Timer

## Quick start

Choose durations in Settings, open Timer, and select **Start**. Use the switch at the top to change between light and dark mode instantly. Binary settings use switches; regular actions remain buttons.

## Timer controls

- **Start** begins the current period.
- **Pause / Continue** pauses and resumes a regular period.
- **Skip period** moves to the next mode without recording the duration.
- **Reset** returns to stopped Work and records a reset in Statistics.
- **Continue and start the next period** appears for a manual transition, records the overrun once, and starts the next period immediately.

With automatic transitions, the next period starts immediately and no overrun is counted. With manual transitions, the application shows **Overtime**, **Short break overrun**, or **Long break overrun**, and time prefixed with `+`. Start, pause, skip, and reset remain disabled during an overrun so no time is lost.

## Appearance and accessibility

Comet, Aurora, Warm, and Custom themes each have light and dark modes. The custom-theme editor stores the modes separately, validates `#RRGGBB`, and warns when contrast is below 4.5:1. Cancel restores saved colors; reset restores the safe Comet palette.

The Qt Widgets interface follows Windows/Qt scaling and supports keyboard focus. Switches work with the mouse, `Space`, or `Enter`; their state is conveyed by position, color, and ON/OFF text. Command buttons also use `Space` or `Enter`, provide brief press feedback, and show a high-contrast outline only during keyboard navigation. When motion is disabled, an immediate color change replaces animation.

On first launch, the main window uses about 80% of the available screen. It remembers its size and position and returns to a visible monitor after resolution changes. At medium and narrow widths, navigation collapses to icons with tooltips, button groups wrap, and Settings scrolls without clipping pinned actions.

Dark mode styles the viewport and tray menu and requests a dark native title bar when Windows DWM supports it. The original tomato-and-timer icon is used for windows, the taskbar, tray, and packaged EXE.

## Overrun indication

Choose pulse, enlarged digits, signal beacons, an accent border, a wave indicator, or no animation. Color changes, scope, speed, intensity, and three colors are configured independently. Preview does not modify the timer, statistics, notifications, or opacity.

The main window and widget receive the same effect frame. Continue or exit restores regular colors and sizes immediately. With motion disabled, the static accessible indication, state name, and `+` sign remain.

## Floating widget

The **Show widget** switch on the Timer page shows and hides the same window. Seven layouts are available: Minimal, Compact, Expanded, Micro, Row, Ring, and Scoreboard. All use the same `TimerEngine`.

Type, size, and position are stored separately for each layout. Manual resizing creates a custom size. Opacity ranges from 5 to 100%; during an overrun, the widget can temporarily become fully opaque and then return to the exact saved value.

In Expanded view, a narrow action bar wraps whole actions. Continue is never abbreviated. At minimum width only Open may become an icon with a tooltip; the remaining actions wrap to the next row.

## Notifications, statistics, and tray

An automatic-transition notification can be closed. A manual notification includes Continue; its close button dismisses only the window and does not lose overrun time. The same command remains available in the main window and widget.

Statistics separates regular work, regular breaks, and three overrun types for today and all time. Closing the main window can minimize the application to the tray. A normal full exit saves accumulated overrun time.

One application instance runs per Windows user. A second launch shows a system message without creating another interface.
</translation>
    </message>
    <message>
      <source>help.subtitle</source>
      <translation>Features and safe application behavior.</translation>
    </message>
    <message>
      <source>help.title</source>
      <translation>Help</translation>
    </message>
    <message>
      <source>main.brand_subtitle</source>
      <translation>A calm work rhythm</translation>
    </message>
    <message>
      <source>nav.help</source>
      <translation>Help</translation>
    </message>
    <message>
      <source>nav.settings</source>
      <translation>Settings</translation>
    </message>
    <message>
      <source>nav.statistics</source>
      <translation>Statistics</translation>
    </message>
    <message>
      <source>nav.timer</source>
      <translation>Timer</translation>
    </message>
    <message>
      <source>notification.auto_transition</source>
      <translation>{completed}

The next period has already started: {next_period}.</translation>
    </message>
    <message>
      <source>notification.completed.long_break</source>
      <translation>Long break completed.</translation>
    </message>
    <message>
      <source>notification.completed.short_break</source>
      <translation>Short break completed.</translation>
    </message>
    <message>
      <source>notification.completed.work</source>
      <translation>Work period completed.</translation>
    </message>
    <message>
      <source>notification.default.long_break_end</source>
      <translation>Long break completed. Time to start a new work period.</translation>
    </message>
    <message>
      <source>notification.default.short_break_end</source>
      <translation>Short break completed. Time to return to work.</translation>
    </message>
    <message>
      <source>notification.default.work_end</source>
      <translation>Work period completed. Time for a break.</translation>
    </message>
    <message>
      <source>notification.manual_transition</source>
      <translation>{completed}

Select Continue to start {next_period}.</translation>
    </message>
    <message>
      <source>overrun.effect.beacons</source>
      <translation>Signal beacons</translation>
    </message>
    <message>
      <source>overrun.effect.border</source>
      <translation>Accent border</translation>
    </message>
    <message>
      <source>overrun.effect.none</source>
      <translation>No animation</translation>
    </message>
    <message>
      <source>overrun.effect.pulse</source>
      <translation>Pulse</translation>
    </message>
    <message>
      <source>overrun.effect.scale</source>
      <translation>Enlarge digits</translation>
    </message>
    <message>
      <source>overrun.effect.wave</source>
      <translation>Wave indicator</translation>
    </message>
    <message>
      <source>overrun.intensity.medium</source>
      <translation>Medium</translation>
    </message>
    <message>
      <source>overrun.intensity.strong</source>
      <translation>Strong</translation>
    </message>
    <message>
      <source>overrun.intensity.weak</source>
      <translation>Subtle</translation>
    </message>
    <message>
      <source>overrun.scope.both</source>
      <translation>Digits and timer card</translation>
    </message>
    <message>
      <source>overrun.scope.card</source>
      <translation>Timer card</translation>
    </message>
    <message>
      <source>overrun.scope.digits</source>
      <translation>Timer digits only</translation>
    </message>
    <message>
      <source>overrun.speed.fast</source>
      <translation>Fast</translation>
    </message>
    <message>
      <source>overrun.speed.normal</source>
      <translation>Normal</translation>
    </message>
    <message>
      <source>overrun.speed.slow</source>
      <translation>Slow</translation>
    </message>
    <message>
      <source>settings.appearance.dark_mode</source>
      <translation>Dark mode</translation>
    </message>
    <message>
      <source>settings.appearance.dark_mode.description</source>
      <translation>OFF — light mode, ON — dark mode.</translation>
    </message>
    <message>
      <source>settings.appearance.edit_colors</source>
      <translation>Customize colors</translation>
    </message>
    <message>
      <source>settings.appearance.editor_unavailable</source>
      <translation>The editor is not available in this window.</translation>
    </message>
    <message>
      <source>settings.appearance.language</source>
      <translation>Interface language</translation>
    </message>
    <message>
      <source>settings.appearance.subtitle</source>
      <translation>Complete palettes update every open window without a restart.</translation>
    </message>
    <message>
      <source>settings.appearance.title</source>
      <translation>Appearance</translation>
    </message>
    <message>
      <source>settings.logic.long_break_interval</source>
      <translation>Work periods before a long break</translation>
    </message>
    <message>
      <source>settings.logic.subtitle</source>
      <translation>The order of work, short breaks, and long breaks.</translation>
    </message>
    <message>
      <source>settings.logic.title</source>
      <translation>Timer behavior</translation>
    </message>
    <message>
      <source>settings.logic.use_long_break</source>
      <translation>Use long breaks</translation>
    </message>
    <message>
      <source>settings.logic.use_long_break.description</source>
      <translation>After the specified number of work periods.</translation>
    </message>
    <message>
      <source>settings.notifications.auto_transition</source>
      <translation>Automatic transition</translation>
    </message>
    <message>
      <source>settings.notifications.auto_transition.description</source>
      <translation>ON — the next period starts immediately; OFF — overrun time is counted.</translation>
    </message>
    <message>
      <source>settings.notifications.enabled</source>
      <translation>Notifications</translation>
    </message>
    <message>
      <source>settings.notifications.long_break_end</source>
      <translation>Long break completion</translation>
    </message>
    <message>
      <source>settings.notifications.short_break_end</source>
      <translation>Short break completion</translation>
    </message>
    <message>
      <source>settings.notifications.sound</source>
      <translation>Notification sound</translation>
    </message>
    <message>
      <source>settings.notifications.subtitle</source>
      <translation>A manual transition can always be completed from the main window or widget.</translation>
    </message>
    <message>
      <source>settings.notifications.title</source>
      <translation>Notifications</translation>
    </message>
    <message>
      <source>settings.notifications.work_end</source>
      <translation>Work completion</translation>
    </message>
    <message>
      <source>settings.overrun.allow_motion</source>
      <translation>Allow effect motion</translation>
    </message>
    <message>
      <source>settings.overrun.change_color</source>
      <translation>Change timer color</translation>
    </message>
    <message>
      <source>settings.overrun.color_dialog</source>
      <translation>Overrun color</translation>
    </message>
    <message>
      <source>settings.overrun.effect</source>
      <translation>Primary effect</translation>
    </message>
    <message>
      <source>settings.overrun.intensity</source>
      <translation>Intensity</translation>
    </message>
    <message>
      <source>settings.overrun.invalid_colors</source>
      <translation>Invalid colors were replaced with values from the active theme.</translation>
    </message>
    <message>
      <source>settings.overrun.opaque_widget</source>
      <translation>Make the widget opaque during overrun</translation>
    </message>
    <message>
      <source>settings.overrun.scope</source>
      <translation>Color change area</translation>
    </message>
    <message>
      <source>settings.overrun.separate_colors</source>
      <translation>Separate colors</translation>
    </message>
    <message>
      <source>settings.overrun.speed</source>
      <translation>Speed</translation>
    </message>
    <message>
      <source>settings.overrun.subtitle</source>
      <translation>One shared frame is applied to the main window and the open widget.</translation>
    </message>
    <message>
      <source>settings.overrun.title</source>
      <translation>Overrun indication</translation>
    </message>
    <message>
      <source>settings.overrun.use_theme_color</source>
      <translation>Use theme color</translation>
    </message>
    <message>
      <source>settings.profiles.apply</source>
      <translation>Apply profile</translation>
    </message>
    <message>
      <source>settings.profiles.default_cannot_delete</source>
      <translation>The default profile cannot be deleted.</translation>
    </message>
    <message>
      <source>settings.profiles.default_name</source>
      <translation>Default</translation>
    </message>
    <message>
      <source>settings.profiles.defaults</source>
      <translation>Default settings</translation>
    </message>
    <message>
      <source>settings.profiles.delete</source>
      <translation>Delete profile</translation>
    </message>
    <message>
      <source>settings.profiles.delete_confirmation</source>
      <translation>Delete profile “{profile_name}”?</translation>
    </message>
    <message>
      <source>settings.profiles.delete_title</source>
      <translation>Delete profile</translation>
    </message>
    <message>
      <source>settings.profiles.dialog_title</source>
      <translation>Profile</translation>
    </message>
    <message>
      <source>settings.profiles.enter_name</source>
      <translation>Enter a profile name.</translation>
    </message>
    <message>
      <source>settings.profiles.name_placeholder</source>
      <translation>Profile name</translation>
    </message>
    <message>
      <source>settings.profiles.restore_personal</source>
      <translation>Restore my settings</translation>
    </message>
    <message>
      <source>settings.profiles.save</source>
      <translation>Save profile</translation>
    </message>
    <message>
      <source>settings.profiles.select_profile</source>
      <translation>Select a profile from the list.</translation>
    </message>
    <message>
      <source>settings.profiles.subtitle</source>
      <translation>Save sets of durations, appearance options, and widget settings.</translation>
    </message>
    <message>
      <source>settings.profiles.title</source>
      <translation>Profiles</translation>
    </message>
    <message>
      <source>settings.save</source>
      <translation>Save settings</translation>
    </message>
    <message>
      <source>settings.section.appearance</source>
      <translation>Appearance</translation>
    </message>
    <message>
      <source>settings.section.logic</source>
      <translation>Timer behavior</translation>
    </message>
    <message>
      <source>settings.section.notifications</source>
      <translation>Notifications</translation>
    </message>
    <message>
      <source>settings.section.overrun</source>
      <translation>Overrun</translation>
    </message>
    <message>
      <source>settings.section.profiles</source>
      <translation>Profiles</translation>
    </message>
    <message>
      <source>settings.section.time</source>
      <translation>Time</translation>
    </message>
    <message>
      <source>settings.section.tray</source>
      <translation>Tray and autostart</translation>
    </message>
    <message>
      <source>settings.section.widget</source>
      <translation>Widget</translation>
    </message>
    <message>
      <source>settings.subtitle</source>
      <translation>Theme and widget changes apply immediately; other changes apply after saving.</translation>
    </message>
    <message>
      <source>settings.time.format</source>
      <translation>Time format</translation>
    </message>
    <message>
      <source>settings.time.long_break_minutes</source>
      <translation>Long break, minutes</translation>
    </message>
    <message>
      <source>settings.time.short_break_minutes</source>
      <translation>Short break, minutes</translation>
    </message>
    <message>
      <source>settings.time.subtitle</source>
      <translation>Durations are applied safely when you save.</translation>
    </message>
    <message>
      <source>settings.time.title</source>
      <translation>Time</translation>
    </message>
    <message>
      <source>settings.time.work_minutes</source>
      <translation>Work, minutes</translation>
    </message>
    <message>
      <source>settings.title</source>
      <translation>Settings</translation>
    </message>
    <message>
      <source>settings.tray.autostart</source>
      <translation>Start with Windows</translation>
    </message>
    <message>
      <source>settings.tray.autostart_current</source>
      <translation>Autostart is enabled and points to the application's current folder.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_disabled</source>
      <translation>Autostart is disabled.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_python</source>
      <translation>Running from Python: autostart can be enabled in the EXE version.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_stale</source>
      <translation>The autostart path is outdated. Update it after moving the application.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_title</source>
      <translation>Autostart</translation>
    </message>
    <message>
      <source>settings.tray.close_to_tray</source>
      <translation>Minimize to tray when closing</translation>
    </message>
    <message>
      <source>settings.tray.minimize_on_start</source>
      <translation>Minimize the application after launch</translation>
    </message>
    <message>
      <source>settings.tray.subtitle</source>
      <translation>The system tray runs in the shared Qt GUI thread.</translation>
    </message>
    <message>
      <source>settings.tray.title</source>
      <translation>Tray and autostart</translation>
    </message>
    <message>
      <source>settings.tray.update_autostart</source>
      <translation>Update autostart path</translation>
    </message>
    <message>
      <source>settings.widget.always_on_top</source>
      <translation>Always on top</translation>
    </message>
    <message>
      <source>settings.widget.dialog_title</source>
      <translation>Widget</translation>
    </message>
    <message>
      <source>settings.widget.opacity</source>
      <translation>Widget opacity</translation>
    </message>
    <message>
      <source>settings.widget.opacity.description</source>
      <translation>Lower values make the widget more transparent. Minimum — 5%.</translation>
    </message>
    <message>
      <source>settings.widget.position_reset</source>
      <translation>The position for the current type has been reset.</translation>
    </message>
    <message>
      <source>settings.widget.reset_position</source>
      <translation>Reset position for current type</translation>
    </message>
    <message>
      <source>settings.widget.size</source>
      <translation>Size</translation>
    </message>
    <message>
      <source>settings.widget.subtitle</source>
      <translation>Visibility is controlled by the switch on the Timer page.</translation>
    </message>
    <message>
      <source>settings.widget.title</source>
      <translation>Floating widget</translation>
    </message>
    <message>
      <source>settings.widget.type</source>
      <translation>Widget type</translation>
    </message>
    <message>
      <source>startup.already_running</source>
      <translation>Pomodoro Timer is starting or is already running. Wait for the window to open or use the application that is already open.</translation>
    </message>
    <message>
      <source>startup.lock.already_running</source>
      <translation>Another application instance is already running.</translation>
    </message>
    <message>
      <source>startup.lock.create_failed</source>
      <translation>Could not create the system lock (WinError {error_code}).</translation>
    </message>
    <message>
      <source>startup.lock.release_failed</source>
      <translation>Could not release the system lock (WinError {error_code}).</translation>
    </message>
    <message>
      <source>startup.lock.secondary_close_failed</source>
      <translation>Another instance is already running, but its secondary handle could not be closed (WinError {error_code}).</translation>
    </message>
    <message>
      <source>startup.lock.unsupported</source>
      <translation>The single-instance system lock is supported only on Windows.</translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_cycles</source>
      <translation>
        <numerusform>Complete cycle</numerusform>
        <numerusform>Complete cycles</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_long_breaks</source>
      <translation>
        <numerusform>Long break</numerusform>
        <numerusform>Long breaks</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_short_breaks</source>
      <translation>
        <numerusform>Short break</numerusform>
        <numerusform>Short breaks</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_work_periods</source>
      <translation>
        <numerusform>Work period</numerusform>
        <numerusform>Work periods</numerusform>
      </translation>
    </message>
    <message>
      <source>stats.metric.long_break_overrun</source>
      <translation>Long break overrun</translation>
    </message>
    <message>
      <source>stats.metric.overwork_time</source>
      <translation>Overtime</translation>
    </message>
    <message>
      <source>stats.metric.rest_time</source>
      <translation>Break time</translation>
    </message>
    <message>
      <source>stats.metric.short_break_overrun</source>
      <translation>Short break overrun</translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.skipped_periods</source>
      <translation>
        <numerusform>Skipped period</numerusform>
        <numerusform>Skipped periods</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.timer_resets</source>
      <translation>
        <numerusform>Timer reset</numerusform>
        <numerusform>Timer resets</numerusform>
      </translation>
    </message>
    <message>
      <source>stats.metric.work_time</source>
      <translation>Work time</translation>
    </message>
    <message>
      <source>stats.period.all_time</source>
      <translation>All time</translation>
    </message>
    <message>
      <source>stats.period.today</source>
      <translation>Today</translation>
    </message>
    <message>
      <source>stats.reset.action</source>
      <translation>Reset statistics</translation>
    </message>
    <message>
      <source>stats.reset.confirmation</source>
      <translation>Are you sure you want to delete all statistics?</translation>
    </message>
    <message>
      <source>stats.reset.title</source>
      <translation>Reset statistics</translation>
    </message>
    <message>
      <source>stats.subtitle</source>
      <translation>Regular time and overruns are tracked separately.</translation>
    </message>
    <message>
      <source>stats.title</source>
      <translation>Statistics</translation>
    </message>
    <message>
      <source>theme.appearance.dark</source>
      <translation>Dark</translation>
    </message>
    <message>
      <source>theme.appearance.light</source>
      <translation>Light</translation>
    </message>
    <message>
      <source>theme.contrast.accent</source>
      <translation>Accent text / accent</translation>
    </message>
    <message>
      <source>theme.contrast.button</source>
      <translation>Button text / button</translation>
    </message>
    <message>
      <source>theme.contrast.long_break</source>
      <translation>Long break / card</translation>
    </message>
    <message>
      <source>theme.contrast.long_break_overrun</source>
      <translation>Long break overrun / card</translation>
    </message>
    <message>
      <source>theme.contrast.overwork</source>
      <translation>Overtime / card</translation>
    </message>
    <message>
      <source>theme.contrast.primary_card</source>
      <translation>Primary text / card</translation>
    </message>
    <message>
      <source>theme.contrast.secondary_card</source>
      <translation>Secondary text / card</translation>
    </message>
    <message>
      <source>theme.contrast.short_break</source>
      <translation>Short break / card</translation>
    </message>
    <message>
      <source>theme.contrast.short_break_overrun</source>
      <translation>Short break overrun / card</translation>
    </message>
    <message>
      <source>theme.contrast.work</source>
      <translation>Work / card</translation>
    </message>
    <message>
      <source>theme.description.aurora</source>
      <translation>Cool blue and violet accents</translation>
    </message>
    <message>
      <source>theme.description.comet</source>
      <translation>Calm neutral palette</translation>
    </message>
    <message>
      <source>theme.description.custom</source>
      <translation>Your independent light and dark palettes</translation>
    </message>
    <message>
      <source>theme.description.warm</source>
      <translation>Soft sandy and warm surfaces</translation>
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
      <translation>Custom</translation>
    </message>
    <message>
      <source>theme.name.warm</source>
      <translation>Warm</translation>
    </message>
    <message>
      <source>theme_editor.color.accent</source>
      <translation>Accent</translation>
    </message>
    <message>
      <source>theme_editor.color.accent_hover</source>
      <translation>Hover</translation>
    </message>
    <message>
      <source>theme_editor.color.background</source>
      <translation>Main background</translation>
    </message>
    <message>
      <source>theme_editor.color.border</source>
      <translation>Borders</translation>
    </message>
    <message>
      <source>theme_editor.color.button_background</source>
      <translation>Button color</translation>
    </message>
    <message>
      <source>theme_editor.color.button_text</source>
      <translation>Button text</translation>
    </message>
    <message>
      <source>theme_editor.color.card_background</source>
      <translation>Card background</translation>
    </message>
    <message>
      <source>theme_editor.color.disabled</source>
      <translation>Disabled elements</translation>
    </message>
    <message>
      <source>theme_editor.color.error</source>
      <translation>Error</translation>
    </message>
    <message>
      <source>theme_editor.color.focus</source>
      <translation>Focus</translation>
    </message>
    <message>
      <source>theme_editor.color.on_accent</source>
      <translation>Accent button text</translation>
    </message>
    <message>
      <source>theme_editor.color.secondary_background</source>
      <translation>Secondary background</translation>
    </message>
    <message>
      <source>theme_editor.color.success</source>
      <translation>Success</translation>
    </message>
    <message>
      <source>theme_editor.color.text_primary</source>
      <translation>Primary text</translation>
    </message>
    <message>
      <source>theme_editor.color.text_secondary</source>
      <translation>Secondary text</translation>
    </message>
    <message>
      <source>theme_editor.color.warning</source>
      <translation>Warning</translation>
    </message>
    <message>
      <source>theme_editor.contrast.ok</source>
      <translation>Contrast check: the main combinations meet the 4.5:1 guideline.</translation>
    </message>
    <message numerus="yes">
      <source>theme_editor.contrast.warning</source>
      <translation>
        <numerusform>Contrast check: {count} combination is below 4.5:1. Confirmation will be required when applying.</numerusform>
        <numerusform>Contrast check: {count} combinations are below 4.5:1. Confirmation will be required when applying.</numerusform>
      </translation>
    </message>
    <message>
      <source>theme_editor.create_copy</source>
      <translation>Create copy</translation>
    </message>
    <message>
      <source>theme_editor.create_from</source>
      <translation>Create from</translation>
    </message>
    <message>
      <source>theme_editor.editing_mode</source>
      <translation>Mode being edited</translation>
    </message>
    <message>
      <source>theme_editor.group.service_states</source>
      <translation>Status colors</translation>
    </message>
    <message>
      <source>theme_editor.group.surfaces</source>
      <translation>Surfaces</translation>
    </message>
    <message>
      <source>theme_editor.group.text_controls</source>
      <translation>Text and controls</translation>
    </message>
    <message>
      <source>theme_editor.group.timer_states</source>
      <translation>Timer states</translation>
    </message>
    <message>
      <source>theme_editor.low_contrast.confirmation</source>
      <translation>Some combinations are below 4.5:1:

{details}

Save anyway?</translation>
    </message>
    <message>
      <source>theme_editor.low_contrast.title</source>
      <translation>Low contrast</translation>
    </message>
    <message>
      <source>theme_editor.reset.confirmation</source>
      <translation>Reset both modes to the safe Comet theme?</translation>
    </message>
    <message>
      <source>theme_editor.reset.title</source>
      <translation>Reset theme</translation>
    </message>
    <message>
      <source>theme_editor.reset_all</source>
      <translation>Reset entire theme</translation>
    </message>
    <message>
      <source>theme_editor.reset_mode</source>
      <translation>Reset current mode</translation>
    </message>
    <message>
      <source>theme_editor.subtitle</source>
      <translation>Edit light and dark modes independently.</translation>
    </message>
    <message>
      <source>theme_editor.title</source>
      <translation>Custom theme</translation>
    </message>
    <message>
      <source>timer.mode.long_break</source>
      <translation>Long break</translation>
    </message>
    <message>
      <source>timer.mode.long_break_overrun</source>
      <translation>Long break overrun</translation>
    </message>
    <message>
      <source>timer.mode.overwork</source>
      <translation>Overtime</translation>
    </message>
    <message>
      <source>timer.mode.short_break</source>
      <translation>Short break</translation>
    </message>
    <message>
      <source>timer.mode.short_break_overrun</source>
      <translation>Short break overrun</translation>
    </message>
    <message>
      <source>timer.mode.work</source>
      <translation>Work</translation>
    </message>
    <message>
      <source>timer.overrun.waiting_status</source>
      <translation>Period completed — overrun is counted until you continue</translation>
    </message>
    <message>
      <source>timer.page.subtitle</source>
      <translation>One timer for the main window, notifications, and widget.</translation>
    </message>
    <message>
      <source>timer.page.title</source>
      <translation>Focus session</translation>
    </message>
    <message>
      <source>timer.status.accessible_name</source>
      <translation>Timer status</translation>
    </message>
    <message>
      <source>timer.status.overrun</source>
      <translation>Overrun is being tracked</translation>
    </message>
    <message>
      <source>timer.status.paused</source>
      <translation>Timer paused</translation>
    </message>
    <message>
      <source>timer.status.running</source>
      <translation>Timer running</translation>
    </message>
    <message>
      <source>timer.status.stopped</source>
      <translation>Timer stopped</translation>
    </message>
    <message>
      <source>timer.widget.show</source>
      <translation>Show widget</translation>
    </message>
    <message>
      <source>timer.widget.show.description</source>
      <translation>Position, size, type, and opacity are saved separately.</translation>
    </message>
    <message>
      <source>toggle.accessible_description</source>
      <translation>ON — enabled, OFF — disabled</translation>
    </message>
    <message>
      <source>toggle.accessible_name</source>
      <translation>Switch</translation>
    </message>
    <message>
      <source>toggle.off</source>
      <translation>OFF</translation>
    </message>
    <message>
      <source>toggle.on</source>
      <translation>ON</translation>
    </message>
    <message>
      <source>toggle.state.off</source>
      <translation>OFF, disabled</translation>
    </message>
    <message>
      <source>toggle.state.on</source>
      <translation>ON, enabled</translation>
    </message>
    <message>
      <source>tray.exit</source>
      <translation>Exit</translation>
    </message>
    <message>
      <source>tray.hide</source>
      <translation>Hide window</translation>
    </message>
    <message>
      <source>tray.reset</source>
      <translation>Reset</translation>
    </message>
    <message>
      <source>tray.show</source>
      <translation>Show window</translation>
    </message>
    <message>
      <source>tray.start_pause</source>
      <translation>Start / Pause</translation>
    </message>
    <message numerus="yes">
      <source>widget.completed_work_periods</source>
      <translation>
        <numerusform>Completed work period: {count}</numerusform>
        <numerusform>Completed work periods: {count}</numerusform>
      </translation>
    </message>
    <message>
      <source>widget.size.custom</source>
      <translation>Custom</translation>
    </message>
    <message>
      <source>widget.size.large</source>
      <translation>Large</translation>
    </message>
    <message>
      <source>widget.size.medium</source>
      <translation>Medium</translation>
    </message>
    <message>
      <source>widget.size.small</source>
      <translation>Small</translation>
    </message>
    <message>
      <source>widget.type.compact</source>
      <translation>Compact</translation>
    </message>
    <message>
      <source>widget.type.compact.description</source>
      <translation>A classic compact card with the primary action.</translation>
    </message>
    <message>
      <source>widget.type.expanded</source>
      <translation>Expanded</translation>
    </message>
    <message>
      <source>widget.type.expanded.description</source>
      <translation>Cycle information and the full set of primary timer actions.</translation>
    </message>
    <message>
      <source>widget.type.micro</source>
      <translation>Micro</translation>
    </message>
    <message>
      <source>widget.type.micro.description</source>
      <translation>The smallest window: usually just the time.</translation>
    </message>
    <message>
      <source>widget.type.minimal</source>
      <translation>Minimal</translation>
    </message>
    <message>
      <source>widget.type.minimal.description</source>
      <translation>Large time, state name, and minimal detail.</translation>
    </message>
    <message>
      <source>widget.type.ring</source>
      <translation>Ring</translation>
    </message>
    <message>
      <source>widget.type.ring.description</source>
      <translation>Time inside a circular period indicator.</translation>
    </message>
    <message>
      <source>widget.type.row</source>
      <translation>Row</translation>
    </message>
    <message>
      <source>widget.type.row.description</source>
      <translation>A horizontal row for the edge of the screen.</translation>
    </message>
    <message>
      <source>widget.type.scoreboard</source>
      <translation>Scoreboard</translation>
    </message>
    <message>
      <source>widget.type.scoreboard.description</source>
      <translation>Large monospaced digits in a calm scoreboard style.</translation>
    </message>
    <message>
      <source>widget.window_title</source>
      <translation>Pomodoro widget</translation>
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
      <translation>Save</translation>
    </message>
    <message>
      <source>Save All</source>
      <translation>Save All</translation>
    </message>
    <message>
      <source>Open</source>
      <translation>Open</translation>
    </message>
    <message>
      <source>&amp;Yes</source>
      <translation>&amp;Yes</translation>
    </message>
    <message>
      <source>Yes to &amp;All</source>
      <translation>Yes to &amp;All</translation>
    </message>
    <message>
      <source>&amp;No</source>
      <translation>&amp;No</translation>
    </message>
    <message>
      <source>N&amp;o to All</source>
      <translation>N&amp;o to All</translation>
    </message>
    <message>
      <source>Abort</source>
      <translation>Abort</translation>
    </message>
    <message>
      <source>Retry</source>
      <translation>Retry</translation>
    </message>
    <message>
      <source>Ignore</source>
      <translation>Ignore</translation>
    </message>
    <message>
      <source>Close</source>
      <translation>Close</translation>
    </message>
    <message>
      <source>Cancel</source>
      <translation>Cancel</translation>
    </message>
    <message>
      <source>Discard</source>
      <translation>Discard</translation>
    </message>
    <message>
      <source>Help</source>
      <translation>Help</translation>
    </message>
    <message>
      <source>Apply</source>
      <translation>Apply</translation>
    </message>
    <message>
      <source>Reset</source>
      <translation>Reset</translation>
    </message>
    <message>
      <source>Restore Defaults</source>
      <translation>Restore Defaults</translation>
    </message>
  </context>
</TS>
