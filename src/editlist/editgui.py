from tkinter.simpledialog import Dialog
from datetime import datetime
from subprocess import run
from os import startfile
from shutil import move

from tkinter.filedialog import (
    askopenfilenames as Askfiles,
    askopenfilename as Askfile
)
from tkinter import (
    LabelFrame as LFrame,
    StringVar,
    IntVar,
    Canvas,
    Frame,
    Text,
    Tk
)
from tkinter.ttk import (
    Combobox,
    Button,
    Entry
)
from re import (
    split as re_split,
    sub as re_sub
)

try:
    from .pathclear import clearPathInput
    from .buildbody import BuildBody
    from .getinfo import GetF95Info
    from ..constants import *
except ImportError:
    from pathlib import Path
    pth = Path(__file__).parents[2]
    run(['py', '-m', pth.name, 'console'], cwd=pth.parent)
    raise SystemExit

if TYPE_CHECKING:
    from ..gamelibrary import GameLib


class EditGUI(Dialog):
    parent: U[Tk, LFrame, Canvas]
    gamelib: "GameLib"
    allGames: U[dict[Path, Path], list[Path]]
    adding: bool
    updateGames: U[bool, Path]
    newGameCt: int
    wintitle: str
    addPpthLine: C
    catToggles: dict[str, IntVar]
    catSelects: dict[str, Combobox]
    tagToggles: dict[str, IntVar]
    tagSelects: dict[str, Combobox]
    pathLbl: StringVar
    infoEnts: dict[str, StringVar]
    progPaths: dict[Frame, dict[str, U[bool, Entry, Button]]]
    titleEnt: Entry
    infoDesc: Text
    game: Path
    oldgame: Path
    old_ver: str

    def __init__(self, parent: U[Tk, LFrame, Canvas], gamelib: "GameLib", allGames: U[dict, list], adding: bool):
        self.parent = parent
        self.gamelib = gamelib
        self.allGames = allGames
        self.adding = adding
        self.updateGames = False
        self.infoEnts = dict()
        self.progPaths = dict()
        self.old_ver = None
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

    @classmethod
    def EditGames(cls, parent: U[Tk, LFrame, Canvas], gamelib: "GameLib", allGames: U[dict, list], adding: bool = False) -> U[bool, Path]:
        res = cls(parent, gamelib, allGames, adding)
        return res.updateGames

#     ___  __  ________   ___
#    / _ )/ / / /  _/ /  / _ \
#   / _  / /_/ // // /__/ // /
#  /____/\____/___/____/____/

    def body(self, master: Frame) -> Entry:
        # initialize window
        self.geometry(f'{EDIT_WD}x{EDIT_HT}')
        master.pack(expand=True,
                    fill='both')
        master.columnconfigure(0, weight=1)
        for n in [1, 2, 3]:
            master.rowconfigure(n, weight=1)
        # create GUI
        BuildBody(gui=self,
                  parent=master)
        # fill info
        self.getNext()
        return self.titleEnt

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
                         command=self.trySubmit)
        saveBtn.grid(column=curCol,
                     row=0,
                     sticky='' if self.adding else 'w',
                     padx=25)

#    _______________  _  _______  ________
#   / ___/ __/_  __/ / |/ / __/ |/_/_  __/
#  / (_ / _/  / /   /    / _/_>  <  / /
#  \___/___/ /_/   /_/|_/___/_/|_| /_/

    def getNext(self) -> None:
        if self.allGames:
            self.clearData()
            if isinstance(self.allGames, dict):
                self.game, self.oldgame = self.allGames.popitem()
                data = self.gamelib.masterlist.get(self.oldgame)
                self.fillData(data)
            else:
                self.game = self.oldgame = self.allGames.pop()
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
        self.update()

    def fillData(self, data: GAMEDATA_TYPE = None) -> None:
        self.pathLbl.set(self.game.name)
        if data:
            exePaths = self.searchForExe(insert=False)
            data['Info'].update({'Version': '',
                                 'Program Path': exePaths})
            data['Categories'].update({'Status': 'Updated'})
            self.insertMasterlistData(data)
        elif self.game in self.gamelib.masterlist:
            self.insertMasterlistData(None)
        else:
            self.initializeInfo()

