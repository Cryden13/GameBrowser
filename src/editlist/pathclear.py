from tkinter.ttk import Entry


def clearPathInput(widget: Entry, defTxt: str) -> None:
    widget.select_clear()
    widget.delete(0, 'end')
    widget.insert(0, defTxt)
    widget.configure(style='Path.TEntry')


if __name__ == '__main__':
    from subprocess import Popen
    from pathlib import Path
    pth = Path(__file__).parents[2]
    Popen(['py', '-m', pth.name, 'console'], cwd=pth.parent).wait()
    raise SystemExit
