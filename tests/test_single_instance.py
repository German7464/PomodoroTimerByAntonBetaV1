"""Системная блокировка и раннее поведение точки входа."""

import os
from pathlib import Path
import subprocess
import sys
import time
import unittest
from uuid import uuid4

import main as entrypoint
from app.single_instance import (
    ALREADY_RUNNING_MESSAGE,
    SingleInstanceError,
    SingleInstanceLock,
)


class FakeLock:
    """Управляемая блокировка для теста точки входа без Tkinter."""

    def __init__(self, acquired: bool = True, error: Exception | None = None) -> None:
        self.result = acquired
        self.error = error
        self.release_calls = 0

    def acquire(self) -> bool:
        if self.error is not None:
            raise self.error
        return self.result

    def release(self) -> None:
        self.release_calls += 1


class FakeWindow:
    """Окно без Tk, считающее запуск цикла."""

    def __init__(self) -> None:
        self.run_calls = 0

    def run(self) -> None:
        self.run_calls += 1


class EntryPointTests(unittest.TestCase):
    """Проверяет, что второй процесс не доходит до фабрики интерфейса."""

    def test_already_running_message_matches_user_contract(self) -> None:
        self.assertEqual(
            ALREADY_RUNNING_MESSAGE,
            "Pomodoro Timer уже запускается или уже запущен. "
            "Дождитесь открытия окна либо используйте уже открытое приложение.",
        )

    def test_first_instance_runs_ui_and_releases_lock(self) -> None:
        lock = FakeLock(acquired=True)
        window = FakeWindow()
        messages: list[tuple[str, bool]] = []

        result = entrypoint.main(
            lock_factory=lambda: lock,
            window_factory=lambda: window,
            message_function=lambda message, error=False: messages.append((message, error)),
        )

        self.assertEqual(result, 0)
        self.assertEqual(window.run_calls, 1)
        self.assertEqual(lock.release_calls, 1)
        self.assertEqual(messages, [])

    def test_second_instance_shows_message_without_starting_ui(self) -> None:
        lock = FakeLock(acquired=False)
        window_calls = 0
        messages: list[tuple[str, bool]] = []

        def create_window() -> FakeWindow:
            nonlocal window_calls
            window_calls += 1
            return FakeWindow()

        result = entrypoint.main(
            lock_factory=lambda: lock,
            window_factory=create_window,
            message_function=lambda message, error=False: messages.append((message, error)),
        )

        self.assertEqual(result, 0)
        self.assertEqual(window_calls, 0)
        self.assertEqual(lock.release_calls, 0)
        self.assertEqual(messages, [(ALREADY_RUNNING_MESSAGE, False)])

    def test_lock_error_is_reported_and_does_not_start_ui(self) -> None:
        lock = FakeLock(error=SingleInstanceError("mutex failed"))
        window_calls = 0
        messages: list[tuple[str, bool]] = []

        def create_window() -> FakeWindow:
            nonlocal window_calls
            window_calls += 1
            return FakeWindow()

        result = entrypoint.main(
            lock_factory=lambda: lock,
            window_factory=create_window,
            message_function=lambda message, error=False: messages.append((message, error)),
        )

        self.assertEqual(result, 1)
        self.assertEqual(window_calls, 0)
        self.assertEqual(messages, [("mutex failed", True)])


@unittest.skipUnless(os.name == "nt", "Именованный mutex проверяется в Windows")
class WindowsMutexTests(unittest.TestCase):
    """Проверяет реальный kernel mutex без Tkinter."""

    def test_first_acquires_second_is_rejected_then_release_allows_next(self) -> None:
        name = f"Local\\PomodoroTimerByAnton.Tests.{uuid4().hex}"
        first = SingleInstanceLock(name)
        second = SingleInstanceLock(name)
        third = SingleInstanceLock(name)

        try:
            self.assertTrue(first.acquire())
            self.assertFalse(second.acquire())
            first.release()
            self.assertTrue(third.acquire())
        finally:
            first.release()
            second.release()
            third.release()

    def test_process_termination_does_not_leave_permanent_lock(self) -> None:
        name = f"Local\\PomodoroTimerByAnton.Tests.{uuid4().hex}"
        project_root = Path(__file__).resolve().parent.parent
        script = (
            "import sys, time; "
            "from app.single_instance import SingleInstanceLock; "
            "lock=SingleInstanceLock(sys.argv[1]); "
            "assert lock.acquire(); "
            "print('ready', flush=True); "
            "time.sleep(30)"
        )
        process = subprocess.Popen(
            [sys.executable, "-c", script, name],
            cwd=project_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        competing = SingleInstanceLock(name)
        recovered = SingleInstanceLock(name)
        try:
            self.assertEqual(process.stdout.readline().strip(), "ready")
            self.assertFalse(competing.acquire())
            process.terminate()
            process.wait(timeout=10)

            deadline = time.monotonic() + 5
            while time.monotonic() < deadline:
                if recovered.acquire():
                    break
                time.sleep(0.05)
            self.assertTrue(recovered.acquired)
        finally:
            if process.poll() is None:
                process.terminate()
                process.wait(timeout=10)
            if process.stdout is not None:
                process.stdout.close()
            if process.stderr is not None:
                process.stderr.close()
            competing.release()
            recovered.release()


if __name__ == "__main__":
    unittest.main()
