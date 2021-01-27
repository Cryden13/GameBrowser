from changecolor import lighten, darken
from scrolledframe import ScrolledFrame
from re import split as re_split
from editlist import *


class GUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.configure(padx=PAD*2)
        self.scrWd = self.winfo_screenwidth()
        self.scrHt = self.winfo_screenheight()
        self.geometry('{}x{}+{:.0f}+{:.0f}'.format(WIDTH,
                                                   HEIGHT,
                                                   (self.scrWd-WIDTH)/2,
                                                   (self.scrHt-HEIGHT)/2))
        self.title("Game List")

        s = Style()
        s.configure('.', font=FONT_MD)
        s.configure('TEntry', width=50)
        self.defBG = self.cget('bg')
        self.litBG = lighten('RGB',
                             self.winfo_rgb(self.defBG),
                             5,
                             'HEX',
                             16)
        self.update_idletasks()

    def start_main(self, gameClass):
        # init vars
        self.gameClass = gameClass
        self.catToggles = {i: IntVar() for i in CAT_TOG}
        self.catLists = dict()
        self.tagToggles = {i: IntVar() for i in TAG_TOG}
        self.tagLists = dict()
        # add elements
        btn = Button(self,
                     text="Check for new games",
                     command=self.checkForNew)
        btn.place(anchor='sw',
                  relx=0,
                  x=PAD,
                  y=SEARCH_HT)
        self.createSearch()
        self.createBrowse()

    def checkForNew(self):
        if self.gameClass.checkForNewGames():
            self.searchBrowse()

    def createSearch(self):
        self.prevSearch = set()
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
        for n in range(2):
            btnFrm.columnconfigure(n, weight=1)
        b1 = Button(btnFrm,
                    text="Clear",
                    command=self.clearSearch)
        b1.grid(row=0,
                column=0,
                padx=50)
        b2 = Button(btnFrm,
                    text="Go!",
                    command=self.searchBrowse)
        b2.grid(row=0,
                column=1,
                padx=50)

    def createBrowse(self):
        self.browseFrm = ScrolledFrame(self,
                                       scrollbars='e',
                                       padding=PAD,
                                       dohide=False,
                                       doupdate=False,
                                       scrollspeed=1,
                                       relief='sunken')
        self.browseFrm.place(anchor='s',
                             relx=0.5,
                             rely=1,
                             y=-PAD,
                             relwidth=1,
                             relheight=1,
                             height=-SEARCH_HT-PAD*2)
        self.gameList = {**self.gameClass.masterList}
        self.redrawList()

    def redrawList(self):
        for w in self.browseFrm.winfo_children():
            w.destroy()
        for i, (gFol, data) in enumerate(self.gameList.items()):
            BG = self.litBG if (i % 2) else self.defBG
            lineItem = Canvas(self.browseFrm,
                              background=BG)
            lineItem.grid(row=i,
                          column=0,
                          padx=PAD / 2,
                          pady=PAD / 2)
            self.fillLineItem(lineItem,
                              BG,
                              gFol,
                              data)
        # update scrolledframe
        self.update_idletasks()
        self.browseFrm.redraw()

    def fillLineItem(self, lineItem, BG, gFol, data):

        def canvasButton(color, txt, row, cmd, fnt=FONT_SM):
            cnvBtn = Canvas(toolFrm,
                            width=BTNSIZE,
                            height=BTNSIZE,
                            bg=BG)
            cnvBtn.grid(row=row,
                        column=0,
                        sticky='ns',
                        pady=2)
            cir = cnvBtn.create_oval(0, 0,
                                     BTNSIZE-1,
                                     BTNSIZE-1,
                                     fill=color)
            cnvBtn.create_text(BTNSIZE/2,
                               BTNSIZE/2,
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
                if not mbox.askyesno("No update", "There has been no update according to the url. Open anyway?"):
                    return
        os_startfile(curUrl)

    def startGame(self, event, gFolder, gTitle, gPath):
        def startSub(exe):
            tw.destroy()
            os_startfile(exe)
        try:
            if ';' not in gPath:
                exe = os_path.join(PATH_GAMES, gPath)
                os_startfile(exe)
            else:
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
                                 command=lambda x=exe: startSub(x))
                    btn.pack()
        except Exception:
            if mbox.askyesno("Error", "Couldn't start '{}'.\nWould you like to change the executable path?\n{}".format(gTitle, gPath)):
                self.editGame(event, gFolder)

    def editGame(self, event, game):
        updateGame = EditGames(self,
                               self.gameClass,
                               [game],
                               True)
        if updateGame:
            lineItem = event.widget
            BG = lineItem.cget('background')
            for _ in range(2):
                lineItem = self.nametowidget(lineItem.winfo_parent())
            for child in lineItem.winfo_children():
                child.destroy()
            data = self.gameClass.masterList[updateGame]
            self.gameList.update({updateGame: data})
            self.fillLineItem(lineItem,
                              BG,
                              updateGame,
                              data)
            # self.update_idletasks()
            self.browseFrm.redraw()

    def searchBrowse(self):
        sInfo = {**self.catToggles, **self.catLists,
                 **self.tagToggles, **self.tagLists}
        search = {k for k, v in sInfo.items() if v.get() and v.get() != 'Any'}
        if search == self.prevSearch:
            return
        elif self.prevSearch and search.issubset(self.prevSearch):
            searchDict = {**self.gameList}
        else:
            searchDict = {**self.gameClass.masterList}
        self.gameList = dict()
        for game, allData in searchDict.items():
            data = {**allData['Categories'], **allData['Tags']}
            dataVals = {k for k, v in data.items() if v}
            if search.issubset(dataVals):
                self.gameList.update({game: allData})
        self.prevSearch = search
        self.redrawList()

    def clearSearch(self):
        for _, v in {**self.catToggles, **self.tagToggles}.items():
            v.set(0)
        for _, v in {**self.catLists, **self.tagLists}.items():
            v.current(0)
        if len(self.gameList) != len(self.gameClass.masterList):
            self.gameList = {**self.gameClass.masterList}
            self.redrawList()
