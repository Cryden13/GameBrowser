from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QMainWindow,
    QVBoxLayout,
    QFileDialog
)

from .ui_browse import Ui_MainWindow
from ..searchBoxes import SearchBoxes
from ..gamelibrary import GameLibrary
from ..constants import *
from ..edit import EditUI
from .lineItem import (
    LineItem,
    UpdateLineItems
)


class MainWindow(Ui_MainWindow):
    win: QMainWindow
    game_lib: GameLibrary
    # reference dict for the QVBoxLayouts within every recent tab, where {<layout_name>: <layout>}
    recent_tab_layouts: dict[str, QVBoxLayout]
    # reference dict for the QVBoxLayouts within every non-recent tab, where {<layout_letters>: <layout>}
    tab_layouts: dict[str, QVBoxLayout]
    # all search options, formatted as {Categories: {<type>: {<cat>: <input>}}, Tags: {<type>: {<tag>: <input>}}}
    search_inputs: dict[str, dict[str, dict[str, U[QComboBox, QCheckBox]]]]
    # current search terms, formatted as {Categories: {<cat>: <val>}, Tags: {<tag>: <val>}}
    cur_search: dict[str, dict[str, U[str, int]]]
    # currently searched for games
    game_search: list[Path]
    # reference dict for all lineitems
    lineitem_pointers: dict[Path, list[LineItem]]

    def __init__(self, app: QApplication):
        self.win = QMainWindow()
        self.win.setWindowIcon(QIcon(PATH_ICON))
        self.setupUi(self.win)
        self.win.show()
        self.startMain()
        app.exec()

#     ___  __  ________   ___
#    / _ )/ / / /  _/ /  / _ \
#   / _  / /_/ // // /__/ // /
#  /____/\____/___/____/____/

    def startMain(self):
        # init vars
        self.game_lib = GameLibrary(self.win)
        self.recent_tab_layouts = self.game_lib.recent_tab_layouts
        self.recent_tab_layouts.update({'played': self.vLayout_tab_rPlayed,
                                        'updated': self.vLayout_tab_rUpdated,
                                        'added': self.vLayout_tab_rAdded})
        self.tab_layouts = self.game_lib.tab_layouts
        self.tab_layouts.update({var[12:]: layout for var, layout in self.__dict__.items()
                                 if var[:12] == 'vLayout_tab_' and var[12] != 'r'})
        self.lineitem_pointers = self.game_lib.lineitem_pointers
        ctg_srch = SearchBoxes(self.gBox_search_categories,
                               self.gLayout_search_categories)
        tag_srch = SearchBoxes(self.gBox_search_tags, self.gLayout_search_tags)
        self.search_inputs = {
            'Categories': {
                'cmbBox': {
                    ttl: ctg_srch.createComboBox(ttl, ['Any', *cnt]) for ttl, cnt in CAT_SEL.items()
                },
                'chkBox': {
                    txt: ctg_srch.createCheckBox(txt, False) for txt in CAT_TOG
                }
            },
            'Tags': {
                'cmbBox': {
                    ttl: tag_srch.createComboBox(ttl, ['Any', *cnt]) for ttl, cnt in TAG_SEL.items()
                },
                'chkBox': {
                    txt: tag_srch.createCheckBox(txt) for txt in TAG_TOG
                }
            }
        }
        self.clearSearch()
        self.game_search = list(self.game_lib.master_list.keys())
        # bind menu buttons
        self.menuAction_add.triggered.connect(self.addNew)
        self.menuAction_check.triggered.connect(self.checkForNew)
        # bind search btns
        self.btn_search_clear.clicked.connect(self.clearSearch)
        self.btn_search_search.clicked.connect(self.searchBrowse)
        # build ui
        self.createLibrary()
        self.createRecents()

    def createLibrary(self):
        for gfol in self.game_lib.master_list:
            li = LineItem(game_lib=self.game_lib,
                          gpath=gfol)
            pointers = [None, None, None, li]
            self.lineitem_pointers.update({gfol: pointers})

    def createRecents(self):
        for i, (rCategory, vb_layout) in enumerate(self.recent_tab_layouts.items()):
            recent_list = {gpth: ginfo
                           for title in self.game_lib.recent_list[rCategory]
                           for gpth, ginfo in self.game_lib.master_list.items()
                           if title == ginfo['Info']['Title']}
            for gfol in recent_list:
                li = LineItem(game_lib=self.game_lib,
                              gpath=gfol,
                              vb_layout=vb_layout)
                pointers = self.lineitem_pointers.get(gfol)
                pointers[i] = li
                self.lineitem_pointers.update({gfol: pointers})

#     ______  ___  ___________
#    / __/ / / / |/ / ___/ __/
#   / _// /_/ /    / /___\ \
#  /_/  \____/_/|_/\___/___/

    def addNew(self):
        new_path_raw: str = QFileDialog.getExistingDirectory(
            caption="Select the new game's directory",
            directory=str(FPATH_GAMES)
        )
        if new_path_raw:
            new_path = Path(new_path_raw).resolve()
            edit_ui = EditUI(game_lib=self.game_lib)
            edit_ui.simpleInfo(fol=new_path)
            if edit_ui.output != 'cancel':
                UpdateLineItems(self.game_lib, edit_ui)

    def checkForNew(self):
        self.game_lib.checkForNewGames()

#     ___________   ___  _______ __
#    / __/ __/ _ | / _ \/ ___/ // /
#   _\ \/ _// __ |/ , _/ /__/ _  /
#  /___/___/_/ |_/_/|_|\___/_//_/

    def clearSearch(self):
        for types in self.search_inputs.values():
            for cmbBox in types['cmbBox'].values():
                cmbBox.setCurrentIndex(0)
            for chkBox in types['chkBox'].values():
                chkBox.setCheckState(Qt.PartiallyChecked)
        self.cur_search = {'Categories': {}, 'Tags': {}}
        for lineitems in self.lineitem_pointers.values():
            for lineitem in lineitems:
                lineitem.widget.show()

    def searchBrowse(self):
        categories = {
            k: v.currentText() for k, v in self.search_inputs['Categories']['cmbBox'].items()
            if v.currentText() != 'Any'
        }
        categories.update({
            k: 0 for k, v in self.search_inputs['Categories']['chkBox'].items()
            if v.checkState() == Qt.Unchecked
        })
        categories.update({
            k: 1 for k, v in self.search_inputs['Categories']['chkBox'].items()
            if v.checkState() == Qt.Checked
        })
        tags = {
            k: v.currentText() for k, v in self.search_inputs['Tags']['cmbBox'].items()
            if v.currentText() != 'Any'
        }
        tags.update({
            k: 0 for k, v in self.search_inputs['Tags']['chkBox'].items()
            if v.checkState() == Qt.Unchecked
        })
        tags.update({
            k: 1 for k, v in self.search_inputs['Tags']['chkBox'].items()
            if v.checkState() == Qt.Checked
        })
        search = (categories | tags)
        if search != self.cur_search:
            if search:
                self.game_search.clear()
                for gpth, ginfo in self.game_lib.master_list.items():
                    data = (ginfo['Categories'] | ginfo['Tags'])
                    if search.items() <= data.items():
                        self.game_search.append(gpth)
                for gpth, lineitems in self.lineitem_pointers.items():
                    for lineitem in lineitems:
                        if gpth in self.game_search:
                            lineitem.widget.show()
                        else:
                            lineitem.widget.hide()
                if self.tabWidget.currentIndex() < 3:
                    self.tabWidget.setCurrentIndex(3)
                self.cur_search = search
            else:
                self.clearSearch()
