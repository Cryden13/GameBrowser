from tkinter import Tk, Toplevel, Frame, Canvas, Label, Text, StringVar, IntVar, Event
from tkinter import LabelFrame as LFrame
from tkinter.ttk import Style, Button, Notebook, Combobox
from scrolledframe import ScrolledFrame as SFrame
from changecolor import lighten
from os import startfile
from time import time

try:
    from ..editlist import EditGames
    from .lineitem import LineItem
    from ..subframe import SubFrm
    from ..constants import *
except ImportError:
    from subprocess import run
    from pathlib import Path
    pth = Path(__file__).parents[2]
    run(['py', '-m', pth.name, 'console'], cwd=pth.parent)
    raise SystemExit

if TYPE_CHECKING:
    from ..gamelibrary import GameLib


disp_child: list[U[Canvas, LFrame, Text]] = list
FillLineItem = LineItem.Fill


class BrowseGUI(Tk):
    gamelib: "GameLib"
    bgDef: str
    bgLit: str
    statMsg: StringVar
    curSearch: dict[str, U[str, int]]
    gameSearch: list[Path]
    gamePointers: dict[Path,
                       dict[str, dict[str, U[Canvas, SFrame, disp_child]]]]
    searchFrm: LFrame
    catToggles: dict[str, IntVar]
    catSelects: dict[str, Combobox]
    tagToggles: dict[str, IntVar]
    tagSelects: dict[str, Combobox]
    searchCt: StringVar
    gameDisplay: Notebook
    playedScrl: SFrame
    updatedScrl: SFrame
    addedScrl: SFrame
    statLbl: Label
    time: float

    def __init__(self):
        Tk.__init__(self)
        self.configure(padx=PAD)
        self.geometry(f'{MAIN_WD}'
                      f'x{MAIN_HT}'
                      f'+{CENTER_X - MAIN_WD // 2}'
                      f'+{CENTER_Y - MAIN_HT // 2}')
        self.title("Game List")
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        Style().configure('.', font=FONT_DEF)
        self.option_add('*font', FONT_DEF)
        self.option_add('*TEntry.font', FONT_MD)
        self.option_add('*TCombobox.font', FONT_MD)
        self.update_idletasks()

    def on_exit(self):
        self.showLabel("Closing")
        for w in self.gameDisplay.winfo_children():
            self.gameDisplay.select(w)
            w.destroy()
            self.updateLabel()
        self.destroy()

