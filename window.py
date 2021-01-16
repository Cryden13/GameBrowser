from changecolor import lighten, darken
from scrolledframe import ScrolledFrame
from re import split as re_split
from editlist import *


class GUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.configure(padx=PAD*2)
        self.scrWd, self.scrHt = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry('{}x{}+{:.0f}+{:.0f}'.format(
            WIDTH, HEIGHT, (self.scrWd-WIDTH)/2, (self.scrHt-HEIGHT)/2))
        self.title('Game List')

        s = Style()
        s.configure('.', font=FONT_MD)
        s.configure('TEntry', width=50)
        self.defBG = self.cget('bg')
        self.litBG = lighten('RGB', self.winfo_rgb(self.defBG), 5, 'HEX', 16)
        self.update_idletasks()

    def start_main(self, gameClass):
        self.gameClass = gameClass
        self.createSearch()
        self.createBrowse()

    def createSearch(self):
        self.searchFrm = LFrame(self, font=FONT_LG, text="Search", padx=PAD)
        self.searchFrm.place(anchor='n', relx=0.5, rely=0,
                             relwidth=0.6, relheight=0.3)
        [self.searchFrm.rowconfigure(n, weight=2) for n in [0, 1]]
        self.searchFrm.columnconfigure(0, weight=1)
        self.createCatFrm()
        self.createTagFrm()
        btnFrm = Frame(self.searchFrm)
        btnFrm.grid(row=2, column=0, pady=PAD)
        [btnFrm.columnconfigure(n, weight=1) for n in range(2)]
        b1 = Button(btnFrm, text="Clear", command=self.clearSearch)
        b1.grid(row=0, column=0, padx=50)
        b2 = Button(btnFrm, text="Go!", command=self.searchBrowse)
        b2.grid(row=0, column=1, padx=50)

    def createCatFrm(self):
        catFrm = LFrame(self.searchFrm, font=FONT_MD,
                        text="Categories", padx=PAD)
        catFrm.grid(row=0, column=0, sticky='ew')
        curRow, curCol = 0, 0
        self.catToggles = {i: IntVar() for i in CAT_TOG}
        self.catLists = {}
        for c, v in self.catToggles.items():
            chk = Checkbutton(catFrm, text=c, variable=v)
            chk.grid(row=curRow, column=curCol, sticky='w', padx=PAD / 2)
            if curCol == 5:
                curRow, curCol = [curRow + 1, 0]
            else:
                curCol += 1
        for c, v in CAT_LST.items():
            v = ['Any', *v]
            lf = LFrame(catFrm, font=FONT_SM, text=c)
            lf.grid(row=curRow, column=curCol, padx=PAD/2)
            cb = Combobox(lf, values=v, width=13)
            cb.grid(sticky='w')
            cb.current(0)
            self.catLists.update({c: cb})
            if curCol == 5:
                curRow, curCol = [curRow + 1, 0]
            else:
                curCol += 1
        [catFrm.columnconfigure(n, minsize=GRIDMIN) for n in range(6)]

    def createTagFrm(self):
        tagFrm = LFrame(self.searchFrm, font=FONT_MD, text="Tags", padx=PAD)
        tagFrm.grid(row=1, column=0, sticky='ew')
        curRow, curCol = 0, 0
        self.tagToggles = {i: IntVar() for i in TAG_TOG}
        self.tagLists = {}
        for c, v in self.tagToggles.items():
            chk = Checkbutton(tagFrm, text=c, variable=v)
            chk.grid(row=curRow, column=curCol, sticky='w', padx=PAD/2)
            if curCol == 5:
                curRow, curCol = [curRow + 1, 0]
            else:
                curCol += 1
        for c, v in TAG_LST.items():
            v = ['Any', *v]
            lf = LFrame(tagFrm, font=FONT_SM, text=c)
            lf.grid(row=curRow, column=curCol, padx=PAD/2)
            cb = Combobox(lf, values=v, width=13)
            cb.grid(sticky='w')
            cb.current(0)
            self.tagLists.update({c: cb})
            if curCol == 5:
                curRow, curCol = [curRow + 1, 0]
            else:
                curCol += 1
        [tagFrm.columnconfigure(n, minsize=GRIDMIN) for n in range(6)]

    def createBrowse(self):

        def scanGames():
            self.changed = False
            self.gameClass.checkGames()
            if self.changed:
                self.searchBrowse()

        btn = Button(self, text="Check for new games", command=scanGames)
        btn.place(anchor='sw', relx=0, x=PAD, rely=0.3)

        self.browseFrm = ScrolledFrame(self, scrollbars='e', padding=PAD, dohide=False,
                                       doupdate=False, scrollspeed=1, relief='sunken')
        self.browseFrm.place(anchor='n', relx=0.5, rely=0.3, y=PAD,
                             relwidth=1, relheight=0.7, height=-PAD*2)

        self.gameList = {**self.gameClass.masterList}
        self.redrawList()

    def redrawList(self):
        [w.destroy() for w in self.browseFrm.winfo_children()]
        for i, (gFol, data) in enumerate(self.gameList.items()):
            BG = self.litBG if (i % 2) else self.defBG
            lineItem = Canvas(self.browseFrm, background=BG)
            lineItem.grid(row=i, column=0, padx=PAD / 2, pady=PAD / 2)
            self.fillLineItem(lineItem, BG, gFol, data)
        # update scrolledframe
        self.update_idletasks()
        self.browseFrm.redraw()

    def fillLineItem(self, lineItem, BG, gFol, data):

        def canvasButton(color, txt, row, cmd, fnt=FONT_SM):
            cnvBtn = Canvas(toolFrm, width=BTNSIZE, height=BTNSIZE, bg=BG)
            cnvBtn.grid(row=row, column=0, sticky='ns', pady=2)
            cir = cnvBtn.create_oval(0, 0, BTNSIZE-1, BTNSIZE-1, fill=color)
            cnvBtn.create_text(BTNSIZE/2, BTNSIZE/2, text=txt, font=fnt)
            hlcolor = darken('HEX', color)
            cnvBtn.bind('<ButtonRelease-1>', cmd)
            def onEnter(e): cnvBtn.itemconfig(cir, fill=hlcolor)
            cnvBtn.bind('<Enter>', onEnter)
            def onLeave(e): cnvBtn.itemconfig(cir, fill=color)
            cnvBtn.bind('<Leave>', onLeave)

        def textbox(title, wt, txt, txtcol='SystemButtonText'):
            lf = LFrame(lineItem, font=FONT_SM, text=title, background=BG)
            lf.grid(row=0, column=curCol, sticky='ns')
            t = Text(lf, font=FONT_MD, height=5, width=wt, wrap='word',
                     padx=PAD/2, pady=PAD/2, background=BG, foreground=txtcol)
            t.grid()
            t.insert('end', txt)
            t.config(state='disabled')

        info = data['Info']
        cats = {**data['Categories']}
        tags = data['Tags']
        gTitle = info['Title']
        curCol = 0
        # tools
        toolFrm = LFrame(lineItem, font=FONT_SM, text='Tools', background=BG)
        toolFrm.grid(row=0, column=curCol, sticky='ns')
        toolFrm.columnconfigure(0, weight=1)
        # play btn
        def playBtn(e): self.startGame(e, gFol, gTitle, info['Program Path'])
        canvasButton('#87ffb9', '▶', 0, playBtn, fnt=FONT_LG)
        # link btn
        def linkBtn(e): self.checkForUpdate(info['URL'])
        canvasButton('#9cd4ff', 'www', 1, linkBtn)
        # edit btn
        def editBtn(e): self.editGame(e, gFol)
        canvasButton('#e3b668', 'Edit', 2, editBtn)
        # title
        curCol += 1
        txt = gTitle + ' [Eroge]' if cats.pop('Eroge') else gTitle
        txtcol = 'gold' if cats.pop('Favorite') else 'SystemButtonText'
        textbox("Title", 17, txt, txtcol)
        # version
        curCol += 1
        txtcol = 'white' if cats.pop('Completed') else 'SystemButtonText'
        textbox("Version", 8, info['Version'], txtcol)
        # categories
        curCol += 1
        curCats = ['{}: {}'.format(c, v) for c, v in cats.items()]
        textbox("Categories", 15, '\n'.join(curCats))
        # tags
        curCol += 1
        curTags = [t for t, v in tags.items() if v and t not in TAG_LST]
        curTags += ['{} {}'.format(tags['{}'.format(n)], n) for n in TAG_LST]
        textbox("Tags", 23, ', '.join(curTags))
        # description
        curCol += 1
        textbox("Description", 75, info['Description'])

    def checkForUpdate(self, curUrl):
        if 'f95zone' in curUrl and curUrl == req_url().head(curUrl, allow_redirects=True).url:
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
                    Button(tw, text=name, command=lambda x=exe: startSub(x)).pack()
        except Exception:
            if mbox.askyesno("Error", "Couldn't start '{}'.\nWould you like to change the executable path?\n{}".format(gTitle, gPath)):
                self.editGame(event, gFolder)

    def editGame(self, event, game):
        self.changed = False
        editWin = EditGames(self, self.gameClass, [game])
        try:
            self.wait_window(editWin)
        except Exception:
            pass
        if self.changed:
            lineItem = event.widget
            BG = lineItem.cget('background')
            for _ in range(2):
                lineItem = self.nametowidget(lineItem.winfo_parent())
            for child in lineItem.winfo_children():
                child.destroy()
            data = self.gameClass.masterList[self.changed]
            self.gameList.update({self.changed: data})
            self.fillLineItem(lineItem, BG, self.changed, data)
            # self.update_idletasks()
            self.browseFrm.redraw()

    def searchBrowse(self):
        self.gameClass.alphabetize()
        sCats = {k: 0 for k in CAT_LST}
        sCats.update({
            k: v.get() for k, v in {**self.catToggles, **self.catLists}.items() if v.get() != 'Any'})
        sTags = {k: 0 for k in TAG_LST}
        sTags.update({
            k: v.get() for k, v in {**self.tagToggles, **self.tagLists}.items() if v.get() != 'Any'})
        listRemove = []
        for cat, val in sCats.items():
            if val:
                for game, data in self.gameClass.masterList.items():
                    if data['Categories'][cat] != val:
                        listRemove.append(game)
        for tag, val in sTags.items():
            if val:
                for game, data in self.gameClass.masterList.items():
                    if data['Tags'][tag] != val:
                        listRemove.append(game)
        self.gameList = {
            game: data for game, data in self.gameClass.masterList.items() if game not in listRemove}
        self.redrawList()

    def clearSearch(self):
        [v.set(0) for k, v in {**self.catToggles, **self.tagToggles}.items()]
        [v.current(0) for k, v in {**self.catLists, **self.tagLists}.items()]
        self.gameList = {**self.gameClass.masterList}
        self.redrawList()
