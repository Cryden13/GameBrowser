# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Cryden\Desktop\PyQt5\ui_picker.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GamePickerDialog(object):
    def setupUi(self, GamePickerDialog):
        GamePickerDialog.setObjectName("GamePickerDialog")
        GamePickerDialog.setWindowModality(QtCore.Qt.WindowModal)
        GamePickerDialog.resize(400, 420)
        GamePickerDialog.setMinimumSize(QtCore.QSize(400, 420))
        font = QtGui.QFont()
        font.setFamily("Ebrima")
        font.setPointSize(12)
        GamePickerDialog.setFont(font)
        self.vLayout_main = QtWidgets.QVBoxLayout(GamePickerDialog)
        self.vLayout_main.setContentsMargins(3, 3, 3, 3)
        self.vLayout_main.setSpacing(3)
        self.vLayout_main.setObjectName("vLayout_main")
        self.label = QtWidgets.QLabel(GamePickerDialog)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.vLayout_main.addWidget(self.label)
        self.scrollArea = QtWidgets.QScrollArea(GamePickerDialog)
        self.scrollArea.setStyleSheet("QPushButton {\n"
                                      "    font-size: 12pt;\n"
                                      "}")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaContents = QtWidgets.QWidget()
        self.scrollAreaContents.setGeometry(QtCore.QRect(0, 0, 392, 356))
        self.scrollAreaContents.setObjectName("scrollAreaContents")
        self.vLayout_contents = QtWidgets.QVBoxLayout(self.scrollAreaContents)
        self.vLayout_contents.setContentsMargins(3, 3, 3, 3)
        self.vLayout_contents.setSpacing(3)
        self.vLayout_contents.setObjectName("vLayout_contents")
        self.scrollArea.setWidget(self.scrollAreaContents)
        self.vLayout_main.addWidget(self.scrollArea)
        self.buttonBox = QtWidgets.QDialogButtonBox(GamePickerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.vLayout_main.addWidget(self.buttonBox)

        self.retranslateUi(GamePickerDialog)
        self.buttonBox.accepted.connect(
            GamePickerDialog.accept)  # type: ignore
        self.buttonBox.rejected.connect(
            GamePickerDialog.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(GamePickerDialog)

    def retranslateUi(self, GamePickerDialog):
        _translate = QtCore.QCoreApplication.translate
        GamePickerDialog.setWindowTitle(
            _translate("GamePickerDialog", "Dialog"))
        self.label.setText(_translate(
            "GamePickerDialog", "Pick an executable:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    GamePickerDialog = QtWidgets.QDialog()
    ui = Ui_GamePickerDialog()
    ui.setupUi(GamePickerDialog)
    GamePickerDialog.show()
    sys.exit(app.exec_())