#     ___  _____________  _________   ______
#    / _ \/ __/_  __/ _ \/  _/ __/ | / / __/
#   / , _/ _/  / / / , _// // _/ | |/ / _/
#  /_/|_/___/ /_/ /_/|_/___/___/ |___/___/

    def initializeInfo(self) -> None:
        # set title and url
        data = self.gamelib.newlist.get(self.game)
        if data:
            self.infoEnts['Title'].set(data['name'])
            self.infoEnts['URL'].set(data['url'])
            self.infoEnts['Image'].set(data['image'])
            self.searchForExe()
            self.lookupURL()
        else:
            raw = self.game.stem
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

    def lookupURL(self) -> None:
        url = self.infoEnts['URL'].get()
        if not url:
            Mbox.showerror("Error", "No URL specified")
            return
        elif 'f95zone' in url:
            GetF95Info(self.catToggles, self.catSelects, self.tagToggles,
                       self.tagSelects, self.infoEnts, self.infoDesc, url)
        elif Mbox.askyesno(title="Retrieval Failed",
                           message="Only F95zone links supported. Open url instead?"):
            self.openURL()

    def openURL(self) -> None:
        url = self.infoEnts['URL'].get()
        if not url:
            Mbox.showerror("Error", "No URL specified")
            return
        try:
            startfile(url)
        except Exception:
            Mbox.showerror("Error", "Invalid URL")

    def insertMasterlistData(self, data: GAMEDATA_TYPE = None) -> None:
        if not data:
            data = self.gamelib.masterlist[self.game]
        cattag = dict[str, U["IntVar", "Combobox"]]
        # insert info
        for lbl, cb in self.infoEnts.items():
            cb.set(data['Info'][lbl])
        self.old_ver = re_split(pattern=r' (?=\([\d/]{8}\)$)',
                                string=data['Info']['Version'])
        self.infoEnts['Version'].set(self.old_ver[0])
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
            try:
                cb.set(data['Tags'][lbl])
            except KeyError:
                cb.set(0)