#     ___  __  ________   ___
#    / _ )/ / / /  _/ /  / _ \
#   / _  / /_/ // // /__/ // /
#  /____/\____/___/____/____/

    def start_main(self, gamelib) -> None:
        # init vars
        self.gamelib = gamelib
        bg = self.winfo_rgb(self.cget('background'))
        self.bgDef = f"#{''.join(f'{n >> 8:02x}' for n in bg)}"
        self.bgLit = lighten(color=self.bgDef,
                             percent=5,
                             inputtype='HEX')
        self.statMsg = StringVar()
        self.curSearch = dict()
        self.gameSearch = list()
        self.gamePointers = dict()
        for gFol in self.gamelib.masterlist.keys():
            self.gameSearch.append(gFol)
            self.gamePointers[gFol] = dict(played=dict(),
                                           updated=dict(),
                                           added=dict(),
                                           browse=dict())
        # add elements
        chkBtn = Button(master=self,
                        text="Check for new games",
                        command=self.checkForNew)
        chkBtn.place(anchor='sw',
                     relx=0,
                     x=PAD,
                     y=SEARCH_HT)
        rfrshBtn = Button(master=self,
                          text="Refresh",
                          command=self.redrawAll)
        rfrshBtn.place(anchor='sw',
                       relx=0.5,
                       x=(SEARCH_WD // 2 + PAD),
                       y=SEARCH_HT)
        self.createSearch()
        self.createDisplay()
        self.redrawAll("Loading")

    def createSearch(self) -> None:
        # create container
        self.searchFrm = LFrame(master=self,
                                font=FONT_TTL,
                                text="Search",
                                padx=PAD)
        self.searchFrm.place(anchor='n',
                             relx=0.5,
                             rely=0,
                             width=SEARCH_WD,
                             height=SEARCH_HT)
        self.searchFrm.columnconfigure(0, weight=1)
        self.searchFrm.rowconfigure(0, weight=2)
        self.searchFrm.rowconfigure(1, weight=2)
        # add category frame
        cfrm, self.catToggles, self.catSelects = SubFrm.cats(
            parent=self.searchFrm,
            setCbx=True)
        cfrm.grid(column=0,
                  row=0,
                  sticky='nsew')
        # add tag frame
        tfrm, self.tagToggles, self.tagSelects = SubFrm.tags(
            parent=self.searchFrm,
            setCbx=True)
        tfrm.grid(column=0,
                  row=1,
                  pady=PAD,
                  sticky='nsew')
        # add buttons
        btnFrm = Frame(master=self.searchFrm)
        btnFrm.grid(column=0,
                    row=2,
                    pady=PAD)
        btnFrm.columnconfigure(0, weight=1)
        btnFrm.columnconfigure(1, weight=1)
        clrBtn = Button(master=btnFrm,
                        text="Clear",
                        command=self.clearSearch)
        clrBtn.grid(column=0,
                    row=0,
                    padx=50)
        srchBtn = Button(master=btnFrm,
                         text="Search",
                         command=self.searchBrowse)
        srchBtn.grid(column=1,
                     row=0,
                     padx=50)
        self.searchCt = StringVar()
        resCtLbl = Label(master=btnFrm,
                         textvariable=self.searchCt,
                         font=FONT_SM)
        resCtLbl.place(anchor='center',
                       relx=0.5,
                       rely=0.5)

    def createDisplay(self) -> None:
        displayFrm = Frame(master=self,
                           padx=PAD,
                           pady=PAD,
                           bd=2,
                           relief='sunken')
        displayFrm.columnconfigure(0, weight=1)
        displayFrm.rowconfigure(0, weight=1)
        displayFrm.place(anchor='s',
                         relx=0.5,
                         rely=1,
                         y=(-PAD),
                         relwidth=1,
                         relheight=1,
                         height=(-SEARCH_HT - PAD * 2))

        self.gameDisplay = Notebook(master=displayFrm)
        self.gameDisplay.grid(column=0,
                              row=0,
                              sticky='nsew')
        self.gameDisplay.grid_remove()

        recentDisplay = Notebook(master=self.gameDisplay)
        self.gameDisplay.add(recentDisplay, text=" Recent ")

        self.playedScrl = self.createScrollFrm(parent=recentDisplay)
        recentDisplay.add(self.playedScrl.container, text=" Recently Played ")
        self.updatedScrl = self.createScrollFrm(parent=recentDisplay)
        recentDisplay.add(self.updatedScrl.container,
                          text=" Recently Updated ")
        self.addedScrl = self.createScrollFrm(parent=recentDisplay)
        recentDisplay.add(self.addedScrl.container, text=" Recently Added ")

        self.statLbl = Label(master=displayFrm,
                             textvariable=self.statMsg,
                             font=FONT_TTL)
        self.statLbl.grid(column=0,
                          row=0,
                          sticky='nsew')

    @ staticmethod
    def createScrollFrm(parent: U[Notebook, Toplevel]) -> SFrame:
        return SFrame(master=parent,
                      scrollbars='e',
                      padding=0,
                      doupdate=False,
                      scrollspeed=1,
                      relief='sunken',
                      bd=1)

#     ___  _______  ___  ___ _      __
#    / _ \/ __/ _ \/ _ \/ _ | | /| / /
#   / , _/ _// // / , _/ __ | |/ |/ /
#  /_/|_/___/____/_/|_/_/ |_|__/|__/

    def redrawAll(self, lbl: str = "Redrawing") -> None:
        self.showLabel(lbl)
        self.redrawPlayed()
        self.redrawUpdated()
        self.redrawAdded()
        self.redrawDisplay()
        self.showDisplay()

    def redrawPlayed(self): self.recentRedraw(self.playedScrl, 'played')
    def redrawUpdated(self): self.recentRedraw(self.updatedScrl, 'updated')
    def redrawAdded(self): self.recentRedraw(self.addedScrl, 'added')

    def recentRedraw(self, scrl: SFrame, key: str) -> None:
        for w in scrl.winfo_children():
            w.destroy()
        recentlist = {f: d for t in self.gamelib.recentlist[key]
                      for f, d in self.gamelib.masterlist.items()
                      if t == d['Info']['Title']}
        for i, (gFol, data) in enumerate(recentlist.items()):
            self.updateLabel()
            bg = self.bgLit if (i % 2) else self.bgDef
            lineItem = Canvas(master=scrl,
                              bg=bg)
            lineItem.grid(column=0,
                          row=i,
                          padx=(PAD // 2),
                          pady=(PAD // 2))
            child = FillLineItem(lineItem=lineItem,
                                 bg=bg,
                                 gFol=gFol,
                                 data=data,
                                 startFunc=self.startGame,
                                 editFunc=self.editGame)
            if gFol not in self.gamePointers:
                self.gamePointers[gFol] = dict(played=dict(),
                                               updated=dict(),
                                               added=dict(),
                                               browse=dict())
            self.gamePointers[gFol][key] = dict(lineitem=lineItem,
                                                page=scrl,
                                                children=child)
        scrl.redraw()

    def redrawDisplay(self) -> None:
        for info in self.gamePointers.values():
            pg = info['browse'].get('page')
            if pg:
                info['browse']['page'].destroy()
        pgSplit = self.gamelib.splitByLetter()
        for pg, gFols in pgSplit.items():
            sframe = self.createScrollFrm(parent=self.gameDisplay)
            self.gameDisplay.add(sframe.container, text=f'{pg: ^10}')
            for row, gFol in enumerate(gFols):
                self.updateLabel()
                data = self.gamelib.masterlist.get(gFol)
                bg = self.bgLit if (row % 2) else self.bgDef
                lineItem = Canvas(sframe,
                                  background=bg)
                lineItem.grid(column=0,
                              row=row,
                              padx=(PAD // 2),
                              pady=(PAD // 2))
                child = FillLineItem(lineItem=lineItem,
                                     bg=bg,
                                     gFol=gFol,
                                     data=data,
                                     startFunc=self.startGame,
                                     editFunc=self.editGame)
                self.gamePointers[gFol].update(browse=dict(lineitem=lineItem,
                                                           page=sframe,
                                                           children=child))
            self.gameDisplay.select(sframe.container)
            sframe.redraw()

#    __  _____  ___  ___ __________
#   / / / / _ \/ _ \/ _ /_  __/ __/
#  / /_/ / ___/ // / __ |/ / / _/
#  \____/_/  /____/_/ |_/_/ /___/

    def showDisplay(self, index: int = 0) -> None:
        self.statLbl.grid_remove()
        self.gameDisplay.select(index)
        self.gameDisplay.grid()
        self.update_idletasks()

    def showLabel(self, msg: str) -> None:
        self.statMsg.set(f"{msg}, Please wait")
        self.gameDisplay.grid_remove()
        self.statLbl.grid()
        self.update()
        self.time = time()

    def updateLabel(self) -> None:
        t = time()
        if (t - self.time) > 1:
            msg = self.statMsg.get()
            self.statMsg.set(f"{msg}.")
            self.statLbl.update_idletasks()
            self.time = t

    def updateDisplay(self) -> None:
        indices: dict[SFrame, int] = dict()
        for gFol, info in self.gamePointers.items():
            lib = info['browse']
            line = lib['lineitem']
            if gFol in self.gameSearch:
                sframe = lib['page']
                i = indices.get(sframe, 0)
                bg = self.bgLit if (i % 2) else self.bgDef
                line.grid()
                line.configure(background=bg)
                for w in lib['children']:
                    w.configure(background=bg)
                indices[sframe] = (i + 1)
            else:
                line.grid_remove()
        self.update_idletasks()
        for pg in indices:
            self.gameDisplay.select(pg.container)
            pg.redraw()

#     ______  ___  ___________
#    / __/ / / / |/ / ___/ __/
#   / _// /_/ /    / /___\ \
#  /_/  \____/_/|_/\___/___/

    def startGame(self, event: Event, gFolder: Path, gTitle: str, gPath: U[Path, dict[str, Path]]) -> None:
        def run(exe: Path) -> None:
            if tw:
                tw.destroy()
            try:
                startfile(exe)
                # update recent
                curList = self.gamelib.recentlist['played'].copy()
                if gTitle in curList:
                    curList.remove(gTitle)
                curList.insert(0, gTitle)
                while len(curList) > MAX_RECENT_GAMES:
                    curList.pop()
                if curList != self.gamelib.recentlist['played']:
                    self.gamelib.recentlist['played'] = curList
                    self.redrawPlayed()
                    self.gamelib.saveRecent()
            except Exception:
                if Mbox.askyesno(title="Error",
                                 message=(f"Couldn't start '{gTitle}'.\n"
                                          f"Would you like to change the executable path? "
                                          f"(Current Path = '{exe.relative_to(PATH_GAMES)}')")):
                    self.editGame(gFolder)

        if isinstance(gPath, Path):
            tw = None
            run(gPath)
        else:
            tw = Toplevel(master=self,
                          padx=PAD,
                          pady=PAD)
            tw.overrideredirect(1)
            scrl = SFrame(master=tw,
                          scrollbars='e',
                          padding=0,
                          doupdate=False,
                          scrollspeed=1,
                          bd=0)
            scrl.place(relx=0,
                       rely=0,
                       relwidth=1,
                       relheight=1)
            for lbl, exePath in gPath.items():
                btn = Button(master=scrl,
                             text=lbl,
                             command=lambda x=exePath: run(x))
                btn.grid(sticky='ew')
            scrl.redraw()
            wd = (scrl.winfo_reqwidth() +
                  scrl.scrollbar_v.winfo_reqwidth() +
                  PAD * 2)
            ht = min(RUN_MAX_HT, (scrl.winfo_reqheight() + PAD * 2))
            posX = event.x_root - 5
            posY = event.y_root
            if (posX + wd) > SCREEN_WD:
                posX = (posX - wd)
            if (posY + ht) > SCREEN_HT:
                posY = (posY - ht)
            tw.geometry(f'{wd}x{ht}+{posX}+{posY}')
            tw.focus_set()
            tw.bind('<FocusOut>', lambda _: tw.destroy())

    def editGame(self, gFol: Path) -> None:
        updateGame: Path = EditGames(parent=self,
                                     gamelib=self.gamelib,
                                     allGames=[gFol])
        if updateGame:
            # update gameSearch
            if updateGame not in self.gameSearch and gFol in self.gameSearch:
                self.gameSearch.pop(self.gameSearch.index(gFol))
                self.gameSearch.append(updateGame)
            # get vars
            data = self.gamelib.masterlist[updateGame]
            allInfo = self.gamePointers.pop(gFol)
            self.gamePointers[updateGame] = dict(play=dict(),
                                                 new=dict(),
                                                 browse=dict())
            for key, info in allInfo.items():
                if not info:
                    continue
                lineItem = info['lineitem']
                bg: str = lineItem.cget('background')
                # remove current children
                for child in info['children']:
                    child.destroy()
                # refill line item
                info['children'] = FillLineItem(lineItem=lineItem,
                                                bg=bg,
                                                gFol=updateGame,
                                                data=data,
                                                startFunc=self.startGame,
                                                editFunc=self.editGame)
                info['page'].redraw()
                self.gamePointers[updateGame][key] = info
            self.redrawUpdated()

    def checkForNew(self) -> None:
        updateGames = self.gamelib.checkForNewGames()
        if updateGames:
            if self.curSearch:
                self.clearSearch("Reloading")
            self.showLabel("Reloading")
            self.redrawDisplay()
            self.redrawAdded()
            self.showDisplay()

#     ___________   ___  _______ __
#    / __/ __/ _ | / _ \/ ___/ // /
#   _\ \/ _// __ |/ , _/ /__/ _  /
#  /___/___/_/ |_/_/|_|\___/_//_/

    def clearSearch(self, lbl: str = "Clearing") -> None:
        for chk in (self.catToggles | self.tagToggles).values():
            chk.set(0)
        for cbx in (self.catSelects | self.tagSelects).values():
            cbx.current(0)
        self.searchCt.set('')
        if self.curSearch:
            self.showLabel(lbl)
            self.gameSearch = list(self.gamelib.masterlist)
            self.updateDisplay()
            self.curSearch.clear()
            self.showDisplay()

    def searchBrowse(self) -> None:
        sInfo: dict[str, U[IntVar, Combobox]]
        sInfo = (self.catToggles | self.catSelects |
                 self.tagToggles | self.tagSelects)
        search = dict()
        for key, v in sInfo.items():
            if v.get() not in [0, 'Any']:
                val = 0 if v.get() == -1 else v.get()
                search[key] = val
        if search != self.curSearch:
            if search:
                self.showLabel("Searching")
                self.gameSearch.clear()
                for gFol, allData in self.gamelib.masterlist.items():
                    self.updateLabel()
                    data = (allData['Categories'] | allData['Tags'])
                    if search.items() <= data.items():
                        self.gameSearch.append(gFol)
                self.searchCt.set(f'{len(self.gameSearch)}\nresults')
                self.updateDisplay()
                self.curSearch = search
                self.showDisplay(1)
            else:
                self.clearSearch()
