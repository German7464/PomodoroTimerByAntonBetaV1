<?xml version='1.0' encoding='utf-8'?>
<TS version="2.1" language="fr_FR">
  <context>
    <name>PomodoroTimer</name>
    <message>
      <source>action.apply</source>
      <translation>Appliquer</translation>
    </message>
    <message>
      <source>action.cancel</source>
      <translation>Annuler</translation>
    </message>
    <message>
      <source>action.choose</source>
      <translation>Choisir</translation>
    </message>
    <message>
      <source>action.close</source>
      <translation>Fermer</translation>
    </message>
    <message>
      <source>action.continue</source>
      <translation>Continuer</translation>
    </message>
    <message>
      <source>action.continue_next_period</source>
      <translation>Continuer et commencer la prochaine période</translation>
    </message>
    <message>
      <source>action.open</source>
      <translation>Ouvrir</translation>
    </message>
    <message>
      <source>action.open_main_window</source>
      <translation>Ouvrir la fenêtre principale</translation>
    </message>
    <message>
      <source>action.pause</source>
      <translation>Pause</translation>
    </message>
    <message>
      <source>action.preview</source>
      <translation>Aperçu</translation>
    </message>
    <message>
      <source>action.refresh</source>
      <translation>Rafraîchir</translation>
    </message>
    <message>
      <source>action.reset</source>
      <translation>Réinitialiser</translation>
    </message>
    <message>
      <source>action.show</source>
      <translation>Afficher</translation>
    </message>
    <message>
      <source>action.skip</source>
      <translation>Passer</translation>
    </message>
    <message>
      <source>action.start</source>
      <translation>Démarrer</translation>
    </message>
    <message>
      <source>dialog.color.choose</source>
      <translation>Choisissez une couleur</translation>
    </message>
    <message>
      <source>dialog.color.invalid_hex</source>
      <translation>Corrigez les valeurs : le format #RRGGBB est obligatoire.</translation>
    </message>
    <message>
      <source>dialog.color.title</source>
      <translation>Couleur</translation>
    </message>
    <message>
      <source>error.autostart.python_unavailable</source>
      <translation>Le démarrage automatique est disponible uniquement dans le fichier EXE fourni. Il ne peut pas être activé lors de l'exécution à partir de Python.</translation>
    </message>
    <message>
      <source>error.data.portable_fallback</source>
      <translation>Les données n'ont pas pu être écrites à côté de l'application. Les paramètres seront temporairement stockés dans votre dossier utilisateur. Pour le mode portable, déplacez l'application vers un dossier accessible en écriture.</translation>
    </message>
    <message>
      <source>error.data.portable_title</source>
      <translation>Mode portable</translation>
    </message>
    <message>
      <source>error.data.unavailable</source>
      <translation>Le dossier des paramètres de l'application n'a pas pu être créé.</translation>
    </message>
    <message>
      <source>error.widget.hide</source>
      <translation>Impossible de masquer le widget : {error}</translation>
    </message>
    <message>
      <source>error.widget.show</source>
      <translation>Impossible d'afficher le widget : {error}</translation>
    </message>
    <message>
      <source>error.widget.state_mismatch</source>
      <translation>la fenêtre n'est pas entrée dans l'état demandé</translation>
    </message>
    <message>
      <source>help.content</source>
      <translation># Minuterie Pomodoro

## Démarrage rapide

Choisissez les durées dans Paramètres, ouvrez Minuteur et sélectionnez **Démarrer**. Utilisez l'interrupteur en haut pour basculer instantanément entre les modes clair et sombre. Les paramètres binaires utilisent des commutateurs ; les actions régulières restent des boutons.

## Commandes de minuterie

- **Démarrer** commence la période en cours.
- **Pause / Continue** met en pause et reprend une période régulière.
- **Période de saut** passe au mode suivant sans enregistrer la durée.
- **Reset** revient au travail arrêté et enregistre une réinitialisation dans les statistiques.
- **Continuer et démarrer la période suivante** apparaît pour une transition manuelle, enregistre le dépassement une fois et démarre immédiatement la période suivante.

Avec les transitions automatiques, la période suivante démarre immédiatement et aucun dépassement n'est comptabilisé. Avec les transitions manuelles, l'application affiche **Surmenage**, **Dépassement de courte pause** ou **Dépassement de longue pause** et le temps préfixé par « + ». Le démarrage, la pause, le saut et la réinitialisation restent désactivés pendant un dépassement afin qu'aucun temps ne soit perdu.

## Apparence et accessibilité

Les thèmes Comet, Aurora, Warm et Custom ont chacun des modes clair et sombre. L'éditeur de thème personnalisé stocke les modes séparément, valide « #RRGGBB » et avertit lorsque le contraste est inférieur à 4,5 : 1. Annuler restaure les couleurs enregistrées ; la réinitialisation restaure la palette Comet sécurisée.

