from tkinter import Tk, Canvas, Frame, StringVar, Text, LabelFrame as LFrame
from tkinter.filedialog import askopenfilenames as Askfiles
from tkinter.ttk import Label, Entry, Button
from tkinter.simpledialog import Dialog

from os import startfile as os_startfile, listdir as os_listdir
from subprocess import run as openatfile
from re import sub as re_sub

from builders import SubFrm, GetF95Info, ProgramPathInput, clearPathInput
from constants import *

if TYPE_CHECKING:
    from tkinter import IntVar
    from tkinter.ttk import Combobox

    from gamelibrary import GameLib


class _EditGamesDialog(Dialog):
    parent: U[Tk, LFrame, Canvas]
    gamelib: "GameLib"
    allGames: U[dict, list]
    adding: bool
    updateGames: bool
    newGameCt: int
    wintitle: str
    cnvs: Canvas
    catToggles: "dict[str, IntVar]"
    catSelects: "dict[str, Combobox]"
    tagToggles: "dict[str, IntVar]"
    tagSelects: "dict[str, Combobox]"
    pathLbl: StringVar
    infoEnts: dict[str, StringVar]
    progPaths: oDict[Frame, dict[str, U[bool, Entry, Button]]]
    titleEnt: Entry
    infoDesc: Text
    game: str
    gamePath: str

    def __init__(self, parent, gamelib, allGames, adding):
        self.parent = parent
        self.gamelib = gamelib
        self.allGames = allGames
        self.adding = adding
        self.updateGames = False
        if adding:
            self.newGameCt = len(allGames)
            if self.newGameCt > 1:
                self.wintitle = f"Add Games ({{}} of {self.newGameCt})"
                title = self.wintitle.format(1)
            else:
                title = "Add Game"
        else:
            title = "Edit Game"
        Dialog.__init__(self,
                        parent=self.parent,
                        title=title)

    def buttonbox(self) -> None:
        btnFrm = LFrame(self,
                        pady=PAD)
        btnFrm.pack(fill='x')
        for n in range(3):
            btnFrm.columnconfigure(n, weight=1)
        curCol = int()
        closeBtn = Button(btnFrm,
                          text="Close",
                          command=self.destroy)
        closeBtn.grid(column=curCol,
                      row=0,
                      sticky='' if self.adding else 'e',
                      padx=25)
        curCol += 1
        if self.adding:
            skipBtn = Button(btnFrm,
                             text="Skip",
                             command=self.getNext)
            skipBtn.grid(column=curCol,
                         row=0,
                         padx=25)
        curCol += 1
        saveBtn = Button(btnFrm,
                         text="Save",
                         command=self.submit)
        saveBtn.grid(column=curCol,
                     row=0,
                     sticky='' if self.adding else 'w',
                     padx=25)

    def body(self, _) -> Entry:
        # initialize window
        self.geometry(self.parent.geometry())
        self.geometry(f'{EDIT_WD}x{EDIT_HT}')
        # create container
        self.cnvs = Canvas(self)
        self.cnvs.pack(expand=True,
                       fill='both')
        self.cnvs.columnconfigure(0, weight=1)
        for n in [1, 2, 3]:
            self.cnvs.rowconfigure(n, weight=1)
        # create GUI
        self.createHeader()
        self.createInfoFrm()
        cfrm, self.catToggles, self.catSelects = SubFrm.cats(parent=self.cnvs,
                                                             setCbx=False)
        cfrm.grid(column=0,
                  row=2,
                  sticky='nsew')
        tfrm, self.tagToggles, self.tagSelects = SubFrm.tags(parent=self.cnvs,
                                                             setCbx=False)
        tfrm.grid(column=0,
                  row=3,
                  sticky='nsew')
        # fill info
        self.getNext()
        return self.titleEnt

    def createHeader(self) -> None:
        pathFrm = LFrame(self.cnvs,
                         text="Folder/Item",
                         padx=PAD)
        pathFrm.grid(column=0,
                     row=0,
                     sticky='ew')
        pathFrm.columnconfigure(0, weight=1)
        # label
        self.pathLbl = StringVar()
        lbl = Label(pathFrm,
                    font=FONT_LG,
                    textvariable=self.pathLbl)
        lbl.grid(column=0,
                 row=0,
                 sticky='w')
        pathBtn = Button(master=pathFrm,
                         text="Open",
                         command=(lambda: openatfile(
                                  ['explorer.exe', '/select,', self.gamePath])))
        pathBtn.grid(column=1,
                     row=0)

    def createInfoFrm(self) -> None:
        def addInfoItems(item: str, sz: U[int, list[int]]) -> O[U[Entry, Text]]:
            def description() -> Text:
                txt = Text(master=infoFrm,
                           width=sz,
                           height=5,
                           wrap='word',
                           padx=(PAD // 2),
                           pady=(PAD // 2))
                txt.grid(column=1,
                         row=curRow,
                         columnspan=2,
                         sticky='w',
                         pady=(0, PAD))
                return txt

            def programFiles() -> None:
                scrl = ProgramPathInput(*sz,
                                        parent=infoFrm,
                                        startRow=curRow,
                                        progPaths=self.progPaths)
                browseBtn = Button(master=scrl,
                                   text="Browse for Executable...",
                                   command=self.browseFolders)
                browseBtn.grid(column=1,
                               row=PROGFILE_INPUT_ROWS,
                               sticky='w')
                scrl.redraw()

            def entries() -> O[Entry]:
                var = StringVar()
                ent = Entry(master=infoFrm,
                            textvariable=var,
                            width=sz)
                ent.grid(column=1,
                         row=curRow,
                         sticky='w')
                self.infoEnts[item] = var
                if item == 'URL':
                    # add url button
                    urlBtn = Button(master=infoFrm,
                                    text="Lookup/Open Webpage",
                                    command=self.lookupOpenURL)
                    urlBtn.grid(column=2,
                                row=curRow)
                elif item == 'Title':
                    return ent

            # add label
            lbl = Label(master=infoFrm,
                        text=item)
            lbl.grid(column=0,
                     row=curRow,
                     pady=(2, 0),
                     sticky='n')
            # add entries
            if item == 'Description':
                wgt = description()
            elif item == 'Program Path':
                wgt = programFiles()
            else:
                wgt = entries()
            return wgt

        # create main frame
        infoFrm = LFrame(master=self.cnvs,
                         text="Info",
                         padx=PAD)
        infoFrm.grid(column=0,
                     row=1,
                     sticky='nsew')
        infoFrm.columnconfigure(3, weight=1)
        # init vars
        self.infoEnts = dict()
        self.progPaths = oDict()
        curRow = int()
        # build info prompts
        for item, size in INFO_ENT.items():
            widget = addInfoItems(item, size)
            if widget:
                if isinstance(widget, Entry):
                    self.titleEnt = widget
                elif isinstance(widget, Text):
                    self.infoDesc = widget
            curRow += 1

    def getNext(self) -> None:
        if self.allGames:
            self.clearData()
            if isinstance(self.allGames, dict):
                out = self.allGames.popitem()
                self.game = out[0]
                self.fillData(out[1])
            else:
                self.game = self.allGames.pop()
                if self.adding and self.newGameCt > 1:
                    ct = (self.newGameCt - len(self.allGames))
                    self.title(self.wintitle.format(ct))
                self.fillData()
        else:
            self.destroy()

    def clearData(self) -> None:
        self.pathLbl.set('')
        # clear info
        for ent in self.infoEnts.values():
            ent.set('')
        for i, info in enumerate(self.progPaths.values()):
            if i:
                info['button'].invoke()
            else:
                clearPathInput(info['name'], "Preferred name")
                clearPathInput(info['path'], "Path to executable")
        self.infoDesc.delete(1.0, 'end')
        # clear togs
        for tog in (self.catToggles | self.tagToggles).values():
            tog.set(0)
        # clear lists
        for cbx in (self.catSelects | self.tagSelects).values():
            cbx.set('')

    def fillData(self, data: O[GAMEDATA_TYPE] = None) -> None:
        self.pathLbl.set(self.game)
        self.gamePath = os_path.join(PATH_GAMES, self.game)
        if data:
            exePaths = self.searchForExe(insert=False)
            data['Info'].update({'Version': '',
                                 'Program Path': exePaths})
            self.insertMasterlistData(data)
        elif self.game in self.gamelib.masterlist:
            self.insertMasterlistData(None)
        else:
            self.initializeInfo()

    def searchForExe(self, insert: bool = True) -> U[str, list]:
        def searchThis(item: str) -> str:
            if os_path.isfile(item):
                return str()
            elif os_path.splitext(item)[-1] in FILETYPES:
                return os_path.relpath(item)
            # else
            for extension in FILETYPES:
                for f in os_listdir(item):
                    if os_path.splitext(f)[-1].lower() == extension:
                        return os_path.relpath(os_path.join(item, f))
            return str()

        exePaths = searchThis(self.gamePath)
        if exePaths:
            if insert:
                self.insertProgPaths(exePaths)
        else:
            fols = os_listdir(self.gamePath)
            folPaths = [os_path.join(self.gamePath, sub) for sub in fols]
            exePaths = [f for f in [searchThis(fol) for fol in folPaths] if f]
            if not exePaths:
                if Mbox.askyesno(title="Missing Executable",
                                 message=(f"Couldn't find executable(s) for '{self.game}.'\n"
                                          f"Would you like to open the search?"),
                                 parent=self):
                    self.browseFolders()
            elif insert:
                self.insertProgPaths(exePaths)
        return exePaths

    def insertProgPaths(self, exePaths: U[str, list[str], dict[str, str]]) -> None:
        # get all blank frames and the last shown frame
        blankFrms: list[Frame] = list()
        for frm, dct in self.progPaths.items():
            if dct['show']:
                lastShown = frm
            else:
                blankFrms.append(frm)
        frm: Frame = lastShown
        if isinstance(exePaths, str):
            self.progPaths[frm]['path'].delete(0, 'end')
            self.progPaths[frm]['path'].insert(0, exePaths)
        else:
            addBtn = self.progPaths[next(iter(self.progPaths))]['button']
            iterFrms = iter(blankFrms)
            if isinstance(exePaths, list):
                for i, path in enumerate(exePaths):
                    if i:
                        addBtn.invoke()
                        frm = next(iterFrms)
                    self.progPaths[frm]['path'].delete(0, 'end')
                    self.progPaths[frm]['path'].insert(0, path)
            else:
                for i, (name, path) in enumerate(exePaths.items()):
                    if i:
                        addBtn.invoke()
                        frm = next(iterFrms)
                    self.progPaths[frm]['name'].delete(0, 'end')
                    self.progPaths[frm]['name'].insert(0, name)
                    self.progPaths[frm]['path'].delete(0, 'end')
                    self.progPaths[frm]['path'].insert(0, path)

    def initializeInfo(self) -> None:
        # set title and url
        data = self.gamelib.newList.get(self.game)
        if data:
            self.infoEnts['Title'].set(data['name'])
            self.infoEnts['URL'].set(data['url'])
            self.searchForExe()
            self.lookupOpenURL(open=True)
        else:
            raw = os_path.splitext(self.game)[0]
            spaced = re_sub(pattern=r'([a-z])([A-Z])(?=\w)',
                            repl=r'\1 \2',
                            string=raw.replace("_", " "))
            capped = re_sub(pattern=r'(?:^|(?<= ))([a-z])(?=\w{3})',
                            repl=lambda m: m.group(1).upper(),
                            string=spaced)
            name = re_sub(pattern=(r'(?i)(\W*('
                                   r'pc|win|eng|english|v|ver|ch|ep|final'
                                   r'|(\d|\.\d)[\d\.]*.{0,2}[\d\.]*|[([{].+?[)}\]])\W*)+$'),
                          repl='',
                          string=capped)
            self.infoEnts['Title'].set(name)
            self.searchForExe()

    def lookupOpenURL(self, open: bool = False) -> None:
        url = self.infoEnts['URL'].get()
        ver = self.infoEnts['Version'].get()
        if open or ver or 'f95zone' not in url:
            if url:
                try:
                    os_startfile(url)
                except Exception:
                    Mbox.showerror("Error", "Invalid URL")
            else:
                Mbox.showerror("Error", "No URL specified")
        if 'f95zone' in url and not ver:
            GetF95Info(self.catToggles, self.catSelects, self.tagToggles,
                       self.tagSelects, self.infoEnts, self.infoDesc, url)

    def insertMasterlistData(self, data: O[GAMEDATA_TYPE] = None) -> None:
        if not data:
            data = self.gamelib.masterlist[self.game]
        cattag = dict[str, U["IntVar", "Combobox"]]
        # insert info
        for lbl, cb in self.infoEnts.items():
            cb.set(data['Info'][lbl])
        progPaths = data['Info']['Program Path']
        self.insertProgPaths(progPaths)
        self.infoDesc.insert(1.0, data['Info']['Description'])
        # insert categories
        cats: cattag = (self.catToggles | self.catSelects)
        for lbl, cb in cats.items():
            cb.set(data['Categories'][lbl])
        # insert tags
        tags: cattag = (self.tagToggles | self.tagSelects)
        for lbl, cb in tags.items():
            cb.set(data['Tags'][lbl])

    def browseFolders(self) -> None:
        rawPaths: list = Askfiles(title="Select the game executable(s)",
                                  initialdir=self.gamePath)
        if rawPaths:
            relpaths = [os_path.relpath(p) for p in rawPaths]
            self.insertProgPaths(relpaths)
        self.deiconify()

    def submit(self) -> None:
        if 'f95zone' in self.infoEnts['URL'].get():
            url = re_sub(r'(?<=threads/).+?\.(?=\d+/$)',
                         '',
                         self.infoEnts['URL'].get())
            self.infoEnts['URL'].set(url)
        gamePath, progPaths = self.getProgPaths()
        inf_ents = {k: v.get() for k, v in self.infoEnts.items()}
        inf_pths = {'Program Path': progPaths}
        inf_dscs = {'Description': self.infoDesc.get(1.0, 'end-1c').strip()}
        cat_togs = {k: v.get() for k, v in self.catToggles.items()}
        cat_lsts = {k: v.get() for k, v in self.catSelects.items()}
        tag_togs = {k: v.get() for k, v in self.tagToggles.items()}
        tag_lsts = {k: v.get() for k, v in self.tagSelects.items()}
        # update 'new list' if necessary
        if self.gamelib.newList.pop(self.game, None):
            self.gamelib.saveNew()
        # check if data is new
        gamePath = gamePath.split('\\')[0]
        newData = {'Info': (inf_ents | inf_pths | inf_dscs),
                   'Categories': (cat_togs | cat_lsts),
                   'Tags': (tag_togs | tag_lsts)}
        oldData = self.gamelib.masterlist.get(self.game)
        if newData != oldData:
            self.updateData(gamePath, oldData, newData)
        self.getNext()

    def getProgPaths(self) -> tuple[str, U[str, list, dict]]:
        pPthDct: dict[str, str] = dict()
        isDct = False
        for d in self.progPaths.values():
            if d['show']:
                pth = d['path'].get().strip()
                if pth != "Path to executable":
                    nm = d['name'].get().strip()
                    if nm != "Preferred name":
                        isDct = True
                    else:
                        nm = pth
                    pPthDct[nm] = pth
        if len(pPthDct) == 1:
            pPths = pPthDct.popitem()[0]
            gamePath = pPths
        elif isDct:
            pPths = pPthDct
            gamePath = pPths[next(iter(pPths))]
        else:
            pPths = list(pPthDct)
            gamePath = pPths[0]
        return (gamePath, pPths)

    def updateData(self, gamePath: str, oldData: O[GAMEDATA_TYPE], newData: GAMEDATA_TYPE) -> None:
        newPath = self.game != gamePath
        oldVer = self.gamelib.masterlist[self.game]['Info']['Version'] if oldData else ''
        newVer = newData['Info']['Version']
        oldTitle = self.gamelib.masterlist[self.game]['Info']['Title'] if oldData else ''
        newTitle = newData['Info']['Title']
        if newPath or not oldData or oldVer != newVer:
            # update recent list
            curList = self.gamelib.recentList['new'].copy()
            if oldData:
                if oldTitle in curList:
                    curList.remove(oldTitle)
            curList.insert(0, newTitle)
            while len(curList) > MAX_RECENT_GAMES:
                curList.pop()
            if curList != self.gamelib.recentList['new']:
                self.gamelib.recentList['new'] = curList
                self.gamelib.saveRecent()
            # check if path has changed
            if newPath:
                self.gamelib.masterlist.pop(self.game, None)
                self.game = gamePath
        elif oldTitle != newTitle:
            i = self.gamelib.recentList['new'].index(oldTitle)
            self.gamelib.recentList['new'][i] = newTitle
            self.gamelib.saveRecent()
        # update master list
        self.gamelib.masterlist[self.game] = newData
        self.gamelib.save()
        self.updateGames = True if self.adding else self.game


def EditGames(parent: U[Tk, LFrame, Canvas], gamelib: "GameLib", allGames: U[dict, list], adding: bool = False) -> U[bool, str]:
    res = _EditGamesDialog(parent, gamelib, allGames, adding)
    return res.updateGames
