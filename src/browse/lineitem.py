from textwrap import wrap as txtWrap
from typing import TYPE_CHECKING
from os import startfile
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QLabel,
    QScrollArea
)
from PyQt5.QtCore import (
    QPoint,
    QRect,
    Qt
)
from PyQt5.QtGui import (
    QBrush,
    QColor,
    QFont,
    QFontMetrics,
    QImage,
    QPainter,
    QPainterPath,
    QPen
)

from .ui_lineItem import Ui_LineItem
from .gamePicker import GamePicker
from ..messageBox import Messagebox as Mbox
from ..edit import EditUI
from ..constants import *

if TYPE_CHECKING:
    from ..gamelibrary import GameLibrary


class _ImageLabel(QLabel):
    def __init__(self, parent: QWidget, img: str, text: str, status: str):
        self._clr = TEXT_COLORS.__dict__.get(status)
        self._img = img
        self._text = txtWrap(text=text,
                             width=22)
        QLabel.__init__(self, parent)
        self.setToolTip(f'<img src="{img}">')

    def paintEvent(self, _):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)

        img = QImage(self._img)
        image = img.scaled(195, 110)
        qp.drawImage(QPoint(), image)
        qp.fillRect(QRect(0, 0, 195, 110), QBrush(QColor(0, 0, 0, 95)))

        font = QFont()
        font.setPointSize(12)
        qp.setFont(font)

        pen = QPen(Qt.black)
        pen.setWidth(3)
        ppth = QPainterPath()
        x = 20
        for line in self._text:
            ppth.addText(2, x, font, line)
            x += QFontMetrics(font).height()
        qp.strokePath(ppth, pen)
        qp.fillPath(ppth, QColor(self._clr))

        qp.end()


