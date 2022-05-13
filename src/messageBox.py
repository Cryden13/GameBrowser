from typing import Union as _U
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QMessageBox as _QMessageBox,
    QPushButton as _QPushButton
)

from .constants import PATH_ICON


class Messagebox:
    _btnTable = {'ok': _QMessageBox.Ok,
                 'open': _QMessageBox.Open,
                 'save': _QMessageBox.Save,
                 'cancel': _QMessageBox.Cancel,
                 'close': _QMessageBox.Close,
                 'yes': _QMessageBox.Yes,
                 'no': _QMessageBox.No,
                 'abort': _QMessageBox.Abort,
                 'retry': _QMessageBox.Retry,
                 'ignore': _QMessageBox.Ignore}
    _btntext: str = None

    def __init__(self, icon, title: str, message: str, buttons: tuple[str, ...]):
        mbox = _QMessageBox()
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

    def _buttonClicked(self, btn: _QPushButton):
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
        mbox = cls(icon=_QMessageBox.Question,
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
        mbox = cls(icon=[_QMessageBox.Information, _QMessageBox.Warning, _QMessageBox.Critical][errorlevel],
                   title=title,
                   message=message,
                   buttons=buttons)
        return mbox._btntext


if __name__ == '__main__':
    from subprocess import run
    from pathlib import Path
    pth = Path(__file__).parents[1]
    run(['py', '-m', pth.name], cwd=pth.parent)
    raise SystemExit
