from tkinter import Tk, Toplevel, Frame, Canvas, Label, Text, StringVar, LabelFrame as LFrame
from scrolledframe import ScrolledFrame as SFrame
from tkinter.ttk import Style, Button, Notebook
from os import startfile as os_startfile
from changecolor import lighten

from editlist import EditGames
from builders import SubFrm, FillLineItem
from constants import *

if TYPE_CHECKING:
    from tkinter import IntVar, Event, Widget
    from tkinter.ttk import Combobox

    from gamelibrary import GameLib


disp_child = list[U[Canvas, LFrame, Text]]
disp_type = dict[SFrame, dict[Canvas, dict[str, U[str, disp_child]]]]


class GUI(Tk):
    gamelib: "GameLib"
    bgDef: str
    bgLit: str
    statMsg: StringVar
    displayData: disp_type
    gameSearch: list[str]
    curSearch: dict[str, U[str, int]]
    searchFrm: LFrame
    catToggles: "dict[str, IntVar]"
    catSelects: "dict[str, Combobox]"
    tagToggles: "dict[str, IntVar]"
    tagSelects: "dict[str, Combobox]"
    gameDisplay: Notebook
    playedScrl: SFrame
    addedScrl: SFrame
    statLbl: Label

    def __init__(self):
        Tk.__init__(self)
        self.configure(padx=PAD)
        self.geometry(f'{MAIN_WD}'
                      f'x{MAIN_HT}'
                      f'+{CENTER.x - MAIN_WD / 2:.0f}'
                      f'+{CENTER.y - MAIN_HT / 2:.0f}')
        self.title("Game List")
        self.protocol("WM_DELETE_WINDOW",
                      lambda: [self.withdraw(), self.destroy()])
        Style().configure('.', font=FONT_DEF)
        self.option_add('*font', FONT_DEF)
        self.option_add('*TEntry.font', FONT_MD)
        self.option_add('*TCombobox.font', FONT_MD)
        self.update_idletasks()

    def start_main(self, gamelib) -> None:
        # init vars
        self.gamelib = gamelib
        self.bgDef = self.cget('background')
        self.bgLit = lighten(color=self.winfo_rgb(self.bgDef),
                             percent=5,
                             inputtype='RGB16')
        self.statMsg = StringVar()
        self.displayData = dict()
        self.gameSearch = list(self.gamelib.masterlist)
        self.curSearch = dict()
        # add elements
        chkBtn = Button(master=self,
                        text="Check for new games",
                        command=self.checkForNew)
        chkBtn.place(anchor='sw',
                     relx=0,
                     x=PAD,
                     y=SEARCH_HT)
        self.createSearch()
        self.createDisplay()
        self.showDisplay()

    def createSearch(self) -> None:
        # create container
        self.searchFrm = LFrame(master=self,
                                font=FONT_CAP,
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
        self.playedScrl = self.createScrollFrm(parent=self.gameDisplay)
        self.gameDisplay.add(self.playedScrl.container, text='  Recent  ')
        self.addedScrl = self.createScrollFrm(parent=self.gameDisplay)
        self.gameDisplay.add(self.addedScrl.container, text='New/Updated')
        self.gameDisplay.grid(column=0,
                              row=0,
                              sticky='nsew')
        self.gameDisplay.grid_remove()

        self.statLbl = Label(master=displayFrm,
                             textvariable=self.statMsg,
                             font=FONT_CAP)
        self.statLbl.grid(column=0,
                          row=0,
                          sticky='nsew')

        self.showLabel("Loading")
        self.redrawPlayed()
        self.redrawAdded()
        self.redrawDisplay()

    @staticmethod
    def createScrollFrm(parent: U[Notebook, Toplevel]) -> SFrame:
        return SFrame(master=parent,
                      scrollbars='e',
                      padding=0,
                      dohide=False,
                      doupdate=False,
                      scrollspeed=1,
                      relief='sunken',
                      bd=1)

    def redrawRecent(self, scrl: SFrame, key: str) -> None:
        for w in scrl.winfo_children():
            w.destroy()
        for gFol, data in self.gamelib.masterlist.items():
            title = data['Info']['Title']
            if title in self.gamelib.recentList[key]:
                i = self.gamelib.recentList[key].index(title)
                bg = self.bgLit if (i % 2) else self.bgDef
                lineItem = Canvas(master=scrl,
                                  bg=bg)
                lineItem.grid(column=0,
                              row=i,
                              padx=(PAD // 2),
                              pady=(PAD // 2))
                FillLineItem(lineItem=lineItem,
                             bg=bg,
                             gFol=gFol,
                             data=data,
                             startFunc=self.startGame,
                             editFunc=self.editGame)
        scrl.redraw()

    def redrawPlayed(self): self.redrawRecent(self.playedScrl, 'play')
    def redrawAdded(self): self.redrawRecent(self.addedScrl, 'new')

    def redrawDisplay(self) -> None:
        for page in self.displayData:
            page.destroy()
        self.displayData.clear()
        pgSplit = self.gamelib.splitByLetter()
        for pg, gFols in pgSplit.items():
            sframe = self.createScrollFrm(parent=self.gameDisplay)
            self.displayData[sframe] = dict()
            self.gameDisplay.add(sframe.container, text=f'{pg: ^10}')
            for row, gFol in enumerate(gFols):
                data = self.gamelib.masterlist.get(gFol)
                bg = self.bgLit if (row % 2) else self.bgDef
                lineItem = Canvas(sframe,
                                  background=bg)
                lineItem.grid(column=0,
                              row=row,
                              padx=PAD / 2,
                              pady=PAD / 2)
                FillLineItem(lineItem=lineItem,
                             bg=bg,
                             gFol=gFol,
                             data=data,
                             startFunc=self.startGame,
                             editFunc=self.editGame,
                             page=sframe,
                             displayData=self.displayData)
        for pg in self.displayData:
            pg.redraw()
            pg.scrollCanvas.yview_moveto(0)

    def showDisplay(self, index: int = 0) -> None:
        self.statLbl.grid_remove()
        self.gameDisplay.grid()
        self.gameDisplay.select(index)
        self.update()

    def showLabel(self, msg: str) -> None:
        self.statMsg.set(f"{msg}, Please Wait...")
        self.gameDisplay.grid_remove()
        self.statLbl.grid()
        self.update()

    def startGame(self, event: "Event", gFolder: str, gTitle: str, gPath: U[str, list, dict]) -> None:
        def run(exe: str) -> None:
            if tw:
                tw.destroy()
            try:
                os_startfile(exe)
                # update recent
                curList = self.gamelib.recentList['play'].copy()
                if gTitle in curList:
                    curList.remove(gTitle)
                curList.insert(0, gTitle)
                while len(curList) > MAX_RECENT_GAMES:
                    curList.pop()
                if curList != self.gamelib.recentList['play']:
                    self.gamelib.recentList['play'] = curList
                    self.redrawPlayed()
                    self.gamelib.saveRecent()
            except Exception:
                if Mbox.askyesno(title="Error",
                                 message=(f"Couldn't start '{gTitle}'.\n"
                                          f"Would you like to change the executable path? "
                                          f"(Current Path = '{exe}')")):
                    self.editGame(event, gFolder)

        pathInfo: dict[str, str] = dict()
        if isinstance(gPath, str):
            tw = None
            run(os_path.join(PATH_GAMES, gPath))
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
            if isinstance(gPath, dict):
                for lbl, ex in gPath.items():
                    pathInfo[lbl] = os_path.join(PATH_GAMES, ex)
            else:
                for ex in gPath:
                    lbl = os_path.splitext(os_path.basename(ex))[0]
                    pathInfo[lbl] = os_path.join(PATH_GAMES, ex)
            for lbl, exePath in pathInfo.items():
                btn = Button(master=scrl,
                             text=lbl,
                             command=lambda x=exePath: run(x))
                btn.grid(sticky='ew')
            scrl.redraw()
            wd = (scrl.winfo_reqwidth() + scrl.vScrbar.winfo_reqwidth() + PAD * 2)
            ht = min(RUN_MAX_HT, (scrl.winfo_reqheight() + PAD * 2))
            posX = event.x_root - 5
            posY = event.y_root
            if (posX + wd) > CENTER.mon.width:
                posX = (posX - wd)
            if (posY + ht) > CENTER.mon.height:
                posY = (posY - ht)
            tw.geometry(f'{wd}x{ht}+{posX}+{posY}')
            tw.focus_set()
            tw.bind('<FocusOut>', lambda _: tw.destroy())

    def editGame(self, event: "Event", game: str) -> None:
        updateGame: str = EditGames(parent=self,
                                    gamelib=self.gamelib,
                                    allGames=[game])
        if updateGame:
            # get vars
            item: "Widget" = event.widget
            for _ in range(2):
                item = self.nametowidget(item.winfo_parent())
            lineItem: Canvas = item
            for page, line in self.displayData.items():
                if lineItem in line:
                    break
            if not page:
                return
            bg: str = lineItem.cget('background')
            data = self.gamelib.masterlist[updateGame]
            # remove current children
            for child in lineItem.winfo_children():
                child.destroy()
            # update gameSearch
            if updateGame not in self.gameSearch and game in self.gameSearch:
                self.gameSearch.pop(self.gameSearch.index(game))
                self.gameSearch.append(updateGame)
            # refill line item
            FillLineItem(lineItem=lineItem,
                         bg=bg,
                         gFol=updateGame,
                         data=data,
                         startFunc=self.startGame,
                         editFunc=self.editGame,
                         page=page,
                         displayData=self.displayData)
            page.redraw()
            self.redrawAdded()

    def checkForNew(self) -> None:
        updateGames = self.gamelib.checkForNewGames()
        if updateGames:
            self.showLabel("Reloading")
            self.redrawDisplay()
            if self.curSearch:
                self.clearSearch("Reloading")
            self.redrawAdded()
            self.showDisplay()

    def updateDisplay(self) -> None:
        for lines in self.displayData.values():
            index = int()
            for line, info in lines.items():
                if info['folder'] in self.gameSearch:
                    bg = self.bgLit if (index % 2) else self.bgDef
                    line.grid()
                    line.configure(background=bg)
                    for w in info['children']:
                        w.configure(background=bg)
                    index += 1
                else:
                    line.grid_remove()
        self.update()
        for pg in self.displayData:
            pg.redraw()
            pg.scrollCanvas.yview_moveto(0)

    def clearSearch(self, lbl: str = "Clearing") -> None:
        for chk in (self.catToggles | self.tagToggles).values():
            chk.set(0)
        for cbx in (self.catSelects | self.tagSelects).values():
            cbx.current(0)
        if self.curSearch:
            self.showLabel(lbl)
            self.gameSearch = list(self.gamelib.masterlist)
            self.updateDisplay()
            self.curSearch.clear()
            self.showDisplay()

    def searchBrowse(self) -> None:
        sInfo: "dict[str, U[IntVar, Combobox]]"
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
                    data = (allData['Categories'] | allData['Tags'])
                    if search.items() <= data.items():
                        self.gameSearch.append(gFol)
                self.updateDisplay()
                self.curSearch = search
                self.showDisplay(2)
            else:
                self.clearSearch()
