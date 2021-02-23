from tkinter import Tk, Canvas, Frame, StringVar, Text, LabelFrame as LFrame
from tkinter.filedialog import askopenfilenames as Askfiles
from tkinter.ttk import Label, Entry, Button, Style
from tkinter.simpledialog import Dialog

from os import startfile as os_startfile, listdir as os_listdir, system as os_system
from re import sub as re_sub, findall as re_findall
from bs4 import BeautifulSoup as Html
from urllib3 import PoolManager
from changecolor import invert

from constants import _createSubFrm as SubFrm, _SELECTOR as Sel
from constants import *
from scrolledframe import ScrolledFrame as SFrame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gamelibrary import GameLib
    from tkinter import IntVar
    from tkinter.ttk import Combobox


class _EditGamesDialog(Dialog):
    def __init__(self, parent: U[Tk, LFrame, Canvas], gamelib: "GameLib", allGames: U[dict, list], adding: bool):
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
        invertTextCol = str(invert(color=self.winfo_rgb('SystemButtonText'),
                                   inputtype='RGB',
                                   bitdepth=16))
        Style().configure('Path.TEntry',
                          foreground=invertTextCol)
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
                         font=FONT_MD,
                         text="Folder/Item",
                         padx=PAD)
        pathFrm.grid(column=0,
                     row=0,
                     sticky='ew')
        self.pathLbl = StringVar()
        lbl = Label(pathFrm,
                    font=FONT_LG,
                    textvariable=self.pathLbl)
        lbl.grid(column=0,
                 row=0,
                 sticky='nsew')

    def createInfoFrm(self) -> None:
        def addInfoItems(item: str, sz: U[int, list[int]]) -> Opt[U[Entry, Text]]:
            def description() -> Text:
                txt = Text(master=infoFrm,
                           font=FONT_MD,
                           width=sz[0],
                           height=sz[1],
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
                scrl = SFrame(master=infoFrm,
                              scrollbars='e',
                              padding=0,
                              doupdate=False,
                              scrollspeed=1,
                              relief='sunken',
                              bd=1,
                              height=sz[0])
                scrl.grid(column=1,
                          columnspan=3,
                          row=curRow,
                          sticky='nsew')
                self.createPathLines(*sz[1:],
                                     parent=scrl,
                                     firstRow=curRow)
                scrl.redraw()

            def entries() -> Opt[Entry]:
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
                         font=FONT_MD,
                         text="Info",
                         padx=PAD)
        infoFrm.grid(column=0,
                     row=1,
                     sticky='nsew')
        infoFrm.columnconfigure(3, weight=1)
        # init vars
        self.infoEnts: dict[str, StringVar] = dict()
        self.progPaths: oDict[
            Frame, dict[str, U[bool, Entry, Button]]] = oDict()
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

    @staticmethod
    def clearPathEnt(widget: Entry, defTxt: str) -> None:
        widget.select_clear()
        widget.delete(0, 'end')
        widget.insert(0, defTxt)
        widget.configure(style='Path.TEntry')

    def createPathLines(self, nWd: int, pWd: int, parent: SFrame, firstRow: int) -> None:
        def updateNameEnt(*args) -> bool:
            return updateEnt("Preferred name", *args)

        def updatePathEnt(*args) -> bool:
            return updateEnt("Path to executable", *args)

        def updateEnt(defTxt: str, name: str, why: str, newTxt: str) -> bool:
            widget: Entry = self.nametowidget(name)
            if why == 'key':
                if newTxt:
                    widget.configure(style='TEntry')
            elif why == 'focusin':
                if newTxt == defTxt:
                    widget.select_range(0, 'end')
            elif not newTxt or newTxt == defTxt:
                self.clearPathEnt(widget, defTxt)
            return True

        def addLine() -> None:
            topNameEnt.grid()
            for frame, info in self.progPaths.items():
                if info['show']:
                    continue
                else:
                    frame.grid()
                    self.progPaths[frame]['show'] = True
                    break
            parent.redraw()

        def removeLine(frame: Frame) -> None:
            frame.grid_remove()
            self.progPaths[frame]['show'] = False
            d = self.progPaths[frame]
            self.clearPathEnt(d['name'], "Preferred name")
            self.clearPathEnt(d['path'], "Path to executable")
            active = [i for i in self.progPaths.values() if i['show']]
            if len(active) == 1:
                topNameEnt.grid_remove()
            parent.redraw()

        pathEntVal = parent.register(updatePathEnt)
        nameEntVal = parent.register(updateNameEnt)
        curRow = firstRow
        for i in range(50):
            # create holding frame
            frm = Frame(parent)
            frm.columnconfigure(1, weight=1)
            frm.grid(column=0,
                     row=curRow,
                     columnspan=2,
                     sticky='w')
            # create 'name' entry
            nameEnt = Entry(master=frm,
                            style='Path.TEntry',
                            validate='all',
                            validatecommand=(nameEntVal, '%W', '%V', '%P'),
                            width=nWd)
            nameEnt.grid(column=0,
                         row=0)
            nameEnt.insert(0, "Preferred name")
            # create 'path' entry
            pathEnt = Entry(master=frm,
                            style='Path.TEntry',
                            validate='all',
                            validatecommand=(pathEntVal, '%W', '%V', '%P'),
                            width=pWd)
            pathEnt.grid(column=1,
                         row=0)
            pathEnt.insert(0, "Path to executable")
            if i == 0:
                topNameEnt = nameEnt
                # create 'add' button
                btn = Button(master=frm,
                             text="Add Another Executable",
                             command=addLine)
                nameEnt.grid_remove()
            else:
                # create 'remove' button
                btn = Button(master=frm,
                             text="Remove",
                             command=(lambda f=frm: removeLine(f)))
                frm.grid_remove()
            btn.grid(column=2,
                     row=0)
            # add to dict
            self.progPaths[frm] = {'show': i == 0,
                                   'name': nameEnt,
                                   'path': pathEnt,
                                   'button': btn}
            curRow += 1
        browseBtn = Button(master=parent,
                           text="Browse for Executable...",
                           command=self.browseFolders)
        browseBtn.grid(column=1,
                       row=curRow,
                       sticky='w')

    def getNext(self) -> None:
        if self.allGames:
            self.clearData()
            if isinstance(self.allGames, dict):
                out = self.allGames.popitem()
                self.game = str(out[0])
                self.fillData(out[1])
            else:
                self.game: str = self.allGames.pop()
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
                self.clearPathEnt(info['name'], "Preferred name")
                self.clearPathEnt(info['path'], "Path to executable")
        self.infoDesc.delete(1.0, 'end')
        # clear togs
        for tog in (self.catToggles | self.tagToggles).values():
            tog.set(0)
        # clear lists
        for cbx in (self.catSelects | self.tagSelects).values():
            cbx.set('')

    def fillData(self, data: Opt[GAMEDATA_TYPE] = None) -> None:
        self.pathLbl.set(self.game)
        self.gamePath: str = os_path.join(PATH_GAMES, self.game)
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
            if os_path.splitext(item)[1] in FILETYPES:
                return os_path.relpath(item)
            elif os_path.isfile(item):
                return str()
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
        if open or 'f95zone' not in url:
            if url:
                try:
                    os_startfile(url)
                except Exception:
                    Mbox.showerror("Error", "Invalid URL")
            else:
                Mbox.showerror("Error", "No URL specified")
        if 'f95zone' in url and not self.infoEnts['Version'].get():
            self.getF95Info(url)

    def getF95Info(self, url: str) -> None:
        def req_url():
            raw = pool.request('GET', url).data
            return raw.decode('utf-8', errors='ignore')

        def formatStr(s: str) -> str:
            string = re_sub(r'\s*(\r+|\n+)\s*',
                            r'\n',
                            ''.join(s))
            encoded = string.encode('ascii', 'ignore')
            return encoded.decode().strip()

        def getProtagonist() -> str:
            rawProtag = {t.split(' ')[0] for t in allTags
                         if 'protagonist' in t}
            protagCt = len(rawProtag)
            if protagCt == 0:
                return 'Unknown'
            elif protagCt == 1:
                for protag in TAG_SEL['Protagonist']:
                    if protag.lower() in rawProtag:
                        return protag
                return 'Unknown'
            elif rawProtag in [{'male', 'female'}, {'male', 'female', 'multiple'}]:
                return 'Male/Female'
            elif 'multiple' in rawProtag or protagCt > 1:
                return 'Multiple'
            else:
                return 'Unknown'

        # retrieve data
        pool = PoolManager()
        page = Html(req_url(), 'html.parser')

        # get catagory data
        rawTitle = page.select(Sel.title)
        if rawTitle:
            rawTitle = rawTitle[0].get_text().lower()
            rawCatInfo = re_findall(r'(?<=\[).+?(?=\])',
                                    formatStr(rawTitle))
            if rawCatInfo:
                if 'completed' in rawCatInfo:
                    self.catToggles['Completed'].set(1)
                for c in CAT_SEL['Format']:
                    if c.lower() in rawCatInfo:
                        self.catSelects['Format'].set(c)
        # get tag data
        rawTags = {t.get_text() for t in page.select(Sel.tags)}
        if rawTags:
            subbedTags = {v for k, v in (TAG_EQU | CAT_EQU).items()
                          if k in rawTags}
            allTags = rawTags - {*TAG_EQU, *CAT_EQU} | subbedTags
            if allTags:
                # set toggle tags
                for tag in [t for t in TAG_TOG if t.lower() in allTags]:
                    self.tagToggles[tag].set(1)
                # set toggle categories
                for tag in [t for t in CAT_TOG if t.lower() in allTags]:
                    self.catToggles[tag].set(1)
                # set art category
                for art in [t for t in CAT_SEL['Art'] if t.lower() in allTags]:
                    self.catSelects['Art'].set(art)
                # set protagonist
                if 'character creation' in allTags:
                    protag = 'Created'
                else:
                    protag = getProtagonist()
                self.tagSelects['Protagonist'].set(protag)
        # get description
        rawContent = page.select(Sel.desc)
        if rawContent:
            rawDesc = rawContent[0].find_parent().get_text()
            desc = re_sub(r'(?s)\s*(Overview:?|Spoiler.+?register now\.)\s*',
                          r'',
                          formatStr(rawDesc))
            self.infoDesc.insert(1.0, desc.strip())
        # get version
        rawVer: list[str] = [el.next_sibling for el in page.select(Sel.ver)
                             if 'version' in el.get_text().lower()]
        if rawVer:
            ver = rawVer[0].strip(' :')
            self.infoEnts['Version'].set(ver)
        os_system('nircmd stdbeep')

    def insertMasterlistData(self, data: Opt[GAMEDATA_TYPE] = None) -> None:
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

        inf_ents = {k: v.get() for k, v in self.infoEnts.items()}
        inf_pths = {'Program Path': pPths}
        inf_dscs = {'Description': self.infoDesc.get(1.0, 'end-1c').strip()}
        cat_togs = {k: v.get() for k, v in self.catToggles.items()}
        cat_lsts = {k: v.get() for k, v in self.catSelects.items()}
        tag_togs = {k: v.get() for k, v in self.tagToggles.items()}
        tag_lsts = {k: v.get() for k, v in self.tagSelects.items()}
        # update 'new list' if necessary
        if self.gamelib.newList.pop(self.game, None):
            self.gamelib.saveNew()
        # check if data is new
        gamePath: str = gamePath.split('\\')[0]
        newData = {'Info': (inf_ents | inf_pths | inf_dscs),
                   'Categories': (cat_togs | cat_lsts),
                   'Tags': (tag_togs | tag_lsts)}
        if self.game != gamePath or newData != self.gamelib.masterlist.get(self.game):
            # check if path has changed
            if self.game != gamePath:
                self.gamelib.masterlist.pop(self.game, None)
                self.game = gamePath
            # update master list
            self.gamelib.masterlist[self.game] = newData
            self.gamelib.save()
            self.updateGames = True if self.adding else self.game
        self.getNext()


def EditGames(parent: U[Tk, LFrame, Canvas], gamelib: "GameLib", allGames: U[dict, list], adding: bool = False) -> U[bool, str]:
    res = _EditGamesDialog(parent, gamelib, allGames, adding)
    return res.updateGames
