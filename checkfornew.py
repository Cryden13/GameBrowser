from tkinter import Tk
from os import chdir

from constants import PATH_GAMES, CENTER, EDIT_WD, EDIT_HT
from gamelibrary import GameLib


class HiddenTk(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry(f'+{CENTER.x - EDIT_WD / 2:.0f}'
                      f'+{CENTER.y - EDIT_HT / 2:.0f}')
        self.withdraw()


def main():
    chdir(PATH_GAMES)
    root = HiddenTk()
    gamelib = GameLib(root)
    gamelib.checkForNewGames()


if __name__ == '__main__':
    main()
