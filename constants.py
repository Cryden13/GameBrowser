from typing import TYPE_CHECKING, Union as U, Optional as O, Callable as C
from screeninfo import get_monitors as _get_monitors
from collections import OrderedDict as oDict
from tkinter import messagebox as Mbox
from os import path as os_path


# screen var
class CENTER:
    mon = _get_monitors()[0]
    x = (mon.width // 2)
    y = (mon.height // 2)


# path vars
PATH_PROG = os_path.dirname(__file__)
PATH_LIST = os_path.join(PATH_PROG, 'lib', 'Game List.json')
PATH_NEW = os_path.join(PATH_PROG, 'lib', 'New Games.json')
PATH_RECENT = os_path.join(PATH_PROG, 'lib', 'Recent.json')
PATH_GAMES = os_path.dirname(PATH_PROG)
# size vars for 'browse'
MAIN_WD = 1300
MAIN_HT = 1200
SEARCH_WD = 825
SEARCH_HT = 250
RUN_MAX_HT = 400
BTN_SIZE = 30
TEXTBOX_WD = dict(
    title=17,
    version=8,
    categories=19,
    tags=24
)
MAX_GAMES_PER_PAGE = 50
MAX_RECENT_GAMES = 15
# size vars for 'edit'
EDIT_WD = round(MAIN_WD * 0.85)
EDIT_HT = round(MAIN_HT * 0.55)
PROGFILE_INPUT_ROWS = 60
# other size vars
ADD_WD = 500
ADD_HT = 200
PAD = 6
INFO_MAX_COLS = 8
COMBOBOX_WD = 10
# default vars
FONT_DEF = 'Ebrima 11'
FONT_SM = 'Ebrima 8'
FONT_MD = 'Ebrima 10'
FONT_LG = 'Ebrima 14'
FONT_CAP = ['Gauge Heavy', 18]
COLOR_PLAY = 'spring green'
COLOR_LINK = 'light sky blue'
COLOR_EDIT = 'tan1'
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
INFO_ENT: oDict[str, U[int, list[int]]] = oDict({  # 'info entry label': entry_width
    'Title': 75,
    'URL': 100,
    'Version': 25,
    'Program Path': [105, 35, 85],  # [scroll_height, name_width, path_width]
    'Description': 75
})

CAT_TOG: list[str] = [
    'Favorite',
    'Eroge',
    'Completed',
    'Abandoned'
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
        'Unreal',
        'Wolf RPG'
    ],
    'Art': [
        'Real Porn',
        'Text',
        'Pixel',
        '3D',
        'Drawn'
    ],
    'Protagonist': [
        'Male',
        'Female',
        'Futa/Trans',
        'Multiple',
        'Created',
        'Unknown'
    ]
})
CAT_EQU: dict[str, str] = {  # 'f95zone tag': 'preferred alias'
    'japanese game': 'eroge',
    'text based': 'text',
    '3dcg': '3d',
    '2dcg': 'drawn'
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
    'Vore',
    'Yuri'
]
TAG_SEL: oDict[str, list[str]] = oDict({  # 'Combobox label': ['Combobox options']
})
TAG_EQU: dict[str, str] = {  # 'f95zone tag': 'preferred alias'
    'scat': 'gross',
    'urination': 'gross',
    'female domination': 'femdom',
    'lesbian': 'yuri'
}


# optional vars
class _SELECTOR:
    title = 'div[uix_component="MainContent"] h1.p-title-value'
    tags = 'li.groupedTags > a'
    desc = 'article.message-body.js-selectToQuote > div.bbWrapper > div > b'
    ver = 'article.message-body.js-selectToQuote b'
