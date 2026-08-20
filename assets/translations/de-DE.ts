<?xml version='1.0' encoding='utf-8'?>
<TS version="2.1" language="de_DE">
  <context>
    <name>PomodoroTimer</name>
    <message>
      <source>action.apply</source>
      <translation>Anwenden</translation>
    </message>
    <message>
      <source>action.cancel</source>
      <translation>Abbrechen</translation>
    </message>
    <message>
      <source>action.choose</source>
      <translation>Auswählen</translation>
    </message>
    <message>
      <source>action.close</source>
      <translation>Schließen</translation>
    </message>
    <message>
      <source>action.continue</source>
      <translation>Fortsetzen</translation>
    </message>
    <message>
      <source>action.continue_next_period</source>
      <translation>Fortsetzen und nächste Phase starten</translation>
    </message>
    <message>
      <source>action.open</source>
      <translation>Öffnen</translation>
    </message>
    <message>
      <source>action.open_main_window</source>
      <translation>Hauptfenster öffnen</translation>
    </message>
    <message>
      <source>action.pause</source>
      <translation>Pause</translation>
    </message>
    <message>
      <source>action.preview</source>
      <translation>Vorschau</translation>
    </message>
    <message>
      <source>action.refresh</source>
      <translation>Aktualisieren</translation>
    </message>
    <message>
      <source>action.reset</source>
      <translation>Zurücksetzen</translation>
    </message>
    <message>
      <source>action.show</source>
      <translation>Zeigen</translation>
    </message>
    <message>
      <source>action.skip</source>
      <translation>Überspringen</translation>
    </message>
    <message>
      <source>action.start</source>
      <translation>Starten</translation>
    </message>
    <message>
      <source>dialog.color.choose</source>
      <translation>Wählen Sie eine Farbe</translation>
    </message>
    <message>
      <source>dialog.color.invalid_hex</source>
      <translation>Korrigieren Sie die Werte: Das Format #RRGGBB ist erforderlich.</translation>
    </message>
    <message>
      <source>dialog.color.title</source>
      <translation>Farbe</translation>
    </message>
    <message>
      <source>error.autostart.python_unavailable</source>
      <translation>Autostart ist nur in der gepackten EXE-Datei verfügbar. Es kann nicht aktiviert werden, wenn es von Python aus ausgeführt wird.</translation>
    </message>
    <message>
      <source>error.data.portable_fallback</source>
      <translation>Es konnten keine Daten neben die Anwendung geschrieben werden. Die Einstellungen werden vorübergehend in Ihrem Benutzerordner gespeichert. Verschieben Sie die Anwendung im tragbaren Modus in einen beschreibbaren Ordner.</translation>
    </message>
    <message>
      <source>error.data.portable_title</source>
      <translation>Tragbarer Modus</translation>
    </message>
    <message>
      <source>error.data.unavailable</source>
      <translation>Der Anwendungseinstellungsordner konnte nicht erstellt werden.</translation>
    </message>
    <message>
      <source>error.widget.hide</source>
      <translation>Das Widget konnte nicht ausgeblendet werden: {error}</translation>
    </message>
    <message>
      <source>error.widget.show</source>
      <translation>Das Widget konnte nicht angezeigt werden: {error}</translation>
    </message>
    <message>
      <source>error.widget.state_mismatch</source>
      <translation>Das Fenster hat nicht den angeforderten Zustand erreicht</translation>
    </message>
    <message>
      <source>help.content</source>
      <translation># Pomodoro-Timer

## Schnellstart

Wählen Sie die Dauer in den Einstellungen aus, öffnen Sie den Timer und wählen Sie **Start**. Mit dem Schalter oben können Sie sofort zwischen Hell- und Dunkelmodus wechseln. Binäre Einstellungen verwenden Schalter; Normale Aktionen bleiben Schaltflächen.

## Timer-Steuerung

- **Start** beginnt mit der aktuellen Periode.
- **Pause/Fortfahren** pausiert und setzt einen regelmäßigen Zeitraum fort.
- **Zeitraum überspringen** wechselt zum nächsten Modus, ohne die Dauer aufzuzeichnen.
- **Reset** kehrt zur gestoppten Arbeit zurück und zeichnet einen Reset in der Statistik auf.
- **Fortfahren und die nächste Periode starten** erscheint bei einem manuellen Übergang, zeichnet die Überschreitung einmal auf und startet sofort die nächste Periode.

Bei automatischen Übergängen beginnt die nächste Periode sofort und es werden keine Überschreitungen gezählt. Bei manuellen Übergängen zeigt die Anwendung **Überlastung**, **Überschreitung einer kurzen Pause** oder **Überschreitung einer langen Pause** und eine Zeit mit dem Präfix „+“ an. Start, Pause, Überspringen und Zurücksetzen bleiben während eines Überlaufs deaktiviert, sodass keine Zeit verloren geht.

## Aussehen und Zugänglichkeit

Die Themen „Comet“, „Aurora“, „Warm“ und „Benutzerdefiniert“ verfügen jeweils über helle und dunkle Modi. Der benutzerdefinierte Theme-Editor speichert die Modi separat, validiert „#RRGGBB“ und warnt, wenn der Kontrast unter 4,5:1 liegt. Abbrechen stellt gespeicherte Farben wieder her; Durch Zurücksetzen wird die sichere Comet-Palette wiederhergestellt.

