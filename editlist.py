from tkinter import Tk, Toplevel, Canvas, IntVar, StringVar, Text, LabelFrame as LFrame, messagebox as mbox
from tkinter.filedialog import askopenfilenames
from tkinter.ttk import Label, Button, Entry, Checkbutton, Combobox, Style, Frame
from tkinter.simpledialog import Dialog
from time import sleep
from re import sub as re_sub, search as re_search, findall as re_findall
from requests import Session as req_url
from lxml import html
from constants import *


class _EditGamesDialog(Dialog):
    def __init__(self, parent, gameClass, allGames, showSkip):
        self.parent = parent
        self.gameClass = gameClass
        self.allGames = allGames
        self.showSkip = showSkip
        self.updateGames = False
        Dialog.__init__(self,
                        self.parent,
                        "Edit Games")

    def buttonbox(self):
        btnFrm = LFrame(self,
                        pady=PAD)
        btnFrm.pack(fill='x')
        for n in range(3):
            btnFrm.columnconfigure(n, weight=1)
        curCol = 0
        st = ['', ''] if self.showSkip else ['e', 'w']
        closeBtn = Button(btnFrm,
                          text="Close",
                          command=self.destroy)
        closeBtn.grid(row=0,
                      column=curCol,
                      sticky=st[0],
                      padx=25)
        curCol += 1
        if self.showSkip:
            skipBtn = Button(btnFrm,
                             text="Skip",
                             command=self.getNext)
            skipBtn.grid(row=0,
                         column=curCol,
                         padx=25)
        curCol += 1
        self.saveBtn = Button(btnFrm,
                              text="Save",
                              command=self.submit)
        self.saveBtn.grid(row=0,
                          column=curCol,
                          sticky=st[1],
                          padx=25)

    def body(self, master):
        # initialize window
        self.geometry(self.parent.geometry())
        self.geometry('{:.0f}x{:.0f}'.format(WIDTH * 0.7, HEIGHT * 0.7))
        # create container
        self.cnvs = Canvas(self)
        self.cnvs.pack(expand=True,
                       fill='both')
        for n in list('123'):
            self.cnvs.rowconfigure(n, weight=1)
        self.cnvs.columnconfigure(0, weight=1)
        # create GUI
        self.createHeader()
        self.createInfoFrm()
        self.createCatFrm()
        self.createTagFrm()
        # fill info
        self.getNext()
        return self.infoEnts['Title']

    def getNext(self):
        if self.allGames:
            self.clearData()
            self.doF95Lookup = False
            self.game = self.allGames.pop()
            self.gamePath = os_path.join(PATH_GAMES,
                                         self.game)
            self.fillData()
        else:
            self.destroy()

    def clearData(self):
        self.pathLbl.set('')
        # clear info
        for _, ent in self.infoEnts.items():
            ent.delete(0, 'end')
        self.infoDesc.delete(1.0, 'end')
        # clear togs
        for _, tog in {**self.catToggles, **self.tagToggles}.items():
            tog.set(0)
        # clear lists
        for _, cbx in {**self.catLists, **self.tagLists}.items():
            cbx.set('')

    def fillData(self):
        self.pathLbl.set(self.game)
        self.fillInfoData()
        if self.doF95Lookup:
            self.getF95Info()
        if self.game in self.gameClass.masterList:
            self.insertInfo()

    def createHeader(self):
        pathFrm = LFrame(self.cnvs,
                         font=FONT_MD,
                         text="Folder Name",
                         padx=PAD)
        pathFrm.grid(row=0,
                     column=0,
                     sticky='ew')
        self.pathLbl = StringVar()
        lbl = Label(pathFrm,
                    font=FONT_LG,
                    textvariable=self.pathLbl)
        lbl.grid(row=0,
                 column=0,
                 sticky='nsew')

    def createInfoFrm(self):

        def browseFolders():
            rawPaths = askopenfilenames(title="Select the game executable(s)",
                                        initialdir=os_path.join(PATH_GAMES, self.game))
            if rawPaths:
                relpaths = [os_path.relpath(p) for p in rawPaths]
                paths = '; '.join(relpaths)
                if self.infoEnts['Program Path'].get():
                    paths = '; ' + paths
                self.infoEnts['Program Path'].insert('end', paths)
            self.deiconify()

        infoFrm = LFrame(self.cnvs,
                         font=FONT_MD,
                         text="Info",
                         padx=PAD)
        infoFrm.grid(row=1,
                     column=0,
                     sticky='nsew')
        infoFrm.columnconfigure(2, weight=1)
        for r, i in enumerate(INFO_ENT):
            Label(infoFrm, text=i).grid(row=r, column=0)
        f95btn = Button(infoFrm,
                        text='f95zone lookup',
                        command=self.getF95Info)
        f95btn.grid(row=INFO_ENT.index('URL'),
                    column=2)
        urlBtn = Button(infoFrm,
                        text='Open URL',
                        command=lambda: os_startfile(self.infoEnts['URL'].get()))
        urlBtn.grid(row=INFO_ENT.index('URL'),
                    column=3)
        browseBtn = Button(infoFrm,
                           text="Browse",
                           command=browseFolders)
        browseBtn.grid(row=len(INFO_ENT),
                       column=1,
                       sticky='e')
        # add entries
        self.infoEnts = {i: Entry(infoFrm, width=85) for i in INFO_ENT}
        for r, (i, e) in enumerate(self.infoEnts.items()):
            e.grid(row=r, column=1)
        # add textbox for description
        l1 = Label(infoFrm,
                   text="Description")
        l1.grid(row=len(INFO_ENT)+1,
                column=0,
                sticky='w')
        self.infoDesc = Text(infoFrm,
                             font=FONT_MD,
                             height=5,
                             width=75,
                             wrap='word',
                             padx=3,
                             pady=3)
        self.infoDesc.grid(row=len(INFO_ENT)+1,
                           column=1,
                           columnspan=2,
                           sticky='w')

    def createCatFrm(self):
        self.catToggles = {i: IntVar() for i in CAT_TOG}
        self.catLists = dict()
        createSubFrm(self.cnvs,
                     "Categories",
                     2,
                     self.catToggles,
                     self.catLists,
                     CAT_LST,
                     MAX_CAT_COL)

    def createTagFrm(self):
        self.tagToggles = {i: IntVar() for i in TAG_TOG}
        self.tagLists = dict()
        createSubFrm(self.cnvs,
                     "Tags",
                     3,
                     self.tagToggles,
                     self.tagLists,
                     TAG_LST,
                     MAX_TAG_COL)

    def fillInfoData(self):

        def defaultData(g):
            n = re_sub(r'([a-z])([A-Z])',
                       r'\1 \2',
                       g.replace("_", " "))
            return {'name': n, 'url': ''}

        def searchForExe(searchThis):
            if os_path.splitext(searchThis)[1] in FILETYPES:
                return os_path.relpath(searchThis)
            elif os_path.isfile(searchThis):
                return ''
            else:
                ex = ''
                fs = os_listdir(searchThis)
                for ext in FILETYPES:
                    for f in fs:
                        if os_path.splitext(f)[1].lower() == ext:
                            ex = os_path.relpath(os_path.join(searchThis, f))
                            break
                    if ex:
                        break
                return ex

        if self.game not in self.gameClass.masterList:
            # set title and url from either 'New Games' or default
            data = NEW_DATA.get(self.game, defaultData(self.game))
            if 'f95zone' in data['url']:
                self.doF95Lookup = True
            self.infoEnts['Title'].insert(0, data['name'])
            self.infoEnts['URL'].insert(0, data['url'])
            # try to find exe
            exePath = searchForExe(self.gamePath)
            if exePath:
                self.infoEnts['Program Path'].insert(0, exePath)
            else:
                fs = os_listdir(self.gamePath)
                folPaths = {os_path.realpath(sub) for sub in fs}
                exePaths = {searchForExe(fol) for fol in folPaths} - {''}
                if exePaths:
                    exePaths = '; '.join(exePaths)
                    self.infoEnts['Program Path'].insert(0, exePaths)
                else:
                    mbox.showinfo("Missing Executable",
                                  "Couldn't find executable(s) for '%s'. Please add them manually, separated by a semicolon" % self.game,
                                  parent=self)

    def formatData(self, data):
        string = ''.join(data)
        encoded = string.encode('ascii', 'ignore')
        return encoded.decode().strip()

    def getF95Info(self):
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
        rawCatInfo = re_findall(r'(?<=\[).+?(?=\])',
                                rawHeader)
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
            protag = 'Unknown'
            rawProtag = set()
            for t in allTags:
                if 'protagonist' in t:
                    rawProtag |= {t.split(' ')[0]}
            protagCt = len(rawProtag)
            if protagCt <= 1:
                for p in TAG_LST['Protagonist']:
                    if p.lower() in rawProtag:
                        protag = p
                        break
            elif rawProtag in [{'male', 'female'}, {'male', 'female', 'multiple'}]:
                protag = 'Male/Female'
            elif 'multiple' in rawProtag or protagCt > 1:
                protag = 'Multiple'
            self.tagLists['Protagonist'].set(protag)
        # get description
        rawDesc = self.formatData(page.xpath(xpath_desc)[0].text_content())
        desc = re_sub(r'\s*(\r+|\n+)\s*',
                      r'\n',
                      rawDesc)
        frmtDesc = re_sub(r'(?s)Overview:|Spoiler:.+$',
                          r'',
                          desc).strip()
        self.infoDesc.insert(1.0, frmtDesc)
        # get version
        v = page.xpath(xpath_ver)
        v = v[0].strip(' :') if v else ''
        self.infoEnts['Version'].insert('end', v)
        os_system('nircmd stdbeep')

    def insertInfo(self):
        data = self.gameClass.masterList[self.game]
        # insert info
        for lbl, cb in self.infoEnts.items():
            cb.insert(0, data['Info'][lbl])
        self.infoDesc.insert(1.0, data['Info']['Description'])
        # insert categories
        for lbl, cb in {**self.catToggles, **self.catLists}.items():
            cb.set(data['Categories'][lbl])
        # insert tags
        for lbl, cb in {**self.tagToggles, **self.tagLists}.items():
            cb.set(data['Tags'][lbl])

    def submit(self):
        inf_ents = {k: v.get().strip() for k, v in self.infoEnts.items()}
        inf_dscs = {'Description': self.infoDesc.get(1.0, 'end-1c').strip()}
        cat_togs = {k: v.get() for k, v in self.catToggles.items()}
        cat_lsts = {k: v.get().strip() for k, v in self.catLists.items()}
        tag_togs = {k: v.get() for k, v in self.tagToggles.items()}
        tag_lsts = {k: v.get().strip() for k, v in self.tagLists.items()}
        self.gameClass.masterList.update(
            {self.game: {
                'Info': {**inf_ents, **inf_dscs},
                'Categories': {**cat_togs, **cat_lsts},
                'Tags': {**tag_togs, **tag_lsts}
            }})
        self.gameClass.save()
        self.updateGames = True
        self.getNext()


