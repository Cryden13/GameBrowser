from tkinter import Tk, Toplevel, Canvas, IntVar, Text, LabelFrame as LFrame, messagebox as mbox
from tkinter.filedialog import askopenfilenames
from tkinter.ttk import Label, Button, Entry, Checkbutton, Combobox, Style, Frame
from time import sleep
from re import sub as re_sub, search as re_search, findall as re_findall
from requests import Session as req_url
from lxml import html
from constants import *


class EditGames(Toplevel):
    def __init__(self, root, gameClass, games, showSkip=False):
        # initialize window
        Toplevel.__init__(self, root, padx=PAD*2, pady=PAD)
        self.root, self.gameClass, self.showSkip = root, gameClass, showSkip
        self.title("Edit Games")
        self.transient(root)
        self.protocol("WM_DELETE_WINDOW", lambda: self.closeWindow(True))
        self.geometry(root.geometry())
        self.geometry('{:.0f}x{:.0f}'.format(WIDTH*0.7, HEIGHT*0.7))
        self.grab_set()

        # iterate through games
        self.curProcess = IntVar()
        for g in games:
            self.doF95Lookup = False
            self.curProcess.set(1)
            self.game = g
            self.gameDir = os_path.join(PATH_GAMES, self.game)
            self.createGUI()
            if self.doF95Lookup:
                self.getInfoF95()
            if self.game in self.gameClass.masterList:
                self.insertInfo()
            self.wait_variable(self.curProcess)
            if self.curProcess.get() == 0:
                break
        self.closeWindow(True)

    def closeWindow(self, close=False):
        if close:
            self.curProcess.set(0)
            self.root.focus_force()
            self.destroy()
        else:
            self.cnvs.destroy()
            self.curProcess.set(2)

    def createGUI(self):
        self.cnvs = Canvas(self)
        self.cnvs.place(relx=0, rely=0, relwidth=1, relheight=1)
        [self.cnvs.rowconfigure(n, weight=1) for n in [1, 2, 3]]
        self.cnvs.columnconfigure(0, weight=1)
        # create header
        pathFrm = LFrame(self.cnvs, font=FONT_MD, text="Folder Name", padx=PAD)
        pathFrm.grid(row=0, column=0, sticky='ew')
        self.pathLbl = Label(pathFrm, font=FONT_LG, text=self.game)
        self.pathLbl.grid(row=0, column=0, sticky='nsew')
        # create body
        self.createInfoFrm()
        self.createCatFrm()
        self.createTagFrm()
        # create footer
        btnFrm = LFrame(self.cnvs, pady=PAD)
        btnFrm.grid(row=4, column=0, columnspan=2, sticky='nsew', pady=PAD)
        [btnFrm.columnconfigure(n, weight=1) for n in [0, 1, 2]]
        curCol = 0
        st = ['', ''] if self.showSkip else ['e', 'w']
        b1 = Button(btnFrm, text="Close",
                    command=lambda: self.closeWindow(True))
        b1.grid(row=0, column=curCol, sticky=st[0], padx=25)
        curCol += 1
        if self.showSkip:
            b2 = Button(btnFrm, text="Skip", command=self.closeWindow)
            b2.grid(row=0, column=curCol, padx=25)
        b3 = Button(btnFrm, text="Save", command=self.submit)
        b3.grid(row=0, column=curCol+1, sticky=st[1], padx=25)

    def createInfoFrm(self):

        def defaultData(g):
            n = re_sub(r'([a-z])([A-Z])', r'\1 \2', g.replace("_", " "))
            return {'name': n, 'url': ''}

        def searchForExe(searchMe):
            if os_path.splitext(searchMe)[1] in FILETYPES:
                return os_path.relpath(searchMe)
            elif os_path.isfile(searchMe):
                return ''
            else:
                p = [os_path.relpath(os_path.join(searchMe, f)) for e in FILETYPES for f in os_listdir(
                    searchMe) if os_path.splitext(f)[1].lower() == e]
                return p[0] if p else ''

        def browseFolders():
            rawPaths = askopenfilenames(title="Select the game executable(s)",
                                        initialdir=os_path.join(PATH_GAMES, self.game))
            if rawPaths:
                add = '; ' if self.infoEnts['Program Path'].get() else ''
                paths = add + '; '.join([os_path.relpath(p) for p in rawPaths])
                self.infoEnts['Program Path'].insert('end', paths)
            self.deiconify()

        infoFrm = LFrame(self.cnvs, font=FONT_MD, text="Info", padx=PAD)
        infoFrm.grid(row=1, column=0, sticky='nsew')
        infoFrm.columnconfigure(2, weight=1)
        for r, i in enumerate(INFO_ENT):
            Label(infoFrm, text=i).grid(row=r, column=0)
        b1 = Button(infoFrm, text='f95zone lookup', command=self.getInfoF95)
        b1.grid(row=INFO_ENT.index('URL'), column=2)
        b2 = Button(infoFrm, text='Open URL',
                    command=lambda: os_startfile(self.infoEnts['URL'].get()))
        b2.grid(row=INFO_ENT.index('URL'), column=3)
        # add entries
        self.infoEnts = {i: Entry(infoFrm, width=85) for i in INFO_ENT}
        for r, (i, e) in enumerate(self.infoEnts.items()):
            e.grid(row=r, column=1)
        if self.game not in self.gameClass.masterList:
            # set title and url from either 'New Games' or default
            data = NEW_DATA.get(self.game, defaultData(self.game))
            if 'f95zone' in data['url']:
                self.doF95Lookup = True
            self.infoEnts['Title'].insert(0, data['name'])
            self.infoEnts['URL'].insert(0, data['url'])
            # try to find exe
            exePath = searchForExe(self.gameDir)
            if exePath:
                self.infoEnts['Program Path'].insert(0, exePath)
            else:
                folPaths = {os_path.join(self.gameDir, sub)
                            for sub in os_listdir(self.gameDir)}
                exePaths = {searchForExe(fol) for fol in folPaths} - {''}
                if exePaths:
                    exePaths = '; '.join(exePaths)
                    self.infoEnts['Program Path'].insert(0, exePaths)
                else:
                    mbox.showinfo("Missing Executable",
                                  "Couldn't find executable for '%s'. Please add them manually, separated by a semicolon" % self.game,
                                  parent=self)
            self.deiconify()
        b1 = Button(infoFrm, text="Browse", command=browseFolders)
        b1.grid(row=len(INFO_ENT), column=1, sticky='e')
        # add textbox for description
        l1 = Label(infoFrm, text="Description")
        l1.grid(row=len(INFO_ENT)+1, column=0, sticky='w')
        self.infoDesc = Text(infoFrm, font=FONT_MD, height=5,
                             width=75, wrap='word', padx=3, pady=3)
        self.infoDesc.grid(row=len(INFO_ENT)+1, column=1,
                           columnspan=2, sticky='w')

    def createCatFrm(self):
        catFrm = LFrame(self.cnvs, font=FONT_MD, text="Categories", padx=PAD)
        catFrm.grid(row=2, column=0, sticky='nsew')
        curRow, curCol = 0, 0
        self.catToggles = {i: IntVar() for i in CAT_TOG}
        self.catLists = {}
        # add checkbuttons
        for c, v in self.catToggles.items():
            chk = Checkbutton(catFrm, text=c, variable=v)
            chk.grid(row=curRow, column=curCol, padx=PAD/2)
            if curCol == MAX_CAT_COL:
                curRow, curCol = [curRow + 1, 0]
            else:
                curCol += 1
        # add comboboxes
        for c, v in CAT_LST.items():
            lf = LFrame(catFrm, font=FONT_SM, text=c)
            lf.grid(row=curRow, column=curCol, padx=PAD/2)
            cb = Combobox(lf, values=v, width=13)
            cb.grid(sticky='w')
            # cb.current(0)
            self.catLists.update({c: cb})
            if curCol == MAX_CAT_COL:
                curRow, curCol = [curRow + 1, 0]
            else:
                curCol += 1
        [catFrm.columnconfigure(n, minsize=GRIDMIN) for n in range(6)]

    def createTagFrm(self):
        tagFrm = LFrame(self.cnvs, font=FONT_MD, text="Tags", padx=PAD)
        tagFrm.grid(row=3, column=0, sticky='nsew')
        curRow, curCol = 0, 0
        self.tagToggles = {i: IntVar() for i in TAG_TOG}
        self.tagLists = {}
        # add checkbuttons
        for c, v in self.tagToggles.items():
            chk = Checkbutton(tagFrm, text=c, variable=v)
            chk.grid(row=curRow, column=curCol, sticky='w', padx=PAD/2)
            if curCol == MAX_TAG_COL:
                curRow, curCol = [curRow + 1, 0]
            else:
                curCol += 1
        # add comboboxes
        for c, v in TAG_LST.items():
            lf = LFrame(tagFrm, font=FONT_SM, text=c)
            lf.grid(row=curRow, column=curCol, padx=PAD/2)
            cb = Combobox(lf, values=v, width=13)
            cb.grid(sticky='w')
            # cb.current(0)
            self.tagLists.update({c: cb})
            if curCol == MAX_TAG_COL:
                curRow, curCol = [curRow + 1, 0]
            else:
                curCol += 1
        [tagFrm.columnconfigure(n, minsize=GRIDMIN) for n in range(6)]

    def formatData(self, data):
        string = ''.join(data)
        encoded = string.encode('ascii', 'ignore')
        return encoded.decode().strip()

    def getInfoF95(self):
        # set url and check it
        url = self.infoEnts['URL'].get()
        if not url:
            mbox.showerror("Error", "No URL specified")
            return
        elif 'f95zone' not in url:
            mbox.showerror("Error", "Only f95zone urls supported")
            return

        # set data paths
        xpath_title = '//div[@uix_component="MainContent"]//h1[@class="p-title-value"]//child::text()'
        xpath_tags = '//li[@class="groupedTags"]/a//child::text()'
        xpath_desc = '//article[@class="message-body js-selectToQuote"]/div[@class="bbWrapper"]/div[count(b)>0]'
        xpath_ver = '//article[@class="message-body js-selectToQuote"]//b[contains(translate(text(), "VERSION", "version"), "version")]/following-sibling::text()[1]'
        # retrieve data
        page = html.fromstring(req_url().get(url).content)

        # get catagory info
        rawHeader = self.formatData(page.xpath(xpath_title)).lower()
        rawCatInfo = re_findall(r'(?<=\[).+?(?=\])', rawHeader)
        if rawHeader and rawCatInfo:
            if 'completed' in rawCatInfo:
                self.catToggles['Completed'].set(1)
            [self.catLists['Format'].set(
                c) for c in CAT_LST['Format'] if c.lower() in rawCatInfo]

        # get tag info
        rawTags = set(page.xpath(xpath_tags))
        rep = {v for k, v in {**TAG_EQU, **CAT_EQU}.items() if k in rawTags}
        allTags = rawTags - set(TAG_EQU) - set(CAT_EQU) | rep
        if allTags:
            # set toggle tags
            tagTogs = [t for t in TAG_TOG if t.lower() in allTags]
            [self.tagToggles[t].set(1) for t in tagTogs]
            # set toggle categories
            catTogs = [t for t in CAT_TOG if t.lower() in allTags]
            [self.catToggles[t].set(1) for t in catTogs]
            # set art category
            art = [t for t in CAT_LST['Art'] if t.lower() in allTags]
            [self.catLists['Art'].set(c) for c in art]
            # get protagonist info
            rawProtag = {
                t.split(' ')[0] for t in allTags if 'protagonist' in t}
            protagCt = len(rawProtag)
            if protagCt <= 1:
                pUp = [p for p in TAG_LST['Protagonist']
                       if p.lower() in rawProtag]
                protag = pUp[0] if pUp else 'Unknown'
            elif rawProtag in [{'male', 'female'}, {'male', 'female', 'multiple'}]:
                protag = 'Male/Female'
            else:
                protag = 'Multiple' if 'multiple' in rawProtag or protagCt > 1 else 'Unknown'
            self.tagLists['Protagonist'].set(protag)
        # get description
        rawDesc = self.formatData(page.xpath(xpath_desc)[0].text_content())
        desc = re_sub(r'\s*(\r+|\n+)\s*', r'\n', rawDesc)
        frmtDesc = re_sub(r'(?s)Overview:|Spoiler:.+$', r'', desc).strip()
        self.infoDesc.insert(1.0, frmtDesc)
        # get version
        v = page.xpath(xpath_ver)
        v = v[0].strip(' :') if v else ''
        self.infoEnts['Version'].insert('end', v)
        os_system('nircmd stdbeep')

    def insertInfo(self):
        data = self.gameClass.masterList[self.game]
        # insert info
        [cb.insert(0, data['Info'][lbl]) for lbl, cb in self.infoEnts.items()]
        self.infoDesc.insert(1.0, data['Info']['Description'])
        # insert categories
        for lbl, cb in {**self.catToggles, **self.catLists}.items():
            cb.set(data['Categories'][lbl])
        # insert tags
        for lbl, cb in {**self.tagToggles, **self.tagLists}.items():
            cb.set(data['Tags'][lbl])

    def submit(self):
        infoEnts = {k: v.get().strip() for k, v in self.infoEnts.items()}
        infoDesc = {'Description': self.infoDesc.get(1.0, 'end-1c').strip()}
        catTogs = {k: v.get() for k, v in self.catToggles.items()}
        catLists = {k: v.get().strip() for k, v in self.catLists.items()}
        tagTogs = {k: v.get() for k, v in self.tagToggles.items()}
        tagLists = {k: v.get().strip() for k, v in self.tagLists.items()}
        self.gameClass.masterList.update(
            {self.game: {
                'Info': {**infoEnts, **infoDesc},
                'Categories': {**catTogs, **catLists},
                'Tags': {**tagTogs, **tagLists}
            }})
        self.gameClass.save()
        self.root.changed = self.game
        self.closeWindow()