Die Qt Widgets-Schnittstelle folgt der Windows/Qt-Skalierung und unterstützt den Tastaturfokus. Schalter funktionieren mit der Maus, „Leertaste“ oder „Enter“; Ihr Zustand wird durch Position, Farbe und EIN/AUS-Text übermittelt. Befehlsschaltflächen verwenden auch „Leertaste“ oder „Eingabetaste“, geben eine kurze Rückmeldung beim Drücken und zeigen nur während der Tastaturnavigation einen kontrastreichen Umriss an. Wenn die Bewegung deaktiviert ist, wird die Animation durch einen sofortigen Farbwechsel ersetzt.

Beim ersten Start belegt das Hauptfenster etwa 80 % des verfügbaren Bildschirms. Es merkt sich seine Größe und Position und kehrt nach Auflösungsänderungen zu einem sichtbaren Monitor zurück. Bei mittlerer und schmaler Breite wird die Navigation auf Symbole mit Tooltips, umgebrochenen Schaltflächengruppen und Bildlauf in den Einstellungen reduziert, ohne dass angeheftete Aktionen abgeschnitten werden.

Der dunkle Modus formatiert das Ansichtsfenster und das Taskleistenmenü und fordert eine dunkle native Titelleiste an, wenn Windows DWM dies unterstützt. Das ursprüngliche Tomaten-und-Timer-Symbol wird für Windows, die Taskleiste, die Taskleiste und gepackte EXE-Dateien verwendet.

## Überlaufanzeige

Wählen Sie Puls, vergrößerte Ziffern, Signalbaken, einen Akzentrand, eine Wellenanzeige oder keine Animation. Farbänderungen, Umfang, Geschwindigkeit, Intensität und drei Farben können unabhängig voneinander konfiguriert werden. Die Vorschau ändert weder den Timer noch die Statistiken, Benachrichtigungen oder die Deckkraft.

Das Hauptfenster und das Widget erhalten den gleichen Effektrahmen. „Weiter“ oder „Beenden“ stellt sofort die normalen Farben und Größen wieder her. Bei deaktivierter Bewegung bleiben die statische Zugriffsanzeige, der Statusname und das „+“-Zeichen erhalten.

## Schwebendes Widget

Der Schalter **Widget anzeigen** auf der Timer-Seite zeigt und verbirgt dasselbe Fenster. Es stehen sieben Layouts zur Verfügung: Minimal, Kompakt, Erweitert, Mikro, Zeile, Ring und Anzeigetafel. Alle verwenden die gleiche „TimerEngine“.

Typ, Größe und Position werden für jedes Layout separat gespeichert. Durch manuelle Größenänderung wird eine benutzerdefinierte Größe erstellt. Die Deckkraft reicht von 5 bis 100 %; Während eines Überlaufs kann das Widget vorübergehend vollständig undurchsichtig werden und dann auf den genauen gespeicherten Wert zurückkehren.

In der erweiterten Ansicht werden ganze Aktionen von einer schmalen Aktionsleiste umschlossen. Continue wird niemals abgekürzt. Nur bei minimaler Breite kann „Öffnen“ zu einem Symbol mit einem Tooltip werden; Die verbleibenden Aktionen werden in die nächste Zeile verschoben.

## Benachrichtigungen, Statistiken und Taskleiste

Eine automatische Übergangsbenachrichtigung kann geschlossen werden. Eine manuelle Benachrichtigung umfasst „Weiter“; Die Schaltfläche „Schließen“ schließt nur das Fenster und es geht keine Überlaufzeit verloren. Derselbe Befehl bleibt im Hauptfenster und im Widget verfügbar.

Die Statistik unterscheidet zwischen regulärer Arbeit, regelmäßigen Pausen und drei Überschreitungstypen für heute und alle Zeiten. Durch Schließen des Hauptfensters kann die Anwendung in der Taskleiste minimiert werden. Ein normaler vollständiger Ausstieg spart die angesammelte Nachlaufzeit.

