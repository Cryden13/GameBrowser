from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import (
    QDialogButtonBox,
    QVBoxLayout,
    QScrollArea,
    QDialog,
    QWidget,
    QLabel
)
from PyQt5.QtCore import (
    QMetaObject,
    QSize,
    QRect,
    Qt
)

from ..constants import *


class Ui_GamePickerDialog(object):
    def setupUi(self, GamePickerDialog: QDialog):
        GamePickerDialog.setWindowTitle("Game Picker")
        GamePickerDialog.setObjectName("GamePickerDialog")
        GamePickerDialog.setWindowModality(Qt.WindowModal)
        GamePickerDialog.resize(RUN_MAX_WD, RUN_MAX_HT)
        GamePickerDialog.setMinimumSize(QSize(RUN_MAX_WD, RUN_MAX_HT))
        font = QFont()
        font.setFamily(FONT_FAMILY)
        font.setPointSize(FONT_SZ_TITLE)
        GamePickerDialog.setFont(font)
        self.vLayout_main = QVBoxLayout(GamePickerDialog)
        self.vLayout_main.setContentsMargins(PAD, PAD, PAD, PAD)
        self.vLayout_main.setSpacing(PAD)
        self.vLayout_main.setObjectName("vLayout_main")
        self.label = QLabel(GamePickerDialog)
        self.label.setText("Pick an executable:")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setObjectName("label")
        self.vLayout_main.addWidget(self.label)
        self.scrollArea = QScrollArea(GamePickerDialog)
        self.scrollArea.setStyleSheet(
            f"QPushButton {{font-size: {FONT_SZ_TITLE}pt;}}")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaContents = QWidget()
        self.scrollAreaContents.setGeometry(QRect(0, 0, 392, 356))
        self.scrollAreaContents.setObjectName("scrollAreaContents")
        self.vLayout_contents = QVBoxLayout(self.scrollAreaContents)
        self.vLayout_contents.setContentsMargins(PAD, PAD, PAD, PAD)
        self.vLayout_contents.setSpacing(PAD)
        self.vLayout_contents.setObjectName("vLayout_contents")
        self.scrollArea.setWidget(self.scrollAreaContents)
        self.vLayout_main.addWidget(self.scrollArea)
        self.buttonBox = QDialogButtonBox(GamePickerDialog)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.vLayout_main.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(
            GamePickerDialog.accept)  # type: ignore
        self.buttonBox.rejected.connect(
            GamePickerDialog.reject)  # type: ignore
        QMetaObject.connectSlotsByName(GamePickerDialog)
