from json import load as json_load, dump as json_dump
from tkinter.filedialog import askdirectory as Askdir
from os import path as os_path, listdir as os_listdir
from re import match as re_match

from editlist import EditGames
from constants import *

if TYPE_CHECKING:
    from tkinter import Tk

    from browse import GUI


class GameLib:
    root: "U[Tk, GUI]"
    masterlist: oDict[str, GAMEDATA_TYPE]
    recentList: dict[str, list[str]]
    newList: dict[str, dict[str, str]]

    def __init__(self, root: "U[Tk, GUI]"):
        self.root = root
        with open(PATH_LIST, 'r') as f:
            self.masterlist = oDict(json_load(f))
        with open(PATH_RECENT, 'r') as f:
            self.recentList = json_load(f)
        with open(PATH_NEW, 'r') as f:
            self.newList = json_load(f)
        self.checkForMissingGames()
        self.insertNewTags()

    def checkForMissingGames(self) -> None:
        missingGames = [g for g in self.masterlist if g not in os_listdir()]
        ct = len(missingGames)
        notFound = ("could not be found.\n"
                    "Press <abort> to delete this item, "
                    "<retry> to search for this item, "
                    "or <ignore> to skip this check.")
        srchTtl = "Select the main folder/file for"
        for i, game in enumerate(missingGames):
            ans = Mbox.askquestion(title=f"Missing Reference ({i+1} of {ct})",
                                   message=f"'{game}' {notFound}",
                                   icon='warning',
                                   type='abortretryignore')
            if ans == 'abort':
                self.masterlist.pop(game)
                self.save()
            elif ans == 'retry':
                newPath: str = Askdir(title=f"{srchTtl} '{game}'",
                                      initialdir=PATH_GAMES,
                                      mustexist=True)
                if newPath:
                    data = self.masterlist.get(game)
                    EditGames(parent=self.root,
                              gamelib=self,
                              allGames={os_path.relpath(newPath): data})
            else:
                break

    def insertNewTags(self) -> None:
        doUpdate = False
        for game, data in self.masterlist.items():
            for n in set(INFO_ENT) - set(data['Info']):
                self.masterlist[game]['Info'][n] = 0
                doUpdate = True
            for n in (set(CAT_TOG) | set(CAT_SEL)) - set(data['Categories']):
                self.masterlist[game]['Categories'][n] = 0
                doUpdate = True
            for n in set(TAG_TOG) - set(data['Tags']):
                self.masterlist[game]['Tags'][n] = 0
                doUpdate = True
        if doUpdate:
            self.save()

    def alphabetize(self) -> None:
        # create dict where {game_title(lowercase): game_folder}
        ttl2Fol: dict(str, str) = dict()
        for fol, data in self.masterlist.items():
            ttl2Fol[data['Info']['Title'].lower()] = fol
        # create list of lowercase, alphabetized titles
        alphaTtls: list[str] = list(ttl2Fol)
        alphaTtls.sort()
        # create alphabetized list of folder names
        alphaFols: list[str] = [ttl2Fol[ttl] for ttl in alphaTtls]
        # update the list
        self.masterlist = oDict([(fol, self.masterlist[fol])
                                 for fol in alphaFols])

    def splitByLetter(self) -> oDict[str, list[str]]:
        # create ordered dict 'alpha' where {'game_title_first_letter': ['game_folders']}
        gameByLetter: dict[str, list[str]] = dict()
        for fol, data in self.masterlist.items():
            # get the first letters of the game title
            firstLetters = str(data['Info']['Title'][:2]).strip()
            if re_match(r'[^A-Za-z]', firstLetters[0]):
                firstLetters = str('#')
            # check if another game has already started with those letters/create new list
            lst = list(gameByLetter.pop(firstLetters, list()))
            lst.append(fol)
            gameByLetter[firstLetters] = lst
        # alphabetize the ordered dict
        alphaDct: dict[str, str] = {l.lower(): l for l in gameByLetter}
        alphaLst: list[str] = list(alphaDct)
        alphaLst.sort()
        alpha: oDict[str, list[str]] = oDict()
        for letter in alphaLst:
            l = alphaDct[letter]
            alpha[l] = gameByLetter[l]
        # create ordered dict 'out' where {'letter_range': ['game_folders']}
        out: oDict[str, list[str]] = oDict()
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
                    lbl = first if first == last else f'{first}-{last}'
                    first = letter
                out[lbl] = folList
                folList = fols
            else:
                folList += fols
            last = letter
        lbl = first if first == last[0] else f'{first}-{last[0]}'
        out[lbl] = folList
        return out

    def checkForNewGames(self) -> bool:
        newGames: list[str] = list()
        for game in os_listdir():
            if game == os_path.basename(PATH_PROG):
                continue
            if not os_path.isdir(game):
                if os_path.splitext(game)[-1] not in FILETYPES:
                    continue
            if game in self.masterlist:
                continue
            newGames.append(game)
        if newGames:
            newGames.sort()
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
        with open(PATH_LIST, 'w') as f:
            json_dump(self.masterlist, f, indent=4)

    def saveRecent(self) -> None:
        with open(PATH_RECENT, 'w') as f:
            json_dump(self.recentList, f, indent=4)

    def saveNew(self) -> None:
        with open(PATH_NEW, 'w') as f:
            json_dump(self.newList, f, indent=4)
