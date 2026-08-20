"""Встроенная справка профессионального Qt-интерфейса."""

from PySide6.QtWidgets import QDialog, QTextBrowser, QVBoxLayout, QWidget

from app.ui.components import PageHeader
from app.i18n import localization_manager, tr
from app.ui.design_system import TOKENS
from app.ui.icons import application_icon
from app.ui.qt_app import fit_window_to_available_screen


class HelpView(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(TOKENS.spacing.xl, TOKENS.spacing.xl, TOKENS.spacing.xl, TOKENS.spacing.xl)
        layout.setSpacing(TOKENS.spacing.lg)
        layout.addWidget(PageHeader("help.title", "help.subtitle", self))
        self.browser = QTextBrowser(self)
        self.browser.setOpenExternalLinks(True)
        self.browser.setMarkdown(tr("help.content"))
        layout.addWidget(self.browser, 1)
        localization_manager().language_changed.connect(self._retranslate_ui)

    def _retranslate_ui(self, _language_code: str) -> None:
        self.browser.setMarkdown(tr("help.content"))


class HelpWindow(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("help.title"))
        self.setWindowIcon(application_icon())
        fit_window_to_available_screen(
            self, parent, preferred=(760, 620), minimum=(560, 420),
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(HelpView(self))
        localization_manager().language_changed.connect(self._retranslate_ui)

    def _retranslate_ui(self, _language_code: str) -> None:
        self.setWindowTitle(tr("help.title"))
