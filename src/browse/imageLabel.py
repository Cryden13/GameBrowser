from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import (
    QPoint,
    QRect,
    Qt
)
from PyQt5.QtGui import (
    QBrush,
    QColor,
    QFont,
    QImage,
    QPainter,
    QPainterPath,
    QPen
)
from typing import Union as U
from pathlib import Path


class ImageLabel(QLabel):
    def __init__(self, image: U[Path, str], text: str, color: tuple):
        self._img = image
        self._text = text
        self._clr = color
        QLabel.__init__(self)
        self.setToolTip(f'<img src="{image}">')

    def paintEvent(self, _):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)

        img = QImage(str(self._img))
        image = img.scaled(170, 105)
        qp.drawImage(QPoint(), image)
        qp.fillRect(QRect(0, 0, 170, 105), QBrush(QColor(0, 0, 0, 95)))

        font = QFont()
        font.setFamily('Ebrima')
        font.setBold(True)
        font.setPointSize(11)
        qp.setFont(font)

        pen = QPen(Qt.black)
        pen.setWidth(2)
        ppth = QPainterPath()
        ppth.addText(3, 14, font, self._text)
        qp.strokePath(ppth, pen)
        qp.fillPath(ppth, QColor(*self._clr))

        qp.end()

    def updateData(self, image: U[Path, str] = None, text: str = None, color: tuple = None):
        if image:
            self._img = image
        if text:
            self._text = text
        if color:
            self._clr = color
        self.paintEvent('')