class LineItem(Ui_LineItem):
    game_lib: "GameLibrary"
    parent_layout: QVBoxLayout
    widget: QWidget
    gpath: U[Path, dict[str, Path]]
    ginfo: GAMEDATA_TYPE

    def __init__(self, game_lib: "GameLibrary", gpath: Path, vb_layout: QVBoxLayout = None):
        self.widget = QWidget(game_lib.main_win)
        self.setupUi(self.widget)
        # init vars
        self.game_lib = game_lib
        self.gpath = gpath
        self.ginfo = self.game_lib.master_list[self.gpath]
        if vb_layout == None:
            vb_layout = self.getParentLayout(self.ginfo['Info']['Title'])
        self.parent_layout = vb_layout
        # build widget
        self.fill()
        self.parent_layout.addWidget(self.widget)
        self.widget.show()
        # bind buttons
        self.btn_tools_play.clicked.connect(self.playGameBtn)
        self.btn_tools_web.clicked.connect(self.openWebpage)
        self.btn_tools_edit.clicked.connect(self.editGame)

    def fill(self):
        # title
        if self.ginfo['Categories']['Favorite']:
            stat = 'Favorite'
        elif self.ginfo['Categories']['Completed']:
            stat = 'Completed'
        elif self.ginfo['Categories']['Abandoned']:
            stat = 'Abandoned'
        else:
            stat = 'default'
        img = self.ginfo['Info']['Image']
        if img:
            img = FPATH_IMGS.joinpath(img)
            if not img.exists():
                img = FPATH_IMGS.joinpath('error.jpg')
        else:
            img = FPATH_IMGS.joinpath('default.png')
        txt = self.ginfo['Info']['Title']
        self.img_lbl = _ImageLabel(parent=self.widget,
                                   img=str(img),
                                   text=txt,
                                   status=stat)
        self.vLayout_title.addWidget(self.img_lbl)
        # version
        self.label_version.setText(self.ginfo['Info']['Version'])
        # categories
        ctgs = [f"{ctg}: {self.ginfo['Categories'][ctg]}"
                for ctg in ['Status', 'Genre', 'Engine', 'Art', 'Protagonist']]
        self.label_category.setText('\n'.join(ctgs))
        # tags
        self.label_tags.setText(', '.join(
            [t for t, v in self.ginfo['Tags'].items() if v]))
        # description
        desc = self.ginfo['Info']['Description']
        self.textEdit_description.setPlainText(desc)

    def playGameBtn(self):
        ppth = self.ginfo['Info']['Program Path']
        if isinstance(ppth, Path):
            self.startGame(ppth)
        else:
            pick = GamePicker(parent=self.game_lib.main_win,
                              game_lib=self.game_lib,
                              gpths=ppth).gpath
            if pick:
                self.startGame(pick)

    def startGame(self, exe: Path):
        try:
            startfile(exe)
            # update recent
            cur_list = self.game_lib.recent_list['played'].copy()
            if self.ginfo['Info']['Title'] in cur_list:
                cur_list.remove(self.ginfo['Info']['Title'])
            cur_list.insert(0, self.ginfo['Info']['Title'])
            while len(cur_list) > MAX_RECENT_GAMES:
                cur_list.pop()
            if cur_list != self.game_lib.recent_list['played']:
                self.game_lib.recent_list['played'] = cur_list
                self.game_lib.saveRecent()
        except:
            ans = Mbox.askquestion(title='Error',
                                   message=(f"Couldn't start '{self.ginfo['Info']['Title']}'\n"
                                            "Would you like to change the executable path?\n"
                                            f"(Current Path: '{exe.relative_to(FPATH_GAMES)}')"))
            if ans == 'Yes':
                self.editGame()

    def openWebpage(self):
        startfile(self.ginfo['Info']['URL'])

    def editGame(self):
        edit_ui = EditUI(game_lib=self.game_lib)
        edit_ui.fullInfo(self.gpath, self.ginfo)
        if edit_ui.output != 'cancel':
            UpdateLineItems(self.game_lib, edit_ui)

    def update(self, new_gpath: Path, insert_first: bool = True):
        self.img_lbl.deleteLater()
        self.gpath = new_gpath
        self.ginfo = self.game_lib.master_list[new_gpath]
        self.fill()
        if insert_first:
            self.parent_layout.insertWidget(0, self.widget)
            scrollArea = self.parent_layout.parent()
            while not isinstance(scrollArea, QScrollArea):
                scrollArea = scrollArea.parent()
            vbar = scrollArea.verticalScrollBar()
            vbar.setValue(vbar.minimum())

    def getParentLayout(self, title: str) -> QVBoxLayout:
        l = title[0].upper()
        for letters, layout in self.game_lib.tab_layouts.items():
            if l in letters:
                return layout
        return self.game_lib.tab_layouts['numA']


class UpdateLineItems:
    gpath: Path
    ginfo: GAMEDATA_TYPE

    def __init__(self, game_lib: "GameLibrary", edit_ui: EditUI):
        self.game_lib = game_lib
        self.gpath = edit_ui.game_path
        ogpath = edit_ui.orig_path
        self.ginfo = self.game_lib.master_list[self.gpath]
        if edit_ui.output == 'new':
            self.addNewLineitem(layout_index=3,
                                vb_layout=None)
            self.addNewLineitem(layout_index=2,
                                vb_layout=self.game_lib.recent_tab_layouts['added'])
        else:
            lineitem_pointers = self.game_lib.lineitem_pointers[ogpath]
            for i, lineitem in enumerate(lineitem_pointers):
                if lineitem != None:
                    lineitem.update(new_gpath=self.gpath,
                                    insert_first=(i % 2))
            if lineitem_pointers[1] == None:
                self.addNewLineitem(layout_index=1,
                                    vb_layout=self.game_lib.recent_tab_layouts['updated'])

    def addNewLineitem(self, layout_index: int, vb_layout: O[QVBoxLayout]):
        li = LineItem(game_lib=self.game_lib,
                      gpath=self.gpath,
                      vb_layout=vb_layout)
        li.parent_layout.insertWidget(0, li.widget)
        pointers = self.game_lib.lineitem_pointers.get(self.gpath,
                                                       [None, None, None, None])
        pointers[layout_index] = li
        self.game_lib.lineitem_pointers.update({self.gpath: pointers})
