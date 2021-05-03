from tkinter.ttk import Style
from tkinter import Tk

try:
    from ..constants import *
except ImportError:
    from subprocess import run
    from pathlib import Path
    pth = Path(__file__).parents[2]
    run(['py', '-m', pth.name, 'check', 'console'], cwd=pth.parent)
    raise SystemExit


if TYPE_CHECKING:
    from ..gamelibrary import GameLib


class CheckGUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry(f'+{CENTER_X - EDIT_WD // 2}'
                      f'+{CENTER_Y - EDIT_HT // 2}')
        self.withdraw()
        Style().configure('.', font=FONT_DEF)
        self.option_add('*font', FONT_DEF)
        self.option_add('*TEntry.font', FONT_MD)
        self.option_add('*TCombobox.font', FONT_MD)
        self.update_idletasks()

    def start_main(self, gamelib: "GameLib") -> None:
        gamelib.checkForNewGames()
        self.destroy()
