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
MAIN_WD = _cfg.getint(_sct, 'window_width')
MAIN_HT = _cfg.getint(_sct, 'window_height')
EDIT_WD = _cfg.getint(_sct, 'edit_ui_width')
EDIT_HT = _cfg.getint(_sct, 'edit_ui_height')
RUN_MAX_WD = _cfg.getint(_sct, 'run_submenu_width')
RUN_MAX_HT = _cfg.getint(_sct, 'run_submenu_height')
MAX_RECENT_GAMES = _cfg.getint(_sct, 'recent_game_limit')


# colors
_sct = 'Colors'
TEXT_COLORS = {
    'default': '#' + _cfg.get(_sct, 'default'),
    'Completed': '#' + _cfg.get(_sct, 'complete'),
    'Favorite': '#' + _cfg.get(_sct, 'favorite'),
    'Abandoned': '#' + _cfg.get(_sct, 'abandoned')
}


# js selectors
class _SELECTORS:
    title, tags, desc, ver = [_cfg.get('Javascript Selectors', k) for
                              k in ['title', 'tags', 'description', 'version']]


# reference vars
FILETYPES: list[str] = list()
_ftypes: list[str] = list()
for _nm, _exts in _cfg.items('Executable File Types'):
    _exts = [f'.{_ext.strip(".")}' for _ext in _split(r', ?', _exts)]
    _fexts = _joinwith(_exts, ' ', ' ', '*{}')
    FILETYPES += _exts
    _ftypes.append(f'{_nm.title()} files ({_fexts})')
FILETYPENAMES: str = ';;'.join([*_ftypes, 'All files (*.*)'])

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

# screen vars
_mon: dict[str, list[int]] = _GetMonitorInfo(_MonitorFromPoint((0, 0)))
SCREEN_WD = _mon.get('Monitor', [0]*4)[2]
SCREEN_HT = _mon.get('Work', [0]*4)[3]
CENTER_X = (SCREEN_WD // 2)
CENTER_Y = (SCREEN_HT // 2)


if __name__ == '__main__':
    from subprocess import run
    pth = Path(__file__).parents[1]
    run(['py', '-m', pth.name], cwd=pth.parent)
    raise SystemExit
