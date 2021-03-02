from tkinter.ttk import Checkbutton, Combobox, Entry, Button, Style
from tkinter import IntVar, Frame, Canvas, Text, LabelFrame as LFrame
from re import sub as re_sub, findall as re_findall
from scrolledframe import ScrolledFrame as SFrame
from bs4 import BeautifulSoup as Html
from os import system as os_system, startfile as os_startfile
from urllib3 import PoolManager
from changecolor import invert, darken

from constants import _SELECTOR as Sel
from constants import *

if TYPE_CHECKING:
    from tkinter import Widget, StringVar, Event


class SubFrm(LFrame):
    setCbx: bool
    togVar: list[str]
    selVar: dict[str, list]
    row = col = int()

    def __init__(self, master: "Widget", title: str):
        LFrame.__init__(self,
                        master=master,
                        text=title,
                        font=FONT_LG,
                        padx=PAD)

    def builder(self) -> tuple[LFrame, dict[str, IntVar], dict[str, Combobox]]:
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
    def cats(cls, parent: "Widget", setCbx: bool) -> tuple[LFrame, dict[str, IntVar], dict[str, Combobox]]:
        cls.setCbx = setCbx
        cls.togVar = CAT_TOG
        cls.selVar = CAT_SEL
        return cls(parent, "Categories").builder()

    @classmethod
    def tags(cls, parent: "Widget", setCbx: bool) -> tuple[LFrame, dict[str, IntVar], dict[str, Combobox]]:
        cls.setCbx = setCbx
        cls.togVar = TAG_TOG
        cls.selVar = TAG_SEL
        return cls(parent, "Tags").builder()