L'interface Qt Widgets suit la mise à l'échelle Windows/Qt et prend en charge la mise au point du clavier. Les commutateurs fonctionnent avec la souris, « Espace » ou « Entrée » ; leur état est indiqué par la position, la couleur et le texte ON/OFF. Les boutons de commande utilisent également « Espace » ou « Entrée », fournissent un bref retour d'information sur la pression et affichent un contour très contrasté uniquement pendant la navigation au clavier. Lorsque le mouvement est désactivé, un changement de couleur immédiat remplace l'animation.

Au premier lancement, la fenêtre principale utilise environ 80 % de l'écran disponible. Il mémorise sa taille et sa position et revient à un moniteur visible après un changement de résolution. Aux largeurs moyennes et étroites, la navigation se réduit à des icônes avec des info-bulles, des groupes de boutons s'ajustent et les paramètres défilent sans couper les actions épinglées.

Le mode sombre stylise la fenêtre et le menu de la barre d’état et demande une barre de titre native sombre lorsque Windows DWM le prend en charge. L'icône originale de tomate et de minuterie est utilisée pour Windows, la barre des tâches, la barre d'état système et le fichier EXE packagé.

## Indication de dépassement

Choisissez une impulsion, des chiffres agrandis, des balises de signal, une bordure d'accent, un indicateur d'onde ou aucune animation. Les changements de couleur, la portée, la vitesse, l'intensité et les trois couleurs sont configurés indépendamment. L'aperçu ne modifie pas le minuteur, les statistiques, les notifications ou l'opacité.

La fenêtre principale et le widget reçoivent le même cadre d'effet. Continuer ou quitter restaure immédiatement les couleurs et les tailles normales. Lorsque le mouvement est désactivé, l'indication statique accessible, le nom de l'état et le signe «+» restent.

## Widget flottant

Le bouton **Afficher le widget** sur la page Minuterie affiche et masque la même fenêtre. Sept mises en page sont disponibles : Minimal, Compact, Étendu, Micro, Ligne, Anneau et Tableau de bord. Tous utilisent le même « TimerEngine ».

Le type, la taille et la position sont stockés séparément pour chaque mise en page. Le redimensionnement manuel crée une taille personnalisée. L'opacité varie de 5 à 100 % ; lors d'un dépassement, le widget peut temporairement devenir complètement opaque puis revenir à la valeur exacte enregistrée.

En vue développée, une barre d'action étroite englobe des actions entières. Continuer n’est jamais abrégé. À la largeur minimale, seul Open peut devenir une icône avec une info-bulle ; les actions restantes passent à la ligne suivante.

## Notifications, statistiques et barre d'état

Une notification de transition automatique peut être fermée. Une notification manuelle inclut Continuer ; son bouton de fermeture ferme uniquement la fenêtre et ne perd pas de temps de dépassement. La même commande reste disponible dans la fenêtre principale et le widget.

Les statistiques séparent le travail régulier, les pauses régulières et trois types de dépassement pour aujourd'hui et pour toujours. La fermeture de la fenêtre principale peut minimiser l'application dans la barre d'état. Une sortie complète normale permet d'économiser le temps de dépassement accumulé.

Une instance d'application s'exécute par utilisateur Windows. Un deuxième lancement affiche un message système sans créer une autre interface.</translation>
    </message>
    <message>
      <source>help.subtitle</source>
      <translation>Fonctionnalités et comportement sécurisé des applications.</translation>
    </message>
    <message>
      <source>help.title</source>
      <translation>Aide</translation>
    </message>
    <message>
      <source>main.brand_subtitle</source>
      <translation>Un rythme de travail calme</translation>
    </message>
    <message>
      <source>nav.help</source>
      <translation>Aide</translation>
    </message>
    <message>
      <source>nav.settings</source>
      <translation>Paramètres</translation>
    </message>
    <message>
      <source>nav.statistics</source>
      <translation>Statistiques</translation>
    </message>
    <message>
      <source>nav.timer</source>
      <translation>Minuteur</translation>
    </message>
    <message>
      <source>notification.auto_transition</source>
      <translation>{completed}

La prochaine période a déjà commencé : {next_period}.</translation>
    </message>
    <message>
      <source>notification.completed.long_break</source>
      <translation>Longue pause terminée.</translation>
    </message>
    <message>
      <source>notification.completed.short_break</source>
      <translation>Courte pause terminée.</translation>
    </message>
    <message>
      <source>notification.completed.work</source>
      <translation>Période de travail terminée.</translation>
    </message>
    <message>
      <source>notification.default.long_break_end</source>
      <translation>Longue pause terminée. Il est temps de commencer une nouvelle période de travail.</translation>
    </message>
    <message>
      <source>notification.default.short_break_end</source>
      <translation>Courte pause terminée. Il est temps de retourner au travail.</translation>
    </message>
    <message>
      <source>notification.default.work_end</source>
      <translation>Période de travail terminée. Il est temps de faire une pause.</translation>
    </message>
    <message>
      <source>notification.manual_transition</source>
      <translation>{completed}

