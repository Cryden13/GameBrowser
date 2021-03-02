from os import chdir

from constants import PATH_GAMES
from browse import GUI
from gamelibrary import GameLib


if __name__ == '__main__':
    chdir(PATH_GAMES)
    root = GUI()
    gamelib = GameLib(root)
    root.start_main(gamelib)
    root.mainloop()
