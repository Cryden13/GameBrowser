# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

from ..constants import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(MAIN_WD, MAIN_HT)
        MainWindow.setMinimumSize(QtCore.QSize(MAIN_WD, MAIN_HT))
        MainWindow.setMaximumSize(QtCore.QSize(MAIN_WD, MAIN_HT))
        font = QtGui.QFont()
        font.setFamily("Ebrima")
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("QGroupBox {\n"
                                 "    color: #849db8;\n"
                                 "    border: 1px solid #849db8;\n"
                                 "    font-family: Ebrima;\n"
                                 "    padding: 6px 3px 3px 3px;\n"
                                 "    margin-top: 1em;\n"
                                 "}\n"
                                 "QGroupBox::title {\n"
                                 "    subcontrol-origin: margin;\n"
                                 "    subcontrol-position: left top;\n"
                                 "    left: 8px;\n"
                                 "}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.vLayout_centralwidget = QtWidgets.QVBoxLayout(self.centralwidget)
        self.vLayout_centralwidget.setContentsMargins(3, 3, 3, 3)
        self.vLayout_centralwidget.setSpacing(3)
        self.vLayout_centralwidget.setObjectName("vLayout_centralwidget")
        self.hLayout_search = QtWidgets.QHBoxLayout()
        self.hLayout_search.setSpacing(0)
        self.hLayout_search.setObjectName("hLayout_search")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hLayout_search.addItem(spacerItem)
        self.gBox_search = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.gBox_search.sizePolicy().hasHeightForWidth())
        self.gBox_search.setSizePolicy(sizePolicy)
        self.gBox_search.setMinimumSize(QtCore.QSize(1000, 250))
        font = QtGui.QFont()
        font.setFamily("Ebrima")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.gBox_search.setFont(font)
        self.gBox_search.setStyleSheet("QComboBox {\n"
                                       "    font-size: 10pt;\n"
                                       "    font-family: Ebrima;\n"
                                       "    height: 1.5em;\n"
                                       "}\n"
                                       "QCheckBox {\n"
                                       "    font-size: 10pt;\n"
                                       "    font-family: Ebrima;\n"
                                       "}\n"
                                       "QPushButton {color: #849db8;}")
        self.gBox_search.setObjectName("gBox_search")
        self.vLayout_gbox_search = QtWidgets.QVBoxLayout(self.gBox_search)
        self.vLayout_gbox_search.setContentsMargins(3, 9, 3, 3)
        self.vLayout_gbox_search.setSpacing(3)
        self.vLayout_gbox_search.setObjectName("vLayout_gbox_search")
        self.gBox_search_categories = QtWidgets.QGroupBox(self.gBox_search)
        font = QtGui.QFont()
        font.setFamily("Ebrima")
        font.setPointSize(14)
        self.gBox_search_categories.setFont(font)
        self.gBox_search_categories.setObjectName("gBox_search_categories")
        self.gLayout_search_categories = QtWidgets.QGridLayout(
            self.gBox_search_categories)
        self.gLayout_search_categories.setContentsMargins(3, 6, 3, 3)
        self.gLayout_search_categories.setObjectName(
            "gLayout_search_categories")
        self.vLayout_gbox_search.addWidget(self.gBox_search_categories)
        self.gBox_search_tags = QtWidgets.QGroupBox(self.gBox_search)
        font = QtGui.QFont()
        font.setFamily("Ebrima")
        font.setPointSize(14)
        self.gBox_search_tags.setFont(font)
        self.gBox_search_tags.setObjectName("gBox_search_tags")
        self.gLayout_search_tags = QtWidgets.QGridLayout(self.gBox_search_tags)
        self.gLayout_search_tags.setContentsMargins(3, 3, 3, 3)
        self.gLayout_search_tags.setSpacing(3)
        self.gLayout_search_tags.setObjectName("gLayout_search_tags")
        self.vLayout_gbox_search.addWidget(self.gBox_search_tags)
        self.hLayout_search_btns = QtWidgets.QHBoxLayout()
        self.hLayout_search_btns.setSpacing(0)
        self.hLayout_search_btns.setObjectName("hLayout_search_btns")
        self.btn_search_clear = QtWidgets.QPushButton(self.gBox_search)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_search_clear.sizePolicy().hasHeightForWidth())
        self.btn_search_clear.setSizePolicy(sizePolicy)
        self.btn_search_clear.setObjectName("btn_search_clear")
        self.hLayout_search_btns.addWidget(self.btn_search_clear)
        self.btn_search_search = QtWidgets.QPushButton(self.gBox_search)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_search_search.sizePolicy().hasHeightForWidth())
        self.btn_search_search.setSizePolicy(sizePolicy)
        self.btn_search_search.setObjectName("btn_search_search")
        self.hLayout_search_btns.addWidget(self.btn_search_search)
        self.vLayout_gbox_search.addLayout(self.hLayout_search_btns)
        self.hLayout_search.addWidget(self.gBox_search)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hLayout_search.addItem(spacerItem1)
        self.vLayout_centralwidget.addLayout(self.hLayout_search)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Ebrima")
        font.setPointSize(12)
        self.tabWidget.setFont(font)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_recent_play = QtWidgets.QWidget()
        self.tab_recent_play.setObjectName("tab_recent_play")
        self.hLayout_tab_recent_play = QtWidgets.QHBoxLayout(
            self.tab_recent_play)
        self.hLayout_tab_recent_play.setContentsMargins(0, 0, 0, 0)
        self.hLayout_tab_recent_play.setSpacing(0)
        self.hLayout_tab_recent_play.setObjectName("hLayout_tab_recent_play")
        self.scrollArea_tab_recent_play = QtWidgets.QScrollArea(
            self.tab_recent_play)
        self.scrollArea_tab_recent_play.setWidgetResizable(True)
        self.scrollArea_tab_recent_play.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.scrollArea_tab_recent_play.setObjectName(
            "scrollArea_tab_recent_play")
        self.scrollAreaContents_tab_recent_add = QtWidgets.QWidget()
        self.scrollAreaContents_tab_recent_add.setGeometry(
            QtCore.QRect(0, 0, 98, 28))
        self.scrollAreaContents_tab_recent_add.setObjectName(
            "scrollAreaContents_tab_recent_add")
        self.vLayout_tab_rPlayed = QtWidgets.QVBoxLayout(
            self.scrollAreaContents_tab_recent_add)
        self.vLayout_tab_rPlayed.setContentsMargins(3, 3, 3, 3)
        self.vLayout_tab_rPlayed.setSpacing(3)
        self.vLayout_tab_rPlayed.setObjectName("vLayout_tab_rPlayed")
        self.scrollArea_tab_recent_play.setWidget(
            self.scrollAreaContents_tab_recent_add)
        self.hLayout_tab_recent_play.addWidget(self.scrollArea_tab_recent_play)
        self.tabWidget.addTab(self.tab_recent_play, "")
        self.tab_recent_update = QtWidgets.QWidget()
        self.tab_recent_update.setObjectName("tab_recent_update")
        self.hLayout_tab_recent_update = QtWidgets.QHBoxLayout(
            self.tab_recent_update)
        self.hLayout_tab_recent_update.setContentsMargins(0, 0, 0, 0)
        self.hLayout_tab_recent_update.setSpacing(0)
        self.hLayout_tab_recent_update.setObjectName(
            "hLayout_tab_recent_update")
        self.scrollArea_tab_recent_update = QtWidgets.QScrollArea(
            self.tab_recent_update)
        self.scrollArea_tab_recent_update.setWidgetResizable(True)
        self.scrollArea_tab_recent_update.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.scrollArea_tab_recent_update.setObjectName(
            "scrollArea_tab_recent_update")
        self.scrollAreaContents_tab_recent_update = QtWidgets.QWidget()
        self.scrollAreaContents_tab_recent_update.setGeometry(
            QtCore.QRect(0, 0, 98, 28))
        self.scrollAreaContents_tab_recent_update.setObjectName(
            "scrollAreaContents_tab_recent_update")
        self.vLayout_tab_rUpdated = QtWidgets.QVBoxLayout(
            self.scrollAreaContents_tab_recent_update)
        self.vLayout_tab_rUpdated.setContentsMargins(3, 3, 3, 3)
        self.vLayout_tab_rUpdated.setSpacing(3)
        self.vLayout_tab_rUpdated.setObjectName("vLayout_tab_rUpdated")
        self.scrollArea_tab_recent_update.setWidget(
            self.scrollAreaContents_tab_recent_update)
        self.hLayout_tab_recent_update.addWidget(
            self.scrollArea_tab_recent_update)
        self.tabWidget.addTab(self.tab_recent_update, "")
        self.tab_recent_add = QtWidgets.QWidget()
        self.tab_recent_add.setObjectName("tab_recent_add")
        self.hLayout_tab_recent_add = QtWidgets.QHBoxLayout(
            self.tab_recent_add)
        self.hLayout_tab_recent_add.setContentsMargins(0, 0, 0, 0)
        self.hLayout_tab_recent_add.setSpacing(0)
        self.hLayout_tab_recent_add.setObjectName("hLayout_tab_recent_add")
        self.scrollArea_tab_recent_add = QtWidgets.QScrollArea(
            self.tab_recent_add)
        self.scrollArea_tab_recent_add.setWidgetResizable(True)
        self.scrollArea_tab_recent_add.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.scrollArea_tab_recent_add.setObjectName(
            "scrollArea_tab_recent_add")
        self.scrollAreaContents_tab_recent_update_2 = QtWidgets.QWidget()
        self.scrollAreaContents_tab_recent_update_2.setGeometry(
            QtCore.QRect(0, 0, 1336, 918))
        self.scrollAreaContents_tab_recent_update_2.setObjectName(
            "scrollAreaContents_tab_recent_update_2")
        self.vLayout_tab_rAdded = QtWidgets.QVBoxLayout(
            self.scrollAreaContents_tab_recent_update_2)
        self.vLayout_tab_rAdded.setContentsMargins(3, 3, 3, 3)
        self.vLayout_tab_rAdded.setSpacing(3)
        self.vLayout_tab_rAdded.setObjectName("vLayout_tab_rAdded")
        self.scrollArea_tab_recent_add.setWidget(
            self.scrollAreaContents_tab_recent_update_2)
        self.hLayout_tab_recent_add.addWidget(self.scrollArea_tab_recent_add)
        self.tabWidget.addTab(self.tab_recent_add, "")
        self.tab_numA = QtWidgets.QWidget()
        self.tab_numA.setObjectName("tab_numA")
        self.hLayout_tab_numA = QtWidgets.QHBoxLayout(self.tab_numA)
        self.hLayout_tab_numA.setContentsMargins(0, 0, 0, 0)
        self.hLayout_tab_numA.setSpacing(0)
        self.hLayout_tab_numA.setObjectName("hLayout_tab_numA")
        self.scrollArea_tab_numA = QtWidgets.QScrollArea(self.tab_numA)
        self.scrollArea_tab_numA.setWidgetResizable(True)
        self.scrollArea_tab_numA.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.scrollArea_tab_numA.setObjectName("scrollArea_tab_numA")
        self.scrollAreaContents_tab_numA = QtWidgets.QWidget()
        self.scrollAreaContents_tab_numA.setGeometry(
            QtCore.QRect(0, 0, 98, 28))
        self.scrollAreaContents_tab_numA.setObjectName(
            "scrollAreaContents_tab_numA")
        self.vLayout_tab_numA = QtWidgets.QVBoxLayout(
            self.scrollAreaContents_tab_numA)
        self.vLayout_tab_numA.setContentsMargins(3, 3, 3, 3)
        self.vLayout_tab_numA.setSpacing(3)
        self.vLayout_tab_numA.setObjectName("vLayout_tab_numA")
        self.scrollArea_tab_numA.setWidget(self.scrollAreaContents_tab_numA)
        self.hLayout_tab_numA.addWidget(self.scrollArea_tab_numA)
        self.tabWidget.addTab(self.tab_numA, "")
        self.tab_BC = QtWidgets.QWidget()
        self.tab_BC.setObjectName("tab_BC")
        self.hLayout_tab_BC = QtWidgets.QHBoxLayout(self.tab_BC)
        self.hLayout_tab_BC.setContentsMargins(0, 0, 0, 0)
        self.hLayout_tab_BC.setSpacing(0)
        self.hLayout_tab_BC.setObjectName("hLayout_tab_BC")
        self.scrollArea_tab_BC = QtWidgets.QScrollArea(self.tab_BC)
        self.scrollArea_tab_BC.setWidgetResizable(True)
        self.scrollArea_tab_BC.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.scrollArea_tab_BC.setObjectName("scrollArea_tab_BC")
        self.scrollAreaContents_tab_BC = QtWidgets.QWidget()
        self.scrollAreaContents_tab_BC.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.scrollAreaContents_tab_BC.setObjectName(
            "scrollAreaContents_tab_BC")
        self.vLayout_tab_BC = QtWidgets.QVBoxLayout(
            self.scrollAreaContents_tab_BC)
        self.vLayout_tab_BC.setContentsMargins(3, 3, 3, 3)
        self.vLayout_tab_BC.setSpacing(3)
        self.vLayout_tab_BC.setObjectName("vLayout_tab_BC")
        self.scrollArea_tab_BC.setWidget(self.scrollAreaContents_tab_BC)
        self.hLayout_tab_BC.addWidget(self.scrollArea_tab_BC)
        self.tabWidget.addTab(self.tab_BC, "")
        self.tab_DE = QtWidgets.QWidget()
        self.tab_DE.setObjectName("tab_DE")
        self.hLayout_tab_DE = QtWidgets.QHBoxLayout(self.tab_DE)
        self.hLayout_tab_DE.setContentsMargins(0, 0, 0, 0)
        self.hLayout_tab_DE.setSpacing(0)
        self.hLayout_tab_DE.setObjectName("hLayout_tab_DE")
        self.scrollArea_tab_DE = QtWidgets.QScrollArea(self.tab_DE)
        self.scrollArea_tab_DE.setWidgetResizable(True)
        self.scrollArea_tab_DE.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.scrollArea_tab_DE.setObjectName("scrollArea_tab_DE")
        self.scrollAreaContents_tab_DE = QtWidgets.QWidget()
        self.scrollAreaContents_tab_DE.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.scrollAreaContents_tab_DE.setObjectName(
            "scrollAreaContents_tab_DE")
        self.vLayout_tab_DE = QtWidgets.QVBoxLayout(
            self.scrollAreaContents_tab_DE)
        self.vLayout_tab_DE.setContentsMargins(3, 3, 3, 3)
        self.vLayout_tab_DE.setSpacing(3)
        self.vLayout_tab_DE.setObjectName("vLayout_tab_DE")
        self.scrollArea_tab_DE.setWidget(self.scrollAreaContents_tab_DE)
        self.hLayout_tab_DE.addWidget(self.scrollArea_tab_DE)
        self.tabWidget.addTab(self.tab_DE, "")
        self.tab_FG = QtWidgets.QWidget()
        self.tab_FG.setObjectName("tab_FG")
        self.hLayout_tab_FG = QtWidgets.QHBoxLayout(self.tab_FG)
        self.hLayout_tab_FG.setContentsMargins(0, 0, 0, 0)
        self.hLayout_tab_FG.setSpacing(0)
        self.hLayout_tab_FG.setObjectName("hLayout_tab_FG")
        self.scrollArea_tab_FG = QtWidgets.QScrollArea(self.tab_FG)
        self.scrollArea_tab_FG.setWidgetResizable(True)
        self.scrollArea_tab_FG.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.scrollArea_tab_FG.setObjectName("scrollArea_tab_FG")
        self.scrollAreaContents_tab_FG = QtWidgets.QWidget()
        self.scrollAreaContents_tab_FG.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.scrollAreaContents_tab_FG.setObjectName(
            "scrollAreaContents_tab_FG")
        self.vLayout_tab_FG = QtWidgets.QVBoxLayout(
            self.scrollAreaContents_tab_FG)
        self.vLayout_tab_FG.setContentsMargins(3, 3, 3, 3)
        self.vLayout_tab_FG.setSpacing(3)
        self.vLayout_tab_FG.setObjectName("vLayout_tab_FG")
        self.scrollArea_tab_FG.setWidget(self.scrollAreaContents_tab_FG)
        self.hLayout_tab_FG.addWidget(self.scrollArea_tab_FG)
        self.tabWidget.addTab(self.tab_FG, "")
        self.tab_HI = QtWidgets.QWidget()
        self.tab_HI.setObjectName("tab_HI")
        self.hLayout_tab_HI = QtWidgets.QHBoxLayout(self.tab_HI)
        self.hLayout_tab_HI.setContentsMargins(0, 0, 0, 0)
        self.hLayout_tab_HI.setSpacing(0)
        self.hLayout_tab_HI.setObjectName("hLayout_tab_HI")
        self.scrollArea_tab_HI = QtWidgets.QScrollArea(self.tab_HI)
        self.scrollArea_tab_HI.setWidgetResizable(True)
        self.scrollArea_tab_HI.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.scrollArea_tab_HI.setObjectName("scrollArea_tab_HI")
        self.scrollAreaContents_tab_HI = QtWidgets.QWidget()
        self.scrollAreaContents_tab_HI.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.scrollAreaContents_tab_HI.setObjectName(
            "scrollAreaContents_tab_HI")
        self.vLayout_tab_HI = QtWidgets.QVBoxLayout(
            self.scrollAreaContents_tab_HI)
        self.vLayout_tab_HI.setContentsMargins(3, 3, 3, 3)
        self.vLayout_tab_HI.setSpacing(3)
        self.vLayout_tab_HI.setObjectName("vLayout_tab_HI")
        self.scrollArea_tab_HI.setWidget(self.scrollAreaContents_tab_HI)
        self.hLayout_tab_HI.addWidget(self.scrollArea_tab_HI)
        self.tabWidget.addTab(self.tab_HI, "")
        self.tab_JK = QtWidgets.QWidget()
        self.tab_JK.setObjectName("tab_JK")
        self.hLayout_tab_JK = QtWidgets.QHBoxLayout(self.tab_JK)
        self.hLayout_tab_JK.setContentsMargins(0, 0, 0, 0)
        self.hLayout_tab_JK.setSpacing(0)
        self.hLayout_tab_JK.setObjectName("hLayout_tab_JK")
        self.scrollArea_tab_JK = QtWidgets.QScrollArea(self.tab_JK)
        self.scrollArea_tab_JK.setWidgetResizable(True)
        self.scrollArea_tab_JK.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.scrollArea_tab_JK.setObjectName("scrollArea_tab_JK")
        self.scrollAreaContents_tab_JK = QtWidgets.QWidget()
        self.scrollAreaContents_tab_JK.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.scrollAreaContents_tab_JK.setObjectName(
            "scrollAreaContents_tab_JK")
        self.vLayout_tab_JK = QtWidgets.QVBoxLayout(
            self.scrollAreaContents_tab_JK)
        self.vLayout_tab_JK.setContentsMargins(3, 3, 3, 3)
        self.vLayout_tab_JK.setSpacing(3)
        self.vLayout_tab_JK.setObjectName("vLayout_tab_JK")
        self.scrollArea_tab_JK.setWidget(self.scrollAreaContents_tab_JK)
        self.hLayout_tab_JK.addWidget(self.scrollArea_tab_JK)
        self.tabWidget.addTab(self.tab_JK, "")
        self.tab_LM = QtWidgets.QWidget()
        self.tab_LM.setObjectName("tab_LM")
        self.hLayout_tab_LM = QtWidgets.QHBoxLayout(self.tab_LM)
        self.hLayout_tab_LM.setContentsMargins(0, 0, 0, 0)
        self.hLayout_tab_LM.setSpacing(0)
        self.hLayout_tab_LM.setObjectName("hLayout_tab_LM")
        self.scrollArea_tab_LM = QtWidgets.QScrollArea(self.tab_LM)
        self.scrollArea_tab_LM.setWidgetResizable(True)
        self.scrollArea_tab_LM.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.scrollArea_tab_LM.setObjectName("scrollArea_tab_LM")
        self.scrollAreaContents_tab_LM = QtWidgets.QWidget()
        self.scrollAreaContents_tab_LM.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.scrollAreaContents_tab_LM.setObjectName(
            "scrollAreaContents_tab_LM")
        self.vLayout_tab_LM = QtWidgets.QVBoxLayout(
            self.scrollAreaContents_tab_LM)
        self.vLayout_tab_LM.setContentsMargins(3, 3, 3, 3)
        self.vLayout_tab_LM.setSpacing(3)
        self.vLayout_tab_LM.setObjectName("vLayout_tab_LM")
        self.scrollArea_tab_LM.setWidget(self.scrollAreaContents_tab_LM)
        self.hLayout_tab_LM.addWidget(self.scrollArea_tab_LM)
        self.tabWidget.addTab(self.tab_LM, "")
        self.tab_NO = QtWidgets.QWidget()
        self.tab_NO.setObjectName("tab_NO")
        self.hLayout_tab_NO = QtWidgets.QHBoxLayout(self.tab_NO)
        self.hLayout_tab_NO.setContentsMargins(0, 0, 0, 0)
        self.hLayout_tab_NO.setSpacing(0)
        self.hLayout_tab_NO.setObjectName("hLayout_tab_NO")
        self.scrollArea_tab_NO = QtWidgets.QScrollArea(self.tab_NO)
        self.scrollArea_tab_NO.setWidgetResizable(True)
        self.scrollArea_tab_NO.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.scrollArea_tab_NO.setObjectName("scrollArea_tab_NO")
        self.scrollAreaContents_tab_NO = QtWidgets.QWidget()
        self.scrollAreaContents_tab_NO.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.scrollAreaContents_tab_NO.setObjectName(
            "scrollAreaContents_tab_NO")
        self.vLayout_tab_NO = QtWidgets.QVBoxLayout(
            self.scrollAreaContents_tab_NO)
        self.vLayout_tab_NO.setContentsMargins(3, 3, 3, 3)
        self.vLayout_tab_NO.setSpacing(3)
        self.vLayout_tab_NO.setObjectName("vLayout_tab_NO")
        self.scrollArea_tab_NO.setWidget(self.scrollAreaContents_tab_NO)
        self.hLayout_tab_NO.addWidget(self.scrollArea_tab_NO)
        self.tabWidget.addTab(self.tab_NO, "")
        self.tab_PQR = QtWidgets.QWidget()
        self.tab_PQR.setObjectName("tab_PQR")
        self.hLayout_tab_PQR = QtWidgets.QHBoxLayout(self.tab_PQR)
        self.hLayout_tab_PQR.setContentsMargins(0, 0, 0, 0)
        self.hLayout_tab_PQR.setSpacing(0)
        self.hLayout_tab_PQR.setObjectName("hLayout_tab_PQR")
        self.scrollArea_tab_PQR = QtWidgets.QScrollArea(self.tab_PQR)
        self.scrollArea_tab_PQR.setWidgetResizable(True)
        self.scrollArea_tab_PQR.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.scrollArea_tab_PQR.setObjectName("scrollArea_tab_PQR")
        self.scrollAreaContents_tab_PQR = QtWidgets.QWidget()
        self.scrollAreaContents_tab_PQR.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.scrollAreaContents_tab_PQR.setObjectName(
            "scrollAreaContents_tab_PQR")
        self.vLayout_tab_PQR = QtWidgets.QVBoxLayout(
            self.scrollAreaContents_tab_PQR)
        self.vLayout_tab_PQR.setContentsMargins(3, 3, 3, 3)
        self.vLayout_tab_PQR.setSpacing(3)
        self.vLayout_tab_PQR.setObjectName("vLayout_tab_PQR")
        self.scrollArea_tab_PQR.setWidget(self.scrollAreaContents_tab_PQR)
        self.hLayout_tab_PQR.addWidget(self.scrollArea_tab_PQR)
        self.tabWidget.addTab(self.tab_PQR, "")
        self.tab_ST = QtWidgets.QWidget()
        self.tab_ST.setObjectName("tab_ST")
        self.hLayout_tab_ST = QtWidgets.QHBoxLayout(self.tab_ST)
        self.hLayout_tab_ST.setContentsMargins(0, 0, 0, 0)
        self.hLayout_tab_ST.setSpacing(0)
        self.hLayout_tab_ST.setObjectName("hLayout_tab_ST")
        self.scrollArea_tab_ST = QtWidgets.QScrollArea(self.tab_ST)
        self.scrollArea_tab_ST.setWidgetResizable(True)
        self.scrollArea_tab_ST.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.scrollArea_tab_ST.setObjectName("scrollArea_tab_ST")
        self.scrollAreaContents_tab_ST = QtWidgets.QWidget()
        self.scrollAreaContents_tab_ST.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.scrollAreaContents_tab_ST.setObjectName(
            "scrollAreaContents_tab_ST")
        self.vLayout_tab_ST = QtWidgets.QVBoxLayout(
            self.scrollAreaContents_tab_ST)
        self.vLayout_tab_ST.setContentsMargins(3, 3, 3, 3)
        self.vLayout_tab_ST.setSpacing(3)
        self.vLayout_tab_ST.setObjectName("vLayout_tab_ST")
        self.scrollArea_tab_ST.setWidget(self.scrollAreaContents_tab_ST)
        self.hLayout_tab_ST.addWidget(self.scrollArea_tab_ST)
        self.tabWidget.addTab(self.tab_ST, "")
        self.tab_UV = QtWidgets.QWidget()
        self.tab_UV.setObjectName("tab_UV")
        self.hLayout_tab_UV = QtWidgets.QHBoxLayout(self.tab_UV)
        self.hLayout_tab_UV.setContentsMargins(0, 0, 0, 0)
        self.hLayout_tab_UV.setSpacing(0)
        self.hLayout_tab_UV.setObjectName("hLayout_tab_UV")
        self.scrollArea_tab_UV = QtWidgets.QScrollArea(self.tab_UV)
        self.scrollArea_tab_UV.setWidgetResizable(True)
        self.scrollArea_tab_UV.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.scrollArea_tab_UV.setObjectName("scrollArea_tab_UV")
        self.scrollAreaContents_tab_UV = QtWidgets.QWidget()
        self.scrollAreaContents_tab_UV.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.scrollAreaContents_tab_UV.setObjectName(
            "scrollAreaContents_tab_UV")
        self.vLayout_tab_UV = QtWidgets.QVBoxLayout(
            self.scrollAreaContents_tab_UV)
        self.vLayout_tab_UV.setContentsMargins(3, 3, 3, 3)
        self.vLayout_tab_UV.setSpacing(3)
        self.vLayout_tab_UV.setObjectName("vLayout_tab_UV")
        self.scrollArea_tab_UV.setWidget(self.scrollAreaContents_tab_UV)
        self.hLayout_tab_UV.addWidget(self.scrollArea_tab_UV)
        self.tabWidget.addTab(self.tab_UV, "")
        self.tab_WXYZ = QtWidgets.QWidget()
        self.tab_WXYZ.setObjectName("tab_WXYZ")
        self.hLayout_tab_WXYZ = QtWidgets.QHBoxLayout(self.tab_WXYZ)
        self.hLayout_tab_WXYZ.setContentsMargins(0, 0, 0, 0)
        self.hLayout_tab_WXYZ.setSpacing(0)
        self.hLayout_tab_WXYZ.setObjectName("hLayout_tab_WXYZ")
        self.scrollArea_tab_WXYZ = QtWidgets.QScrollArea(self.tab_WXYZ)
        self.scrollArea_tab_WXYZ.setWidgetResizable(True)
        self.scrollArea_tab_WXYZ.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.scrollArea_tab_WXYZ.setObjectName("scrollArea_tab_WXYZ")
        self.scrollAreaContents_tab_WXYZ = QtWidgets.QWidget()
        self.scrollAreaContents_tab_WXYZ.setGeometry(
            QtCore.QRect(0, 0, 98, 28))
        self.scrollAreaContents_tab_WXYZ.setObjectName(
            "scrollAreaContents_tab_WXYZ")
        self.vLayout_tab_WXYZ = QtWidgets.QVBoxLayout(
            self.scrollAreaContents_tab_WXYZ)
        self.vLayout_tab_WXYZ.setContentsMargins(3, 3, 3, 3)
        self.vLayout_tab_WXYZ.setSpacing(3)
        self.vLayout_tab_WXYZ.setObjectName("vLayout_tab_WXYZ")
        self.scrollArea_tab_WXYZ.setWidget(self.scrollAreaContents_tab_WXYZ)
        self.hLayout_tab_WXYZ.addWidget(self.scrollArea_tab_WXYZ)
        self.tabWidget.addTab(self.tab_WXYZ, "")
        self.vLayout_centralwidget.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1350, 21))
        self.menubar.setObjectName("menubar")
        self.menu_new_games = QtWidgets.QMenu(self.menubar)
        self.menu_new_games.setObjectName("menu_new_games")
        MainWindow.setMenuBar(self.menubar)
        self.menuAction_check = QtWidgets.QAction(MainWindow)
        self.menuAction_check.setShortcutContext(QtCore.Qt.WidgetShortcut)
        self.menuAction_check.setIconVisibleInMenu(False)
        self.menuAction_check.setShortcutVisibleInContextMenu(False)
        self.menuAction_check.setObjectName("menuAction_check")
        self.menuAction_add = QtWidgets.QAction(MainWindow)
        self.menuAction_add.setShortcutContext(QtCore.Qt.WidgetShortcut)
        self.menuAction_add.setIconVisibleInMenu(False)
        self.menuAction_add.setShortcutVisibleInContextMenu(False)
        self.menuAction_add.setObjectName("menuAction_add")
        self.menuAction_add_simple = QtWidgets.QAction(MainWindow)
        self.menuAction_add_simple.setShortcutContext(QtCore.Qt.WidgetShortcut)
        self.menuAction_add_simple.setIconVisibleInMenu(False)
        self.menuAction_add_simple.setShortcutVisibleInContextMenu(False)
        self.menuAction_add_simple.setObjectName("menuAction_add_simple")
        self.menu_new_games.addAction(self.menuAction_check)
        self.menu_new_games.addAction(self.menuAction_add)
        self.menubar.addAction(self.menu_new_games.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.gBox_search.setTitle(_translate("MainWindow", "Search"))
        self.gBox_search_categories.setTitle(
            _translate("MainWindow", "Categories"))
        self.gBox_search_tags.setTitle(_translate("MainWindow", "Tags"))
        self.btn_search_clear.setText(_translate("MainWindow", "Clear"))
        self.btn_search_search.setText(_translate("MainWindow", "Search"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tab_recent_play), _translate("MainWindow", "Recently Played"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tab_recent_update), _translate("MainWindow", "Recently Updated"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tab_recent_add), _translate("MainWindow", "Recently Added"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tab_numA), _translate("MainWindow", "#-A"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tab_BC), _translate("MainWindow", "B-C"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tab_DE), _translate("MainWindow", "D-E"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tab_FG), _translate("MainWindow", "F-G"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tab_HI), _translate("MainWindow", "H-I"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tab_JK), _translate("MainWindow", "J-K"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tab_LM), _translate("MainWindow", "L-M"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tab_NO), _translate("MainWindow", "N-O"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tab_PQR), _translate("MainWindow", "P-R"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tab_ST), _translate("MainWindow", "S-T"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tab_UV), _translate("MainWindow", "U-V"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tab_WXYZ), _translate("MainWindow", "W-Z"))
        self.menu_new_games.setTitle(_translate("MainWindow", "New Games"))
        self.menuAction_check.setText(_translate(
            "MainWindow", "Check for new games"))
        self.menuAction_add.setText(_translate("MainWindow", "Add a new game"))
        self.menuAction_add_simple.setText(
            _translate("MainWindow", "Add a new game (simple)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
