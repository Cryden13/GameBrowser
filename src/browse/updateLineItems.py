from PyQt5.QtWidgets import QVBoxLayout
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Optional as O
)
from .lineItem import LineItem

if TYPE_CHECKING:
    from ..gamelibrary import GameLibrary, GAMEDATA_TYPE
    from ..edit import EditUI


class UpdateLineItems:
    gpath: Path
    ginfo: GAMEDATA_TYPE

    def __init__(self, game_lib: "GameLibrary", edit_ui: EditUI):
        self.game_lib = game_lib
        self.gpath = edit_ui.game_path
        ogpath = edit_ui.orig_path
        self.ginfo = self.game_lib.master_list[self.gpath]
        if edit_ui.output == 'add':
            self.addNewLineitem(3, None)
            self.addNewLineitem(2, self.game_lib.recent_tab_layouts['added'])
        else:
            lineitem_pointers = self.game_lib.lineitem_pointers[ogpath]
            for lineitem in lineitem_pointers:
                lineitem.update(self.gpath)
            if not lineitem_pointers[1]:
                self.addNewLineitem(
                    1, self.game_lib.recent_tab_layouts['updated'])

    def addNewLineitem(self, layout_index: int, vb_layout: O[QVBoxLayout]):
        li = LineItem(game_lib=self.game_lib,
                      gpath=self.gpath,
                      vb_layout=vb_layout)
        pointers = self.game_lib.lineitem_pointers.get(
            self.gpath, [None, None, None, None])
        pointers[layout_index] = li
        self.game_lib.lineitem_pointers.update({self.gpath, pointers})
