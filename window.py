from tkinter import Tk, Toplevel, Frame, Canvas, Label, Text, IntVar, StringVar, LabelFrame as LFrame
from tkinter.ttk import Style, Button, Notebook
from os import startfile as os_startfile
from requests import Session as req_url
from re import split as re_split
from changecolor import lighten, darken
from scrolledframe import ScrolledFrame

from editlist import EditGames, createSubFrm
from constants import *


class GUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.configure(padx=PAD*2)
        self.geometry('{}x{}+{:.0f}+{:.0f}'.format(MAIN_WD,
                                                   MAIN_HT,
                                                   CENTER.x - MAIN_WD / 2,
                                                   CENTER.y - MAIN_HT / 2))
        self.title("Game List")
        s = Style()
        s.configure('.', font=FONT_MD)

        self.defBG = self.cget('bg')
        self.litBG = lighten('RGB',
                             self.winfo_rgb(self.defBG),
                             5,
                             'HEX',
                             16)
        self.statMsg = StringVar(self)
        self.browseAll = False
        self.pages = list()
        self.update_idletasks()

    def start_main(self, gameClass):
        # init vars
        self.gameClass = gameClass
        self.catToggles = {i: IntVar() for i in CAT_TOG}
        self.catLists = dict()
        self.tagToggles = {i: IntVar() for i in TAG_TOG}
        self.tagLists = dict()
        self.gameList = {**self.gameClass.masterList}
        self.prevSearch = dict()
        # add elements
        chkBtn = Button(self,
                        text="Check for new games",
                        command=self.checkForNew)
        chkBtn.place(anchor='sw',
                     relx=0,
                     x=PAD,
                     y=SEARCH_HT)
        self.createSearch()
        self.createBrowse()

    def checkForNew(self):
        updateGames = self.gameClass.checkForNewGames()
        if updateGames:
            self.searchBrowse()

    def createSearch(self):
        # create container
        self.searchFrm = LFrame(self,
                                font=FONT_LG,
                                text="Search",
                                padx=PAD)
        self.searchFrm.place(anchor='n',
                             relx=0.5,
                             rely=0,
                             relwidth=0.6,
                             height=SEARCH_HT)
        for n in [0, 1]:
            self.searchFrm.rowconfigure(n, weight=2)
        self.searchFrm.columnconfigure(0, weight=1)
        # add categories
        createSubFrm(self.searchFrm,
                     "Categories",
                     0,
                     self.catToggles,
                     self.catLists,
                     CAT_LST,
                     MAX_CAT_COL,
                     True)
        # add tags
        createSubFrm(self.searchFrm,
                     "Tags",
                     1,
                     self.tagToggles,
                     self.tagLists,
                     TAG_LST,
                     MAX_TAG_COL,
                     True)
        # add buttons
        btnFrm = Frame(self.searchFrm)
        btnFrm.grid(row=2,
                    column=0,
                    pady=PAD)
        for n in range(3):
            btnFrm.columnconfigure(n, weight=1)
        b1 = Button(btnFrm,
                    text="Clear",
                    command=self.clearSearch)
        b1.grid(row=0,
                column=0,
                padx=50)
        b2 = Button(btnFrm,
                    text="Browse All",
                    command=lambda: self.clearSearch("all"))
        b2.grid(row=0,
                column=1,
                padx=50)
        b3 = Button(btnFrm,
                    text="Go!",
                    command=self.searchBrowse)
        b3.grid(row=0,
                column=2,
                padx=50)

    def createBrowse(self):
        self.browseFrm = Frame(self,
                               padx=PAD,
                               pady=PAD,
                               bd=2,
                               relief='sunken')
        self.browseFrm.columnconfigure(0, weight=1)
        self.browseFrm.rowconfigure(0, weight=1)
        self.browseFrm.place(anchor='s',
                             relx=0.5,
                             rely=1,
                             y=-PAD,
                             relwidth=1,
                             relheight=1,
                             height=-SEARCH_HT-PAD*2)

        self.recentFrm = LFrame(self.browseFrm,
                                text="Recently Played",
                                font=FONT_LG + " bold",
                                labelanchor='n')
        self.recentScrl = self.createScrollFrm(self.recentFrm)
        self.recentScrl.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.recentFrm.grid(row=0, column=0, sticky='nsew')
        self.recentFrm.grid_remove()

        self.allTabs = Notebook(self.browseFrm)
        self.allTabs.grid(row=0, column=0, sticky='nsew')
        self.allTabs.grid_remove()

        self.searchTabs = Notebook(self.browseFrm)
        self.searchTabs.grid(row=0, column=0, sticky='nsew')
        self.searchTabs.grid_remove()

        self.statMsg.set("Loading, Please Wait...")
        self.statLbl = Label(self.browseFrm,
                             textvariable=self.statMsg,
                             font=FONT_LG)
        self.statLbl.grid(row=0, column=0, sticky='nsew')

        self.update()
        self.redrawRecent()
        self.drawList(self.allTabs)
        self.statLbl.grid_remove()
        self.recentFrm.grid()

    def createScrollFrm(self, parent):
        return ScrolledFrame(parent,
                             scrollbars='e',
                             padding=PAD,
                             dohide=False,
                             doupdate=False,
                             scrollspeed=1,
                             relief='sunken',
                             bd=1)

    def redrawRecent(self):
        for w in self.recentScrl.winfo_children():
            w.destroy()
        for gFol, data in self.gameClass.masterList.items():
            if data['Info']['Title'] in self.gameClass.recentList:
                i = self.gameClass.recentList.index(data['Info']['Title'])
                BG = self.litBG if (i % 2) else self.defBG
                lineItem = Canvas(self.recentScrl,
                                  background=BG)
                lineItem.grid(row=i,
                              column=0,
                              padx=PAD / 2,
                              pady=PAD / 2)
                self.fillLineItem(lineItem,
                                  BG,
                                  gFol,
                                  data)
        self.update_idletasks()
        self.recentScrl.redraw()

    def redrawBrowse(self, show):
        if show == "all":
            self.statLbl.grid_remove()
            self.allTabs.grid()
        else:
            self.drawList(self.searchTabs)
            self.statLbl.grid_remove()
            if show == "recent":
                self.recentFrm.grid()
            else:
                self.searchTabs.grid()

    def drawList(self, parent):
        pages = list()
        l = -(-len(self.gameList) // GAMES_PER_PAGE)
        for n in range(l):
            f = self.createScrollFrm(parent)
            pages.append(f)
            parent.add(f.container, text="Page {}".format(n+1))
        ct = 0
        for n, (gFol, data) in enumerate(self.gameList.items()):
            i = n - (ct * GAMES_PER_PAGE)
            if i == GAMES_PER_PAGE:
                ct += 1
                i = n - (ct * GAMES_PER_PAGE)
            pg = pages[ct]
            BG = self.litBG if (i % 2) else self.defBG
            lineItem = Canvas(pg,
                              background=BG)
            lineItem.grid(row=i,
                          column=0,
                          padx=PAD / 2,
                          pady=PAD / 2)
            self.fillLineItem(lineItem,
                              BG,
                              gFol,
                              data)
        self.update_idletasks()
        for pg in pages:
            pg.redraw()

    def fillLineItem(self, lineItem, BG, gFol, data):

        def canvasButton(color, txt, row, cmd, fnt=FONT_SM):
            cnvBtn = Canvas(toolFrm,
                            width=BTN_SIZE,
                            height=BTN_SIZE,
                            bg=BG)
            cnvBtn.grid(row=row,
                        column=0,
                        sticky='ns',
                        pady=2)
            cir = cnvBtn.create_oval(0, 0,
                                     BTN_SIZE-1,
                                     BTN_SIZE-1,
                                     fill=color)
            cnvBtn.create_text(BTN_SIZE/2,
                               BTN_SIZE/2,
                               text=txt,
                               font=fnt)
            hlcolor = darken('HEX', color)
            cnvBtn.bind('<ButtonRelease-1>', cmd)
            def onEnter(e): cnvBtn.itemconfig(cir, fill=hlcolor)
            cnvBtn.bind('<Enter>', onEnter)
            def onLeave(e): cnvBtn.itemconfig(cir, fill=color)
            cnvBtn.bind('<Leave>', onLeave)

        def textbox(title, wt, txt, txtcol='SystemButtonText'):
            lf = LFrame(lineItem,
                        font=FONT_SM,
                        text=title,
                        background=BG)
            lf.grid(row=0,
                    column=curCol,
                    sticky='ns')
            t = Text(lf,
                     font=FONT_MD,
                     height=5,
                     width=wt,
                     wrap='word',
                     padx=PAD / 2,
                     pady=PAD / 2,
                     background=BG,
                     foreground=txtcol)
            t.grid()
            t.insert('end', txt)
            t.config(state='disabled')

        info = {**data['Info']}
        cats = {**data['Categories']}
        tags = {**data['Tags']}
        gTitle = info['Title']
        curCol = 0
        # tools
        toolFrm = LFrame(lineItem,
                         font=FONT_SM,
                         text='Tools',
                         background=BG)
        toolFrm.grid(row=0,
                     column=curCol,
                     sticky='ns')
        toolFrm.columnconfigure(0, weight=1)

        # play btn
        def playBtn(event): self.startGame(event,
                                           gFolder=gFol,
                                           gTitle=gTitle,
                                           gPath=info['Program Path'])
        canvasButton(color='#87ffb9',
                     txt='▶',
                     row=0,
                     cmd=playBtn,
                     fnt=FONT_LG)
        # link btn
        def linkBtn(e): self.checkForUpdate(info['URL'])
        canvasButton(color='#9cd4ff',
                     txt='www',
                     row=1,
                     cmd=linkBtn)
        # edit btn
        def editBtn(e): self.editGame(e, gFol)
        canvasButton(color='#e3b668',
                     txt='Edit',
                     row=2,
                     cmd=editBtn)
        # title
        curCol += 1
        txtcol = 'gold' if cats.pop('Favorite') else 'SystemButtonText'
        textbox(title="Title",
                wt=17,
                txt=gTitle,
                txtcol=txtcol)
        # version
        curCol += 1
        txtcol = 'white' if cats.pop('Completed') else 'SystemButtonText'
        textbox(title="Version",
                wt=8,
                txt=info['Version'],
                txtcol=txtcol)
        # categories
        curCol += 1
        curCats = ['[Eroge]'] if cats.pop('Eroge') else []
        curCats += ['{}: {}'.format(c, v) for c, v in cats.items()]
        textbox(title="Categories",
                wt=15,
                txt='\n'.join(curCats))
        # tags
        curCol += 1
        curTags = [t for t, v in tags.items() if v and t not in TAG_LST]
        curTags += ['{} {}'.format(tags['{}'.format(n)], n) for n in TAG_LST]
        textbox(title="Tags",
                wt=23,
                txt=', '.join(curTags))
        # description
        curCol += 1
        textbox(title="Description",
                wt=75,
                txt=info['Description'])

    def checkForUpdate(self, curUrl):
        if 'f95zone' in curUrl:
            if curUrl == req_url().head(curUrl, allow_redirects=True).url:
                if not Mbox.askyesno("No update", "There has been no update according to the url. Open anyway?"):
                    return
        os_startfile(curUrl)

    def startGame(self, event, gFolder, gTitle, gPath):
        def run(exe, sub=None):
            if sub:
                sub.destroy()
            try:
                os_startfile(exe)
                orig = self.gameClass.recentList.copy()
                if gTitle in self.gameClass.recentList:
                    self.gameClass.recentList.remove(gTitle)
                self.gameClass.recentList.insert(0, gTitle)
                while len(self.gameClass.recentList) > 10:
                    self.gameClass.recentList.pop()
                if self.gameClass.recentList != orig:
                    self.redrawRecent()
                    self.gameClass.saveRecent()
            except Exception:
                if Mbox.askyesno("Error", "Couldn't start '{}'.\nWould you like to change the executable path?\n{}".format(gTitle, gPath)):
                    self.editGame(event, gFolder)
        if ';' in gPath:
            tw = Toplevel(self, padx=PAD, pady=PAD)
            tw.overrideredirect(1)
            tw.geometry('+{}+{}'.format(event.x_root, event.y_root))
            tw.focus_set()
            tw.bind('<FocusOut>', lambda e: tw.destroy())
            for exePath in re_split(r'; ?', gPath):
                exe = os_path.join(PATH_GAMES, exePath)
                name = os_path.splitext(os_path.basename(exePath))[0]
                btn = Button(tw,
                             text=name,
                             command=lambda x=exe: run(x, tw))
                btn.pack()
        else:
            exe = os_path.join(PATH_GAMES, gPath)
            run(exe)

    def editGame(self, event, game):
        updateGame = EditGames(self,
                               self.gameClass,
                               [game])
        if updateGame:
            lineItem = event.widget
            for _ in range(2):
                lineItem = self.nametowidget(lineItem.winfo_parent())
            BG = lineItem.cget('background')
            for child in lineItem.winfo_children():
                child.destroy()
            data = self.gameClass.masterList[game]
            self.gameList.update({game: data})
            self.fillLineItem(lineItem,
                              BG,
                              updateGame,
                              data)
            self.scrollFrm.redraw()

    def clearBrowse(self):
        self.allTabs.grid_remove()
        self.searchTabs.grid_remove()
        self.recentFrm.grid_remove()
        self.statLbl.grid()
        self.update()
        for w in self.searchTabs.winfo_children():
            self.searchTabs.forget(w)

    def searchBrowse(self):
        sInfo = {**self.catToggles, **self.catLists,
                 **self.tagToggles, **self.tagLists}
        search = {k: v.get() for k, v in sInfo.items()
                  if v.get() not in [0, 'Any']}
        if search != self.prevSearch:
            self.browseAll = False
            self.statMsg.set("Searching, Please Wait...")
            self.clearBrowse()
            self.prevSearch = {**search}
            self.gameList = dict()
            for game, allData in self.gameClass.masterList.items():
                data = {**allData['Categories'], **allData['Tags']}
                if search.items() <= data.items():
                    self.gameList.update({game: allData})
            self.redrawBrowse("browse")

    def clearSearch(self, show="recent"):
        self.statMsg.set("Clearing, Please Wait...")
        self.clearBrowse()
        for _, v in {**self.catToggles, **self.tagToggles}.items():
            v.set(0)
        for _, v in {**self.catLists, **self.tagLists}.items():
            v.current(0)
        redraw = False
        if show == "all" and not self.browseAll:
            self.statMsg.set("Loading, Please Wait...")
            self.update_idletasks()
            self.browseAll = True
            redraw = True
        elif show == "recent" and self.browseAll:
            self.browseAll = False
            redraw = True
        if self.prevSearch or redraw:
            self.prevSearch = dict()
            self.gameList = {**self.gameClass.masterList}
            self.redrawBrowse(show)
