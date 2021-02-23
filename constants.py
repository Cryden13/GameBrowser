from tkinter.ttk import Checkbutton as _Checkbutton, Combobox as _Combobox
from tkinter import messagebox as Mbox, LabelFrame as _LFrame, IntVar as _IntVar, StringVar as _StringVar, Canvas as _Canvas
from screeninfo import get_monitors as _get_monitors
from collections import OrderedDict as oDict
from typing import Union as U, Optional as Opt
from os import path as os_path


# screen vars
class CENTER:
    mon = _get_monitors()[0]
    x = round(mon.width / 2)
    y = round(mon.height / 2)


# path vars
PATH_PROG = os_path.dirname(__file__)
PATH_LIST = os_path.join(PATH_PROG, 'lib', 'Game List.json')
PATH_NEW = os_path.join(PATH_PROG, 'lib', 'New Games.json')
PATH_RECENT = os_path.join(PATH_PROG, 'lib', 'Recent.json')
PATH_GAMES = os_path.dirname(PATH_PROG)
# window size vars
MAIN_WD = 1275
MAIN_HT = 1200
EDIT_WD = round(MAIN_WD * 0.77)
EDIT_HT = round(MAIN_HT * 0.55)
ADD_WD = 500
ADD_HT = 200
RUN_MAX_HT = 400
# default vars
SEARCH_HT = 250
BTN_SIZE = 30
GRID_MIN_SIZE = 85
PAD = 6
MAX_CAT_COL = 5
MAX_TAG_COL = 6
MAX_GAMES_PER_PAGE = 50
MAX_RECENT_GAMES = 15
FONT_SM = 'Calibri 8'
FONT_MD = 'Calibri 12'
FONT_LG = 'Calibri 16'
COLOR_PLAY = '#87ffb9'
COLOR_LINK = '#9cd4ff'
COLOR_EDIT = '#e3b668'
GAMEDATA_TYPE = dict[str, dict[str, U[str, int, list[str], dict[str, str]]]]
# reference vars (in order of appearence/preference)
FILETYPES: list[str] = [
    '.exe',
    '.jar',
    '.swf',
    '.html',
    '.url',
    '.lnk'
]
INFO_ENT: oDict[str, U[int, list[int]]] = oDict({  # info entry label = entry_width
    'Title': 75,
    'URL': 100,
    'Version': 25,
    'Program Path': [105, 35, 85],  # [scroll_height, name_width, path_width]
    'Description': [75, 5]  # [text_width, text_height]
})
CAT_TOG: list[str] = [
    'Completed',
    'Eroge',
    'Favorite'
]
CAT_SEL: oDict[str, list[str]] = oDict({  # 'Combobox label': ['Combobox options']
    'Status': [
        'New',
        'Playing',
        'Beaten'
    ],
    'Format': [
        'Flash',
        'HTML',
        'Java',
        'Others',
        'Ren\'Py',
        'RPGM',
        'Unity',
        'Unreal Engine',
        'Wolf RPG'
    ],
    'Art': [
        '3D',
        'Drawn',
        'Pixel',
        'Text',
        'Real Porn'
    ]
})
CAT_EQU: dict[str, str] = {  # 'f95zone tag': 'preferred alias'
    'japanese game': 'eroge',
    'text based': 'text',
    '3dcg': '3d'
}
TAG_TOG: list[str] = [
    'Animated',
    'Bestiality',
    'Corruption',
    'Femdom',
    'Footjob',
    'Furry',
    'Futa/Trans',
    'Gay',
    'Gross',
    'Incest',
    'Loli',
    'Monster Girl',
    'Shota',
    'Sissification',
    'Vore'
]
TAG_SEL: oDict[str, list[str]] = oDict({  # 'Combobox label': ['Combobox options']
    'Protagonist': [
        'Unknown',
        'Male',
        'Female',
        'Futa/Trans',
        'Male/Female',
        'Multiple',
        'Created'
    ]
})
TAG_EQU: dict[str, str] = {  # 'f95zone tag': 'preferred alias'
    'scat': 'gross',
    'urination': 'gross',
    'female domination': 'femdom'
}


# optional vars
class _SELECTOR:
    title = 'div[uix_component="MainContent"] h1.p-title-value'
    tags = 'li.groupedTags > a'
    desc = 'article.message-body.js-selectToQuote > div.bbWrapper > div > b'
    ver = 'article.message-body.js-selectToQuote b'


class _createSubFrm(_LFrame):
    setCbx: bool
    togVar: list[str]
    selVar: dict[str, list]
    maxCol: int

    def __init__(self, master, title):
        _LFrame.__init__(self,
                         master=master,
                         font=FONT_MD,
                         text=title,
                         padx=PAD)
        for n in range(self.maxCol):
            self.columnconfigure(n, minsize=GRID_MIN_SIZE)

    def __builder(self) -> tuple[_LFrame, dict[str, _IntVar], dict[str, _Combobox]]:
        togDict = {item: _IntVar(self) for item in self.togVar}
        selDict: dict[str, _Combobox] = dict()
        curRow = curCol = int()
        # add checkbuttons
        for item, var in togDict.items():
            chk = _Checkbutton(master=self,
                               text=item,
                               variable=var)
            chk.grid(column=curCol,
                     row=curRow,
                     padx=(PAD // 2),
                     sticky='w')
            if curCol < self.maxCol:
                curCol += 1
            else:
                curCol = int()
                curRow += 1
        # add comboboxes
        for item, vals in self.selVar.items():
            lfrm = _LFrame(master=self,
                           text=item,
                           font=FONT_SM)
            lfrm.grid(column=curCol,
                      row=curRow,
                      padx=(PAD // 2))
            cbxVals = ['Any', *vals] if self.setCbx else vals.copy()
            cbx = _Combobox(master=lfrm,
                            values=cbxVals,
                            width=13,
                            state='readonly')
            if self.setCbx:
                cbx.current(0)
            cbx.grid(sticky='w')
            selDict[item] = cbx
            if curCol < self.maxCol:
                curCol += 1
            else:
                curCol = int()
                curRow += 1
        return (self, togDict, selDict)

    @classmethod
    def cats(cls, parent: U[_Canvas, _LFrame], setCbx: bool) -> tuple[_LFrame, dict[str, _IntVar], dict[str, _Combobox]]:
        cls.setCbx = setCbx
        cls.togVar = CAT_TOG
        cls.selVar = CAT_SEL
        cls.maxCol = MAX_CAT_COL
        return cls(parent, "Categories").__builder()

    @classmethod
    def tags(cls, parent: U[_Canvas, _LFrame], setCbx: bool) -> tuple[_LFrame, dict[str, _IntVar], dict[str, _Combobox]]:
        cls.setCbx = setCbx
        cls.togVar = TAG_TOG
        cls.selVar = TAG_SEL
        cls.maxCol = MAX_TAG_COL
        return cls(parent, "Tags").__builder()