Sélectionnez Continuer pour démarrer {next_period}.</translation>
    </message>
    <message>
      <source>overrun.effect.beacons</source>
      <translation>Balises de signalisation</translation>
    </message>
    <message>
      <source>overrun.effect.border</source>
      <translation>Bordure d'accentuation</translation>
    </message>
    <message>
      <source>overrun.effect.none</source>
      <translation>Aucune animation</translation>
    </message>
    <message>
      <source>overrun.effect.pulse</source>
      <translation>Impulsion</translation>
    </message>
    <message>
      <source>overrun.effect.scale</source>
      <translation>Agrandir les chiffres</translation>
    </message>
    <message>
      <source>overrun.effect.wave</source>
      <translation>Indicateur de vague</translation>
    </message>
    <message>
      <source>overrun.intensity.medium</source>
      <translation>Moyen</translation>
    </message>
    <message>
      <source>overrun.intensity.strong</source>
      <translation>Fort</translation>
    </message>
    <message>
      <source>overrun.intensity.weak</source>
      <translation>Subtil</translation>
    </message>
    <message>
      <source>overrun.scope.both</source>
      <translation>Chiffres et carte de minuterie</translation>
    </message>
    <message>
      <source>overrun.scope.card</source>
      <translation>Carte de minuterie</translation>
    </message>
    <message>
      <source>overrun.scope.digits</source>
      <translation>Chiffres de la minuterie uniquement</translation>
    </message>
    <message>
      <source>overrun.speed.fast</source>
      <translation>Rapide</translation>
    </message>
    <message>
      <source>overrun.speed.normal</source>
      <translation>Normale</translation>
    </message>
    <message>
      <source>overrun.speed.slow</source>
      <translation>Lent</translation>
    </message>
    <message>
      <source>settings.appearance.dark_mode</source>
      <translation>Mode sombre</translation>
    </message>
    <message>
      <source>settings.appearance.dark_mode.description</source>
      <translation>OFF – mode clair, ON – mode sombre.</translation>
    </message>
    <message>
      <source>settings.appearance.edit_colors</source>
      <translation>Personnaliser les couleurs</translation>
    </message>
    <message>
      <source>settings.appearance.editor_unavailable</source>
      <translation>L'éditeur n'est pas disponible dans cette fenêtre.</translation>
    </message>
    <message>
      <source>settings.appearance.language</source>
      <translation>Langue de l'interface</translation>
    </message>
    <message>
      <source>settings.appearance.subtitle</source>
      <translation>Les palettes complètes mettent à jour chaque fenêtre ouverte sans redémarrage.</translation>
    </message>
    <message>
      <source>settings.appearance.title</source>
      <translation>Apparence</translation>
    </message>
    <message>
      <source>settings.logic.long_break_interval</source>
      <translation>Périodes de travail avant une longue pause</translation>
    </message>
    <message>
      <source>settings.logic.subtitle</source>
      <translation>L'ordre des travaux, courtes pauses et longues pauses.</translation>
    </message>
    <message>
      <source>settings.logic.title</source>
      <translation>Comportement de la minuterie</translation>
    </message>
    <message>
      <source>settings.logic.use_long_break</source>
      <translation>Utilisez de longues pauses</translation>
    </message>
    <message>
      <source>settings.logic.use_long_break.description</source>
      <translation>Après le nombre spécifié de périodes de travail.</translation>
    </message>
    <message>
      <source>settings.notifications.auto_transition</source>
      <translation>Transition automatique</translation>
    </message>
    <message>
      <source>settings.notifications.auto_transition.description</source>
      <translation>ON — la période suivante commence immédiatement ; OFF — le temps de dépassement est compté.</translation>
    </message>
    <message>
      <source>settings.notifications.enabled</source>
      <translation>Notifications</translation>
    </message>
    <message>
      <source>settings.notifications.long_break_end</source>
      <translation>Fin d'une longue pause</translation>
    </message>
    <message>
      <source>settings.notifications.short_break_end</source>
      <translation>Fin d'un court séjour</translation>
    </message>
    <message>
      <source>settings.notifications.sound</source>
      <translation>Son de notification</translation>
    </message>
    <message>
      <source>settings.notifications.subtitle</source>
      <translation>Une transition manuelle peut toujours être effectuée à partir de la fenêtre principale ou du widget.</translation>
    </message>
    <message>
      <source>settings.notifications.title</source>
      <translation>Notifications</translation>
    </message>
    <message>
      <source>settings.notifications.work_end</source>
      <translation>Achèvement des travaux</translation>
    </message>
    <message>
      <source>settings.overrun.allow_motion</source>
      <translation>Autoriser le mouvement de l'effet</translation>
    </message>
    <message>
      <source>settings.overrun.change_color</source>
      <translation>Changer la couleur du minuteur</translation>
    </message>
    <message>
      <source>settings.overrun.color_dialog</source>
      <translation>Couleur de dépassement</translation>
    </message>
    <message>
      <source>settings.overrun.effect</source>
      <translation>Effet principal</translation>
    </message>
    <message>
      <source>settings.overrun.intensity</source>
      <translation>Intensité</translation>
    </message>
    <message>
      <source>settings.overrun.invalid_colors</source>
      <translation>Les couleurs invalides ont été remplacées par des valeurs du thème actif.</translation>
    </message>
    <message>
      <source>settings.overrun.opaque_widget</source>
      <translation>Rendre le widget opaque lors du dépassement</translation>
    </message>
    <message>
      <source>settings.overrun.scope</source>
      <translation>Zone de changement de couleur</translation>
    </message>
    <message>
      <source>settings.overrun.separate_colors</source>
      <translation>Couleurs séparées</translation>
    </message>
    <message>
      <source>settings.overrun.speed</source>
      <translation>Vitesse</translation>
    </message>
    <message>
      <source>settings.overrun.subtitle</source>
      <translation>Un cadre partagé est appliqué à la fenêtre principale et au widget ouvert.</translation>
    </message>
    <message>
      <source>settings.overrun.title</source>
      <translation>Indication de dépassement</translation>
    </message>
    <message>
      <source>settings.overrun.use_theme_color</source>
      <translation>Utiliser la couleur du thème</translation>
    </message>
    <message>
      <source>settings.profiles.apply</source>
      <translation>Appliquer le profil</translation>
    </message>
    <message>
      <source>settings.profiles.default_cannot_delete</source>
      <translation>Le profil par défaut ne peut pas être supprimé.</translation>
    </message>
    <message>
      <source>settings.profiles.default_name</source>
      <translation>Défaut</translation>
    </message>
    <message>
      <source>settings.profiles.defaults</source>
      <translation>Paramètres par défaut</translation>
    </message>
    <message>
      <source>settings.profiles.delete</source>
      <translation>Supprimer le profil</translation>
    </message>
    <message>
      <source>settings.profiles.delete_confirmation</source>
      <translation>Supprimer le profil « {profile_name} » ?</translation>
    </message>
    <message>
      <source>settings.profiles.delete_title</source>
      <translation>Supprimer le profil</translation>
    </message>
    <message>
      <source>settings.profiles.dialog_title</source>
      <translation>Profil</translation>
    </message>
    <message>
      <source>settings.profiles.enter_name</source>
      <translation>Entrez un nom de profil.</translation>
    </message>
    <message>
      <source>settings.profiles.name_placeholder</source>
      <translation>Nom du profil</translation>
    </message>
    <message>
      <source>settings.profiles.restore_personal</source>
      <translation>Restaurer mes paramètres</translation>
    </message>
    <message>
      <source>settings.profiles.save</source>
      <translation>Enregistrer le profil</translation>
    </message>
    <message>
      <source>settings.profiles.select_profile</source>
      <translation>Sélectionnez un profil dans la liste.</translation>
    </message>
    <message>
      <source>settings.profiles.subtitle</source>
      <translation>Enregistrez des ensembles de durées, d’options d’apparence et de paramètres de widget.</translation>
    </message>
    <message>
      <source>settings.profiles.title</source>
      <translation>Profils</translation>
    </message>
    <message>
      <source>settings.save</source>
      <translation>Enregistrer les paramètres</translation>
    </message>
    <message>
      <source>settings.section.appearance</source>
      <translation>Apparence</translation>
    </message>
    <message>
      <source>settings.section.logic</source>
      <translation>Comportement de la minuterie</translation>
    </message>
    <message>
      <source>settings.section.notifications</source>
      <translation>Notifications</translation>
    </message>
    <message>
      <source>settings.section.overrun</source>
      <translation>Envahi</translation>
    </message>
    <message>
      <source>settings.section.profiles</source>
      <translation>Profils</translation>
    </message>
    <message>
      <source>settings.section.time</source>
      <translation>Temps</translation>
    </message>
    <message>
      <source>settings.section.tray</source>
      <translation>Plateau et démarrage automatique</translation>
    </message>
    <message>
      <source>settings.section.widget</source>
      <translation>Widget</translation>
    </message>
    <message>
      <source>settings.subtitle</source>
      <translation>Les modifications de thème et de widget s'appliquent immédiatement ; d'autres modifications s'appliquent après l'enregistrement.</translation>
    </message>
    <message>
      <source>settings.time.format</source>
      <translation>Format de l'heure</translation>
    </message>
    <message>
      <source>settings.time.long_break_minutes</source>
      <translation>Longue pause, minutes</translation>
    </message>
    <message>
      <source>settings.time.short_break_minutes</source>
      <translation>Courte pause, minutes</translation>
    </message>
    <message>
      <source>settings.time.subtitle</source>
      <translation>Les durées sont appliquées en toute sécurité lorsque vous enregistrez.</translation>
    </message>
    <message>
      <source>settings.time.title</source>
      <translation>Temps</translation>
    </message>
    <message>
      <source>settings.time.work_minutes</source>
      <translation>Travail, minutes</translation>
    </message>
    <message>
      <source>settings.title</source>
      <translation>Paramètres</translation>
    </message>
    <message>
      <source>settings.tray.autostart</source>
      <translation>Commencez avec Windows</translation>
    </message>
    <message>
      <source>settings.tray.autostart_current</source>
      <translation>Le démarrage automatique est activé et pointe vers le dossier actuel de l'application.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_disabled</source>
      <translation>Le démarrage automatique est désactivé.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_python</source>
      <translation>Exécuté à partir de Python : le démarrage automatique peut être activé dans la version EXE.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_stale</source>
      <translation>Le chemin de démarrage automatique est obsolète. Mettez-le à jour après avoir déplacé l'application.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_title</source>
      <translation>Démarrage automatique</translation>
    </message>
    <message>
      <source>settings.tray.close_to_tray</source>
      <translation>Réduire dans le bac lors de la fermeture</translation>
    </message>
    <message>
      <source>settings.tray.minimize_on_start</source>
      <translation>Réduire l'application après le lancement</translation>
    </message>
    <message>
      <source>settings.tray.subtitle</source>
      <translation>La barre d'état système s'exécute dans le thread partagé de l'interface graphique Qt.</translation>
    </message>
    <message>
      <source>settings.tray.title</source>
      <translation>Plateau et démarrage automatique</translation>
    </message>
    <message>
      <source>settings.tray.update_autostart</source>
      <translation>Mettre à jour le chemin de démarrage automatique</translation>
    </message>
    <message>
      <source>settings.widget.always_on_top</source>
      <translation>Toujours au premier plan</translation>
    </message>
    <message>
      <source>settings.widget.dialog_title</source>
      <translation>Widget</translation>
    </message>
    <message>
      <source>settings.widget.opacity</source>
      <translation>Opacité des widgets</translation>
    </message>
    <message>
      <source>settings.widget.opacity.description</source>
      <translation>Des valeurs inférieures rendent le widget plus transparent. Minimum — 5 %.</translation>
    </message>
    <message>
      <source>settings.widget.position_reset</source>
      <translation>La position du type actuel a été réinitialisée.</translation>
    </message>
    <message>
      <source>settings.widget.reset_position</source>
      <translation>Réinitialiser la position pour le type actuel</translation>
    </message>
    <message>
      <source>settings.widget.size</source>
      <translation>Taille</translation>
    </message>
    <message>
      <source>settings.widget.subtitle</source>
      <translation>La visibilité est contrôlée par le commutateur sur la page Minuterie.</translation>
    </message>
    <message>
      <source>settings.widget.title</source>
      <translation>Widget flottant</translation>
    </message>
    <message>
      <source>settings.widget.type</source>
      <translation>Type de widget</translation>
    </message>
    <message>
      <source>startup.already_running</source>
      <translation>Pomodoro Timer démarre ou est déjà en cours d'exécution. Attendez que la fenêtre s'ouvre ou utilisez l'application déjà ouverte.</translation>
    </message>
    <message>
      <source>startup.lock.already_running</source>
      <translation>Une autre instance d'application est déjà en cours d'exécution.</translation>
    </message>
    <message>
      <source>startup.lock.create_failed</source>
      <translation>Impossible de créer le verrou système (WinError {error_code}).</translation>
    </message>
    <message>
      <source>startup.lock.release_failed</source>
      <translation>Impossible de déverrouiller le système (WinError {error_code}).</translation>
    </message>
    <message>
      <source>startup.lock.secondary_close_failed</source>
      <translation>Une autre instance est déjà en cours d'exécution, mais son handle secondaire n'a pas pu être fermé (WinError {error_code}).</translation>
    </message>
    <message>
      <source>startup.lock.unsupported</source>
      <translation>Le verrouillage système à instance unique est pris en charge uniquement sous Windows.</translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_cycles</source>
      <translation>
        <numerusform>Cycle complet</numerusform>
        <numerusform>Cycles complets</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_long_breaks</source>
      <translation>
        <numerusform>Longue pause</numerusform>
        <numerusform>Longues pauses</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_short_breaks</source>
      <translation>
        <numerusform>Courte pause</numerusform>
        <numerusform>Courts séjours</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_work_periods</source>
      <translation>
        <numerusform>Période de travail</numerusform>
        <numerusform>Périodes de travail</numerusform>
      </translation>
    </message>
    <message>
      <source>stats.metric.long_break_overrun</source>
      <translation>Dépassement de longue pause</translation>
    </message>
    <message>
      <source>stats.metric.overwork_time</source>
      <translation>Temps de surmenage</translation>
    </message>
    <message>
      <source>stats.metric.rest_time</source>
      <translation>Temps de pause</translation>
    </message>
    <message>
      <source>stats.metric.short_break_overrun</source>
      <translation>Dépassement de courte pause</translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.skipped_periods</source>
      <translation>
        <numerusform>Période sautée</numerusform>
        <numerusform>Périodes sautées</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.timer_resets</source>
      <translation>
        <numerusform>Réinitialisation de la minuterie</numerusform>
        <numerusform>La minuterie se réinitialise</numerusform>
      </translation>
    </message>
    <message>
      <source>stats.metric.work_time</source>
      <translation>Temps de travail</translation>
    </message>
    <message>
      <source>stats.period.all_time</source>
      <translation>Tout le temps</translation>
    </message>
    <message>
      <source>stats.period.today</source>
      <translation>Aujourd'hui</translation>
    </message>
    <message>
      <source>stats.reset.action</source>
      <translation>Réinitialiser les statistiques</translation>
    </message>
    <message>
      <source>stats.reset.confirmation</source>
      <translation>Êtes-vous sûr de vouloir supprimer toutes les statistiques ?</translation>
    </message>
    <message>
      <source>stats.reset.title</source>
      <translation>Réinitialiser les statistiques</translation>
    </message>
    <message>
      <source>stats.subtitle</source>
      <translation>Le temps réglementaire et les dépassements sont suivis séparément.</translation>
    </message>
    <message>
      <source>stats.title</source>
      <translation>Statistiques</translation>
    </message>
    <message>
      <source>theme.appearance.dark</source>
      <translation>Sombre</translation>
    </message>
    <message>
      <source>theme.appearance.light</source>
      <translation>Clair</translation>
    </message>
    <message>
      <source>theme.contrast.accent</source>
      <translation>Texte d'accent / accent</translation>
    </message>
    <message>
      <source>theme.contrast.button</source>
      <translation>Texte du bouton / bouton</translation>
    </message>
    <message>
      <source>theme.contrast.long_break</source>
      <translation>Longue pause / carte</translation>
    </message>
    <message>
      <source>theme.contrast.long_break_overrun</source>
      <translation>Dépassement de pause longue / carte</translation>
    </message>
    <message>
      <source>theme.contrast.overwork</source>
      <translation>Surmenage / carte</translation>
    </message>
    <message>
      <source>theme.contrast.primary_card</source>
      <translation>Texte/carte principal</translation>
    </message>
    <message>
      <source>theme.contrast.secondary_card</source>
      <translation>Texte/carte secondaire</translation>
    </message>
    <message>
      <source>theme.contrast.short_break</source>
      <translation>Court séjour / carte</translation>
    </message>
    <message>
      <source>theme.contrast.short_break_overrun</source>
      <translation>Dépassement de courte pause / carte</translation>
    </message>
    <message>
      <source>theme.contrast.work</source>
      <translation>Travail / carte</translation>
    </message>
    <message>
      <source>theme.description.aurora</source>
      <translation>Des accents bleus et violets sympas</translation>
    </message>
    <message>
      <source>theme.description.comet</source>
      <translation>Palette neutre calme</translation>
    </message>
    <message>
      <source>theme.description.custom</source>
      <translation>Vos palettes claires et sombres indépendantes</translation>
    </message>
    <message>
      <source>theme.description.warm</source>
      <translation>Surfaces sablonneuses et chaudes</translation>
    </message>
    <message>
      <source>theme.name.aurora</source>
      <translation>Aurore</translation>
    </message>
    <message>
      <source>theme.name.comet</source>
      <translation>Comète</translation>
    </message>
    <message>
      <source>theme.name.custom</source>
      <translation>Personnalisé</translation>
    </message>
    <message>
      <source>theme.name.warm</source>
      <translation>Chaud</translation>
    </message>
    <message>
      <source>theme_editor.color.accent</source>
      <translation>Accent</translation>
    </message>
    <message>
      <source>theme_editor.color.accent_hover</source>
      <translation>Flotter</translation>
    </message>
    <message>
      <source>theme_editor.color.background</source>
      <translation>Contexte principal</translation>
    </message>
    <message>
      <source>theme_editor.color.border</source>
      <translation>Frontières</translation>
    </message>
    <message>
      <source>theme_editor.color.button_background</source>
      <translation>Couleur du bouton</translation>
    </message>
    <message>
      <source>theme_editor.color.button_text</source>
      <translation>Texte du bouton</translation>
    </message>
    <message>
      <source>theme_editor.color.card_background</source>
      <translation>Fond de carte</translation>
    </message>
    <message>
      <source>theme_editor.color.disabled</source>
      <translation>Éléments désactivés</translation>
    </message>
    <message>
      <source>theme_editor.color.error</source>
      <translation>Erreur</translation>
    </message>
    <message>
      <source>theme_editor.color.focus</source>
      <translation>Se concentrer</translation>
    </message>
    <message>
      <source>theme_editor.color.on_accent</source>
      <translation>Texte du bouton d'accentuation</translation>
    </message>
    <message>
      <source>theme_editor.color.secondary_background</source>
      <translation>Contexte secondaire</translation>
    </message>
    <message>
      <source>theme_editor.color.success</source>
      <translation>Succès</translation>
    </message>
    <message>
      <source>theme_editor.color.text_primary</source>
      <translation>Texte principal</translation>
    </message>
    <message>
      <source>theme_editor.color.text_secondary</source>
      <translation>Texte secondaire</translation>
    </message>
    <message>
      <source>theme_editor.color.warning</source>
      <translation>Avertissement</translation>
    </message>
    <message>
      <source>theme_editor.contrast.ok</source>
      <translation>Contrôle du contraste : les principales combinaisons répondent à la directive 4,5:1.</translation>
    </message>
    <message numerus="yes">
      <source>theme_editor.contrast.warning</source>
      <translation>
        <numerusform>Contrôle du contraste : la combinaison {count} est inférieure à 4,5 : 1. Une confirmation sera requise lors de la candidature.</numerusform>
        <numerusform>Contrôle du contraste : les combinaisons {count} sont inférieures à 4,5 : 1. Une confirmation sera requise lors de la candidature.</numerusform>
      </translation>
    </message>
    <message>
      <source>theme_editor.create_copy</source>
      <translation>Créer une copie</translation>
    </message>
    <message>
      <source>theme_editor.create_from</source>
      <translation>Créer à partir de</translation>
    </message>
    <message>
      <source>theme_editor.editing_mode</source>
      <translation>Mode en cours d'édition</translation>
    </message>
    <message>
      <source>theme_editor.group.service_states</source>
      <translation>Couleurs d'état</translation>
    </message>
    <message>
      <source>theme_editor.group.surfaces</source>
      <translation>Surfaces</translation>
    </message>
    <message>
      <source>theme_editor.group.text_controls</source>
      <translation>Texte et contrôles</translation>
    </message>
    <message>
      <source>theme_editor.group.timer_states</source>
      <translation>États de la minuterie</translation>
    </message>
    <message>
      <source>theme_editor.low_contrast.confirmation</source>
      <translation>Certaines combinaisons sont inférieures à 4,5:1 :

