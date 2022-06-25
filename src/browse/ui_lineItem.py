# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (
    QWidget,
    QSizePolicy,
    QHBoxLayout,
    QGroupBox,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QPlainTextEdit,
    QApplication
)
from PyQt5.QtCore import (
    Qt,
    QSize,
    QMetaObject
)
from PyQt5.QtGui import (
    QFont,
    QCursor
)

from ..constants import *


class Ui_LineItem(object):
    def setupUi(self, LineItem: QWidget):
        LineItem.setWindowTitle("Line Item")
        LineItem.setObjectName("LineItem")
        LineItem.setWindowModality(Qt.WindowModal)
        LineItem.resize(1295, 130)
        sizePolicy = QSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LineItem.sizePolicy().hasHeightForWidth())
        LineItem.setSizePolicy(sizePolicy)
        LineItem.setMinimumSize(QSize(1300, 130))
        font = QFont()
        font.setFamily(FONT_FAMILY)
        font.setPointSize(FONT_SZ_DEFAULT)
        LineItem.setFont(font)
        LineItem.setStyleSheet(f"""\
QGroupBox {{
    color: {TEXT_COLORS.default};
    border: 1px solid {TEXT_COLORS.default};
    font-size: {FONT_SZ_SMALL}pt;
    font-family: {FONT_FAMILY};
    text-decoration: underline;
    padding: {PAD*2}px {PAD}px {PAD}px {PAD}px;
    margin-top: 0.5em;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: {GBOX_POSITION};
    left: {GBOX_OFFSET};
}}
QLabel {{
    font-family: {FONT_FAMILY};
    font-size: {FONT_SZ_DEFAULT}pt;
}}""")
        self.hLayout_lineitem = QHBoxLayout(LineItem)
        self.hLayout_lineitem.setContentsMargins(0, 0, 0, 0)
        self.hLayout_lineitem.setSpacing(PAD)
        self.hLayout_lineitem.setObjectName("hLayout_lineitem")

        self.gBox_tools = QGroupBox(LineItem)
        self.gBox_tools.setTitle("Tools")
        sizePolicy = QSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.gBox_tools.sizePolicy().hasHeightForWidth())
        self.gBox_tools.setSizePolicy(sizePolicy)
        self.gBox_tools.setObjectName("gBox_tools")
        self.verticalLayout = QVBoxLayout(self.gBox_tools)
        self.verticalLayout.setContentsMargins(PAD, PAD, PAD, PAD)
        self.verticalLayout.setObjectName("verticalLayout")

        self.btn_tools_play = QPushButton(self.gBox_tools)
        self.btn_tools_play.setText("▶")
        self.btn_tools_play.setMinimumSize(QSize(30, 30))
        self.btn_tools_play.setMaximumSize(QSize(30, 30))
        self.btn_tools_play.setCursor(
            QCursor(Qt.PointingHandCursor))
        self.btn_tools_play.setStyleSheet(f"""\
QPushButton {{
    background-color: springGreen;
    color: black;
    font-size: 30px;
    border: 1px solid black;
    border-radius: 15px;
    padding-left: 3px;
    padding-bottom: 3px;
}}
QPushButton::hover {{
    background-color: LimeGreen;
}}""")
        self.btn_tools_play.setObjectName("btn_tools_play")
        self.verticalLayout.addWidget(self.btn_tools_play)

        self.btn_tools_web = QPushButton(self.gBox_tools)
        self.btn_tools_web.setText("www")
        self.btn_tools_web.setMinimumSize(QSize(30, 30))
        self.btn_tools_web.setMaximumSize(QSize(30, 30))
        self.btn_tools_web.setCursor(
            QCursor(Qt.PointingHandCursor))
        self.btn_tools_web.setStyleSheet(f"""\
QPushButton {{
    background-color: LightSkyBlue;
    color: black;
    font-size: 10px;
    border: 1px solid black;
    border-radius: 15px;
}}
QPushButton::hover {{
    background-color: SteelBlue;
}}""")
        self.btn_tools_web.setObjectName("btn_tools_web")
        self.verticalLayout.addWidget(self.btn_tools_web)

        self.btn_tools_edit = QPushButton(self.gBox_tools)
        self.btn_tools_edit.setText("edit")
        self.btn_tools_edit.setMinimumSize(QSize(30, 30))
        self.btn_tools_edit.setMaximumSize(QSize(30, 30))
        self.btn_tools_edit.setCursor(
            QCursor(Qt.PointingHandCursor))
        self.btn_tools_edit.setStyleSheet(f"""\
QPushButton {{
    background-color: tan;
    color: black;
    font-size: 12px;
    border: 1px solid black;
    border-radius: 15px;
    padding-bottom: 2px;
}}
QPushButton::hover {{
    background-color: sienna;
}}""")
        self.btn_tools_edit.setObjectName("btn_tools_edit")
        self.verticalLayout.addWidget(self.btn_tools_edit)
        self.hLayout_lineitem.addWidget(self.gBox_tools)

        self.gBox_title = QGroupBox(LineItem)
        self.gBox_title.setTitle("Title")
        sizePolicy = QSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.gBox_title.sizePolicy().hasHeightForWidth())
        self.gBox_title.setSizePolicy(sizePolicy)
        self.gBox_title.setMinimumSize(QSize(203, 0))
        self.gBox_title.setObjectName("gBox_title")
        self.vLayout_title = QVBoxLayout(self.gBox_title)
        self.vLayout_title.setContentsMargins(PAD, 0, PAD, 0)
        self.vLayout_title.setSpacing(0)
        self.vLayout_title.setObjectName("vLayout_title")
        self.hLayout_lineitem.addWidget(self.gBox_title)

        self.gBox_version = QGroupBox(LineItem)
        self.gBox_version.setTitle("Version")
        sizePolicy = QSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.gBox_version.sizePolicy().hasHeightForWidth())
        self.gBox_version.setSizePolicy(sizePolicy)
        self.gBox_version.setObjectName("gBox_version")
        self.vLayout_version = QVBoxLayout(self.gBox_version)
        self.vLayout_version.setContentsMargins(PAD, 0, PAD, 0)
        self.vLayout_version.setSpacing(0)
        self.vLayout_version.setObjectName("vLayout_version")
        self.label_version = QLabel(self.gBox_version)
        self.label_version.setText("_version_")
        sizePolicy = QSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_version.sizePolicy().hasHeightForWidth())
        self.label_version.setSizePolicy(sizePolicy)
        self.label_version.setMinimumSize(QSize(75, 0))
        self.label_version.setMaximumSize(QSize(75, 16777215))
        self.label_version.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_version.setWordWrap(True)
        self.label_version.setTextInteractionFlags(
            Qt.TextSelectableByMouse)
        self.label_version.setObjectName("label_version")
        self.vLayout_version.addWidget(self.label_version)
        self.hLayout_lineitem.addWidget(self.gBox_version)

        self.gBox_categories = QGroupBox(LineItem)
        self.gBox_categories.setTitle("Categories")
        sizePolicy = QSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.gBox_categories.sizePolicy().hasHeightForWidth())
        self.gBox_categories.setSizePolicy(sizePolicy)
        self.gBox_categories.setObjectName("gBox_categories")
        self.vLayout_categories = QVBoxLayout(self.gBox_categories)
        self.vLayout_categories.setContentsMargins(PAD, 0, PAD, 0)
        self.vLayout_categories.setSpacing(0)
        self.vLayout_categories.setObjectName("vLayout_categories")
        self.label_category = QLabel(self.gBox_categories)
        self.label_category.setText("_categories_")
        sizePolicy = QSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_category.sizePolicy().hasHeightForWidth())
        self.label_category.setSizePolicy(sizePolicy)
        self.label_category.setMinimumSize(QSize(150, 0))
        self.label_category.setMaximumSize(QSize(150, 16777215))
        self.label_category.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_category.setWordWrap(True)
        self.label_category.setTextInteractionFlags(
            Qt.TextSelectableByMouse)
        self.label_category.setObjectName("label_category")
        self.vLayout_categories.addWidget(self.label_category)
        self.hLayout_lineitem.addWidget(self.gBox_categories)

        self.gBox_tags = QGroupBox(LineItem)
        self.gBox_tags.setTitle("Tags")
        sizePolicy = QSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.gBox_tags.sizePolicy().hasHeightForWidth())
        self.gBox_tags.setSizePolicy(sizePolicy)
        self.gBox_tags.setObjectName("gBox_tags")
        self.vLayout_tags = QVBoxLayout(self.gBox_tags)
        self.vLayout_tags.setContentsMargins(PAD, 0, PAD, 0)
        self.vLayout_tags.setSpacing(0)
        self.vLayout_tags.setObjectName("vLayout_tags")
        self.label_tags = QLabel(self.gBox_tags)
        self.label_tags.setText("_tags_")
        sizePolicy = QSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_tags.sizePolicy().hasHeightForWidth())
        self.label_tags.setSizePolicy(sizePolicy)
        self.label_tags.setMinimumSize(QSize(200, 0))
        self.label_tags.setMaximumSize(QSize(200, 16777215))
        self.label_tags.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_tags.setWordWrap(True)
        self.label_tags.setTextInteractionFlags(
            Qt.TextSelectableByMouse)
        self.label_tags.setObjectName("label_tags")
        self.vLayout_tags.addWidget(self.label_tags)
        self.hLayout_lineitem.addWidget(self.gBox_tags)

        self.gBox_description = QGroupBox(LineItem)
        self.gBox_description.setTitle("GroupBox")
        self.gBox_description.setObjectName("gBox_description")
        self.vLayout_description = QVBoxLayout(self.gBox_description)
        self.vLayout_description.setContentsMargins(PAD, 0, PAD, 0)
        self.vLayout_description.setSpacing(0)
        self.vLayout_description.setObjectName("vLayout_description")
        self.textEdit_description = QPlainTextEdit(
            self.gBox_description)
        sizePolicy = QSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.textEdit_description.sizePolicy().hasHeightForWidth())
        self.textEdit_description.setSizePolicy(sizePolicy)
        self.textEdit_description.setMaximumSize(QSize(16777215, 111))
        font = QFont()
        font.setFamily(FONT_FAMILY)
        font.setPointSize(FONT_SZ_DEFAULT)
        self.textEdit_description.setFont(font)
        self.textEdit_description.setReadOnly(True)
        self.textEdit_description.setObjectName("textEdit_description")
        self.vLayout_description.addWidget(self.textEdit_description)
        self.hLayout_lineitem.addWidget(self.gBox_description)

        QMetaObject.connectSlotsByName(LineItem)


if __name__ == "__main__":
    from sys import argv, exit
    app = QApplication(argv)
    LineItem = QWidget()
    ui = Ui_LineItem()
    ui.setupUi(LineItem)
    LineItem.show()
    exit(app.exec_())
