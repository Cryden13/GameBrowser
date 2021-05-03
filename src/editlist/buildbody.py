from tkinter.ttk import Label, Button, Entry
from tkinter import Text, Frame, StringVar
from tkinter import LabelFrame as LFrame
from commandline import openatfile

try:
    from ..constants import *
    from ..subframe import SubFrm
    from .pathinput import ProgramPathInput
except ImportError:
    from subprocess import run
    from pathlib import Path
    pth = Path(__file__).parents[2]
    run(['py', '-m', pth.name, 'console'], cwd=pth.parent)
    raise SystemExit

if TYPE_CHECKING:
    from .editgui import EditGUI


class BuildBody(LFrame):
    gui: "EditGUI"
    curRow: int
    item: str
    size: int

    def __init__(self, gui: "EditGUI", parent: Frame):
        LFrame.__init__(self,
                        master=parent,
                        text="Info",
                        padx=PAD)
        self.gui = gui
        self.buildHeader()
        self.buildEntries()
        self.buildSelects()

    def buildHeader(self) -> None:
        pathFrm = LFrame(self.master,
                         text="Top Path",
                         padx=PAD)
        pathFrm.grid(column=0,
                     row=0,
                     sticky='ew')
        pathFrm.columnconfigure(0, weight=1)
        # label
        self.gui.pathLbl = StringVar()
        lbl = Label(pathFrm,
                    font=FONT_LG,
                    textvariable=self.gui.pathLbl)
        lbl.grid(column=0,
                 row=0,
                 sticky='w')
        pathBtn = Button(master=pathFrm,
                         text="Open",
                         command=(lambda: openatfile(self.gui.game)))
        pathBtn.grid(column=1,
                     row=0)

    def buildEntries(self) -> None:
        self.grid(column=0,
                  row=1,
                  sticky='nsew')
        self.columnconfigure(3, weight=1)
        self.curRow = 0
        for self.item, self.size in INFO_ENT.items():
            # add label
            lbl = Label(master=self,
                        text=self.item)
            lbl.grid(column=0,
                     row=self.curRow,
                     pady=(2, 0),
                     sticky='n')
            # add entry fields
            if self.item == 'Description':
                self.description()
            elif self.item == 'Program Path':
                self.programFiles()
            else:
                self.entries()
            self.curRow += 1

    def description(self) -> None:
        txt = Text(master=self,
                   width=self.size,
                   height=TEXTBOX_HT,
                   wrap='word',
                   padx=(PAD // 2),
                   pady=(PAD // 2))
        txt.grid(column=1,
                 row=self.curRow,
                 columnspan=2,
                 sticky='w',
                 pady=(0, PAD))
        self.gui.infoDesc = txt

    def programFiles(self) -> None:
        self.rowconfigure(self.curRow, weight=1)
        scrl = ProgramPathInput(parent=self,
                                startRow=self.curRow,
                                entryWd=self.size,
                                progPaths=self.gui.progPaths)
        btnfrm = Frame(master=scrl)
        for n in (0, 1):
            btnfrm.columnconfigure(n, weight=1)
        btnfrm.grid(column=0,
                    columnspan=3,
                    row=PROGFILE_INPUT_ROWS,
                    sticky='ew')
        addBtn = Button(master=btnfrm,
                        text="Add Another Exe",
                        command=scrl.addLine)
        addBtn.grid(column=0,
                    row=0,
                    padx=10,
                    sticky='e')
        browseBtn = Button(master=btnfrm,
                           text="Browse for Executable...",
                           command=self.gui.browseFolders)
        browseBtn.grid(column=1,
                       row=0,
                       padx=10,
                       sticky='w')
        scrl.redraw()
        self.gui.addPpthLine = scrl.addLine

    def entries(self) -> None:
        var = StringVar()
        ent = Entry(master=self,
                    textvariable=var,
                    width=self.size)
        ent.grid(column=1,
                 row=self.curRow,
                 sticky='w')
        self.gui.infoEnts[self.item] = var
        if self.item == 'URL':
            # add url button
            urlBtn = Button(master=self,
                            text="Lookup/Open Webpage",
                            command=self.gui.lookupOpenURL)
            urlBtn.grid(column=2,
                        row=self.curRow)
        elif self.item == 'Image':
            # add img button
            imgBtn = Button(master=self,
                            text="Search for image",
                            command=lambda v=var: self.gui.browseImgs(v))
            imgBtn.grid(column=2,
                        row=self.curRow,
                        sticky='w')
        elif self.item == 'Title':
            self.gui.titleEnt = ent

    def buildSelects(self) -> None:
        cfrm, self.gui.catToggles, self.gui.catSelects = SubFrm.cats(parent=self.master,
                                                                     setCbx=False)
        cfrm.grid(column=0,
                  row=2,
                  sticky='nsew')
        tfrm, self.gui.tagToggles, self.gui.tagSelects = SubFrm.tags(parent=self.master,
                                                                     setCbx=False)
        tfrm.grid(column=0,
                  row=3,
                  sticky='nsew')
