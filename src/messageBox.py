from typing import Union as _U
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QDialogButtonBox,
    QVBoxLayout,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QCheckBox,
    QDialog,
    QWidget
)

from .constants import PATH_ICON


class Messagebox:
    _btnTable = {'ok': QMessageBox.Ok,
                 'open': QMessageBox.Open,
                 'save': QMessageBox.Save,
                 'cancel': QMessageBox.Cancel,
                 'close': QMessageBox.Close,
                 'yes': QMessageBox.Yes,
                 'no': QMessageBox.No,
                 'abort': QMessageBox.Abort,
                 'retry': QMessageBox.Retry,
                 'ignore': QMessageBox.Ignore}
    _btntext: str = None

    def __init__(self, icon, title: str, message: str, buttons: tuple[str, ...]):
        mbox = QMessageBox()
        mbox.setIcon(icon)
        mbox.setWindowIcon(QIcon(PATH_ICON))
        mbox.setWindowTitle(title)
        mbox.setText(message)
        btns = 0
        for btn in buttons:
            btns |= self._btnTable.get(btn.lower(), 0)
        mbox.setStandardButtons(btns)
        mbox.buttonClicked.connect(self._buttonClicked)
        mbox.exec()

    def _buttonClicked(self, btn: QPushButton):
        self._btntext = btn.text().strip('&')

    @classmethod
    def askquestion(cls, title: str, message: str, buttons: tuple[str, ...] = ('Yes', 'No')) -> _U[str, None]:
        """-----
        Ask a question and return the response

        Parameters
        ----------
        title (str): the messagebox window's title 

        message (str): the messagebox body text 

        buttons (tuple[str, ...], optional): [default=('Yes', 'No')] the buttons to show. Any combination of ok, open, save, cancel, close, yes, no, abort, retry, ignore


        Returns:
        --------
        str | None : the text of the pressed response, or None if the window was closed
        """
        mbox = cls(icon=QMessageBox.Question,
                   title=title,
                   message=message,
                   buttons=buttons)
        return mbox._btntext

    @classmethod
    def showinfo(cls, title: str, message: str, buttons: tuple[str, ...] = ('Ok',), errorlevel=0) -> _U[str, None]:
        """-----
        Shows a simple information window

        Parameters
        ----------
        title (str): the messagebox window's title 

        message (str): the messagebox body text 

        buttons (tuple[str, ...], optional): [default=('Ok')] the buttons to show. Any combination of ok, open, save, cancel, close, yes, no, abort, retry, ignore

        errorlevel (int, optional): [default=0] the errorlevel. 0 for information, 1 for warning, 2 for critical


        Returns:
        --------
        str | None : the text of the pressed response, or None if the window was closed
        """
        mbox = cls(icon=[QMessageBox.Information, QMessageBox.Warning, QMessageBox.Critical][errorlevel],
                   title=title,
                   message=message,
                   buttons=buttons)
        return mbox._btntext


class SelectDialog:
    dlg: QDialog
    ans: list[str]
    fields: dict[str, QCheckBox]

    def __init__(self, parent: QWidget, title: str, fields: tuple[str]):
        self.dlg = QDialog(parent)
        self.dlg.setWindowTitle(title)
        # set defaults
        self.ans = list()
        font = self.dlg.font()
        font.setPointSize(11)
        self.dlg.setFont(font)
        # construct layouts
        main_layout = QVBoxLayout(self.dlg)
        scrl = QScrollArea(self.dlg)
        scrl.setWidgetResizable(True)
        contents = QWidget()
        contents.setStyleSheet('background-color: #2d3640;')
        scrl.setWidget(contents)
        layout = QVBoxLayout(contents)
        layout.setSpacing(8)
        main_layout.addWidget(scrl)
        # construct widgets
        self.fields = dict()
        for lbl in fields:
            cbx = QCheckBox(parent=contents, text=lbl)
            if lbl[:-3] in fields:
                cbx.setChecked(False)
            else:
                cbx.setChecked(True)
            self.fields.update({lbl: cbx})
            layout.addWidget(cbx)
        # construct buttonbox
        btnbox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        btnbox.accepted.connect(self.submit)
        btnbox.rejected.connect(self.dlg.close)
        btnbox.setCenterButtons(True)
        main_layout.addWidget(btnbox)
        # run
        self.dlg.exec()

    def submit(self):
        self.ans = [lbl for lbl, cbx in self.fields.items()
                    if cbx.isChecked()]
        self.dlg.close()