#     ___  ___  ____  _________________
#    / _ \/ _ \/ __ \/ ___/ __/ __/ __/
#   / ___/ , _/ /_/ / /__/ _/_\ \_\ \
#  /_/  /_/|_|\____/\___/___/___/___/

    def insertProgPaths(self, exePaths: U[Path, list[Path], dict[str, Path]]) -> None:
        # get all blank frames and the last shown frame
        blankFrms: list[Frame] = list()
        for frm, dct in self.progPaths.items():
            if dct['show']:
                lastShown = frm
            else:
                blankFrms.append(frm)
        frm: Frame = lastShown
        if isinstance(exePaths, Path):
            self.progPaths[frm]['path'].delete(0, 'end')
            self.progPaths[frm]['path'].insert(0,
                                               exePaths.relative_to(PATH_GAMES))
        else:
            iterFrms = iter(blankFrms)
            if isinstance(exePaths, list):
                for i, p in enumerate(exePaths):
                    path = p.relative_to(PATH_GAMES)
                    if i:
                        self.addPpthLine()
                        frm = next(iterFrms)
                    self.progPaths[frm]['path'].delete(0, 'end')
                    self.progPaths[frm]['path'].insert(0, path)
            else:
                for i, (name, p) in enumerate(exePaths.items()):
                    path = p.relative_to(PATH_GAMES)
                    if i:
                        self.addPpthLine()
                        frm = next(iterFrms)
                    if self.progPaths[frm]['name'].get() == 'Preferred name':
                        self.progPaths[frm]['name'].delete(0, 'end')
                        self.progPaths[frm]['name'].insert(0, name)
                    self.progPaths[frm]['path'].delete(0, 'end')
                    self.progPaths[frm]['path'].insert(0, path)

    def searchForExe(self, insert: bool = True) -> U[Path, list[Path]]:
        def searchHere(item: Path) -> O[Path]:
            if item.is_dir():
                for ext in FILETYPES:
                    for f in item.glob(f'*{ext}'):
                        if f.stem[-2:] != '32':
                            return f
            elif item.suffix in FILETYPES:
                return item
            else:
                return

        exePaths = searchHere(self.game)
        if exePaths:
            if insert:
                self.insertProgPaths(exePaths)
        else:
            exePaths = {Path(p).stem: Path(p)
                        for p in filter(None,
                                        [searchHere(fol) for fol
                                         in self.game.iterdir()])}
            if not exePaths:
                find = Mbox.askyesno(title="Missing Executable",
                                     message=(f"Couldn't find executable(s) for '{self.game.name}.'\n"
                                              f"Would you like to open the search?"),
                                     parent=self)
                if find:
                    self.browseFolders()
            elif insert:
                self.insertProgPaths(exePaths)
        return exePaths

    def browseFolders(self) -> None:
        rawPaths: list[str] = Askfiles(title=f"Select the executable(s) for '{self.game.stem}'",
                                       filetypes=FILETYPENAMES,
                                       **(dict(initialdir=self.game) if self.game.is_dir() else
                                          dict(initialdir=self.game.parent, initialfile=self.game.name)))
        if rawPaths:
            relpaths = {Path(p).stem: Path(p)
                        for p in rawPaths}
            self.insertProgPaths(relpaths)
        self.deiconify()

    def browseImgs(self, var: StringVar) -> None:
        pth: str = Askfile(title=f"Select the image for '{self.game.stem}'",
                           filetypes=[('Image file (*.png; *.jpg; *.jpeg; *.gif)',
                                       '*.png; *.jpg; *.jpeg; *.gif')],
                           initialdir=PATH_IMGS)
        if pth:
            var.set(str(Path(pth).relative_to(PATH_IMGS)))
        self.deiconify()

