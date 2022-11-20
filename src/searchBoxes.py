from PyQt5.QtGui import QFont
from math import ceil
from PyQt5.QtWidgets import (
    QSizePolicy,
    QVBoxLayout,
    QGridLayout,
    QGroupBox,
    QComboBox,
    QCheckBox
)

from .constants import *


class SearchBoxes:
    row: int
    column: int
    parent: QGroupBox
    parent_layout: QGridLayout
    wrap_at: int

    def __init__(self, parent: QGroupBox, parent_layout: QGridLayout, total_count: int):
        self.parent = parent
        self.parent_layout = parent_layout
        if total_count <= 10:
            self.wrap_at = 10
        elif total_count <= 20:
            self.wrap_at = ceil(total_count / 2)
        else:
            self.wrap_at = ceil(total_count / 3)
        self.row = 0
        self.column = 0

    def _incrementColumn(self):
        self.column += 1
        if self.column == self.wrap_at:
            self.column = 0
            self.row += 1

    def createComboBox(self, title: str, contents: list[str]) -> QComboBox:
        # gBox
        gBox = QGroupBox(self.parent)
        gBox.setTitle(title)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(gBox.sizePolicy().hasHeightForWidth())
        gBox.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamily(FONT_FAMILY)
        font.setPointSize(FONT_SZ_DEFAULT)
        gBox.setFont(font)
        # layout
        vLayout = QVBoxLayout(gBox)
        vLayout.setContentsMargins(PAD, PAD, PAD, PAD)
        vLayout.setSpacing(PAD)
        # comboBox
        cmbBox = QComboBox(gBox)
        for item in contents:
            cmbBox.addItem(item)
        # add to layouts
        vLayout.addWidget(cmbBox)
        self.parent_layout.addWidget(gBox, self.row, self.column, 1, 1)
        # update row/col and return
        self._incrementColumn()
        return cmbBox

    def createCheckBox(self, text: str, tristate: bool = True) -> QCheckBox:
        # chkBox
        chkBox = QCheckBox(self.parent)
        chkBox.setTristate(tristate)
        chkBox.setText(text)
        # add to layout
        self.parent_layout.addWidget(chkBox, self.row, self.column, 1, 1)
        # update row/col and return
        self._incrementColumn()
        return chkBox
