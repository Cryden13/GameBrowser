from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QGroupBox,
    QVBoxLayout,
    QGridLayout,
    QComboBox,
    QCheckBox,
    QSizePolicy
)


class SearchBoxes:
    row: int
    column: int
    parent: QGroupBox
    parent_layout: QGridLayout

    def __init__(self, parent: QGroupBox, parent_layout: QGridLayout):
        self.parent = parent
        self.parent_layout = parent_layout
        self.row = 0
        self.column = 0

    def _incrementColumn(self):
        self.column += 1
        if self.column == 10:
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
        font.setFamily("Ebrima")
        font.setPointSize(10)
        gBox.setFont(font)
        # layout
        vLayout = QVBoxLayout(gBox)
        vLayout.setContentsMargins(3, 3, 3, 3)
        vLayout.setSpacing(3)
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
