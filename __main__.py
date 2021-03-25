from contextlib import redirect_stderr
from traceback import format_exc
from subprocess import Popen
from sys import argv
from os import chdir


try:
    from .src import *
except ImportError:
    from pathlib import Path
    pth = Path(__file__).parent
    Popen(['py', '-m', pth.name, 'console'], cwd=pth.parent).wait()
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
        with errlog.open('w') as log:
            with redirect_stderr(log):
                try:
                    self.run()
                except:
                    log.write(f'\n{format_exc()}')
        if errlog.read_text():
            Popen(['powershell',
                   '-command',
                   f'[system.media.systemsounds]::Hand.play(); Start-Process "{errlog}"'])
        else:
            errlog.unlink()


if __name__ == '__main__':
    main()
