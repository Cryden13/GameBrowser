from traceback import format_exc
from gamelibrary import *


os_chdir(PATH_GAMES)
root = GUI()
gamelib = GameLib(root)
root.start_main(gamelib)
root.mainloop()
if format_exc()[: 14] != "NoneType: None":
    input("Fatal Exception occured. Press Enter to continue: ")
