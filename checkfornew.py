from tkinter.ttk import Style
from tkinter import Tk
from os import chdir

from gamelibrary import GameLib
from constants import *


class HiddenTk(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry(f'+{CENTER.x - EDIT_WD / 2:.0f}'
                      f'+{CENTER.y - EDIT_HT / 2:.0f}')
        self.withdraw()
        Style().configure('.', font=FONT_DEF)
        self.option_add('*font', FONT_DEF)
        self.option_add('*TEntry.font', FONT_MD)
        self.option_add('*TCombobox.font', FONT_MD)


def main():
    chdir(PATH_GAMES)
    root = HiddenTk()
    gamelib = GameLib(root)
    gamelib.checkForNewGames()


if __name__ == '__main__':
    main()