def createSubFrm(parent, title, row, togDict, listDict, LST, MAX_COL, setCbx=False):
    frm = LFrame(parent,
                 font=FONT_MD,
                 text=title,
                 padx=PAD)
    frm.grid(row=row,
             column=0,
             sticky='nsew')
    for n in range(MAX_COL):
        frm.columnconfigure(n, minsize=GRIDMIN)
    curRow = curCol = 0
    # add checkbuttons
    for c, v in togDict.items():
        chk = Checkbutton(frm,
                          text=c,
                          variable=v)
        chk.grid(row=curRow,
                 column=curCol,
                 padx=PAD/2,
                 sticky='w')
        if curCol == MAX_COL:
            curRow += 1
            curCol = 0
        else:
            curCol += 1
    # add comboboxes
    for c, v in LST.items():
        lf = LFrame(frm,
                    font=FONT_SM,
                    text=c)
        lf.grid(row=curRow,
                column=curCol,
                padx=PAD/2)
        cbx = Combobox(lf,
                       values=(['Any', *v] if setCbx else v),
                       width=13)
        cbx.grid(sticky='w')
        if setCbx:
            cbx.current(0)
        listDict.update({c: cbx})
        if curCol == MAX_COL:
            curRow += 1
            curCol = 0
        else:
            curCol += 1


def EditGames(parent, gameClass, allGames, showSkip=False):
    args = [parent, gameClass, allGames, showSkip]
    return _EditGamesDialog(*args).updateGames
