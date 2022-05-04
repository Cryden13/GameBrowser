from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from pathlib import Path
from PyQt5.QtWidgets import (
    QDialog,
    QPushButton,
    QMainWindow
)
from typing import (
    TYPE_CHECKING,
    Optional as O
)

from .ui_picker import Ui_GamePickerDialog
from ..constants import PATH_ICON

if TYPE_CHECKING:
    from ..gamelibrary import GameLibrary


class GamePicker(Ui_GamePickerDialog):
    dlg: QDialog
    game_lib: "GameLibrary"
    gpths: dict[str, Path]
    gpath: O[Path] = None

    def __init__(self, parent: QMainWindow, game_lib: "GameLibrary", gpths: dict[str, Path]):
        self.game_lib = game_lib
        self.gpths = gpths
        self.dlg = QDialog(parent)
        self.dlg.setWindowIcon(QIcon(PATH_ICON))
        self.dlg.setWindowFlags(self.dlg.windowFlags() | Qt.WindowFlags(
            Qt.FramelessWindowHint))
        self.setupUi(self.dlg)
        self.fill()
        self.dlg.exec()

    def fill(self):
        for title, pth in self.gpths.items():
            btn = QPushButton(self.scrollAreaContents)
            btn.setText(title)
            btn.clicked.connect(lambda *_, p=pth: self.startGame(p))
            self.vLayout_contents.addWidget(btn)

    def startGame(self, gpath: Path):
        self.gpath = gpath
        self.dlg.close()