class FillLineItem:
    lineitem: Canvas
    bg: str
    fol: str
    info: dict[str, str]
    title: str
    children: list[U[Canvas, LFrame, Text]]
    col: int
    row: int
    toolFrm: LFrame

    def __init__(self, lineItem: Canvas, bg: str, gFol: str, data: GAMEDATA_TYPE, startFunc: "C",
                 editFunc: "C", page: O[SFrame] = None, displayData: O[dict] = None):
        self.lineitem = lineItem
        self.bg = bg
        self.fol = gFol
        self.info = data['Info'].copy()
        cats = data['Categories'].copy()
        tags = data['Tags'].copy()
        self.title = self.info['Title']
        self.children = list()
        self.col = self.row = 0

        self.fillTools(startFunc, editFunc)
        self.fillText(cats, tags)

        if page:
            displayData[page][lineItem] = dict(folder=gFol,
                                               children=self.children)

    def fillTools(self, startFunc: "C", editFunc: "C") -> None:
        self.toolFrm = LFrame(master=self.lineitem,
                              font=FONT_SM,
                              text='Tools',
                              background=self.bg)
        self.toolFrm.grid(column=0,
                          row=0,
                          sticky='ns')
        self.toolFrm.columnconfigure(0, weight=1)

        # play btn
        def startGame(event: "Event"): startFunc(event=event,
                                                 gFolder=self.fol,
                                                 gTitle=self.title,
                                                 gPath=self.info['Program Path'])
        playBtn = self.canvasButton(color=COLOR_PLAY,
                                    txt='▶',
                                    cmd=startGame,
                                    fnt=FONT_CAP)
        # link btn
        def openLink(_): os_startfile(self.info['URL'])
        linkBtn = self.canvasButton(color=COLOR_LINK,
                                    txt='www',
                                    cmd=openLink)
        # edit btn
        def editGame(event: "Event"): editFunc(event=event,
                                               game=self.fol)
        editBtn = self.canvasButton(color=COLOR_EDIT,
                                    txt='Edit',
                                    cmd=editGame)
        self.children += [self.toolFrm, playBtn, linkBtn, editBtn]

    def canvasButton(self, color: str, txt: str, cmd: "C[[Event], None]", fnt: str = FONT_SM) -> Canvas:
        cnvBtn = Canvas(master=self.toolFrm,
                        width=BTN_SIZE,
                        height=BTN_SIZE,
                        bg=self.bg)
        cnvBtn.grid(column=0,
                    row=self.row,
                    sticky='ns',
                    pady=2)
        cir = cnvBtn.create_oval(0, 0,
                                 (BTN_SIZE - 1),
                                 (BTN_SIZE - 1),
                                 fill=color)
        cnvBtn.create_text((BTN_SIZE // 2),
                           (BTN_SIZE // 2 - 2),
                           text=txt,
                           font=fnt)
        hlcolor: str = darken(color=self.toolFrm.winfo_rgb(color),
                              inputtype='RGB16')
        cnvBtn.bind('<ButtonRelease-1>', cmd)

        def onEnter(_): cnvBtn.itemconfig(cir, fill=hlcolor)
        cnvBtn.bind('<Enter>', onEnter)

        def onLeave(_): cnvBtn.itemconfig(cir, fill=color)
        cnvBtn.bind('<Leave>', onLeave)
        self.row += 1
        return cnvBtn

    def fillText(self, cats: dict[str, U[str, int]], tags: dict[str, U[str, int]]) -> None:
        # title
        clr = 'gold' if cats.pop('Favorite') else 'SystemButtonText'
        self.children += self.textbox(title="Title",
                                      wd=TEXTBOX_WD['title'],
                                      txt=self.title,
                                      txtcol=clr)
        # version
        complete = cats.pop('Completed')
        abandoned = cats.pop('Abandoned')
        clr = 'white' if complete else 'darkred' if abandoned else 'SystemButtonText'
        self.children += self.textbox(title="Version",
                                      wd=TEXTBOX_WD['version'],
                                      txt=self.info['Version'],
                                      txtcol=clr)
        # categories
        curCats = ['[Eroge]'] if cats.pop('Eroge') else list()
        curCats += [f'{c}: {v}' for c, v in cats.items()]
        self.children += self.textbox(title="Categories",
                                      wd=TEXTBOX_WD['categories'],
                                      txt='\n'.join(curCats))
        # tags
        curTags = [t for t, v in tags.items() if v]
        self.children += self.textbox(title="Tags",
                                      wd=TEXTBOX_WD['tags'],
                                      txt=', '.join(curTags))
        # description
        self.children += self.textbox(title="Description",
                                      wd=INFO_ENT['Description'],
                                      txt=self.info['Description'])

    def textbox(self, title: str, wd: int, txt: str, txtcol: str = 'SystemButtonText') -> list[LFrame, Text]:
        self.col += 1
        lf = LFrame(master=self.lineitem,
                    font=FONT_SM,
                    text=title,
                    background=self.bg)
        lf.grid(column=self.col,
                row=0,
                sticky='ns')
        t = Text(master=lf,
                 width=wd,
                 height=5,
                 wrap='word',
                 padx=(PAD // 2),
                 pady=(PAD // 2),
                 bg=self.bg,
                 fg=txtcol)
        t.grid()
        t.insert('end', txt)
        t.config(state='disabled')
        return [lf, t]


class GetF95Info(Html):
    catToggles: dict[str, IntVar]
    catSelects: dict[str, Combobox]
    tagToggles: dict[str, IntVar]
    tagSelects: dict[str, Combobox]
    infoEnts: "dict[str, StringVar]"
    infoDesc: "Text"

    def __init__(self, catToggles: dict[str, IntVar], catSelects: dict[str, Combobox],
                 tagToggles: dict[str, IntVar], tagSelects: dict[str, Combobox],
                 infoEnts: "dict[str, StringVar]", infoDesc: "Text", url: str):
        self.catToggles = catToggles
        self.catSelects = catSelects
        self.tagToggles = tagToggles
        self.tagSelects = tagSelects
        self.infoEnts = infoEnts
        self.infoDesc = infoDesc
        pool = PoolManager()
        raw = pool.request('GET', url).data
        decoded = raw.decode('utf-8', errors='ignore')
        Html.__init__(self, decoded, 'html.parser')
        self.getInfo()

    def getInfo(self) -> None:
        # header
        rawHeader = self.select(Sel.title)
        self.fillHeader(rawHeader)
        # tags
        rawTags = {t.get_text() for t in self.select(Sel.tags)}
        self.fillTags(rawTags)
        # description
        rawContent = self.select(Sel.desc)
        self.fillDescription(rawContent)
        # version
        self.fillVersion()
        os_system('nircmd stdbeep')

    def fillHeader(self, rawHeader) -> None:
        if not rawHeader:
            return
        header = rawHeader[0].get_text().lower()
        headerInfo: list[str]
        headerInfo = re_findall(r'(?<=\[).+?(?=\])',
                                self.formatStr(header))
        for item in headerInfo:
            for status in ['Completed', 'Abandoned']:
                if status.lower() in item:
                    self.catToggles[status].set(1)
            for c in CAT_SEL['Format']:
                if c.lower() in item:
                    self.catSelects['Format'].set(c)

    def fillTags(self, rawTags: set[str]) -> None:
        if not rawTags:
            return
        subbedTags = {v for k, v in (TAG_EQU | CAT_EQU).items()
                      if k in rawTags}
        allTags = rawTags - {*TAG_EQU, *CAT_EQU} | subbedTags
        if not allTags:
            return
        # set toggle tags
        for tag in [t for t in TAG_TOG if t.lower() in allTags]:
            self.tagToggles[tag].set(1)
        # set toggle categories
        for tag in [t for t in CAT_TOG if t.lower() in allTags]:
            self.catToggles[tag].set(1)
        # set art category
        for tag in CAT_SEL['Art']:
            if tag.lower() in allTags:
                self.catSelects['Art'].set(tag)
                break
        # set protagonist
        if 'character creation' in allTags:
            protag = 'Created'
        else:
            protag = self.getProtagonist(allTags)
        self.catSelects['Protagonist'].set(protag)

    def fillDescription(self, rawContent) -> None:
        if not rawContent:
            return
        rawDesc = rawContent[0].find_parent().get_text()
        desc = re_sub(r'(?s)\s*(Overview:?|Spoiler.+?register now\.)\s*',
                      r'',
                      self.formatStr(rawDesc))
        self.infoDesc.insert(1.0, desc.strip())

    def fillVersion(self) -> None:
        for el in self.select(Sel.ver):
            if 'version' in el.get_text().lower():
                ver = el.next_sibling.strip(' :')
                self.infoEnts['Version'].set(ver)
                break

    @staticmethod
    def formatStr(s: str) -> str:
        string = re_sub(r'\s*(\r+|\n+)\s*',
                        r'\n',
                        ''.join(s))
        encoded = string.encode('ascii', 'ignore')
        return encoded.decode().strip()

    @staticmethod
    def getProtagonist(allTags: str) -> str:
        rawProtag = {t.split(' ')[0] for t in allTags
                     if 'protagonist' in t}
        protagCt = len(rawProtag)
        if protagCt == 0:
            return 'Unknown'
        elif protagCt == 1:
            for protag in CAT_SEL['Protagonist']:
                if protag.lower() in rawProtag:
                    return protag
        elif 'multiple' in rawProtag or protagCt > 1:
            return 'Multiple'
        return 'Unknown'


class ProgramPathInput(SFrame):
    progPaths: oDict[Frame, dict[str, U[bool, Entry, Button]]]
    topNameEnt: Entry

    def __init__(self, scrollHt: int, nameWd: int, pathWd: int, parent: LFrame, startRow: int,
                 progPaths: oDict[Frame, dict[str, U[bool, Entry, Button]]]):
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
        kwargs = dict(style='Path.TEntry',
                      validate='all')
        vArgs = ('%W', '%V', '%P')
        nameKwargs = kwargs.copy() | dict(
            validatecommand=(parent.register(self.updateName), *vArgs),
            width=nameWd
        )
        pathKwargs = kwargs.copy() | dict(
            validatecommand=(parent.register(self.updatePath), *vArgs),
            width=pathWd
        )
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
        new: dict[str, U[bool, Entry, Button]] = dict()
        # create 'name' entry
        new['name'] = Entry(master=frm, **nKw)
        new['name'].grid(column=0,
                         row=0)
        new['name'].insert(0, "Preferred name")
        # create 'path' entry
        new['path'] = Entry(master=frm, **pKw)
        new['path'].grid(column=1,
                         row=0)
        new['path'].insert(0, "Path to executable")
        # create button
        if curRow == 0:
            new['show'] = True
            self.topNameEnt = new['name']
            # create 'add' button
            new['button'] = Button(master=frm,
                                   text="Add Another Exe",
                                   command=self.addLine)
            new['name'].grid_remove()
        else:
            new['show'] = False
            # create 'remove' button
            new['button'] = Button(master=frm,
                                   text="Remove",
                                   command=(lambda f=frm: self.removeLine(f)))
            frm.grid_remove()
        new['button'].grid(column=2,
                           row=0)
        # add to dict
        self.progPaths[frm] = {**new}

    def updateName(self, *args) -> bool:
        return self.updateEnt("Preferred name", *args)

    def updatePath(self, *args) -> bool:
        return self.updateEnt("Path to executable", *args)

    def updateEnt(self, defTxt: str, name: str, why: str, newTxt: str) -> bool:
        widget: Entry = self.nametowidget(name)
        if why == 'key':
            if newTxt:
                widget.configure(style='TEntry')
        elif why == 'focusin':
            if newTxt == defTxt:
                widget.select_range(0, 'end')
        elif not newTxt or newTxt == defTxt:
            clearPathInput(widget, defTxt)
        return True

    def addLine(self) -> None:
        self.topNameEnt.grid()
        for frame, info in self.progPaths.items():
            if info['show']:
                continue
            else:
                frame.grid()
                self.progPaths[frame]['show'] = True
                break
        self.redraw()

    def removeLine(self, frame: Frame) -> None:
        frame.grid_remove()
        self.progPaths[frame]['show'] = False
        d = self.progPaths[frame]
        clearPathInput(d['name'], "Preferred name")
        clearPathInput(d['path'], "Path to executable")
        active = [i for i in self.progPaths.values() if i['show']]
        if len(active) == 1:
            self.topNameEnt.grid_remove()
        self.redraw()


def clearPathInput(widget: Entry, defTxt: str) -> None:
    widget.select_clear()
    widget.delete(0, 'end')
    widget.insert(0, defTxt)
    widget.configure(style='Path.TEntry')