Pro Windows-Benutzer wird eine Anwendungsinstanz ausgeführt. Bei einem zweiten Start wird eine Systemmeldung angezeigt, ohne dass eine weitere Schnittstelle erstellt wird.</translation>
    </message>
    <message>
      <source>help.subtitle</source>
      <translation>Funktionen und sicheres Anwendungsverhalten.</translation>
    </message>
    <message>
      <source>help.title</source>
      <translation>Helfen</translation>
    </message>
    <message>
      <source>main.brand_subtitle</source>
      <translation>Ein ruhiger Arbeitsrhythmus</translation>
    </message>
    <message>
      <source>nav.help</source>
      <translation>Helfen</translation>
    </message>
    <message>
      <source>nav.settings</source>
      <translation>Einstellungen</translation>
    </message>
    <message>
      <source>nav.statistics</source>
      <translation>Statistiken</translation>
    </message>
    <message>
      <source>nav.timer</source>
      <translation>Timer</translation>
    </message>
    <message>
      <source>notification.auto_transition</source>
      <translation>{completed}

        Die nächste Phase hat bereits begonnen: {next_period}.</translation>
    </message>
    <message>
      <source>notification.completed.long_break</source>
      <translation>Lange Pause beendet.</translation>
    </message>
    <message>
      <source>notification.completed.short_break</source>
      <translation>Kurze Pause beendet.</translation>
    </message>
    <message>
      <source>notification.completed.work</source>
      <translation>Arbeitsphase beendet.</translation>
    </message>
    <message>
      <source>notification.default.long_break_end</source>
      <translation>Lange Pause beendet. Zeit, eine neue Arbeitsphase zu beginnen.</translation>
    </message>
    <message>
      <source>notification.default.short_break_end</source>
      <translation>Kurze Pause beendet. Zeit, zur Arbeit zurückzukehren.</translation>
    </message>
    <message>
      <source>notification.default.work_end</source>
      <translation>Arbeitsphase beendet. Zeit für eine Pause.</translation>
    </message>
    <message>
      <source>notification.manual_transition</source>
      <translation>{completed}

        Wählen Sie „Fortsetzen“, um {next_period} zu starten.</translation>
    </message>
    <message>
      <source>overrun.effect.beacons</source>
      <translation>Signalbaken</translation>
    </message>
    <message>
      <source>overrun.effect.border</source>
      <translation>Akzentgrenze</translation>
    </message>
    <message>
      <source>overrun.effect.none</source>
      <translation>Keine Animation</translation>
    </message>
    <message>
      <source>overrun.effect.pulse</source>
      <translation>Impuls</translation>
    </message>
    <message>
      <source>overrun.effect.scale</source>
      <translation>Ziffern vergrößern</translation>
    </message>
    <message>
      <source>overrun.effect.wave</source>
      <translation>Wellenanzeige</translation>
    </message>
    <message>
      <source>overrun.intensity.medium</source>
      <translation>Mittel</translation>
    </message>
    <message>
      <source>overrun.intensity.strong</source>
      <translation>Stark</translation>
    </message>
    <message>
      <source>overrun.intensity.weak</source>
      <translation>Subtil</translation>
    </message>
    <message>
      <source>overrun.scope.both</source>
      <translation>Ziffern und Timerkarte</translation>
    </message>
    <message>
      <source>overrun.scope.card</source>
      <translation>Timer-Karte</translation>
    </message>
    <message>
      <source>overrun.scope.digits</source>
      <translation>Nur Timerziffern</translation>
    </message>
    <message>
      <source>overrun.speed.fast</source>
      <translation>Schnell</translation>
    </message>
    <message>
      <source>overrun.speed.normal</source>
      <translation>Normal</translation>
    </message>
    <message>
      <source>overrun.speed.slow</source>
      <translation>Langsam</translation>
    </message>
    <message>
      <source>settings.appearance.dark_mode</source>
      <translation>Dunkler Modus</translation>
    </message>
    <message>
      <source>settings.appearance.dark_mode.description</source>
      <translation>AUS – heller Modus, EIN – dunkler Modus.</translation>
    </message>
    <message>
      <source>settings.appearance.edit_colors</source>
      <translation>Passen Sie die Farben an</translation>
    </message>
    <message>
      <source>settings.appearance.editor_unavailable</source>
      <translation>Der Editor ist in diesem Fenster nicht verfügbar.</translation>
    </message>
    <message>
      <source>settings.appearance.language</source>
      <translation>Schnittstellensprache</translation>
    </message>
    <message>
      <source>settings.appearance.subtitle</source>
      <translation>Vollständige Paletten aktualisieren jedes geöffnete Fenster ohne Neustart.</translation>
    </message>
    <message>
      <source>settings.appearance.title</source>
      <translation>Aussehen</translation>
    </message>
    <message>
      <source>settings.logic.long_break_interval</source>
      <translation>Arbeitsphasen vor einer längeren Pause</translation>
    </message>
    <message>
      <source>settings.logic.subtitle</source>
      <translation>Die Reihenfolge der Arbeit, kurze Pausen und lange Pausen.</translation>
    </message>
    <message>
      <source>settings.logic.title</source>
      <translation>Timer-Verhalten</translation>
    </message>
    <message>
      <source>settings.logic.use_long_break</source>
      <translation>Machen Sie lange Pausen</translation>
    </message>
    <message>
      <source>settings.logic.use_long_break.description</source>
      <translation>Nach der angegebenen Anzahl von Arbeitsperioden.</translation>
    </message>
    <message>
      <source>settings.notifications.auto_transition</source>
      <translation>Automatischer Übergang</translation>
    </message>
    <message>
      <source>settings.notifications.auto_transition.description</source>
      <translation>EIN – die nächste Periode beginnt sofort; AUS – Nachlaufzeit wird gezählt.</translation>
    </message>
    <message>
      <source>settings.notifications.enabled</source>
      <translation>Benachrichtigungen</translation>
    </message>
    <message>
      <source>settings.notifications.long_break_end</source>
      <translation>Abschluss der langen Pause</translation>
    </message>
    <message>
      <source>settings.notifications.short_break_end</source>
      <translation>Abschluss der kurzen Pause</translation>
    </message>
    <message>
      <source>settings.notifications.sound</source>
      <translation>Benachrichtigungston</translation>
    </message>
    <message>
      <source>settings.notifications.subtitle</source>
      <translation>Ein manueller Übergang kann immer vom Hauptfenster oder Widget aus durchgeführt werden.</translation>
    </message>
    <message>
      <source>settings.notifications.title</source>
      <translation>Benachrichtigungen</translation>
    </message>
    <message>
      <source>settings.notifications.work_end</source>
      <translation>Abschluss der Arbeiten</translation>
    </message>
    <message>
      <source>settings.overrun.allow_motion</source>
      <translation>Effektbewegung zulassen</translation>
    </message>
    <message>
      <source>settings.overrun.change_color</source>
      <translation>Ändern Sie die Farbe des Timers</translation>
    </message>
    <message>
      <source>settings.overrun.color_dialog</source>
      <translation>Überlauffarbe</translation>
    </message>
    <message>
      <source>settings.overrun.effect</source>
      <translation>Haupteffekt</translation>
    </message>
    <message>
      <source>settings.overrun.intensity</source>
      <translation>Intensität</translation>
    </message>
    <message>
      <source>settings.overrun.invalid_colors</source>
      <translation>Ungültige Farben wurden durch Werte aus dem aktiven Design ersetzt.</translation>
    </message>
    <message>
      <source>settings.overrun.opaque_widget</source>
      <translation>Machen Sie das Widget während des Überlaufs undurchsichtig</translation>
    </message>
    <message>
      <source>settings.overrun.scope</source>
      <translation>Farbwechselbereich</translation>
    </message>
    <message>
      <source>settings.overrun.separate_colors</source>
      <translation>Separate Farben</translation>
    </message>
    <message>
      <source>settings.overrun.speed</source>
      <translation>Geschwindigkeit</translation>
    </message>
    <message>
      <source>settings.overrun.subtitle</source>
      <translation>Ein gemeinsamer Frame wird auf das Hauptfenster und das geöffnete Widget angewendet.</translation>
    </message>
    <message>
      <source>settings.overrun.title</source>
      <translation>Überschreitungsanzeige</translation>
    </message>
    <message>
      <source>settings.overrun.use_theme_color</source>
      <translation>Verwenden Sie die Themenfarbe</translation>
    </message>
    <message>
      <source>settings.profiles.apply</source>
      <translation>Profil anwenden</translation>
    </message>
    <message>
      <source>settings.profiles.default_cannot_delete</source>
      <translation>Das Standardprofil kann nicht gelöscht werden.</translation>
    </message>
    <message>
      <source>settings.profiles.default_name</source>
      <translation>Standard</translation>
    </message>
    <message>
      <source>settings.profiles.defaults</source>
      <translation>Standardeinstellungen</translation>
    </message>
    <message>
      <source>settings.profiles.delete</source>
      <translation>Profil löschen</translation>
    </message>
    <message>
      <source>settings.profiles.delete_confirmation</source>
      <translation>Profil „{profile_name}“ löschen?</translation>
    </message>
    <message>
      <source>settings.profiles.delete_title</source>
      <translation>Profil löschen</translation>
    </message>
    <message>
      <source>settings.profiles.dialog_title</source>
      <translation>Profil</translation>
    </message>
    <message>
      <source>settings.profiles.enter_name</source>
      <translation>Geben Sie einen Profilnamen ein.</translation>
    </message>
    <message>
      <source>settings.profiles.name_placeholder</source>
      <translation>Profilname</translation>
    </message>
    <message>
      <source>settings.profiles.restore_personal</source>
      <translation>Meine Einstellungen wiederherstellen</translation>
    </message>
    <message>
      <source>settings.profiles.save</source>
      <translation>Profil speichern</translation>
    </message>
    <message>
      <source>settings.profiles.select_profile</source>
      <translation>Wählen Sie ein Profil aus der Liste aus.</translation>
    </message>
    <message>
      <source>settings.profiles.subtitle</source>
      <translation>Speichern Sie Sätze von Dauer, Darstellungsoptionen und Widget-Einstellungen.</translation>
    </message>
    <message>
      <source>settings.profiles.title</source>
      <translation>Profile</translation>
    </message>
    <message>
      <source>settings.save</source>
      <translation>Einstellungen speichern</translation>
    </message>
    <message>
      <source>settings.section.appearance</source>
      <translation>Aussehen</translation>
    </message>
    <message>
      <source>settings.section.logic</source>
      <translation>Timer-Verhalten</translation>
    </message>
    <message>
      <source>settings.section.notifications</source>
      <translation>Benachrichtigungen</translation>
    </message>
    <message>
      <source>settings.section.overrun</source>
      <translation>Überrannt</translation>
    </message>
    <message>
      <source>settings.section.profiles</source>
      <translation>Profile</translation>
    </message>
    <message>
      <source>settings.section.time</source>
      <translation>Zeit</translation>
    </message>
    <message>
      <source>settings.section.tray</source>
      <translation>Tray und Autostart</translation>
    </message>
    <message>
      <source>settings.section.widget</source>
      <translation>Widget</translation>
    </message>
    <message>
      <source>settings.subtitle</source>
      <translation>Design- und Widget-Änderungen werden sofort wirksam; Andere Änderungen werden nach dem Speichern wirksam.</translation>
    </message>
    <message>
      <source>settings.time.format</source>
      <translation>Zeitformat</translation>
    </message>
    <message>
      <source>settings.time.long_break_minutes</source>
      <translation>Lange Pause, Minuten</translation>
    </message>
    <message>
      <source>settings.time.short_break_minutes</source>
      <translation>Kurze Pause, Minuten</translation>
    </message>
    <message>
      <source>settings.time.subtitle</source>
      <translation>Dauern werden beim Speichern sicher angewendet.</translation>
    </message>
    <message>
      <source>settings.time.title</source>
      <translation>Zeit</translation>
    </message>
    <message>
      <source>settings.time.work_minutes</source>
      <translation>Arbeit, Minuten</translation>
    </message>
    <message>
      <source>settings.title</source>
      <translation>Einstellungen</translation>
    </message>
    <message>
      <source>settings.tray.autostart</source>
      <translation>Beginnen Sie mit Windows</translation>
    </message>
    <message>
      <source>settings.tray.autostart_current</source>
      <translation>Autostart ist aktiviert und zeigt auf den aktuellen Ordner der Anwendung.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_disabled</source>
      <translation>Autostart ist deaktiviert.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_python</source>
      <translation>Ausführung unter Python: Autostart kann in der EXE-Version aktiviert werden.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_stale</source>
      <translation>Der Autostart-Pfad ist veraltet. Aktualisieren Sie es, nachdem Sie die Anwendung verschoben haben.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_title</source>
      <translation>Autostart</translation>
    </message>
    <message>
      <source>settings.tray.close_to_tray</source>
      <translation>Beim Schließen auf das Fach minimieren</translation>
    </message>
    <message>
      <source>settings.tray.minimize_on_start</source>
      <translation>Minimieren Sie die Anwendung nach dem Start</translation>
    </message>
    <message>
      <source>settings.tray.subtitle</source>
      <translation>Die Taskleiste wird im gemeinsam genutzten Qt-GUI-Thread ausgeführt.</translation>
    </message>
    <message>
      <source>settings.tray.title</source>
      <translation>Tray und Autostart</translation>
    </message>
    <message>
      <source>settings.tray.update_autostart</source>
      <translation>Autostart-Pfad aktualisieren</translation>
    </message>
    <message>
      <source>settings.widget.always_on_top</source>
      <translation>Immer oben</translation>
    </message>
    <message>
      <source>settings.widget.dialog_title</source>
      <translation>Widget</translation>
    </message>
    <message>
      <source>settings.widget.opacity</source>
      <translation>Widget-Deckkraft</translation>
    </message>
    <message>
      <source>settings.widget.opacity.description</source>
      <translation>Niedrigere Werte machen das Widget transparenter. Mindestens 5 %.</translation>
    </message>
    <message>
      <source>settings.widget.position_reset</source>
      <translation>Die Position für den aktuellen Typ wurde zurückgesetzt.</translation>
    </message>
    <message>
      <source>settings.widget.reset_position</source>
      <translation>Position für aktuellen Typ zurücksetzen</translation>
    </message>
    <message>
      <source>settings.widget.size</source>
      <translation>Größe</translation>
    </message>
    <message>
      <source>settings.widget.subtitle</source>
      <translation>Die Sichtbarkeit wird durch den Schalter auf der Timer-Seite gesteuert.</translation>
    </message>
    <message>
      <source>settings.widget.title</source>
      <translation>Schwebendes Widget</translation>
    </message>
    <message>
      <source>settings.widget.type</source>
      <translation>Widget-Typ</translation>
    </message>
    <message>
      <source>startup.already_running</source>
      <translation>Der Pomodoro-Timer startet oder läuft bereits. Warten Sie, bis sich das Fenster öffnet, oder verwenden Sie die bereits geöffnete Anwendung.</translation>
    </message>
    <message>
      <source>startup.lock.already_running</source>
      <translation>Eine andere Anwendungsinstanz wird bereits ausgeführt.</translation>
    </message>
    <message>
      <source>startup.lock.create_failed</source>
      <translation>Die Systemsperre konnte nicht erstellt werden (WinError {error_code}).</translation>
    </message>
    <message>
      <source>startup.lock.release_failed</source>
      <translation>Die Systemsperre konnte nicht aufgehoben werden (WinError {error_code}).</translation>
    </message>
    <message>
      <source>startup.lock.secondary_close_failed</source>
      <translation>Eine andere Instanz läuft bereits, aber ihr sekundäres Handle konnte nicht geschlossen werden (WinError {error_code}).</translation>
    </message>
    <message>
      <source>startup.lock.unsupported</source>
      <translation>Die Einzelinstanz-Systemsperre wird nur unter Windows unterstützt.</translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_cycles</source>
      <translation>
        <numerusform>Kompletter Zyklus</numerusform>
        <numerusform>Komplette Zyklen</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_long_breaks</source>
      <translation>
        <numerusform>Lange Pause</numerusform>
        <numerusform>Lange Pausen</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_short_breaks</source>
      <translation>
        <numerusform>Kurze Pause</numerusform>
        <numerusform>Kurze Pausen</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_work_periods</source>
      <translation>
        <numerusform>Arbeitsphase</numerusform>
        <numerusform>Arbeitsphasen</numerusform>
      </translation>
    </message>
    <message>
      <source>stats.metric.long_break_overrun</source>
      <translation>Lange Pause überzogen</translation>
    </message>
    <message>
      <source>stats.metric.overwork_time</source>
      <translation>Weiterarbeitszeit</translation>
    </message>
    <message>
      <source>stats.metric.rest_time</source>
      <translation>Pausenzeit</translation>
    </message>
    <message>
      <source>stats.metric.short_break_overrun</source>
      <translation>Kurze Pause überzogen</translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.skipped_periods</source>
      <translation>
        <numerusform>Übersprungener Zeitraum</numerusform>
        <numerusform>Übersprungene Stunden</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.timer_resets</source>
      <translation>
        <numerusform>Timer-Reset</numerusform>
        <numerusform>Timer wird zurückgesetzt</numerusform>
      </translation>
    </message>
    <message>
      <source>stats.metric.work_time</source>
      <translation>Arbeitszeit</translation>
    </message>
    <message>
      <source>stats.period.all_time</source>
      <translation>Alle Zeiten</translation>
    </message>
    <message>
      <source>stats.period.today</source>
      <translation>Heute</translation>
    </message>
    <message>
      <source>stats.reset.action</source>
      <translation>Statistiken zurücksetzen</translation>
    </message>
    <message>
      <source>stats.reset.confirmation</source>
      <translation>Sind Sie sicher, dass Sie alle Statistiken löschen möchten?</translation>
    </message>
    <message>
      <source>stats.reset.title</source>
      <translation>Statistiken zurücksetzen</translation>
    </message>
    <message>
      <source>stats.subtitle</source>
      <translation>Reguläre Zeit und Überschreitungen werden separat erfasst.</translation>
    </message>
    <message>
      <source>stats.title</source>
      <translation>Statistiken</translation>
    </message>
    <message>
      <source>theme.appearance.dark</source>
      <translation>Dunkel</translation>
    </message>
    <message>
      <source>theme.appearance.light</source>
      <translation>Hell</translation>
    </message>
    <message>
      <source>theme.contrast.accent</source>
      <translation>Akzenttext / Akzent</translation>
    </message>
    <message>
      <source>theme.contrast.button</source>
      <translation>Schaltflächentext / Schaltfläche</translation>
    </message>
    <message>
      <source>theme.contrast.long_break</source>
      <translation>Lange Pause / Karte</translation>
    </message>
    <message>
      <source>theme.contrast.long_break_overrun</source>
      <translation>Überzogene lange Pause / Karte</translation>
    </message>
    <message>
      <source>theme.contrast.overwork</source>
      <translation>Weiterarbeit / Karte</translation>
    </message>
    <message>
      <source>theme.contrast.primary_card</source>
      <translation>Primärtext/Karte</translation>
    </message>
    <message>
      <source>theme.contrast.secondary_card</source>
      <translation>Sekundärtext/Karte</translation>
    </message>
    <message>
      <source>theme.contrast.short_break</source>
      <translation>Kurze Pause / Karte</translation>
    </message>
    <message>
      <source>theme.contrast.short_break_overrun</source>
      <translation>Überzogene kurze Pause / Karte</translation>
    </message>
    <message>
      <source>theme.contrast.work</source>
      <translation>Arbeit / Karte</translation>
    </message>
    <message>
      <source>theme.description.aurora</source>
      <translation>Kühle blaue und violette Akzente</translation>
    </message>
    <message>
      <source>theme.description.comet</source>
      <translation>Ruhige neutrale Palette</translation>
    </message>
    <message>
      <source>theme.description.custom</source>
      <translation>Ihre unabhängigen hellen und dunklen Paletten</translation>
    </message>
    <message>
      <source>theme.description.warm</source>
      <translation>Weicher Sand und warme Oberflächen</translation>
    </message>
    <message>
      <source>theme.name.aurora</source>
      <translation>Aurora</translation>
    </message>
    <message>
      <source>theme.name.comet</source>
      <translation>Komet</translation>
    </message>
    <message>
      <source>theme.name.custom</source>
      <translation>Benutzerdefiniert</translation>
    </message>
    <message>
      <source>theme.name.warm</source>
      <translation>Warm</translation>
    </message>
    <message>
      <source>theme_editor.color.accent</source>
      <translation>Akzent</translation>
    </message>
    <message>
      <source>theme_editor.color.accent_hover</source>
      <translation>Schweben</translation>
    </message>
    <message>
      <source>theme_editor.color.background</source>
      <translation>Haupthintergrund</translation>
    </message>
    <message>
      <source>theme_editor.color.border</source>
      <translation>Grenzen</translation>
    </message>
    <message>
      <source>theme_editor.color.button_background</source>
      <translation>Knopffarbe</translation>
    </message>
    <message>
      <source>theme_editor.color.button_text</source>
      <translation>Schaltflächentext</translation>
    </message>
    <message>
      <source>theme_editor.color.card_background</source>
      <translation>Kartenhintergrund</translation>
    </message>
    <message>
      <source>theme_editor.color.disabled</source>
      <translation>Deaktivierte Elemente</translation>
    </message>
    <message>
      <source>theme_editor.color.error</source>
      <translation>Fehler</translation>
    </message>
    <message>
      <source>theme_editor.color.focus</source>
      <translation>Fokus</translation>
    </message>
    <message>
      <source>theme_editor.color.on_accent</source>
      <translation>Text der Akzentschaltfläche</translation>
    </message>
    <message>
      <source>theme_editor.color.secondary_background</source>
      <translation>Sekundärer Hintergrund</translation>
    </message>
    <message>
      <source>theme_editor.color.success</source>
      <translation>Erfolg</translation>
    </message>
    <message>
      <source>theme_editor.color.text_primary</source>
      <translation>Primärtext</translation>
    </message>
    <message>
      <source>theme_editor.color.text_secondary</source>
      <translation>Sekundärtext</translation>
    </message>
    <message>
      <source>theme_editor.color.warning</source>
      <translation>Warnung</translation>
    </message>
    <message>
      <source>theme_editor.contrast.ok</source>
      <translation>Kontrastprüfung: Die Hauptkombinationen entsprechen der 4,5:1-Richtlinie.</translation>
    </message>
    <message numerus="yes">
      <source>theme_editor.contrast.warning</source>
      <translation>
        <numerusform>Kontrastprüfung: {count}-Kombination liegt unter 4,5:1. Bei der Bewerbung ist eine Bestätigung erforderlich.</numerusform>
        <numerusform>Kontrastprüfung: {count}-Kombinationen liegen unter 4,5:1. Bei der Bewerbung ist eine Bestätigung erforderlich.</numerusform>
      </translation>
    </message>
    <message>
      <source>theme_editor.create_copy</source>
      <translation>Kopie erstellen</translation>
    </message>
    <message>
      <source>theme_editor.create_from</source>
      <translation>Erstellen aus</translation>
    </message>
    <message>
      <source>theme_editor.editing_mode</source>
      <translation>Modus wird bearbeitet</translation>
    </message>
    <message>
      <source>theme_editor.group.service_states</source>
      <translation>Statusfarben</translation>
    </message>
    <message>
      <source>theme_editor.group.surfaces</source>
      <translation>Oberflächen</translation>
    </message>
    <message>
      <source>theme_editor.group.text_controls</source>
      <translation>Text und Steuerelemente</translation>
    </message>
    <message>
      <source>theme_editor.group.timer_states</source>
      <translation>Timer-Zustände</translation>
    </message>
    <message>
      <source>theme_editor.low_contrast.confirmation</source>
      <translation>Einige Kombinationen liegen unter 4,5:1:

