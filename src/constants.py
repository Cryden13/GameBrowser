from configparser import ConfigParser
from configparser import ExtendedInterpolation as ExtInterp
from tkinter import messagebox as Mbox
from typing import TYPE_CHECKING
from typing import (Union as U,
                    Optional as O,
                    Callable as C)
from screeninfo import get_monitors
from joinwith import joinwith
from PIL import ImageFont
from pathlib import Path
from re import split


GAMEDATA_TYPE: dict[str, dict[str, U[str, int, Path, dict[str, Path]]]] = dict

cfgfile = Path(__file__).parents[1].joinpath('config.cfg')
cfg = ConfigParser(allow_no_value=True,
                   interpolation=ExtInterp())
cfg.optionxform = str
cfg.read_file(open(cfgfile))

# path vars
sct = 'Paths'
PATH_GAMES = Path(cfg.get(sct, 'game_folder'))
PATH_PROG = Path(cfg.get(sct, 'program_folder'))
PATH_LIB = PATH_PROG.joinpath('lib')
PATH_LIST = PATH_LIB.joinpath('Game List.json')
PATH_NEW = PATH_LIB.joinpath('New Games.json')
PATH_RECENT = PATH_LIB.joinpath('Recent.json')
PATH_IMGS = PATH_LIB.joinpath('imgs')

# font vars
sct = 'Fonts'
FONT_DEF = cfg.get(sct, 'default').split(', ')
FONT_SM = cfg.get(sct, 'small').split(', ')
FONT_MD = cfg.get(sct, 'medium').split(', ')
FONT_LG = cfg.get(sct, 'large').split(', ')
FONT_TTL = cfg.get(sct, 'title').split(', ')
fntpth = Path(f'C:\\Windows\\Fonts\\{FONT_DEF[0]}.ttf')
FONT_IMG = ImageFont.truetype(font=str(fntpth if fntpth.exists()
                                       else fntpth.with_stem('Arial')),
                              size=int(FONT_DEF[1]) + 5)

# color vars
sct = 'Colors'
COLOR_PLAY = cfg.get(sct, 'play_button')
COLOR_LINK = cfg.get(sct, 'link_button')
COLOR_EDIT = cfg.get(sct, 'edit_button')

# size vars
sct = 'Sizes'
PAD = cfg.getint(sct, 'padding')
INFO_MAX_COLS = cfg.getint(sct, 'input_colomn_limit')
COMBOBOX_WD = cfg.getint(sct, 'combobox_width')
PROGFILE_INPUT_ROWS = cfg.getint(sct, 'executables_per_game_limit')

# window dimensions
sct = 'Window Dimensions'
MAIN_WD = cfg.getint(sct, 'browse_width')
MAIN_HT = cfg.getint(sct, 'browse_height')
EDIT_WD = cfg.getint(sct, 'edit_width')
EDIT_HT = cfg.getint(sct, 'edit_height')
ADD_WD = cfg.getint(sct, 'add_width')
ADD_HT = cfg.getint(sct, 'add_height')

# browse vars
sct = 'Browse Window'
MAX_GAMES_PER_PAGE = cfg.getint(sct, 'max_games_per_page')
MAX_RECENT_GAMES = cfg.getint(sct, 'recent_limit')
SEARCH_WD = cfg.getint(sct, 'search_width')
SEARCH_HT = cfg.getint(sct, 'search_height')
RUN_MAX_HT = cfg.getint(sct, 'run_submenu_max_height')
BTN_SIZE = cfg.getint(sct, 'tool_button_size')
TEXTBOX_HT = cfg.getint(sct, 'lineitem_char_height')
TEXTBOX_WD = {i: int(v) for i in 'version categories tags'.split()
              for k, v in cfg.items(sct)
              if k.split('_')[0] == i}
IMG_SIZE = cfg.getint(sct, 'title_image_width')
IMG_FADE = f"{255 - cfg.getint(sct, 'title_image_fade'):02x}"


# js selectors
class _SELECTORS:
    title, tags, desc, ver = [cfg.get('Javascript Selectors', k) for
                              k in 'title tags desc ver'.split()]


# reference vars
FILETYPES: list[str] = list()
FILETYPENAMES: list[tuple[str, str]] = [('All types (*.*)', '*')]
for _nm, _exts in cfg.items('Executable File Types'):
    _exts = [f'.{_ext.strip(".")}' for _ext in split(r', ?', _exts)]
    _fexts = joinwith(_exts, '; ', '; ', '*{}')
    FILETYPES += _exts
    FILETYPENAMES.append((f'{_nm.title()} file ({_fexts})', _fexts))

INFO_ENT: dict[str, U[int, list[int]]] = {
    k: int(v) for k, v in cfg.items('Info - Input')
}

CAT_TOG: list[str] = cfg.options('Categories - Toggleable')

CAT_SEL: dict[str, list[str]] = {
    k: v.replace("''", "'").split(', ') for k, v in cfg.items('Categories - Selected')
}

CAT_EQU: dict[str, str] = {
    k.lower(): v.lower() for k, v in cfg.items('Categories - Rename')
}

TAG_TOG: list[str] = [
    t for t in cfg.options('Tags - Toggleable')
]

TAG_SEL: dict[str, list[str]] = {
    k: v.replace("''", "'").split(', ') for k, v in cfg.items('Tags - Selected')
}

TAG_EQU: dict[str, str] = {
    k.lower(): v.lower() for k, v in cfg.items('Tags - Rename')
}

# screen vars
mon = get_monitors()[0]
SCREEN_WD = mon.width
CENTER_X = (SCREEN_WD // 2)
SCREEN_HT = mon.height
CENTER_Y = (SCREEN_HT // 2)

del (ConfigParser,
     ExtInterp,
     ImageFont,
     split,
     joinwith,
     get_monitors,
     cfgfile,
     cfg,
     sct,
     fntpth,
     mon)


if __name__ == '__main__':
    from subprocess import Popen
    pth = Path(__file__).parents[1]
    Popen(['py', '-m', pth.name, 'console'], cwd=pth.parent).wait()
    raise SystemExit