#     ______  _____  __  _____________
#    / __/ / / / _ )/  |/  /  _/_  __/
#   _\ \/ /_/ / _  / /|_/ // /  / /
#  /___/\____/____/_/  /_/___/ /_/

    def trySubmit(self) -> None:
        try:
            self.submit()
        except:
            from traceback import format_exc
            Mbox.showerror('editgui Error', format_exc())

    def submit(self) -> None:
        if 'f95zone' in self.infoEnts['URL'].get():
            url = re_sub(pattern=r'(?<=threads/).+?\.(?=\d+/$)',
                         repl='',
                         string=self.infoEnts['URL'].get())
            self.infoEnts['URL'].set(url)
        if self.getImage():
            return
        gamePath, progPaths = self.getProgPaths()
        inf_ents = {k: v.get().strip() for k, v in self.infoEnts.items()}
        inf_pths = {'Program Path': progPaths}
        inf_dscs = {'Description': self.infoDesc.get(1.0, 'end-1c').strip()}
        cat_togs = {k: v.get() for k, v in self.catToggles.items()}
        if not cat_togs['Completed'] and not cat_togs['Abandoned']:
            new_ver = re_split(pattern=r' (?=\([\d/]{8}\)$)',
                               string=inf_ents['Version'])
            if len(new_ver) == 2:
                pass
            elif isinstance(self.old_ver, str) and new_ver[0] == self.old_ver[0] and len(self.old_ver) == 2:
                inf_ents['Version'] = f"{new_ver[0]} {self.old_ver[1]}"
            else:
                inf_ents['Version'] += f" ({datetime.now().strftime('%m/%d/%y')})"
        cat_lsts = {k: v.get() for k, v in self.catSelects.items()}
        tag_togs = {k: v.get() for k, v in self.tagToggles.items()}
        tag_lsts = {k: v.get() for k, v in self.tagSelects.items()}
        # update 'new list' if necessary
        if self.gamelib.newlist.pop(self.game, None):
            self.gamelib.saveNew()
        # check if data is new
        newData = {'Info': (inf_ents | inf_pths | inf_dscs),
                   'Categories': (cat_togs | cat_lsts),
                   'Tags': (tag_togs | tag_lsts)}
        oldData = self.gamelib.masterlist.get(self.oldgame)
        if newData != oldData:
            self.updateData(gamePath, oldData, newData)
        self.getNext()

    def getImage(self) -> bool:
        def findImg(pth: Path) -> O[Path]:
            image = pth.joinpath(imgstr)
            if not image.suffix:
                for i in pth.iterdir():
                    if i.stem == image.stem:
                        return i
            else:
                return image if image.exists() else None

        imgstr = self.infoEnts['Image'].get()
        if not imgstr:
            return
        img = findImg(PATH_IMGS)
        if not img:
            img = findImg(Path.home().joinpath('desktop'))
            if img:
                img = Path(move(img, PATH_IMGS.joinpath(img.name)))
            else:
                Mbox.showerror('editlist Error',
                               f'The image "{img}" could not be found')
                return True
        self.infoEnts['Image'].set(img.name)
        if img.suffix != ".jpg" and (img.stat().st_size > (1000**2) or img.suffix == '.gif'):
            new = img.with_suffix(".jpg")
            run(f'magick "{img}[0]" "{new}"')
            img.unlink()
            self.infoEnts['Image'].set(new.name)
        return

    def getProgPaths(self) -> tuple[Path, U[Path, dict[str, Path]]]:
        pPthDct: dict[str, Path] = dict()
        rawPath = Path()
        for d in self.progPaths.values():
            if d['show']:
                pth = d['path'].get().strip()
                if pth != "Path to executable":
                    nm = d['name'].get().strip()
                    if nm == "Preferred name":
                        nm = pth
                    pth = PATH_GAMES.joinpath(pth)
                    rawPath = pth
                    pPthDct[nm] = pth
        while not PATH_GAMES.samefile(rawPath.parent):
            rawPath = rawPath.parent
        gamePath = rawPath
        if len(pPthDct) == 1:
            pPthDct = pth
        return (gamePath, pPthDct)

    def updateData(self, gamePath: Path, oldData: O[GAMEDATA_TYPE], newData: GAMEDATA_TYPE) -> None:
        pathIsNew = (not self.game.samefile(gamePath)
                     if self.game.exists() else True)
        oldVer = self.gamelib.masterlist[self.oldgame]['Info']['Version'] if oldData else ''
        newVer = newData['Info']['Version']
        if pathIsNew or not oldData or oldVer != newVer:
            oldTitle = self.gamelib.masterlist[self.oldgame]['Info']['Title'] if oldData else ''
            newTitle = newData['Info']['Title']
            # update recent list
            oldList = 'updated' if oldData else 'added'
            curList = self.gamelib.recentlist[oldList].copy()
            if oldTitle in curList:
                curList.remove(oldTitle)
            if newTitle in curList:
                curList.remove(newTitle)
            curList.insert(0, newTitle)
            while len(curList) > MAX_RECENT_GAMES:
                curList.pop()
            if curList != self.gamelib.recentlist[oldList]:
                self.gamelib.recentlist[oldList] = curList
                self.gamelib.saveRecent()
            # check if path has changed
            if pathIsNew:
                self.gamelib.masterlist.pop(self.oldgame, None)
                self.game = gamePath
        # update master list
        self.gamelib.masterlist[self.game] = newData
        self.gamelib.save()
        self.updateGames = True if self.adding else self.game
