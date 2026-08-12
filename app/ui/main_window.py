"""Главное окно приложения Pomodoro Timer на Tkinter."""

from collections.abc import Callable
import tkinter as tk
from tkinter import messagebox, ttk

from app.autostart import AutostartService
from app.config import APP_NAME, DATA_DIR_WARNING, SETTINGS_FILE, STATISTICS_FILE
from app.models import AppSettings
from app.notifications import NotificationService
from app.statistics import StatisticsService
from app.storage import load_app_settings, save_app_settings
from app.timer_engine import TimerEngine
from app.ui.help_window import HelpView
from app.ui.settings_window import SettingsView
from app.ui.stats_view import StatsView
from app.ui.tray import TrayController
from app.ui.widget_window import WidgetActions, WidgetWindow


class MainWindow:
    """Главное окно с таймером, статистикой, настройками, справкой и треем."""

    def __init__(self) -> None:
        """Создает интерфейс и общую логику приложения."""
        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.resizable(False, False)

        self.settings = load_app_settings(SETTINGS_FILE)
        self.autostart = AutostartService()

        self.timer = TimerEngine(self.settings)
        self.statistics = StatisticsService(STATISTICS_FILE)
        self.notifications = NotificationService(self.root, self.settings)
        self.widget_window = WidgetWindow(
            self.root,
            self.timer,
            self.settings,
            actions=WidgetActions(
                toggle_timer=self.toggle_timer_from_tray,
                continue_period=self.continue_manual_transition,
                skip_period=self.skip_period,
                reset_timer=self.reset,
                show_main_window=self.show_window,
            ),
            save_settings=lambda settings: save_app_settings(SETTINGS_FILE, settings),
            on_visibility_requested=self.set_widget_visibility,
            on_layout_changed=self._on_widget_layout_changed,
        )

        self.tray = TrayController(
            show_window=self._schedule(self.show_window),
            hide_window=self._schedule(self.hide_to_tray),
            toggle_timer=self._schedule(self.toggle_timer_from_tray),
            reset_timer=self._schedule(self.reset),
            exit_app=self._schedule(self.exit_app),
        )
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        timer_tab = ttk.Frame(notebook, padding=28)
        notebook.add(timer_tab, text="Таймер")

        self.stats_view = StatsView(notebook, self.statistics)
        notebook.add(self.stats_view, text="Статистика")

        self.settings_view = SettingsView(
            notebook,
            self.settings,
            self.apply_settings,
            self.autostart.status(),
        )
        notebook.add(self.settings_view, text="Настройки")

        self.help_view = HelpView(notebook)
        notebook.add(self.help_view, text="Справка")

        self.mode_label = ttk.Label(
            timer_tab,
            text=self.timer.mode_name(),
            font=("Segoe UI", 16, "bold"),
        )
        self.mode_label.pack(pady=(0, 8))

        self.time_label = ttk.Label(
            timer_tab,
            text=self.timer.formatted_time(),
            font=("Segoe UI", 48, "bold"),
        )
        self.time_label.pack(pady=(8, 10))

        self.status_label = ttk.Label(timer_tab, text="Таймер остановлен")
        self.status_label.pack(pady=(0, 18))

        controls = ttk.Frame(timer_tab)
        controls.pack()

        self.start_button = ttk.Button(controls, text="Старт", command=self.start)
        self.start_button.grid(row=0, column=0, padx=5)

        self.pause_button = ttk.Button(
            controls,
            text="Пауза",
            command=self.toggle_pause,
            state=tk.DISABLED,
        )
        self.pause_button.grid(row=0, column=1, padx=5)

        self.skip_button = ttk.Button(
            controls,
            text="Пропустить период",
            command=self.skip_period,
        )
        self.skip_button.grid(
            row=0,
            column=2,
            padx=5,
        )
        self.reset_button = ttk.Button(controls, text="Сброс", command=self.reset)
        self.reset_button.grid(row=0, column=3, padx=5)

        self.continue_button = ttk.Button(
            controls,
            text="Продолжить и начать следующий период",
            command=self.continue_manual_transition,
            state=tk.DISABLED,
        )
        self.continue_button.grid(row=1, column=0, columnspan=4, pady=(12, 0))

        self.widget_toggle_button = ttk.Button(
            controls,
            text="Показать виджет",
            command=self.toggle_widget_visibility,
        )
        self.widget_toggle_button.grid(
            row=2,
            column=0,
            columnspan=4,
            pady=(12, 0),
        )

        self.set_widget_visibility(self.settings.widget_enabled, persist=False)

        if DATA_DIR_WARNING:
            self.root.after(300, lambda: messagebox.showwarning("Portable-режим", DATA_DIR_WARNING))

    def run(self) -> None:
        """Запускает трей и цикл обработки событий Tkinter."""
        self.tray.start()
        self._schedule_tick()
        if self.settings.minimize_to_tray_on_start:
            self.root.after(200, self.hide_to_tray)
        self.root.mainloop()

    def start(self) -> None:
        """Запускает отсчет времени."""
        if not self.timer.start():
            self._refresh_labels()
            return
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL, text="Пауза")
        self._refresh_labels()

    def toggle_pause(self) -> None:
        """Ставит таймер на паузу или продолжает отсчет."""
        if not self.timer.toggle_pause():
            self._refresh_labels()
            return
        self._sync_timer_buttons()
        self._refresh_labels()

    def skip_period(self) -> None:
        """Пропускает текущий период Pomodoro."""
        skipped_mode = self.timer.skip_period()
        if skipped_mode is None:
            self._refresh_labels()
            return
        self.statistics.record_skipped_period(skipped_mode)
        self.stats_view.refresh()
        self._refresh_labels()

    def apply_settings(self, settings: AppSettings, autostart_changed: bool = False) -> None:
        """Сохраняет настройки и применяет их к текущему таймеру."""
        should_reset_timer = self._duration_settings_changed(settings)
        if autostart_changed:
            # Autostart changes HKCU Run, so it must happen only after an explicit user toggle.
            try:
                self.autostart.set_enabled(settings.autostart_enabled)
            except RuntimeError as error:
                messagebox.showwarning("Автозапуск", str(error))
                settings.autostart_enabled = self.settings.autostart_enabled
                self.settings_view.autostart_enabled_var.set(settings.autostart_enabled)

        self.settings_view.update_autostart_status(self.autostart.status())
        self.settings = settings
        self.timer.update_settings(settings)
        self.notifications.update_settings(settings)
        self.set_widget_visibility(settings.widget_enabled, persist=False)
        save_app_settings(SETTINGS_FILE, settings)
        if should_reset_timer and not self.timer.state.waiting_for_continue:
            self.timer.reset()
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED, text="Пауза")
        self._refresh_labels()

    def reset(self) -> None:
        """Сбрасывает таймер и обновляет подписи в окне."""
        if not self.timer.reset():
            self._refresh_labels()
            return
        self.statistics.record_reset()
        self.stats_view.refresh()
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED, text="Пауза")
        self._refresh_labels()

    def show_window(self) -> None:
        """Показывает главное окно из трея."""
        self._sync_widget_visibility()
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def hide_to_tray(self) -> None:
        """Скрывает главное окно, оставляя таймер, виджет и трей работать."""
        self.root.withdraw()

    def on_window_close(self) -> None:
        """Обрабатывает закрытие окна согласно настройке пользователя."""
        if self.settings.close_to_tray:
            self.hide_to_tray()
        else:
            self.exit_app()

    def exit_app(self) -> None:
        """Полностью завершает приложение и убирает иконку трея."""
        overrun = self.timer.finalize_overrun_on_exit()
        if overrun is not None:
            self.statistics.record_overrun(overrun.mode, overrun.duration_seconds)
        self.notifications.dismiss()
        self.tray.stop()
        self.root.destroy()

    def toggle_timer_from_tray(self) -> None:
        """Запускает или ставит таймер на паузу из меню трея."""
        if self.timer.state.waiting_for_continue:
            # Во время превышения команда трея не должна незаметно остановить
            # подсчет. Главное окно содержит явную кнопку продолжения.
            self.show_window()
            self._refresh_labels()
            return
        if self.timer.state.is_running:
            self.timer.pause()
        else:
            self.timer.start()
        self._sync_timer_buttons()
        self._refresh_labels()

    def toggle_widget_visibility(self) -> None:
        """Переключает виджет единственной пользовательской кнопкой."""
        self.set_widget_visibility(not self.widget_window.is_visible())

    def set_widget_visibility(self, visible: bool, *, persist: bool = True) -> bool:
        """Применяет, сохраняет и отражает единое состояние видимости виджета."""
        requested_visibility = bool(visible)
        self.settings.widget_enabled = requested_visibility
        error: Exception | None = None
        try:
            self.widget_window.apply_settings(self.settings)
            if self.widget_window.is_visible() != requested_visibility:
                raise RuntimeError("окно не перешло в запрошенное состояние")
        except Exception as caught_error:  # UI boundary: show must not stop the timer.
            error = caught_error
            if requested_visibility:
                self.widget_window.discard_window()

        actual_visibility = self.widget_window.is_visible()
        self.settings.widget_enabled = actual_visibility
        if persist or actual_visibility != requested_visibility:
            try:
                save_app_settings(SETTINGS_FILE, self.settings)
            except OSError as save_error:
                if error is None:
                    error = save_error
        self._sync_widget_visibility()

        if error is not None:
            action = "показать" if requested_visibility else "скрыть"
            messagebox.showwarning(
                "Виджет",
                f"Не удалось {action} виджет: {error}",
            )
            return False
        return True

    def _sync_widget_visibility(self) -> None:
        """Сверяет подпись кнопки и настройку с фактическим Toplevel."""
        visible = self.widget_window.is_visible()
        self.settings.widget_enabled = visible
        if hasattr(self, "widget_toggle_button"):
            self.widget_toggle_button.config(
                text="Скрыть виджет" if visible else "Показать виджет",
            )

    def _on_widget_layout_changed(self, settings: AppSettings) -> None:
        """Синхронизирует ручной размер с уже открытой формой настроек."""
        self.settings = settings
        if hasattr(self, "settings_view"):
            self.settings_view.sync_widget_layouts(settings)

    def continue_after_notification(self) -> None:
        """Продолжает таймер через общий обработчик кнопок уведомления и окна."""
        self.continue_manual_transition()

    def continue_manual_transition(self) -> None:
        """Один раз сохраняет превышение и запускает ожидающий период."""
        overrun = self.timer.continue_to_next_period()
        if overrun is None:
            self._refresh_labels()
            return

        self.statistics.record_overrun(overrun.mode, overrun.duration_seconds)
        self.notifications.dismiss()
        self.stats_view.refresh()
        self._sync_timer_buttons()
        self._refresh_labels()

    def _schedule_tick(self) -> None:
        """Обновляет таймер один раз в секунду через планировщик Tkinter."""
        completed_period = self.timer.tick()
        if completed_period is not None:
            self.statistics.record_completed_period(
                completed_period.mode,
                completed_period.duration_seconds,
                self.settings.use_long_break,
            )
            self.notifications.notify_period_finished(
                completed_period.mode,
                completed_period.next_mode,
                self.continue_after_notification,
            )
            self.stats_view.refresh()
        self._refresh_labels()
        self.root.after(1000, self._schedule_tick)

    def _refresh_labels(self) -> None:
        """Обновляет подписи в интерфейсе по текущему состоянию таймера."""
        self.mode_label.config(text=self.timer.mode_name())
        self.time_label.config(text=self.timer.formatted_time())
        self.widget_window.update()

        if self.timer.state.waiting_for_continue:
            self.status_label.config(
                text="Период завершен — превышение считается до продолжения",
            )
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.DISABLED, text="Пауза")
            self.skip_button.config(state=tk.DISABLED)
            self.reset_button.config(state=tk.DISABLED)
            self.continue_button.config(state=tk.NORMAL)
            return

        self.skip_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)
        self.continue_button.config(state=tk.DISABLED)
        if self.timer.state.is_running:
            self.status_label.config(text="Таймер запущен")
            self.pause_button.config(text="Пауза")
        elif str(self.pause_button["state"]) == tk.DISABLED:
            self.status_label.config(text="Таймер остановлен")
            self.pause_button.config(text="Пауза")
        else:
            self.status_label.config(text="Таймер на паузе")
            self.pause_button.config(text="Продолжить")

    def _sync_timer_buttons(self) -> None:
        """Синхронизирует кнопки после команд из трея."""
        if self.timer.state.waiting_for_continue:
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.DISABLED, text="Пауза")
            self.skip_button.config(state=tk.DISABLED)
            self.reset_button.config(state=tk.DISABLED)
            self.continue_button.config(state=tk.NORMAL)
            return

        self.skip_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)
        self.continue_button.config(state=tk.DISABLED)
        if self.timer.state.is_running:
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL, text="Пауза")
        else:
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.NORMAL, text="Продолжить")

    def _duration_settings_changed(self, new_settings: AppSettings) -> bool:
        """Проверяет, изменились ли длительности периодов таймера."""
        return (
            self.settings.work_minutes != new_settings.work_minutes
            or self.settings.short_break_minutes != new_settings.short_break_minutes
            or self.settings.long_break_minutes != new_settings.long_break_minutes
        )

    def _schedule(self, callback: Callable[[], None]) -> Callable[[], None]:
        """Безопасно выполняет команду трея в потоке Tkinter."""
        def wrapped() -> None:
            self.root.after(0, callback)

        return wrapped
