from commandline import openfile
from winnotify import PlaySound
from os import chdir
from sys import argv
import logging


try:
    from .src import *
except ImportError:
    from subprocess import run
    from pathlib import Path
    pth = Path(__file__).parent
    run(['py', '-m', pth.name, 'console'], cwd=pth.parent)
    raise SystemExit


class main:
    def __init__(self):
        chdir(PATH_GAMES)
        if argv[-1] == 'console':
            self.arg = argv[-2]
            self.run()
        else:
            self.arg = argv[-1]
            self.doLog()

    def run(self):
        root = (AddGUI if self.arg == 'add'
                else CheckGUI if self.arg == 'check'
                else BrowseGUI)()
        gamelib = GameLib(root)
        root.after_idle(root.start_main, gamelib)
        root.mainloop()

    def doLog(self):
        errlog = PATH_PROG.joinpath('errorlog.txt')
        logging.basicConfig(filename=errlog,
                            filemode='w',
                            level=logging.ERROR,
                            format='[%(asctime)s] %(levelname)s: %(module)s.%(funcName)s\n%(message)s\n',
                            datefmt='%m/%d/%Y %I:%M:%S%p')
        try:
            self.run()
        except Exception:
            logging.exception('')
            raise
        finally:
            if errlog.read_text():
                PlaySound()
                openfile(errlog)


if __name__ == '__main__':
    main()
