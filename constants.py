from tkinter import messagebox as _mbox
from screeninfo import get_monitors as _get_monitors
from os import path as os_path


# screen var
_mon = _get_monitors()[0]


class CENTER:
    x = round(_mon.width / 2)
    y = round(_mon.height / 2)


# path vars
PATH_PROG = os_path.dirname(__file__)
_lib = os_path.join(PATH_PROG, 'lib')
PATH_LIST = os_path.join(_lib, 'Game List.json')
PATH_NEW = os_path.join(_lib, 'New Games.json')
PATH_RECENT = os_path.join(_lib, 'Recent.json')
PATH_GAMES = os_path.dirname(PATH_PROG)
# window size vars
MAIN_WD = 1270
MAIN_HT = 1200
EDIT_WD = round(MAIN_WD * 0.7)
EDIT_HT = round(MAIN_HT * 0.7)
ADD_WD = 500
ADD_HT = 200
# default vars
SEARCH_HT = 250
BTN_SIZE = 30
GRID_MIN_SIZE = 85
PAD = 6
MAX_CAT_COL = 5
MAX_TAG_COL = 6
GAMES_PER_PAGE = 50
FONT_SM = 'Calibri 8'
FONT_MD = 'Calibri 12'
FONT_LG = 'Calibri 16'
Mbox = _mbox
# reference vars
FILETYPES = [
    '.exe',
    '.jar',
    '.swf',
    '.html',
    '.url'
]
INFO_ENT = [
    'Title',
    'Version',
    'URL',
    'Program Path'
]
CAT_TOG = [
    'Completed',
    'Eroge',
    'Favorite'
]
CAT_LST = {
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
}
CAT_EQU = {
    'japanese game': 'eroge',
    'text based': 'text',
    '3dcg': '3d'
}
TAG_TOG = [
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
TAG_LST = {
    'Protagonist': [
        'Unknown',
        'Male',
        'Female',
        'Futa/Trans',
        'Male/Female',
        'Multiple',
        'Created'
    ]
}
TAG_EQU = {
    'scat': 'gross',
    'urination': 'gross',
    'female domination': 'femdom'
}