{details}

Enregistrer quand même ?</translation>
    </message>
    <message>
      <source>theme_editor.low_contrast.title</source>
      <translation>Faible contraste</translation>
    </message>
    <message>
      <source>theme_editor.reset.confirmation</source>
      <translation>Réinitialiser les deux modes sur le thème sécurisé Comet ?</translation>
    </message>
    <message>
      <source>theme_editor.reset.title</source>
      <translation>Réinitialiser le thème</translation>
    </message>
    <message>
      <source>theme_editor.reset_all</source>
      <translation>Réinitialiser tout le thème</translation>
    </message>
    <message>
      <source>theme_editor.reset_mode</source>
      <translation>Réinitialiser le mode actuel</translation>
    </message>
    <message>
      <source>theme_editor.subtitle</source>
      <translation>Modifiez les modes clair et sombre indépendamment.</translation>
    </message>
    <message>
      <source>theme_editor.title</source>
      <translation>Thème personnalisé</translation>
    </message>
    <message>
      <source>timer.mode.long_break</source>
      <translation>Longue pause</translation>
    </message>
    <message>
      <source>timer.mode.long_break_overrun</source>
      <translation>Longue pause prolongée</translation>
    </message>
    <message>
      <source>timer.mode.overwork</source>
      <translation>Prolongation du travail</translation>
    </message>
    <message>
      <source>timer.mode.short_break</source>
      <translation>Courte pause</translation>
    </message>
    <message>
      <source>timer.mode.short_break_overrun</source>
      <translation>Courte pause prolongée</translation>
    </message>
    <message>
      <source>timer.mode.work</source>
      <translation>Travail</translation>
    </message>
    <message>
      <source>timer.overrun.waiting_status</source>
      <translation>Période terminée : le dépassement est compté jusqu'à ce que vous continuiez</translation>
    </message>
    <message>
      <source>timer.page.subtitle</source>
      <translation>Une minuterie pour la fenêtre principale, les notifications et le widget.</translation>
    </message>
    <message>
      <source>timer.page.title</source>
      <translation>Séance de concentration</translation>
    </message>
    <message>
      <source>timer.status.accessible_name</source>
      <translation>Statut de la minuterie</translation>
    </message>
    <message>
      <source>timer.status.overrun</source>
      <translation>Le dépassement est comptabilisé</translation>
    </message>
    <message>
      <source>timer.status.paused</source>
      <translation>Minuterie en pause</translation>
    </message>
    <message>
      <source>timer.status.running</source>
      <translation>Minuterie en cours d'exécution</translation>
    </message>
    <message>
      <source>timer.status.stopped</source>
      <translation>Minuterie arrêtée</translation>
    </message>
    <message>
      <source>timer.widget.show</source>
      <translation>Afficher le widget</translation>
    </message>
    <message>
      <source>timer.widget.show.description</source>
      <translation>La position, la taille, le type et l'opacité sont enregistrés séparément.</translation>
    </message>
    <message>
      <source>toggle.accessible_description</source>
      <translation>ON — activé, OFF — désactivé</translation>
    </message>
    <message>
      <source>toggle.accessible_name</source>
      <translation>Changer</translation>
    </message>
    <message>
      <source>toggle.off</source>
      <translation>DÉSACTIVÉ</translation>
    </message>
    <message>
      <source>toggle.on</source>
      <translation>SUR</translation>
    </message>
    <message>
      <source>toggle.state.off</source>
      <translation>OFF, désactivé</translation>
    </message>
    <message>
      <source>toggle.state.on</source>
      <translation>ON, activé</translation>
    </message>
    <message>
      <source>tray.exit</source>
      <translation>Quitter</translation>
    </message>
    <message>
      <source>tray.hide</source>
      <translation>Masquer la fenêtre</translation>
    </message>
    <message>
      <source>tray.reset</source>
      <translation>Réinitialiser</translation>
    </message>
    <message>
      <source>tray.show</source>
      <translation>Afficher la fenêtre</translation>
    </message>
    <message>
      <source>tray.start_pause</source>
      <translation>Démarrer / Pause</translation>
    </message>
    <message numerus="yes">
      <source>widget.completed_work_periods</source>
      <translation>
        <numerusform>Période de travail terminée : {count}</numerusform>
        <numerusform>Périodes de travail complétées : {count}</numerusform>
      </translation>
    </message>
    <message>
      <source>widget.size.custom</source>
      <translation>Personnalisé</translation>
    </message>
    <message>
      <source>widget.size.large</source>
      <translation>Grand</translation>
    </message>
    <message>
      <source>widget.size.medium</source>
      <translation>Moyen</translation>
    </message>
    <message>
      <source>widget.size.small</source>
      <translation>Petit</translation>
    </message>
    <message>
      <source>widget.type.compact</source>
      <translation>Compact</translation>
    </message>
    <message>
      <source>widget.type.compact.description</source>
      <translation>Une carte compacte classique avec l'action principale.</translation>
    </message>
    <message>
      <source>widget.type.expanded</source>
      <translation>Étendu</translation>
    </message>
    <message>
      <source>widget.type.expanded.description</source>
      <translation>Informations sur le cycle et l'ensemble complet des actions du minuteur principal.</translation>
    </message>
    <message>
      <source>widget.type.micro</source>
      <translation>Micro</translation>
    </message>
    <message>
      <source>widget.type.micro.description</source>
      <translation>La plus petite fenêtre : généralement juste le temps.</translation>
    </message>
    <message>
      <source>widget.type.minimal</source>
      <translation>Minimal</translation>
    </message>
    <message>
      <source>widget.type.minimal.description</source>
      <translation>Grande heure, nom de l'état et détails minimes.</translation>
    </message>
    <message>
      <source>widget.type.ring</source>
      <translation>Anneau</translation>
    </message>
    <message>
      <source>widget.type.ring.description</source>
      <translation>Temps à l’intérieur d’un indicateur de période circulaire.</translation>
    </message>
    <message>
      <source>widget.type.row</source>
      <translation>Rangée</translation>
    </message>
    <message>
      <source>widget.type.row.description</source>
      <translation>Une ligne horizontale pour le bord de l'écran.</translation>
    </message>
    <message>
      <source>widget.type.scoreboard</source>
      <translation>Tableau d’affichage</translation>
    </message>
    <message>
      <source>widget.type.scoreboard.description</source>
      <translation>Grands chiffres à espacement fixe dans un style de tableau de bord calme.</translation>
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
      <translation>OK</translation>
    </message>
    <message>
      <source>Save</source>
      <translation>Enregistrer</translation>
    </message>
    <message>
      <source>Save All</source>
      <translation>Tout enregistrer</translation>
    </message>
    <message>
      <source>Open</source>
      <translation>Ouvrir</translation>
    </message>
    <message>
      <source>&amp;Yes</source>
      <translation>&amp;Oui</translation>
    </message>
    <message>
      <source>Yes to &amp;All</source>
      <translation>Oui pour &amp;tout</translation>
    </message>
    <message>
      <source>&amp;No</source>
      <translation>&amp;Non</translation>
    </message>
    <message>
      <source>N&amp;o to All</source>
      <translation>Non pour to&amp;us</translation>
    </message>
    <message>
      <source>Abort</source>
      <translation>Abandonner</translation>
    </message>
    <message>
      <source>Retry</source>
      <translation>Réessayer</translation>
    </message>
    <message>
      <source>Ignore</source>
      <translation>Ignorer</translation>
    </message>
    <message>
      <source>Close</source>
      <translation>Fermer</translation>
    </message>
    <message>
      <source>Cancel</source>
      <translation>Annuler</translation>
    </message>
    <message>
      <source>Discard</source>
      <translation>Ignorer les modifications</translation>
    </message>
    <message>
      <source>Help</source>
      <translation>Aide</translation>
    </message>
    <message>
      <source>Apply</source>
      <translation>Appliquer</translation>
    </message>
    <message>
      <source>Reset</source>
      <translation>Réinitialiser</translation>
    </message>
    <message>
      <source>Restore Defaults</source>
      <translation>Restaurer les valeurs par défaut</translation>
    </message>
  </context>
</TS>
