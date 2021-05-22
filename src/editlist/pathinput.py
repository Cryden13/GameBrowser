from scrolledframe import ScrolledFrame as SFrame
from changecolor import invert
from tkinter.ttk import (
    Entry,
    Button,
    Style
)
from tkinter import (
    LabelFrame as LFrame,
    Frame
)

try:
    from .pathclear import clearPathInput
    from ..constants import *
except ImportError:
    from subprocess import run
    from pathlib import Path
    pth = Path(__file__).parents[2]
    run(['py', '-m', pth.name, 'console'], cwd=pth.parent)
    raise SystemExit

PPTH: dict[Frame, dict[str, U[bool, Entry, Button]]] = dict


class ProgramPathInput(SFrame):
    progPaths: PPTH
    topNameEnt: Entry

    def __init__(self, parent: LFrame, startRow: int, entryWd: int, progPaths: PPTH):
        scrollHt = round(EDIT_HT / 6.3)
        # init frame
        SFrame.__init__(self,
                        master=parent,
                        scrollbars='e',
                        padding=0,
                        doupdate=False,
                        scrollspeed=1,
                        relief='sunken',
                        bd=1,
                        height=scrollHt)
        self.grid(column=1,
                  columnspan=3,
                  row=startRow,
                  sticky='nsew')
        invertTextCol = invert(color=self.winfo_rgb('SystemButtonText'),
                               inputtype='RGB16')
        Style().configure('Path.TEntry',
                          foreground=invertTextCol)
        # init vars
        self.progPaths = progPaths
        nameWd = round(entryWd / 3.5)
        pathWd = (entryWd - nameWd)

        def getkwargs(func, wd):
            vcmd = (parent.register(func), '%W', '%V', '%P')
            return dict(style='Path.TEntry',
                        validate='all',
                        validatecommand=vcmd,
                        width=wd)
        nameKwargs = getkwargs(self.updateName, nameWd)
        pathKwargs = getkwargs(self.updatePath, pathWd)
        # fill frame
        for row in range(PROGFILE_INPUT_ROWS):
            self.builder(row, nameKwargs, pathKwargs)

    def builder(self, curRow: int, nKw: dict, pKw: dict) -> None:
        frm = Frame(self)
        frm.columnconfigure(1, weight=1)
        frm.grid(column=0,
                 row=curRow,
                 columnspan=2,
                 sticky='w')
        new: dict[str, U[bool, Entry]] = dict()
        # create 'name' entry
        new['name'] = Entry(master=frm,
                            **nKw)
        new['name'].grid(column=0,
                         row=0)
        new['name'].insert(0, "Preferred name")
        # create 'path' entry
        new['path'] = Entry(master=frm,
                            **pKw)
        new['path'].grid(column=1,
                         row=0)
        new['path'].insert(0, "Path to executable")
        # properly initialize lineitem
        if curRow == 0:
            new['show'] = True
            self.topNameEnt = new['name']
            new['name'].grid_remove()
        else:
            new['show'] = False
            new['button'] = Button(master=frm,
                                   text="Remove",
                                   command=(lambda f=frm: self.removeLine(f)))
            new['button'].grid(column=2,
                               row=0)
            frm.grid_remove()
        # add to dict
        self.progPaths[frm] = {**new}

    def updateName(self, *args) -> bool:
        return self.updateEnt("Preferred name", *args)

    def updatePath(self, *args) -> bool:
        return self.updateEnt("Path to executable", *args)

    def updateEnt(self, defTxt: str, name: str, eType: str, newTxt: str) -> bool:
        ent: Entry = self.nametowidget(name)
        if eType == 'key':
            if newTxt:
                ent.configure(style='TEntry')
        elif eType == 'focusin':
            if newTxt == defTxt:
                ent.delete(0, 'end')
        elif not newTxt or newTxt == defTxt:
            clearPathInput(ent, defTxt)
        return True

    def addLine(self) -> None:
        self.topNameEnt.grid()
        for frm, info in self.progPaths.items():
            if info['show']:
                continue
            else:
                frm.grid()
                self.progPaths[frm]['show'] = True
                break
        self.redraw()

    def removeLine(self, frm: Frame) -> None:
        frm.grid_remove()
        self.progPaths[frm]['show'] = False
        d = self.progPaths[frm]
        clearPathInput(d['name'], "Preferred name")
        clearPathInput(d['path'], "Path to executable")
        active = [i for i in self.progPaths.values() if i['show']]
        if len(active) == 1:
            self.topNameEnt.grid_remove()
        self.redraw()
