from re import split as _split
from pathlib import Path
from configparser import (
    ExtendedInterpolation as _ExtInterp,
    ConfigParser as _ConfigParser
)
from win32api import (
    GetMonitorInfo as _GetMonitorInfo,
    MonitorFromPoint as _MonitorFromPoint
)
from typing import (
    Union as U,
    Optional as O
)

from joinwith import joinwith as _joinwith


GAMEDATA_TYPE = dict[str, dict[str, U[str, int, Path, dict[str, Path]]]]

_cfgfile = Path(__file__).parent.with_name('config.cfg')
_cfg = _ConfigParser(interpolation=_ExtInterp(),
                     allow_no_value=True)
_cfg.optionxform = str
_cfg.read_file(open(_cfgfile))


# path vars
_sct = 'Paths'
FPATH_GAMES = Path(_cfg.get(_sct, 'game_folder'))
FPATH_PROG = Path(_cfg.get(_sct, 'program_folder'))
FPATH_LIB = FPATH_PROG.joinpath('lib')
FPATH_IMGS = FPATH_LIB.joinpath('images')
PATH_LIST = FPATH_LIB.joinpath('Game List.json')
PATH_NEW = FPATH_LIB.joinpath('New Games.json')
PATH_RECENT = FPATH_LIB.joinpath('Recent.json')
PATH_ICON = str(FPATH_LIB.joinpath('favicon.ico'))

# windows
_sct = 'Windows'
MAIN_WD, MAIN_HT = [int(n) for n in _cfg.get(
    _sct, 'window_dimensions').split('x')]
EDIT_WD, EDIT_HT = [int(n) for n in _cfg.get(
    _sct, 'edit_ui_dimensions').split('x')]
RUN_MAX_WD, RUN_MAX_HT = [int(n) for n in _cfg.get(
    _sct, 'run_submenu_dimensions').split('x')]
MAX_RECENT_GAMES = _cfg.getint(_sct, 'recent_game_limit')

# colors
_sct = 'Colors'


class TEXT_COLORS:
    default = '#' + _cfg.get(_sct, 'default')
    Completed = '#' + _cfg.get(_sct, 'complete')
    Favorite = '#' + _cfg.get(_sct, 'favorite')
    Abandoned = '#' + _cfg.get(_sct, 'abandoned')


# reference vars
CAT_TOG: list[str] = list()
CAT_SEL: dict[str, list[str]] = dict()
for _cat, _opts in _cfg.items('Categories'):
    if _opts:
        CAT_SEL.update({_cat: _split(r', ?', _opts)})
    else:
        CAT_TOG.append(_cat)

TAG_TOG: list[str] = list()
TAG_SEL: dict[str, list[str]] = dict()
for _tag, _opts in _cfg.items('Tags'):
    if _opts:
        TAG_SEL.update({_tag: _split(r', ?', _opts)})
    else:
        TAG_TOG.append(_tag)

TAG_EQU: dict[str, str] = {
    k.lower(): v.lower() for k, v in _cfg.items('Tag Aliases')
}

#     ___   ___ _   _____   _  ______________
#    / _ | / _ \ | / / _ | / |/ / ___/ __/ _ \
#   / __ |/ // / |/ / __ |/    / /__/ _// // /
#  /_/ |_/____/|___/_/ |_/_/|_/\___/___/____/
_adv_cfgfile = Path(__file__).parents[1].joinpath('lib', 'advanced_config.cfg')
_adv_cfg = _ConfigParser(interpolation=_ExtInterp(),
                         allow_no_value=True)
_adv_cfg.optionxform = str
_adv_cfg.read_file(open(_adv_cfgfile))

# js selectors


class _SELECTORS:
    title, tags, desc, ver = [_adv_cfg.get('Javascript Selectors', k) for
                              k in ['title', 'tags', 'description', 'version']]


# text
_sct = 'Text'
FONT_FAMILY = _adv_cfg.get(_sct, 'font_family')
FONT_SZ_SMALL = _adv_cfg.getint(_sct, 'font_size_small')
FONT_SZ_DEFAULT = _adv_cfg.getint(_sct, 'font_size_default')
FONT_SZ_TITLE = _adv_cfg.getint(_sct, 'font_size_title')
FONT_SZ_HEADER = _adv_cfg.getint(_sct, 'font_size_header')
FONT_SZ_MAX = _adv_cfg.getint(_sct, 'font_size_max')
FONT_SHADOW = _adv_cfg.getint(_sct, 'title_shadow')

# executables
FILETYPES: list[str] = list()
_ftypes: list[str] = list()
for _nm, _exts in _adv_cfg.items('Executable File Types'):
    _exts = [f'.{_ext.strip(".")}' for _ext in _split(r', ?', _exts)]
    _fexts = _joinwith(_exts, ' ', ' ', '*{}')
    FILETYPES += _exts
    _ftypes.append(f'{_nm.title()} files ({_fexts})')
FILETYPENAMES: str = ';;'.join([*_ftypes, 'All files (*.*)'])

# windows
_sct = 'Windows'
SEARCH_MIN_WD, SEARCH_MIN_HT = [int(n) for n in
                                _adv_cfg.get(_sct, 'search_min_dimensions').split('x')]
PAD = _adv_cfg.getint(_sct, 'spacing')
GBOX_POSITION = _adv_cfg.get(_sct, 'groupbox_header_position')
GBOX_OFFSET = _adv_cfg.get(_sct, 'groupbox_header_offset')
_mon_from_pt = tuple(int(n) for n in
                     _adv_cfg.get(_sct, 'monitor_from_pt').split(', '))


# screen vars
_mon: dict[str, list[int]] = _GetMonitorInfo(_MonitorFromPoint(_mon_from_pt))
SCREEN_WD = _mon.get('Monitor', [0]*4)[2]
SCREEN_HT = _mon.get('Work', [0]*4)[3]
CENTER_X = (SCREEN_WD // 2)
CENTER_Y = (SCREEN_HT // 2)

if __name__ == '__main__':
    _all = globals().copy()
    for k, v in _all.items():
        if k[0] != '_':
            print(f'{k} = {v}')
