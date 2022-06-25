# -*- coding: utf-8 -*-

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QGroupBox,
    QGridLayout,
    QPushButton,
    QTabWidget,
    QScrollArea,
    QMenuBar,
    QMenu,
    QAction,
    QApplication
)
from PyQt5.QtCore import (
    QSize,
    Qt,
    QRect,
    QMetaObject
)

from ..constants import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow: QMainWindow):
        MainWindow.setWindowTitle("Browse Games")
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(MAIN_WD, MAIN_HT)
        MainWindow.setMinimumSize(QSize(MAIN_WD, MAIN_HT))
        MainWindow.setMaximumSize(QSize(MAIN_WD, MAIN_HT))
        font = QFont()
        font.setFamily(FONT_FAMILY)
        font.setPointSize(FONT_SZ_DEFAULT)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(f"""\
QGroupBox {{
    color: #849db8;
    border: 1px solid #849db8;
    font-family: {FONT_FAMILY};
    padding: {PAD*2}px {PAD}px {PAD}px {PAD}px;
    margin-top: 1em;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: {GBOX_POSITION};
    left: {GBOX_OFFSET};
}}""")

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.vLayout_centralwidget = QVBoxLayout(self.centralwidget)
        self.vLayout_centralwidget.setContentsMargins(PAD, PAD, PAD, PAD)
        self.vLayout_centralwidget.setSpacing(PAD)
        self.vLayout_centralwidget.setObjectName("vLayout_centralwidget")

        self.hLayout_search = QHBoxLayout()
        self.hLayout_search.setSpacing(0)
        self.hLayout_search.setObjectName("hLayout_search")
        spacerItem = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hLayout_search.addItem(spacerItem)
        self.gBox_search = QGroupBox(self.centralwidget)
        self.gBox_search.setTitle("Search")
        sizePolicy = QSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.gBox_search.sizePolicy().hasHeightForWidth())
        self.gBox_search.setSizePolicy(sizePolicy)
        self.gBox_search.setMinimumSize(
            QSize(SEARCH_MIN_WD, SEARCH_MIN_HT))
        font = QFont()
        font.setFamily(FONT_FAMILY)
        font.setPointSize(FONT_SZ_MAX)
        font.setBold(True)
        font.setWeight(75)
        self.gBox_search.setFont(font)
        self.gBox_search.setStyleSheet(f"""\
QComboBox {{
    font-size: {FONT_SZ_DEFAULT}pt;
    font-family: {FONT_FAMILY};
    height: 1.5em;
}}
QCheckBox {{
    font-size: {FONT_SZ_DEFAULT}pt;
    font-family: {FONT_FAMILY};
}}
QPushButton {{color: #849db8;}}""")
        self.gBox_search.setObjectName("gBox_search")

        self.vLayout_gbox_search = QVBoxLayout(self.gBox_search)
        self.vLayout_gbox_search.setContentsMargins(PAD, PAD*3, PAD, PAD)
        self.vLayout_gbox_search.setSpacing(PAD)
        self.vLayout_gbox_search.setObjectName("vLayout_gbox_search")

        self.gBox_search_categories = QGroupBox(self.gBox_search)
        self.gBox_search_categories.setTitle("Categories")
        font = QFont()
        font.setFamily(FONT_FAMILY)
        font.setPointSize(FONT_SZ_HEADER)
        self.gBox_search_categories.setFont(font)
        self.gBox_search_categories.setObjectName("gBox_search_categories")
        self.gLayout_search_categories = QGridLayout(
            self.gBox_search_categories)
        self.gLayout_search_categories.setContentsMargins(PAD, PAD*2, PAD, PAD)
        self.gLayout_search_categories.setObjectName(
            "gLayout_search_categories")
        self.vLayout_gbox_search.addWidget(self.gBox_search_categories)

        self.gBox_search_tags = QGroupBox(self.gBox_search)
        self.gBox_search_tags.setTitle("Tags")
        font = QFont()
        font.setFamily(FONT_FAMILY)
        font.setPointSize(FONT_SZ_HEADER)
        self.gBox_search_tags.setFont(font)
        self.gBox_search_tags.setObjectName("gBox_search_tags")
        self.gLayout_search_tags = QGridLayout(self.gBox_search_tags)
        self.gLayout_search_tags.setContentsMargins(PAD, PAD, PAD, PAD)
        self.gLayout_search_tags.setSpacing(PAD)
        self.gLayout_search_tags.setObjectName("gLayout_search_tags")
        self.vLayout_gbox_search.addWidget(self.gBox_search_tags)
        self.hLayout_search_btns = QHBoxLayout()
        self.hLayout_search_btns.setSpacing(0)
        self.hLayout_search_btns.setObjectName("hLayout_search_btns")

        self.btn_search_clear = QPushButton("Clear", self.gBox_search)
        sizePolicy = QSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_search_clear.sizePolicy().hasHeightForWidth())
        self.btn_search_clear.setSizePolicy(sizePolicy)
        self.btn_search_clear.setObjectName("btn_search_clear")
        self.hLayout_search_btns.addWidget(self.btn_search_clear)

        self.btn_search_search = QPushButton("Search", self.gBox_search)
        sizePolicy = QSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_search_search.sizePolicy().hasHeightForWidth())
        self.btn_search_search.setSizePolicy(sizePolicy)
        self.btn_search_search.setObjectName("btn_search_search")
        self.hLayout_search_btns.addWidget(self.btn_search_search)
        self.vLayout_gbox_search.addLayout(self.hLayout_search_btns)
        self.hLayout_search.addWidget(self.gBox_search)
        spacerItem1 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hLayout_search.addItem(spacerItem1)
        self.vLayout_centralwidget.addLayout(self.hLayout_search)

        self.tabWidget = QTabWidget(self.centralwidget)
        font = QFont()
        font.setFamily(FONT_FAMILY)
        font.setPointSize(FONT_SZ_TITLE)
        self.tabWidget.setFont(font)
        self.tabWidget.setTabShape(QTabWidget.Triangular)
        self.tabWidget.setObjectName("tabWidget")

        (self.tab_rPlayed,
         self.hLayout_tab_rPlayed,
         self.scrollArea_tab_rPlayed,
         self.scrollAreaContents_tab_rPlayed,
         self.vLayout_tab_rPlayed) = self.createTab(tab_name='rPlayed',
                                                    tab_title='Recently Played')

        (self.tab_rUpdated,
         self.hLayout_tab_rUpdated,
         self.scrollArea_tab_rUpdated,
         self.scrollAreaContents_tab_rUpdated,
         self.vLayout_tab_rUpdated) = self.createTab(tab_name="rUpdated",
                                                     tab_title="Recently Updated")

        (self.tab_rAdded,
         self.hLayout_tab_rAdded,
         self.scrollArea_tab_rAdded,
         self.scrollAreaContents_tab_rAdded,
         self.vLayout_tab_rAdded) = self.createTab(tab_name="rAdded",
                                                   tab_title="Recently Added")

        (self.tab_numA,
         self.hLayout_tab_numA,
         self.scrollArea_tab_numA,
         self.scrollAreaContents_tab_numA,
         self.vLayout_tab_numA) = self.createTab(tab_name="numA",
                                                 tab_title="#-A")

        (self.tab_BC,
         self.hLayout_tab_BC,
         self.scrollArea_tab_BC,
         self.scrollAreaContents_tab_BC,
         self.vLayout_tab_BC) = self.createTab(tab_name="BC",
                                               tab_title="B-C")

        (self.tab_DE,
         self.hLayout_tab_DE,
         self.scrollArea_tab_DE,
         self.scrollAreaContents_tab_DE,
         self.vLayout_tab_DE) = self.createTab(tab_name="DE",
                                               tab_title="D-E")

        (self.tab_FG,
         self.hLayout_tab_FG,
         self.scrollArea_tab_FG,
         self.scrollAreaContents_tab_FG,
         self.vLayout_tab_FG) = self.createTab(tab_name="FG",
                                               tab_title="F-G")

        (self.tab_HI,
         self.hLayout_tab_HI,
         self.scrollArea_tab_HI,
         self.scrollAreaContents_tab_HI,
         self.vLayout_tab_HI) = self.createTab(tab_name="HI",
                                               tab_title="H-I")

        (self.tab_JK,
         self.hLayout_tab_JK,
         self.scrollArea_tab_JK,
         self.scrollAreaContents_tab_JK,
         self.vLayout_tab_JK) = self.createTab(tab_name="JK",
                                               tab_title="J-K")

        (self.tab_LM,
         self.hLayout_tab_LM,
         self.scrollArea_tab_LM,
         self.scrollAreaContents_tab_LM,
         self.vLayout_tab_LM) = self.createTab(tab_name="LM",
                                               tab_title="L-M")

        (self.tab_NO,
         self.hLayout_tab_NO,
         self.scrollArea_tab_NO,
         self.scrollAreaContents_tab_NO,
         self.vLayout_tab_NO) = self.createTab(tab_name="NO",
                                               tab_title="N-O")

        (self.tab_PQR,
         self.hLayout_tab_PQR,
         self.scrollArea_tab_PQR,
         self.scrollAreaContents_tab_PQR,
         self.vLayout_tab_PQR) = self.createTab(tab_name="PQR",
                                                tab_title="P-R")

        (self.tab_ST,
         self.hLayout_tab_ST,
         self.scrollArea_tab_ST,
         self.scrollAreaContents_tab_ST,
         self.vLayout_tab_ST) = self.createTab(tab_name="ST",
                                               tab_title="S-T")

        (self.tab_UV,
         self.hLayout_tab_UV,
         self.scrollArea_tab_UV,
         self.scrollAreaContents_tab_UV,
         self.vLayout_tab_UV) = self.createTab(tab_name="UV",
                                               tab_title="U-V")

        (self.tab_WXYZ,
         self.hLayout_tab_WXYZ,
         self.scrollArea_tab_WXYZ,
         self.scrollAreaContents_tab_WXYZ,
         self.vLayout_tab_WXYZ) = self.createTab(tab_name="WXYZ",
                                                 tab_title="W-Z")

        self.vLayout_centralwidget.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, MAIN_WD, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.menu_new_games = QMenu("New Games", self.menubar)
        self.menu_new_games.setObjectName("menu_new_games")
        self.menubar.addAction(self.menu_new_games.menuAction())

        self.menuAction_check = QAction("Check for new games", MainWindow)
        self.menuAction_check.setObjectName("menuAction_check")
        self.menu_new_games.addAction(self.menuAction_check)

        self.menuAction_add = QAction("Add a new game", MainWindow)
        self.menuAction_add.setObjectName("menuAction_add")
        self.menu_new_games.addAction(self.menuAction_add)

        self.menuAction_add_bundle = QAction(
            "Add a new game from a bundle", MainWindow)
        self.menuAction_add_bundle.setObjectName("menuAction_add_bundle")
        self.menu_new_games.addAction(self.menuAction_add_bundle)

        self.menu_verify = QMenu("Verify", self.menubar)
        self.menu_verify.setObjectName("menu_verify")
        self.menubar.addAction(self.menu_verify.menuAction())

        self.menuAction_verify_tags = QAction("Tags", MainWindow)
        self.menuAction_verify_tags.setObjectName("menuAction_verify_tags")
        self.menu_verify.addAction(self.menuAction_verify_tags)

        self.menuAction_verify_exes = QAction("Executables", MainWindow)
        self.menuAction_verify_exes.setObjectName("menuAction_verify_exes")
        self.menu_verify.addAction(self.menuAction_verify_exes)

        self.tabWidget.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(MainWindow)

    def createTab(self, tab_name: str, tab_title: str) -> tuple[QWidget, QHBoxLayout, QScrollArea, QWidget, QVBoxLayout]:
        tab = QWidget()
        tab.setObjectName(f"tab_{tab_name}")

        hLayout = QHBoxLayout(tab)
        hLayout.setContentsMargins(0, 0, 0, 0)
        hLayout.setSpacing(0)
        hLayout.setObjectName(f"hLayout_tab_{tab_name}")

        scrollArea = QScrollArea(tab)
        scrollArea.setWidgetResizable(True)
        scrollArea.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        scrollArea.setObjectName(f"scrollArea_tab_{tab_name}")

        scrollAreaContents = QWidget()
        scrollAreaContents.setGeometry(QRect(0, 0, 98, 28))
        scrollAreaContents.setObjectName(
            f"scrollAreaContents_tab_{tab_name}")

        vLayout = QVBoxLayout(scrollAreaContents)
        vLayout.setContentsMargins(PAD, PAD, PAD, PAD)
        vLayout.setSpacing(PAD)
        vLayout.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        vLayout.setObjectName(f"vLayout_tab_{tab_name}")

        scrollArea.setWidget(scrollAreaContents)
        hLayout.addWidget(scrollArea)
        self.tabWidget.addTab(tab, tab_title)
        return (tab, hLayout, scrollArea, scrollAreaContents, vLayout)


if __name__ == "__main__":
    from sys import argv, exit
    app = QApplication(argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    exit(app.exec_())