{details}

Trotzdem sparen?</translation>
    </message>
    <message>
      <source>theme_editor.low_contrast.title</source>
      <translation>Geringer Kontrast</translation>
    </message>
    <message>
      <source>theme_editor.reset.confirmation</source>
      <translation>Beide Modi auf das sichere Comet-Thema zurücksetzen?</translation>
    </message>
    <message>
      <source>theme_editor.reset.title</source>
      <translation>Thema zurücksetzen</translation>
    </message>
    <message>
      <source>theme_editor.reset_all</source>
      <translation>Gesamtes Theme zurücksetzen</translation>
    </message>
    <message>
      <source>theme_editor.reset_mode</source>
      <translation>Aktuellen Modus zurücksetzen</translation>
    </message>
    <message>
      <source>theme_editor.subtitle</source>
      <translation>Bearbeiten Sie helle und dunkle Modi unabhängig voneinander.</translation>
    </message>
    <message>
      <source>theme_editor.title</source>
      <translation>Benutzerdefiniertes Thema</translation>
    </message>
    <message>
      <source>timer.mode.long_break</source>
      <translation>Lange Pause</translation>
    </message>
    <message>
      <source>timer.mode.long_break_overrun</source>
      <translation>Lange Pause überzogen</translation>
    </message>
    <message>
      <source>timer.mode.overwork</source>
      <translation>Weiterarbeit</translation>
    </message>
    <message>
      <source>timer.mode.short_break</source>
      <translation>Kurze Pause</translation>
    </message>
    <message>
      <source>timer.mode.short_break_overrun</source>
      <translation>Kurze Pause überzogen</translation>
    </message>
    <message>
      <source>timer.mode.work</source>
      <translation>Arbeit</translation>
    </message>
    <message>
      <source>timer.overrun.waiting_status</source>
      <translation>Arbeitsphase beendet – die Überschreitung wird bis zum Fortsetzen gezählt</translation>
    </message>
    <message>
      <source>timer.page.subtitle</source>
      <translation>Ein Timer für das Hauptfenster, Benachrichtigungen und das Widget.</translation>
    </message>
    <message>
      <source>timer.page.title</source>
      <translation>Fokussitzung</translation>
    </message>
    <message>
      <source>timer.status.accessible_name</source>
      <translation>Timer-Status</translation>
    </message>
    <message>
      <source>timer.status.overrun</source>
      <translation>Überschreitung wird erfasst</translation>
    </message>
    <message>
      <source>timer.status.paused</source>
      <translation>Timer angehalten</translation>
    </message>
    <message>
      <source>timer.status.running</source>
      <translation>Timer läuft</translation>
    </message>
    <message>
      <source>timer.status.stopped</source>
      <translation>Timer gestoppt</translation>
    </message>
    <message>
      <source>timer.widget.show</source>
      <translation>Widget anzeigen</translation>
    </message>
    <message>
      <source>timer.widget.show.description</source>
      <translation>Position, Größe, Typ und Deckkraft werden separat gespeichert.</translation>
    </message>
    <message>
      <source>toggle.accessible_description</source>
      <translation>EIN – aktiviert, AUS – deaktiviert</translation>
    </message>
    <message>
      <source>toggle.accessible_name</source>
      <translation>Schalten</translation>
    </message>
    <message>
      <source>toggle.off</source>
      <translation>AUS</translation>
    </message>
    <message>
      <source>toggle.on</source>
      <translation>AN</translation>
    </message>
    <message>
      <source>toggle.state.off</source>
      <translation>AUS, deaktiviert</translation>
    </message>
    <message>
      <source>toggle.state.on</source>
      <translation>EIN, aktiviert</translation>
    </message>
    <message>
      <source>tray.exit</source>
      <translation>Beenden</translation>
    </message>
    <message>
      <source>tray.hide</source>
      <translation>Fenster ausblenden</translation>
    </message>
    <message>
      <source>tray.reset</source>
      <translation>Zurücksetzen</translation>
    </message>
    <message>
      <source>tray.show</source>
      <translation>Fenster anzeigen</translation>
    </message>
    <message>
      <source>tray.start_pause</source>
      <translation>Start / Pause</translation>
    </message>
    <message numerus="yes">
      <source>widget.completed_work_periods</source>
      <translation>
        <numerusform>Abgeschlossene Arbeitsperiode: {count}</numerusform>
        <numerusform>Abgeschlossene Arbeitsperioden: {count}</numerusform>
      </translation>
    </message>
    <message>
      <source>widget.size.custom</source>
      <translation>Benutzerdefiniert</translation>
    </message>
    <message>
      <source>widget.size.large</source>
      <translation>Groß</translation>
    </message>
    <message>
      <source>widget.size.medium</source>
      <translation>Mittel</translation>
    </message>
    <message>
      <source>widget.size.small</source>
      <translation>Klein</translation>
    </message>
    <message>
      <source>widget.type.compact</source>
      <translation>Kompakt</translation>
    </message>
    <message>
      <source>widget.type.compact.description</source>
      <translation>Eine klassische Kompaktkarte mit der Primäraktion.</translation>
    </message>
    <message>
      <source>widget.type.expanded</source>
      <translation>Erweitert</translation>
    </message>
    <message>
      <source>widget.type.expanded.description</source>
      <translation>Zyklusinformationen und der gesamte Satz primärer Timer-Aktionen.</translation>
    </message>
    <message>
      <source>widget.type.micro</source>
      <translation>Mikro</translation>
    </message>
    <message>
      <source>widget.type.micro.description</source>
      <translation>Das kleinste Fenster: meist nur die Zeit.</translation>
    </message>
    <message>
      <source>widget.type.minimal</source>
      <translation>Minimal</translation>
    </message>
    <message>
      <source>widget.type.minimal.description</source>
      <translation>Große Uhrzeit, Staatsname und minimale Details.</translation>
    </message>
    <message>
      <source>widget.type.ring</source>
      <translation>Ring</translation>
    </message>
    <message>
      <source>widget.type.ring.description</source>
      <translation>Zeit innerhalb eines kreisförmigen Periodenindikators.</translation>
    </message>
    <message>
      <source>widget.type.row</source>
      <translation>Zeile</translation>
    </message>
    <message>
      <source>widget.type.row.description</source>
      <translation>Eine horizontale Reihe für den Bildschirmrand.</translation>
    </message>
    <message>
      <source>widget.type.scoreboard</source>
      <translation>Anzeigetafel</translation>
    </message>
    <message>
      <source>widget.type.scoreboard.description</source>
      <translation>Große, monospaced Ziffern im ruhigen Anzeigetafel-Stil.</translation>
    </message>
    <message>
      <source>widget.window_title</source>
      <translation>Pomodoro-Widget</translation>
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
      <translation>Speichern</translation>
    </message>
    <message>
      <source>Save All</source>
      <translation>Alles speichern</translation>
    </message>
    <message>
      <source>Open</source>
      <translation>Öffnen</translation>
    </message>
    <message>
      <source>&amp;Yes</source>
      <translation>&amp;Ja</translation>
    </message>
    <message>
      <source>Yes to &amp;All</source>
      <translation>Ja, &amp;alle</translation>
    </message>
    <message>
      <source>&amp;No</source>
      <translation>&amp;Nein</translation>
    </message>
    <message>
      <source>N&amp;o to All</source>
      <translation>Nein für a&amp;lle</translation>
    </message>
    <message>
      <source>Abort</source>
      <translation>Abbrechen</translation>
    </message>
    <message>
      <source>Retry</source>
      <translation>Wiederholen</translation>
    </message>
    <message>
      <source>Ignore</source>
      <translation>Ignorieren</translation>
    </message>
    <message>
      <source>Close</source>
      <translation>Schließen</translation>
    </message>
    <message>
      <source>Cancel</source>
      <translation>Abbrechen</translation>
    </message>
    <message>
      <source>Discard</source>
      <translation>Verwerfen</translation>
    </message>
    <message>
      <source>Help</source>
      <translation>Hilfe</translation>
    </message>
    <message>
      <source>Apply</source>
      <translation>Anwenden</translation>
    </message>
    <message>
      <source>Reset</source>
      <translation>Zurücksetzen</translation>
    </message>
    <message>
      <source>Restore Defaults</source>
      <translation>Standardwerte wiederherstellen</translation>
    </message>
  </context>
</TS>
