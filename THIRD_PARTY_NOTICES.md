# Third-party notices

PomodoroTimerByAnton uses the following open-source components at runtime:

- **PySide6-Essentials 6.11.1** and **shiboken6 6.11.1**, distributed by the Qt Company under `LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only`. This project selects the LGPL option, uses the unmodified dynamically linked Windows libraries, and does not use GPL-only Qt modules. License texts and source-offer information are available in the PySide6 distribution and at <https://www.qt.io/licensing/open-source-lgpl-obligations>.
- **Qt 6.11.1** libraries bundled through PySide6-Essentials under their respective LGPL-compatible terms. Component notices supplied by Qt remain in the PySide6 runtime distribution.

Development/build tooling:

- **PyInstaller 6.22.0**, `GPL-2.0-or-later` with the PyInstaller bootloader exception permitting distribution of the resulting application.

Project-authored SVG interface icons under `assets/icons/` are dedicated under **CC0-1.0**; see `assets/icons/LICENSE.md`.

No Pillow, pystray, GPL-only Qt module, paid UI kit, proprietary icon pack, or external font is required by the migrated interface.
