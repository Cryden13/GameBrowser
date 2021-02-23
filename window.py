from tkinter import Tk, Toplevel, Frame, Canvas, Label, Text, StringVar, LabelFrame as LFrame, Event, Widget
from scrolledframe import ScrolledFrame as SFrame
from tkinter.ttk import Style, Button, Notebook
from os import startfile as os_startfile
from changecolor import lighten, darken

from constants import _createSubFrm as SubFrm
from editlist import EditGames
from constants import *

from typing import Callable, TYPE_CHECKING
if TYPE_CHECKING:
    from tkinter.ttk import Combobox
    from gamelibrary import GameLib
    from tkinter import IntVar


disp_child = list[U[Canvas, LFrame, Text]]
disp_type = dict[SFrame, dict[Canvas, dict[str, U[str, disp_child]]]]


class GUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.configure(padx=PAD)
        self.geometry(f'{MAIN_WD}'
                      f'x{MAIN_HT}'
                      f'+{CENTER.x - MAIN_WD / 2:.0f}'
                      f'+{CENTER.y - MAIN_HT / 2:.0f}')
        self.title("Game List")
        Style().configure('.', font=FONT_MD)
        self.update_idletasks()

    def start_main(self, gamelib: "GameLib") -> None:
        # init vars
        self.gamelib = gamelib
        self.bgDef = str('SystemButtonFace')
        self.bgLit = str(lighten(color=self.winfo_rgb(self.bgDef),
                                 percent=5,
                                 inputtype='RGB',
                                 bitdepth=16))
        self.statMsg = StringVar()
        self.displayData: disp_type = dict()
        self.gameSearch = list(self.gamelib.masterlist)
        self.curSearch: dict[str, U[str, int]] = dict()
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
                                font=FONT_LG,
                                text="Search",
                                padx=PAD)
        self.searchFrm.place(anchor='n',
                             relx=0.5,
                             rely=0,
                             relwidth=0.6,
                             height=SEARCH_HT)
        self.searchFrm.columnconfigure(0, weight=1)
        self.searchFrm.rowconfigure(0, weight=2)
        self.searchFrm.rowconfigure(1, weight=2)
        # add categories
        cfrm, self.catToggles, self.catSelects = SubFrm.cats(
            parent=self.searchFrm,
            setCbx=True)
        cfrm.grid(column=0,
                  row=0,
                  sticky='nsew')
        # add tags
        tfrm, self.tagToggles, self.tagSelects = SubFrm.tags(
            parent=self.searchFrm,
            setCbx=True)
        tfrm.grid(column=0,
                  row=1,
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
        self.recentScrl = self.createScrollFrm(parent=self.gameDisplay)
        self.gameDisplay.add(self.recentScrl.container, text='  Recent  ')
        self.gameDisplay.grid(column=0,
                              row=0,
                              sticky='nsew')
        self.gameDisplay.grid_remove()

        self.statLbl = Label(master=displayFrm,
                             textvariable=self.statMsg,
                             font=FONT_LG)
        self.statLbl.grid(column=0,
                          row=0,
                          sticky='nsew')

        self.showLabel("Loading")
        self.redrawRecent()
        self.redrawDisplay()

    @staticmethod
    def createScrollFrm(parent: U[Notebook, Toplevel], padding: U[list, int] = [0, 0, 0, PAD], dohide: bool = False, bd: int = 1) -> SFrame:
        return SFrame(master=parent,
                      scrollbars='e',
                      padding=padding,
                      dohide=dohide,
                      doupdate=False,
                      scrollspeed=1,
                      relief='sunken',
                      bd=bd)

    def redrawRecent(self) -> None:
        for w in self.recentScrl.winfo_children():
            w.destroy()
        for gFol, data in self.gamelib.masterlist.items():
            title = data['Info']['Title']
            if title in self.gamelib.recentList:
                i = self.gamelib.recentList.index(title)
                bg = self.bgLit if (i % 2) else self.bgDef
                lineItem = Canvas(self.recentScrl,
                                  background=bg)
                lineItem.grid(column=0,
                              row=i,
                              padx=(PAD / 2),
                              pady=(PAD / 2))
                self.fillLineItem(lineItem=lineItem,
                                  bg=bg,
                                  gFol=gFol,
                                  data=data)
        self.recentScrl.redraw()

    def redrawDisplay(self) -> None:
        for page in self.displayData:
            page.destroy()
        self.displayData.clear()
        pgSplit = self.gamelib.splitByLetter()
        for pg, gFols in pgSplit.items():
            sframe = self.createScrollFrm(self.gameDisplay)
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
                self.fillLineItem(lineItem=lineItem,
                                  bg=bg,
                                  gFol=gFol,
                                  data=data,
                                  page=sframe)
        for pg in self.displayData:
            pg.redraw()

    def showDisplay(self) -> None:
        self.statLbl.grid_remove()
        self.gameDisplay.grid()
        self.update()

    def showLabel(self, msg: str) -> None:
        self.statMsg.set(f"{msg}, Please Wait...")
        self.gameDisplay.grid_remove()
        self.statLbl.grid()
        self.update()

    def fillLineItem(self, lineItem: Canvas, bg: str, gFol: str, data: GAMEDATA_TYPE,
                     page: Opt[SFrame] = None) -> None:

        def canvasButton(color: str, txt: str, cmd: Callable[[Event], None], fnt: str = FONT_SM) -> Canvas:
            cnvBtn = Canvas(toolFrm,
                            width=BTN_SIZE,
                            height=BTN_SIZE,
                            bg=bg)
            cnvBtn.grid(column=0,
                        row=curRow,
                        sticky='ns',
                        pady=2)
            cir = cnvBtn.create_oval(0, 0,
                                     BTN_SIZE - 1,
                                     BTN_SIZE - 1,
                                     fill=color)
            cnvBtn.create_text(BTN_SIZE / 2,
                               BTN_SIZE / 2,
                               text=txt,
                               font=fnt)
            hlcolor = str(darken(color=color,
                                 inputtype='HEX'))
            cnvBtn.bind('<ButtonRelease-1>', cmd)
            def onEnter(_): cnvBtn.itemconfig(cir, fill=hlcolor)
            cnvBtn.bind('<Enter>', onEnter)
            def onLeave(_): cnvBtn.itemconfig(cir, fill=color)
            cnvBtn.bind('<Leave>', onLeave)
            return cnvBtn

        def textbox(title: str, wd: int, txt: str, txtcol: str = 'SystemButtonText') -> list[LFrame, Text]:
            lf = LFrame(lineItem,
                        font=FONT_SM,
                        text=title,
                        background=bg)
            lf.grid(column=curCol,
                    row=0,
                    sticky='ns')
            t = Text(lf,
                     font=FONT_MD,
                     width=wd,
                     height=5,
                     wrap='word',
                     padx=PAD / 2,
                     pady=PAD / 2,
                     background=bg,
                     foreground=txtcol)
            t.grid()
            t.insert('end', txt)
            t.config(state='disabled')
            return [lf, t]

        info = data['Info'].copy()
        cats = data['Categories'].copy()
        tags = data['Tags'].copy()
        gTitle: str = info['Title']
        children: disp_child = list()

        # tools
        toolFrm = LFrame(lineItem,
                         font=FONT_SM,
                         text='Tools',
                         background=bg)
        toolFrm.grid(column=0,
                     row=0,
                     sticky='ns')
        toolFrm.columnconfigure(0, weight=1)
        children.append(toolFrm)

        curCol = curRow = int()

        # play btn
        def playBtn(event: Event): self.startGame(event=event,
                                                  gFolder=gFol,
                                                  gTitle=gTitle,
                                                  gPath=info['Program Path'])
        children.append(canvasButton(color=COLOR_PLAY,
                                     txt='▶',
                                     cmd=playBtn,
                                     fnt=FONT_LG))
        # link btn
        curRow += 1
        def linkBtn(_): os_startfile(info['URL'])
        children.append(canvasButton(color=COLOR_LINK,
                                     txt='www',
                                     cmd=linkBtn))
        # edit btn
        curRow += 1
        def editBtn(event: Event): self.editGame(event=event,
                                                 game=gFol)
        children.append(canvasButton(color=COLOR_EDIT,
                                     txt='Edit',
                                     cmd=editBtn))
        # title
        curCol += 1
        txtcol = 'gold' if cats.pop('Favorite') else 'SystemButtonText'
        children += textbox(title="Title",
                            wd=17,
                            txt=gTitle,
                            txtcol=txtcol)
        # version
        curCol += 1
        txtcol = 'white' if cats.pop('Completed') else 'SystemButtonText'
        children += textbox(title="Version",
                            wd=8,
                            txt=info['Version'],
                            txtcol=txtcol)
        # categories
        curCol += 1
        curCats = ['[Eroge]'] if cats.pop('Eroge') else list()
        curCats += [f'{c}: {v}' for c, v in cats.items()]
        children += textbox(title="Categories",
                            wd=15,
                            txt='\n'.join(curCats))
        # tags
        curCol += 1
        curTags = [t for t, v in tags.items()
                   if v and t not in TAG_SEL]
        curTags += [f'{tags[n]} {n}' for n in TAG_SEL]
        children += textbox(title="Tags",
                            wd=23,
                            txt=', '.join(curTags))
        # description
        curCol += 1
        children += textbox(title="Description",
                            wd=75,
                            txt=info['Description'])
        # save to dict
        if page:
            self.displayData[page][lineItem] = dict(folder=gFol,
                                                    children=children)

    def startGame(self, event: Event, gFolder: str, gTitle: str, gPath: U[str, list, dict]) -> None:
        def run(exe: str) -> None:
            if tw:
                tw.destroy()
            try:
                os_startfile(exe)
                # update recent
                curList = self.gamelib.recentList.copy()
                if gTitle in curList:
                    curList.remove(gTitle)
                curList.insert(0, gTitle)
                while len(curList) > MAX_RECENT_GAMES:
                    curList.pop()
                if curList != self.gamelib.recentList:
                    self.gamelib.recentList = curList
                    self.redrawRecent()
                    self.gamelib.saveRecent()
            except Exception:
                if Mbox.askyesno(title="Error",
                                 message=(f"Couldn't start '{gTitle}'.\n"
                                          f"Would you like to change the executable path? "
                                          f"(Current Path = '{exe}')")):
                    self.editGame(event, gFolder)

        pathInfo = dict()
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
                btn.pack()
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

    def editGame(self, event: Event, game: str) -> None:
        updateGame: str = EditGames(parent=self,
                                    gamelib=self.gamelib,
                                    allGames=[game])
        if updateGame:
            # get vars
            item: Widget = event.widget
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
            self.fillLineItem(lineItem=lineItem,
                              bg=bg,
                              gFol=updateGame,
                              data=data,
                              page=page)
            page.redraw()

    def checkForNew(self) -> None:
        updateGames = self.gamelib.checkForNewGames()
        if updateGames:
            self.showLabel("Reloading")
            self.redrawDisplay()
            if self.curSearch:
                self.clearSearch("Reloading")
            self.showDisplay()

    def updateDisplay(self) -> None:
        index = int()
        for lines in self.displayData.values():
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
        for pg in self.displayData:
            pg.redraw()

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
        sInfo: dict[str, U[IntVar, Combobox]]
        sInfo = (self.catToggles | self.catSelects |
                 self.tagToggles | self.tagSelects)
        search = {k: v.get() for k, v in sInfo.items()
                  if v.get() not in [0, 'Any']}
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
                self.showDisplay()
            else:
                self.clearSearch()
