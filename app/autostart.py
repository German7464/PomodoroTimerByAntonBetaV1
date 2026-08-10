"""Autostart management for the current Windows user."""

from pathlib import Path
import sys
import winreg

from app.config import is_frozen_app


AUTOSTART_DISABLED = "disabled"
AUTOSTART_ENABLED_CURRENT = "enabled_current"
AUTOSTART_ENABLED_STALE = "enabled_stale"

RUN_KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
RUN_VALUE_NAME = "PomodoroTimerByAnton"


class AutostartService:
    """Uses HKCU Run without administrator rights or external shell commands."""

    def is_enabled(self) -> bool:
        """Returns True only when autostart points to the current exe."""
        return self.status() == AUTOSTART_ENABLED_CURRENT

    def status(self) -> str:
        """Checks HKCU Run: disabled, enabled for current exe, or stale."""
        command = self._read_run_value()
        if command is None:
            return AUTOSTART_DISABLED

        if is_frozen_app() and self._same_command(command, self._current_exe_command()):
            return AUTOSTART_ENABLED_CURRENT

        return AUTOSTART_ENABLED_STALE

    def set_enabled(self, enabled: bool) -> None:
        """Changes autostart only when the user explicitly toggles it."""
        if enabled:
            self.enable()
        else:
            self.disable()

    def enable(self) -> None:
        """Writes the current exe path to HKCU Run."""
        if not is_frozen_app():
            raise RuntimeError(
                "Автозапуск доступен только для собранной exe-версии. "
                "При запуске из Python включение автозапуска не выполняется.",
            )

        # HKCU is enough for per-user startup and does not require admin rights.
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, RUN_KEY_PATH) as key:
            winreg.SetValueEx(
                key,
                RUN_VALUE_NAME,
                0,
                winreg.REG_SZ,
                self._current_exe_command(),
            )

    def disable(self) -> None:
        """Removes this app's HKCU Run entry if it exists."""
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                RUN_KEY_PATH,
                0,
                winreg.KEY_SET_VALUE,
            ) as key:
                winreg.DeleteValue(key, RUN_VALUE_NAME)
        except FileNotFoundError:
            return

    def _read_run_value(self) -> str | None:
        """Reads this app's HKCU Run entry without changing the registry."""
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                RUN_KEY_PATH,
                0,
                winreg.KEY_QUERY_VALUE,
            ) as key:
                value, value_type = winreg.QueryValueEx(key, RUN_VALUE_NAME)
        except FileNotFoundError:
            return None

        if value_type not in (winreg.REG_SZ, winreg.REG_EXPAND_SZ) or not isinstance(value, str):
            return None
        return value

    def _current_exe_command(self) -> str:
        """Returns the quoted command that should be stored in HKCU Run."""
        return f'"{Path(sys.executable).resolve()}"'

    def _same_command(self, first: str, second: str) -> bool:
        """Compares Run commands by executable path, ignoring quote/case noise."""
        first_exe = self._extract_executable(first)
        second_exe = self._extract_executable(second)
        if first_exe is None or second_exe is None:
            return first.strip().lower() == second.strip().lower()

        try:
            return Path(first_exe).resolve() == Path(second_exe).resolve()
        except OSError:
            return first_exe.lower() == second_exe.lower()

    def _extract_executable(self, command: str) -> str | None:
        """Extracts executable path from a quoted or plain Run command."""
        command = command.strip()
        if not command:
            return None

        if command.startswith('"'):
            end_quote = command.find('"', 1)
            if end_quote == -1:
                return None
            return command[1:end_quote]

        return command.split(" ", 1)[0]
