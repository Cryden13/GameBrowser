from tkinter.filedialog import askdirectory as Askdir
from tkinter import messagebox as Mbox
from re import match as re_match
from copy import deepcopy
from json import (
    load as json_load,
    dump as json_dump
)

try:
    from .editlist import EditGames
    from .constants import *
except ImportError:
    from subprocess import run
    from pathlib import Path
    pth = Path(__file__).parents[1]
    run(['py', '-m', pth.name, 'console'], cwd=pth.parent)
    raise SystemExit

if TYPE_CHECKING:
    from .addnew import AddGUI
    from .browse import BrowseGUI
    from .checkfornew import CheckGUI


class GameLib:
    root: "U[AddGUI, BrowseGUI, CheckGUI]"
    masterlist: dict[Path, GAMEDATA_TYPE]
    recentlist: dict[str, list[str]]
    newlist: dict[Path, dict[str, str]]

    def __init__(self, root: "U[AddGUI, BrowseGUI, CheckGUI]"):
        global PATH_LIST
        self.root = root
        ans = Mbox.askyesnocancel(title="Choose Library",
                                  message="Open games A-N?")
        if ans:
            PATH_LIST = PATH_LIB.joinpath('Game List 1.json')
        elif ans == False:
            PATH_LIST = PATH_LIB.joinpath('Game List 2.json')
        else:
            raise SystemExit
        # masterlist
        self.masterlist = dict()
        with PATH_LIST.open('r') as f:
            mlist: dict[str, GAMEDATA_TYPE] = json_load(f)
        for k in list(mlist):
            game = Path(k).resolve()
            data = mlist.pop(k)
            ppth = data['Info']['Program Path']
            if isinstance(ppth, dict):
                out = dict()
                for nm, pth in ppth.items():
                    out[nm] = Path(pth).resolve()
            else:
                out = Path(ppth).resolve()
            data['Info']['Program Path'] = out
            self.masterlist[game] = deepcopy(data)
        # recentlist
        with PATH_RECENT.open('r') as f:
            self.recentlist = json_load(f)
        # newlist
        with PATH_NEW.open('r') as f:
            self.newlist = {PATH_GAMES.joinpath(k): v
                            for k, v in json_load(f).items()}
        self.checkForMissingGames()
        self.insertNewTags()

    def checkForMissingGames(self) -> None:
        missingGames = {g: i['Info']['Title']
                        for g, i in self.masterlist.items() if not g.exists()}
        ct = len(missingGames)
        notFound = ("could not be found.\n"
                    "Press <abort> to delete this item, "
                    "<retry> to search for this item, "
                    "or <ignore> to skip this check.")
        for i, (fol, game) in enumerate(missingGames.items()):
            ans = Mbox.askquestion(title=f"Missing Reference ({i+1} of {ct})",
                                   message=f"The folder for '{game}' {notFound}",
                                   icon='warning',
                                   type='abortretryignore')
            if ans == 'abort':
                self.masterlist.pop(fol)
                self.save()
            elif ans == 'retry':
                newPath: str = Askdir(title=f"Select the main folder/file for '{fol.name}'",
                                      initialdir=PATH_GAMES,
                                      mustexist=True)
                if newPath:
                    EditGames(parent=self.root,
                              gamelib=self,
                              allGames={Path(newPath): fol})
            else:
                continue

    def insertNewTags(self) -> None:
        def alpha(d: dict) -> dict:
            alphalst = list(d)
            alphalst.sort()
            alphadct = {i: d[i] for i in alphalst}
            return alphadct

        doUpdate = False
        for game, data in self.masterlist.items():
            for n in set(INFO_ENT) - set(data['Info']):
                data['Info'][n] = 0
                self.masterlist[game]['Info'] = alpha(data['Info'])
                doUpdate = True
            for n in (set(CAT_TOG) | set(CAT_SEL)) - set(data['Categories']):
                data['Categories'][n] = 0
                self.masterlist[game]['Categories'] = alpha(data['Categories'])
                doUpdate = True
            for n in set(TAG_TOG) - set(data['Tags']):
                data['Tags'][n] = 0
                self.masterlist[game]['Tags'] = alpha(data['Tags'])
                doUpdate = True
        if doUpdate:
            self.save()

    def alphabetize(self, data: U[dict[str], list[str]]) -> U[dict[str], list[str]]:
        # create list of lowercase, alphabetized keys from 'data'
        alphaLst = [s.lower() for s in data]
        alphaLst.sort()
        if isinstance(data, list):
            out = alphaLst
        elif isinstance(data, tuple):
            out = tuple(alphaLst)
        else:
            out = {k: v for a in alphaLst
                   for k, v in data.items()
                   if k.lower() == a}
        return out

    def splitByLetter(self) -> dict[str, list[Path]]:
        # create dict 'gameByLetter' where {'game_title_first_letter': ['game_folders']}
        gameByLetter: dict[str, list[Path]] = dict()
        for fol, data in self.masterlist.items():
            # get the first letters of the game title
            firstLetters = str(data['Info']['Title'][:2]).strip().capitalize()
            if re_match(r'[^A-Za-z]', firstLetters[0]):
                firstLetters = str('#')
            # check if another game has already started with those letters/create new list
            lst = list(gameByLetter.pop(firstLetters, list()))
            lst.append(fol)
            gameByLetter[firstLetters] = lst
        # alphabetize the dict
        alphaDct: dict[str, str] = {l.lower(): l for l in gameByLetter}
        alphaLst: list[str] = list(alphaDct)
        alphaLst.sort()
        alpha: dict[str, list[Path]] = dict()
        for letter in alphaLst:
            l = alphaDct[letter]
            alpha[l] = gameByLetter[l]
        # create dict 'out' where {'letter_range': ['game_folders']}
        out: dict[str, list[str]] = dict()
        first = last = next(iter(alpha))
        folList = list()
        for letter, fols in alpha.items():
            if len(folList) + len(fols) > MAX_GAMES_PER_PAGE:
                if letter[0] != last[0]:
                    last = last[0]
                    if first == last:
                        lbl = first
                    else:
                        lbl = f'{first}-{last}'
                    first = letter[0]
                else:
                    lbl = (first if first == last
                           else f'{first}-{last}')
                    first = letter
                out[lbl] = folList
                folList = fols
            else:
                folList += fols
            last = letter
        lbl = (first if first == last[0]
               else f'{first}-{last[0]}')
        out[lbl] = folList
        return out

    def checkForNewGames(self) -> bool:
        allgames = dict()
        with PATH_LIB.joinpath('Game List 1.json').open('r') as f:
            allgames.update(json_load(f))
        with PATH_LIB.joinpath('Game List 2.json').open('r') as f:
            allgames.update(json_load(f))
        newGames: list[Path] = list()
        for game in PATH_GAMES.iterdir():
            if game == PATH_PROG or game.stem[0] == '_':
                continue
            if not game.is_dir():
                if game.suffix not in FILETYPES:
                    continue
            if game in allgames:
                continue
            newGames.append(game)
        if newGames:
            return EditGames(parent=self.root,
                             gamelib=self,
                             allGames=newGames,
                             adding=True)
        else:
            Mbox.showinfo(title="Notice",
                          message="No new games were found!")
            return False

    def save(self) -> None:
        def getRelPath(p: Path) -> str:
            p = p.resolve()
            if p.is_relative_to(PATH_GAMES):
                return str(p.relative_to(PATH_GAMES))
            else:
                return '\\'.join([n for i, n in enumerate(p.parts) if n != PATH_GAMES.parts[i]])

        # create dict 'ttl2Fol' where {lowercase_game_title: game_folder}
        ttl2Fol: dict[str, Path] = {data['Info']['Title']: fol
                                    for fol, data in self.masterlist.items()}
        alphaTtls = self.alphabetize(ttl2Fol)
        alphaFols = [fol for fol in alphaTtls.values()]
        self.masterlist = {fol: self.masterlist[fol]
                           for fol in alphaFols}
        mlist = dict()
        for k in self.masterlist:
            gpath = getRelPath(k)
            data = deepcopy(self.masterlist[k])
            ppth = data['Info']['Program Path']
            if isinstance(ppth, dict):
                for nm, pth in ppth.items():
                    ppth[nm] = getRelPath(pth)
            else:
                ppth = getRelPath(ppth)
            data['Info']['Program Path'] = ppth
            mlist[gpath] = data
        with PATH_LIST.open('w') as f:
            json_dump(mlist, f, indent=4)

    def saveRecent(self) -> None:
        with PATH_RECENT.open('w') as f:
            json_dump(self.recentlist, f, indent=4)

    def saveNew(self) -> None:
        nlist = {str(k.relative_to(PATH_GAMES)): v
                 for k, v in self.newlist.items()
                 if k not in self.masterlist}
        with PATH_NEW.open('w') as f:
            json_dump(nlist, f, indent=4)
