from pathlib import Path
from os import chdir
import logging
from sys import argv

from PyQt5.QtWidgets import QApplication

from commandline import openfile


try:
    from .src import *
except ImportError:
    from subprocess import run
    pth = Path(__file__).parent
    run(['py', '-m', pth.name], cwd=pth.parent)
    raise SystemExit


def main():
    chdir(FPATH_GAMES)
    errlog = Path(__file__).with_name('errorlog.txt')
    logging.basicConfig(filename=errlog,
                        filemode='w',
                        level=logging.ERROR,
                        format='[%(asctime)s] %(levelname)s: %(module)s.%(funcName)s\n%(message)s\n',
                        datefmt='%m/%d/%Y %I:%M:%S%p')
    try:
        app = QApplication(argv)
        MainWindow(app)
    except:
        logging.exception('')
        raise
    finally:
        if errlog.read_text():
            app.beep()
            openfile(errlog)


if __name__ == '__main__':
    main()
