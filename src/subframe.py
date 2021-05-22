from tkinter import (
    LabelFrame as LFrame,
    IntVar,
    Widget
)
from tkinter.ttk import (
    Checkbutton,
    Combobox
)

try:
    from .constants import *
except ImportError:
    from subprocess import run
    from pathlib import Path
    pth = Path(__file__).parents[1]
    run(['py', '-m', pth.name, 'console'], cwd=pth.parent)
    raise SystemExit

OUTTYPE: tuple[LFrame, dict[str, IntVar], dict[str, Combobox]] = tuple


class SubFrm(LFrame):
    setCbx: bool
    togVar: list[str]
    selVar: dict[str, list]
    row = col = int()

    def __init__(self, master: Widget, title: str):
        LFrame.__init__(self,
                        master=master,
                        text=title,
                        font=FONT_LG,
                        padx=PAD)

    def builder(self) -> OUTTYPE:
        def updatePosition() -> None:
            self.col += 1
            if self.col == INFO_MAX_COLS:
                self.col = int()
                self.row += 1

        togDict = {item: IntVar(self) for item in self.togVar}
        selDict: dict[str, Combobox] = dict()

        for item, vals in self.selVar.items():
            selDict[item] = self.addCombobox(item, vals)
            updatePosition()
        for item, var in togDict.items():
            self.addCheckbutton(item, var)
            updatePosition()

        return (self, togDict, selDict)

    def addCheckbutton(self, item: str, var: IntVar) -> None:
        def toggleNo(_) -> None:
            state = chk.state()
            if 'alternate' in state:
                var.set(0)
            else:
                var.set(-1)
                chk.state(['alternate'])

        chk = Checkbutton(master=self,
                          text=item,
                          variable=var)
        chk.grid(column=self.col,
                 row=self.row,
                 padx=(PAD // 2),
                 sticky='sw')
        chk.bind('<ButtonRelease-3>', toggleNo)

    def addCombobox(self, item: str, vals: list[str]) -> Combobox:
        lfrm = LFrame(master=self,
                      text=item,
                      font=FONT_SM)
        lfrm.grid(column=self.col,
                  row=self.row,
                  padx=(PAD // 2),
                  sticky='nw')
        cbxVals = ['Any', *vals] if self.setCbx else [*vals]
        cbx = Combobox(master=lfrm,
                       values=cbxVals,
                       width=COMBOBOX_WD,
                       state='readonly')
        if self.setCbx:
            cbx.current(0)
        cbx.grid(sticky='w')
        return cbx

    @classmethod
    def cats(cls, parent: Widget, setCbx: bool) -> OUTTYPE:
        cls.setCbx = setCbx
        cls.togVar = CAT_TOG
        cls.selVar = CAT_SEL
        return cls(parent, "Categories").builder()

    @classmethod
    def tags(cls, parent: Widget, setCbx: bool) -> OUTTYPE:
        cls.setCbx = setCbx
        cls.togVar = TAG_TOG
        cls.selVar = TAG_SEL
        return cls(parent, "Tags").builder()
