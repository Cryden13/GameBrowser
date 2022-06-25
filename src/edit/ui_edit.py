# -*- coding: utf-8 -*-

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QDialogButtonBox,
    QPlainTextEdit,
    QSizePolicy,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFormLayout,
    QGridLayout,
    QScrollArea,
    QGroupBox,
    QLineEdit,
    QWidget,
    QDialog,
    QLabel,
    QFrame
)
from PyQt5.QtCore import (
    QMetaObject,
    QSize,
    QRect,
    Qt
)

from ..constants import *


class Ui_EditDialog(object):
    def setupUi(self, EditDialog: QDialog):
        EditDialog.setWindowTitle("Edit Game")
        EditDialog.setObjectName("EditDialog")
        EditDialog.setWindowModality(Qt.WindowModal)
        EditDialog.resize(EDIT_WD, EDIT_HT)
        sizePolicy = QSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            EditDialog.sizePolicy().hasHeightForWidth())
        EditDialog.setSizePolicy(sizePolicy)
        EditDialog.setMinimumSize(QSize(EDIT_WD, EDIT_HT))
        EditDialog.setMaximumSize(QSize(EDIT_WD, EDIT_HT))
        font = QFont()
        font.setFamily(FONT_FAMILY)
        font.setPointSize(FONT_SZ_DEFAULT)
        EditDialog.setFont(font)
        EditDialog.setStyleSheet(f"""\
QGroupBox {{
    color: #849db8;
    border: 1px solid #849db8;
    font-family: {FONT_FAMILY};
    font-size: {FONT_SZ_TITLE}pt;
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
}}
QLineEdit {{
    height: 1.5em;
    font-family: {FONT_FAMILY};
    font-size: {FONT_SZ_DEFAULT}pt;    
}}
QComboBox {{
    height: 1.5em;
    font-family: {FONT_FAMILY};
    font-size: {FONT_SZ_DEFAULT}pt;
}}
QCheckBox {{
    font-family: {FONT_FAMILY};
    font-size: {FONT_SZ_DEFAULT}pt;
}}
QPushButton {{
    color: #849db8;
    min-width: 6em;
    padding: 5px;
}}""")
        self.vLayout_addGame = QVBoxLayout(EditDialog)
        self.vLayout_addGame.setObjectName("vLayout_addGame")
        self.gBox_topPath = QGroupBox(EditDialog)
        self.gBox_topPath.setTitle("Top Path")
        sizePolicy = QSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.gBox_topPath.sizePolicy().hasHeightForWidth())
        self.gBox_topPath.setSizePolicy(sizePolicy)
        self.gBox_topPath.setObjectName("gBox_topPath")
        self.hLayout_topPath = QHBoxLayout(self.gBox_topPath)
        self.hLayout_topPath.setContentsMargins(0, 0, 0, 0)
        self.hLayout_topPath.setObjectName("hLayout_topPath")
        self.label_gamepath = QLabel(self.gBox_topPath)
        self.label_gamepath.setText("_gamepath_")
        sizePolicy = QSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_gamepath.sizePolicy().hasHeightForWidth())
        self.label_gamepath.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamily(FONT_FAMILY)
        font.setPointSize(FONT_SZ_HEADER)
        self.label_gamepath.setFont(font)
        self.label_gamepath.setStyleSheet(f"font-size: {FONT_SZ_HEADER}pt;")
        self.label_gamepath.setTextInteractionFlags(
            Qt.NoTextInteraction)
        self.label_gamepath.setObjectName("label_gamepath")
        self.hLayout_topPath.addWidget(self.label_gamepath)
        self.btn_open_game = QPushButton(self.gBox_topPath)
        self.btn_open_game.setText("Open")
        self.btn_open_game.setObjectName("btn_open_game")
        self.hLayout_topPath.addWidget(self.btn_open_game)
        self.btn_edit_game = QPushButton(self.gBox_topPath)
        self.btn_edit_game.setText("Edit")
        self.btn_edit_game.setObjectName("btn_edit_game")
        self.hLayout_topPath.addWidget(self.btn_edit_game)
        self.hLayout_topPath.setStretch(0, 1)
        self.vLayout_addGame.addWidget(self.gBox_topPath)

        self.gBox_url = QGroupBox(EditDialog)
        self.gBox_url.setTitle('URL')
        sizePolicy = QSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.gBox_url.sizePolicy().hasHeightForWidth())
        self.gBox_url.setSizePolicy(sizePolicy)
        self.gBox_url.setObjectName("gBox_url")

        self.hLayout_url = QHBoxLayout(self.gBox_url)
        self.hLayout_url.setSpacing(PAD)
        self.hLayout_url.setObjectName("hLayout_url")
        self.lineEdit_url = QLineEdit(self.gBox_url)
        self.lineEdit_url.setObjectName("lineEdit_url")
        self.hLayout_url.addWidget(self.lineEdit_url)
        self.btn_url_open = QPushButton(self.gBox_url)
        self.btn_url_open.setText("Open URL")
        self.btn_url_open.setObjectName("btn_url_open")
        self.hLayout_url.addWidget(self.btn_url_open)
        self.vLayout_addGame.addWidget(self.gBox_url)

        self.gBox_info = QGroupBox(EditDialog)
        self.gBox_info.setTitle("Info")
        sizePolicy = QSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.gBox_info.sizePolicy().hasHeightForWidth())
        self.gBox_info.setSizePolicy(sizePolicy)
        self.gBox_info.setObjectName("gBox_info")
        self.fLayout_info = QFormLayout(self.gBox_info)
        self.fLayout_info.setLabelAlignment(Qt.AlignCenter)
        self.fLayout_info.setFormAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.fLayout_info.setContentsMargins(PAD, PAD*2, 0, PAD)
        self.fLayout_info.setSpacing(PAD)
        self.fLayout_info.setObjectName("fLayout_info")

        self.btn_url_pull = QPushButton(self.gBox_info)
        self.btn_url_pull.setText("Auto-fill Info From URL")
        sizePolicy = QSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_url_pull.sizePolicy().hasHeightForWidth())
        self.btn_url_pull.setSizePolicy(sizePolicy)
        self.btn_url_pull.setObjectName("btn_url_pull")
        self.fLayout_info.addRow(self.btn_url_pull)

        self.label_title = QLabel(self.gBox_info)
        self.label_title.setText("Title:")
        self.label_title.setTextInteractionFlags(Qt.NoTextInteraction)
        self.label_title.setObjectName("label_title")
        self.fLayout_info.setWidget(
            1, QFormLayout.LabelRole, self.label_title)
        self.lineEdit_title = QLineEdit(self.gBox_info)
        self.lineEdit_title.setObjectName("lineEdit_title")
        self.fLayout_info.setWidget(
            1, QFormLayout.FieldRole, self.lineEdit_title)

        self.label_image = QLabel(self.gBox_info)
        self.label_image.setText("Image Path:")
        self.label_image.setTextInteractionFlags(Qt.NoTextInteraction)
        self.label_image.setObjectName("label_image")
        self.fLayout_info.setWidget(
            2, QFormLayout.LabelRole, self.label_image)
        self.hLayout_info_image = QHBoxLayout()
        self.hLayout_info_image.setSpacing(PAD)
        self.hLayout_info_image.setObjectName("hLayout_info_image")
        self.lineEdit_image = QLineEdit(self.gBox_info)
        self.lineEdit_image.setObjectName("lineEdit_image")
        self.hLayout_info_image.addWidget(self.lineEdit_image)
        self.btn_image_search = QPushButton(self.gBox_info)
        self.btn_image_search.setText("Search for image")
        self.btn_image_search.setObjectName("btn_image_search")
        self.hLayout_info_image.addWidget(self.btn_image_search)
        self.fLayout_info.setLayout(
            2, QFormLayout.FieldRole, self.hLayout_info_image)
        self.label_version = QLabel(self.gBox_info)
        self.label_version.setText("Version:")
        self.label_version.setTextInteractionFlags(Qt.NoTextInteraction)
        self.label_version.setObjectName("label_version")
        self.fLayout_info.setWidget(
            3, QFormLayout.LabelRole, self.label_version)
        self.lineEdit_version = QLineEdit(self.gBox_info)
        self.lineEdit_version.setObjectName("lineEdit_version")
        self.fLayout_info.setWidget(
            3, QFormLayout.FieldRole, self.lineEdit_version)
        self.label_progpths = QLabel(self.gBox_info)
        self.label_progpths.setText("Program Path(s):")
        self.label_progpths.setObjectName("label_progpths")
        self.fLayout_info.setWidget(
            4, QFormLayout.LabelRole, self.label_progpths)
        self.frame_progpths = QFrame(self.gBox_info)
        self.frame_progpths.setStyleSheet("QLineEdit {font-size: 8pt;}")
        self.frame_progpths.setFrameShape(QFrame.StyledPanel)
        self.frame_progpths.setFrameShadow(QFrame.Raised)
        self.frame_progpths.setObjectName("frame_progpths")
        self.vLayout_progpths = QVBoxLayout(self.frame_progpths)
        self.vLayout_progpths.setContentsMargins(0, 0, 0, 0)
        self.vLayout_progpths.setSpacing(PAD)
        self.vLayout_progpths.setObjectName("vLayout_progpths")
        self.gLayout_progpths_title = QGridLayout()
        self.gLayout_progpths_title.setObjectName("gLayout_progpths_title")

        self.label_progpths_path = QLabel(self.frame_progpths)
        self.label_progpths_path.setText("Executable Path")
        font = QFont()
        font.setFamily(FONT_FAMILY)
        font.setPointSize(FONT_SZ_DEFAULT)
        font.setUnderline(True)
        self.label_progpths_path.setFont(font)
        self.label_progpths_path.setAlignment(Qt.AlignCenter)
        self.label_progpths_path.setTextInteractionFlags(
            Qt.NoTextInteraction)
        self.label_progpths_path.setObjectName("label_progpths_path")
        self.gLayout_progpths_title.addWidget(
            self.label_progpths_path, 0, 1, 1, 1)

        self.label_progpths_name = QLabel(self.frame_progpths)
        self.label_progpths_name.setText("Viewable Name")
        font = QFont()
        font.setFamily(FONT_FAMILY)
        font.setPointSize(FONT_SZ_DEFAULT)
        font.setUnderline(True)
        self.label_progpths_name.setFont(font)
        self.label_progpths_name.setAlignment(Qt.AlignCenter)
        self.label_progpths_name.setTextInteractionFlags(
            Qt.NoTextInteraction)
        self.label_progpths_name.setObjectName("label_progpths_name")
        self.gLayout_progpths_title.addWidget(
            self.label_progpths_name, 0, 2, 1, 1)

        self.gLayout_progpths_title.setColumnStretch(1, 7)
        self.gLayout_progpths_title.setColumnStretch(2, 5)
        self.vLayout_progpths.addLayout(self.gLayout_progpths_title)

        self.scrollArea = QScrollArea(self.frame_progpths)
        self.scrollArea.setMinimumSize(QSize(0, 200))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 705, 606))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.vLayout_progpths_scrollArea = QVBoxLayout(
            self.scrollAreaWidgetContents)
        self.vLayout_progpths_scrollArea.setAlignment(Qt.AlignTop)
        self.vLayout_progpths_scrollArea.setContentsMargins(
            PAD*2, PAD*2, PAD*2, PAD*2)
        self.vLayout_progpths_scrollArea.setSpacing(0)
        self.vLayout_progpths_scrollArea.setObjectName(
            "vLayout_progpths_scrollArea")

        self.vLayout_progpths_scrollArea_items = QVBoxLayout()
        self.vLayout_progpths_scrollArea_items.setContentsMargins(0, 0, 0, 0)
        self.vLayout_progpths_scrollArea_items.setAlignment(Qt.AlignTop)
        self.vLayout_progpths_scrollArea_items.setSpacing(PAD)
        self.vLayout_progpths_scrollArea.setObjectName(
            "vLayout_progpths_scrollArea_items")
        self.vLayout_progpths_scrollArea.addLayout(
            self.vLayout_progpths_scrollArea_items)

        self.btn_progpths_add = QPushButton()
        self.btn_progpths_add.setText("Add row")
        sizePolicy = QSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_progpths_add.sizePolicy().hasHeightForWidth())
        self.btn_progpths_add.setSizePolicy(sizePolicy)
        self.btn_progpths_add.setObjectName("btn_progpths_add")
        self.vLayout_progpths_scrollArea.addWidget(self.btn_progpths_add)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.vLayout_progpths.addWidget(self.scrollArea)
        self.hLayout_progpths_btns = QHBoxLayout()
        self.hLayout_progpths_btns.setContentsMargins(0, 0, -1, -1)
        self.hLayout_progpths_btns.setObjectName("hLayout_progpths_btns")

        self.btn_progpths_browse = QPushButton(self.frame_progpths)
        self.btn_progpths_browse.setText("Browse for exe(s)...")
        sizePolicy = QSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_progpths_browse.sizePolicy().hasHeightForWidth())
        self.btn_progpths_browse.setSizePolicy(sizePolicy)
        self.btn_progpths_browse.setObjectName("btn_progpths_browse")
        self.hLayout_progpths_btns.addWidget(self.btn_progpths_browse)

        self.btn_progpths_find = QPushButton(self.frame_progpths)
        self.btn_progpths_find.setText("Auto search for exe(s)")
        sizePolicy = QSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_progpths_find.sizePolicy().hasHeightForWidth())
        self.btn_progpths_find.setSizePolicy(sizePolicy)
        self.btn_progpths_find.setObjectName("btn_progpths_find")
        self.hLayout_progpths_btns.addWidget(self.btn_progpths_find)

        self.vLayout_progpths.addLayout(self.hLayout_progpths_btns)
        self.fLayout_info.setWidget(
            4, QFormLayout.FieldRole, self.frame_progpths)
        self.label_description = QLabel(self.gBox_info)
        self.label_description.setText("Description:")
        self.label_description.setObjectName("label_description")
        self.fLayout_info.setWidget(
            6, QFormLayout.LabelRole, self.label_description)
        self.textEdit_description = QPlainTextEdit(self.gBox_info)
        self.textEdit_description.setMinimumSize(QSize(545, 111))
        self.textEdit_description.setMaximumSize(QSize(545, 111))
        font = QFont()
        font.setFamily(FONT_FAMILY)
        font.setPointSize(FONT_SZ_DEFAULT)
        self.textEdit_description.setFont(font)
        self.textEdit_description.setPlaceholderText("")
        self.textEdit_description.setObjectName("textEdit_description")
        self.fLayout_info.setWidget(
            6, QFormLayout.FieldRole, self.textEdit_description)
        self.vLayout_addGame.addWidget(self.gBox_info)
        self.gBox_categories = QGroupBox(EditDialog)
        self.gBox_categories.setTitle("Categories")
        self.gBox_categories.setStyleSheet(
            f"QGroupBox QGroupBox {{font-size: {FONT_SZ_DEFAULT}pt;}}")
        self.gBox_categories.setObjectName("gBox_categories")
        self.gLayout_categories = QGridLayout(self.gBox_categories)
        self.gLayout_categories.setContentsMargins(PAD, 0, PAD, PAD)
        self.gLayout_categories.setObjectName("gLayout_categories")
        self.vLayout_addGame.addWidget(self.gBox_categories)
        self.gBox_tags = QGroupBox(EditDialog)
        self.gBox_tags.setTitle("Tags")
        self.gBox_tags.setObjectName("gBox_tags")
        self.gLayout_tags = QGridLayout(self.gBox_tags)
        self.gLayout_tags.setObjectName("gLayout_tags")
        self.vLayout_addGame.addWidget(self.gBox_tags)
        self.buttonBox = QDialogButtonBox(EditDialog)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.vLayout_addGame.addWidget(self.buttonBox)

        QMetaObject.connectSlotsByName(EditDialog)
