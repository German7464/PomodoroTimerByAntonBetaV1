"""Системная блокировка единственного экземпляра приложения в Windows."""

from __future__ import annotations

import ctypes
from ctypes import wintypes
import getpass
import hashlib
import os
from pathlib import Path
import sys
from typing import Final


ERROR_ALREADY_EXISTS: Final = 183
MESSAGE_BOX_OK: Final = 0x00000000
MESSAGE_BOX_ICON_INFORMATION: Final = 0x00000040
MESSAGE_BOX_ICON_ERROR: Final = 0x00000010
MESSAGE_BOX_SET_FOREGROUND: Final = 0x00010000

ALREADY_RUNNING_KEY: Final = "startup.already_running"
# Kept as a compatibility-only public constant for integrations released before
# startup messages became locale-aware. The entry point itself uses the key.
ALREADY_RUNNING_MESSAGE: Final = (
    "Pomodoro Timer уже запускается или уже запущен. "
    "Дождитесь открытия окна либо используйте уже открытое приложение."
)


class SingleInstanceError(RuntimeError):
    """Системную блокировку не удалось создать или освободить."""

    def __init__(self, key: str, **parameters: object) -> None:
        super().__init__(key)
        self.key = key
        self.parameters = parameters


def default_mutex_name() -> str:
    """Строит стабильное имя mutex, изолированное для текущего пользователя."""
    identity = "|".join(
        (
            os.environ.get("USERDOMAIN", ""),
            getpass.getuser(),
            str(Path.home()),
        ),
    ).casefold()
    user_digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:16]
    return f"Local\\PomodoroTimerByAnton.SingleInstance.{user_digest}"


class SingleInstanceLock:
    """Удерживает именованный Windows mutex до явного release или конца процесса."""

    def __init__(self, name: str | None = None) -> None:
        self.name = name or default_mutex_name()
        self._handle: int | None = None

    @property
    def acquired(self) -> bool:
        """Показывает, удерживает ли этот объект созданный handle."""
        return self._handle is not None

    def acquire(self) -> bool:
        """Возвращает True первому экземпляру и False при существующем mutex."""
        if self._handle is not None:
            return True
        if os.name != "nt":
            raise SingleInstanceError(
                "startup.lock.unsupported",
            )

        kernel32 = _kernel32()
        ctypes.set_last_error(0)
        handle = kernel32.CreateMutexW(None, False, self.name)
        if not handle:
            error_code = ctypes.get_last_error()
            raise SingleInstanceError(
                "startup.lock.create_failed",
                error_code=error_code,
            )

        error_code = ctypes.get_last_error()
        if error_code == ERROR_ALREADY_EXISTS:
            if not kernel32.CloseHandle(handle):
                close_error = ctypes.get_last_error()
                raise SingleInstanceError(
                    "startup.lock.secondary_close_failed",
                    error_code=close_error,
                )
            return False

        self._handle = int(handle)
        return True

    def release(self) -> None:
        """Закрывает handle; при аварии ОС выполняет то же автоматически."""
        if self._handle is None:
            return
        handle = self._handle
        kernel32 = _kernel32()
        if not kernel32.CloseHandle(handle):
            error_code = ctypes.get_last_error()
            raise SingleInstanceError(
                "startup.lock.release_failed",
                error_code=error_code,
            )
        self._handle = None

    def __enter__(self) -> "SingleInstanceLock":
        if not self.acquire():
            raise SingleInstanceError("startup.lock.already_running")
        return self

    def __exit__(self, *_args: object) -> None:
        self.release()


def show_native_message(message: str, *, error: bool = False) -> None:
    """Показывает сообщение до создания Qt GUI; вне Windows пишет в stderr."""
    if os.name != "nt":
        print(message, file=sys.stderr)
        return

    try:
        user32 = ctypes.WinDLL("user32", use_last_error=True)
        user32.MessageBoxW.argtypes = (
            wintypes.HWND,
            wintypes.LPCWSTR,
            wintypes.LPCWSTR,
            wintypes.UINT,
        )
        user32.MessageBoxW.restype = ctypes.c_int
        icon = MESSAGE_BOX_ICON_ERROR if error else MESSAGE_BOX_ICON_INFORMATION
        result = user32.MessageBoxW(
            None,
            message,
            "Pomodoro Timer",
            MESSAGE_BOX_OK | icon | MESSAGE_BOX_SET_FOREGROUND,
        )
        if result == 0:
            raise ctypes.WinError(ctypes.get_last_error())
    except OSError:
        print(message, file=sys.stderr)


def _kernel32() -> ctypes.WinDLL:
    """Настраивает используемые WinAPI-функции и их типы."""
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateMutexW.argtypes = (
        wintypes.LPVOID,
        wintypes.BOOL,
        wintypes.LPCWSTR,
    )
    kernel32.CreateMutexW.restype = wintypes.HANDLE
    kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel32.CloseHandle.restype = wintypes.BOOL
    return kernel32
