from contextlib import redirect_stderr
from commandline import openfile
from traceback import format_exc
from winnotify import playSound
from datetime import datetime
from os import chdir
from sys import argv


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
        errlog.unlink(missing_ok=True)
        with errlog.open('w') as log:
            with redirect_stderr(log):
                try:
                    self.run()
                except:
                    log.write(f'\n{datetime.now()}\n{format_exc()}')
        if errlog.read_text():
            playSound()
            openfile(errlog)
        else:
            errlog.unlink()


if __name__ == '__main__':
    main()
