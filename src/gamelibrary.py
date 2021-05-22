from tkinter.filedialog import askdirectory as Askdir
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
        self.root = root
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
        missingGames = [g for g in self.masterlist if not g.exists()]
        ct = len(missingGames)
        notFound = ("could not be found.\n"
                    "Press <abort> to delete this item, "
                    "<retry> to search for this item, "
                    "or <ignore> to skip this check.")
        srchTtl = "Select the main folder/file for"
        for i, game in enumerate(missingGames):
            ans = Mbox.askquestion(title=f"Missing Reference ({i+1} of {ct})",
                                   message=f"'{game.name}' {notFound}",
                                   icon='warning',
                                   type='abortretryignore')
            if ans == 'abort':
                self.masterlist.pop(game)
                self.save()
            elif ans == 'retry':
                newPath: str = Askdir(title=f"{srchTtl} '{game.name}'",
                                      initialdir=PATH_GAMES,
                                      mustexist=True)
                if newPath:
                    EditGames(parent=self.root,
                              gamelib=self,
                              allGames={Path(newPath): game})
            else:
                break

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

    def alphabetize(self) -> None:
        # create dict where {lowercase_game_title: game_folder}
        ttl2Fol: dict[str, Path]
        ttl2Fol = {data['Info']['Title'].lower(): fol
                   for fol, data in self.masterlist.items()}
        # create list of lowercase, alphabetized titles
        alphaTtls = list(ttl2Fol)
        alphaTtls.sort()
        # create alphabetized list of folder names
        alphaFols = [ttl2Fol[ttl] for ttl in alphaTtls]
        # update the list
        self.masterlist = {fol: self.masterlist[fol]
                           for fol in alphaFols}

    def splitByLetter(self) -> dict[str, list[Path]]:
        # create dict 'alpha' where {'game_title_first_letter': ['game_folders']}
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
        newGames: list[Path] = list()
        for game in PATH_GAMES.iterdir():
            if game == PATH_PROG or game.stem[0] == '_':
                continue
            if not game.is_dir():
                if game.suffix not in FILETYPES:
                    continue
            if game in self.masterlist:
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
        self.alphabetize()
        mlist = dict()
        for k in self.masterlist:
            gpath = str(k.resolve().relative_to(PATH_GAMES))
            data = deepcopy(self.masterlist[k])
            ppth = data['Info']['Program Path']
            if isinstance(ppth, dict):
                for nm, pth in ppth.items():
                    ppth[nm] = str(pth.resolve().relative_to(PATH_GAMES))
            else:
                ppth = str(ppth.resolve().relative_to(PATH_GAMES))
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
