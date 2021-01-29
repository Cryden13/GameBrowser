from os import path as os_path, listdir as os_listdir, curdir as os_curdir, system as os_system, startfile as os_startfile, chdir as os_chdir
import json


PATH_PROG = os_path.dirname(__file__)
PATH_GAMES = os_path.dirname(PATH_PROG)
PATH_LIST = os_path.join(PATH_PROG, 'Game List.json')
PATH_NEW = os_path.join(PATH_PROG, 'New Games.json')
WIDTH = 1265
HEIGHT = 1200
SEARCH_HT = 250
BTNSIZE = 30
GRIDMIN = 85
PAD = 6
FILETYPES = [
    '.exe',
    '.jar',
    '.swf',
    '.html',
    '.url'
]
MAX_CAT_COL = 5
MAX_TAG_COL = 6

FONT_SM = 'Calibri 8'
FONT_MD = 'Calibri 12'
FONT_LG = 'Calibri 16'

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
        'Multiple'
    ]
}

TAG_EQU = {
    'scat': 'gross',
    'urination': 'gross',
    'female domination': 'femdom'
}
CAT_EQU = {
    'japanese game': 'eroge',
    'text based': 'text',
    '3dcg': '3d'
}

if os_path.exists(PATH_LIST):
    with open(PATH_NEW, 'r') as f:
        NEW_DATA = json.load(f)
