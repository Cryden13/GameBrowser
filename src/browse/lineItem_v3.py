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
    from ..gamelibrary_v3 import (
        Game as GameClass,
        GameLibrary
    )


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
    game_info: "GameClass"

    def __init__(self, game_lib: "GameLibrary", game: "GameClass", vb_layout: QVBoxLayout = None):
        self.widget = QWidget(game_lib.main_win)
        self.setupUi(self.widget)
        # init vars
        self.game_lib = game_lib
        self.game_info = game
        if vb_layout == None:
            vb_layout = self.getParentLayout(self.game_info.Info.Title)
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
        ctg = self.game_info.Categories
        # title
        ttlclr = 'Favorite' if ctg.Favorite else 'default'
        img = self.game_info.Info.Image
        if img:
            img = FPATH_IMGS.joinpath(img)
            if not img.exists():
                img = FPATH_IMGS.joinpath('error.jpg')
        else:
            img = FPATH_IMGS.joinpath('default.png')
        txt = self.game_info.Info.Title
        self.img_lbl = _ImageLabel(parent=self.widget,
                                   img=str(img),
                                   text=txt,
                                   status=ttlclr)
        self.vLayout_title.addWidget(self.img_lbl)
        # version
        ver = 'Completed' if ctg.Completed else 'Abandoned' if ctg.Abandoned else 'default'
        verclr = TEXT_COLORS.__dict__.get(ver)
        self.label_version.setText(self.game_info.Info.Version)
        self.label_version.setStyleSheet(f'QLabel {{color: {verclr};}}')
        # categories
        ctgs = [f"{ctg}: {self.ginfo['Categories'][ctg]}"
                for ctg in ['Status', 'Genre', 'Engine', 'Art', 'Protagonist']]
        self.label_category.setText('\n'.join(ctgs))
        # tags
        self.label_tags.setText(', '.join(
            [t for t, v in self.game_info.Tags.__dict__.items() if v]))
        # description
        desc = self.game_info.Info.Description
        self.textEdit_description.setPlainText(desc)

    def playGameBtn(self):
        ppth = self.game_info.Info.Program_Path
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
            startfile(filepath=exe, cwd=exe.parent)
            # update recent
            cur_list = self.game_lib.recent_list['played'].copy()
            if self.game_info.Info.Title in cur_list:
                cur_list.remove(self.game_info.Info.Title)
            cur_list.insert(0, self.game_info.Info.Title)
            while len(cur_list) > MAX_RECENT_GAMES:
                cur_list.pop()
            if cur_list != self.game_lib.recent_list['played']:
                self.game_lib.recent_list['played'] = cur_list
                self.game_lib.saveRecent()
            # update recent tab
            vb_layout = self.game_lib.recent_tab_layouts['played']
            li = self.game_lib.lineitem_pointers.get(self.game_info.Dir)[0]
            if li == None:
                li = LineItem(game_lib=self.game_lib,
                              gpath=self.game_info.Dir,
                              vb_layout=vb_layout)
            vb_layout.insertWidget(0, li.widget)
        except:
            ans = Mbox.askquestion(title='Error',
                                   message=(f"Couldn't start '{self.game_info.Info.Title}'\n"
                                            "Would you like to change the executable path?\n"
                                            f"(Current Path: '{exe.relative_to(FPATH_GAMES)}')"))
            if ans == 'Yes':
                self.editGame()

    def openWebpage(self):
        startfile(self.game_info.Info.URL)

    def editGame(self):
        edit_ui = EditUI(game_lib=self.game_lib)
        edit_ui.fullInfo()
