# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (
    QWidget,
    QSizePolicy,
    QHBoxLayout,
    QPushButton,
    QLineEdit
)
from PyQt5.QtCore import (
    QSize,
    QMetaObject
)

from ..constants import *


class Ui_ProgramPath(object):
    def setupUi(self, ProgramPath: QWidget):
        ProgramPath.setObjectName("ProgramPath")
        ProgramPath.setStyleSheet("QPushButton {min-width: 1em;}")
        self.hLayout = QHBoxLayout(ProgramPath)
        self.hLayout.setContentsMargins(PAD*2, PAD*2, PAD*2, PAD*2)
        self.hLayout.setObjectName("hLayout")

        self.btn_add = QPushButton(ProgramPath)
        self.btn_add.setText('+')
        self.btn_add.setMaximumSize(QSize(25, 25))
        self.btn_add.setObjectName("btn_add")
        self.hLayout.addWidget(self.btn_add)

        self.lineEdit_exe = QLineEdit(ProgramPath)
        sizePolicy = QSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(7)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lineEdit_exe.sizePolicy().hasHeightForWidth())
        self.lineEdit_exe.setSizePolicy(sizePolicy)
        self.lineEdit_exe.setObjectName("lineEdit_exe")
        self.hLayout.addWidget(self.lineEdit_exe)

        self.lineEdit_name = QLineEdit(ProgramPath)
        sizePolicy = QSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lineEdit_name.sizePolicy().hasHeightForWidth())
        self.lineEdit_name.setSizePolicy(sizePolicy)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.hLayout.addWidget(self.lineEdit_name)

        self.btn_rem = QPushButton(ProgramPath)
        self.btn_rem.setText('-')
        self.btn_rem.setMaximumSize(QSize(25, 25))
        self.btn_rem.setObjectName("btn_rem")
        self.hLayout.addWidget(self.btn_rem)

        QMetaObject.connectSlotsByName(ProgramPath)
