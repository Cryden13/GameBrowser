from tkinter.filedialog import askopenfilenames as Askfiles
from os import path as os_path, listdir as os_listdir
import json

from editlist import EditGames
from constants import *


class GameLib:
    def __init__(self, root):
        self.root = root
        with open(PATH_LIST, 'r') as f:
            self.masterList = json.load(f)
        self.checkForMissingGames()
        with open(PATH_RECENT, 'r') as f:
            self.recentList = json.load(f)
        with open(PATH_NEW, 'r') as f:
            self.newList = json.load(f)

    def checkForMissingGames(self):
        missingGames = [g for g in self.masterList if g not in os_listdir()]
        ttl = "Missing Reference ({} of %d)" % len(missingGames)
        msg = "'{}' could not be found.\nPress <abort> to delete this item, <retry> to search for this item's executable(s), or <ignore> to skip this check"
        searchTtl = "Select the executable(s) for '{}'"
        doUpdate = False
        for i, game in enumerate(missingGames):
            ans = Mbox.askquestion(ttl.format(i+1),
                                   msg.format(game),
                                   icon='warning',
                                   type='abortretryignore')
            if ans == 'abort':
                self.masterList.pop(game)
                doUpdate = True
            elif ans == 'retry':
                exePaths = list()
                addMore = True
                while addMore:
                    newPaths = Askfiles(title=searchTtl.format(game),
                                        initialdir=PATH_GAMES)
                    exePaths += [os_path.relpath(p) for p in newPaths]
                    addMore = Mbox.askyesno("Add More?",
                                            "Are there additional executable(s) to add?")
                if exePaths:
                    data = self.masterList.pop(game)
                    paths = '; '.join(exePaths)
                    data['Info']['Program Path'] = paths
                    self.masterList.update({paths.split('\\')[0]: data})
                    doUpdate = True
            else:
                break
        doUpdate = self.insertNewTags(doUpdate)
        self.root.deiconify()
        if doUpdate:
            self.save()

    def insertNewTags(self, update):
        for game, data in self.masterList.items():
            for n in set(INFO_ENT) - set(data['Info']):
                self.masterList[game]['Info'][n] = 0
                update = True
            for n in (set(CAT_TOG) | set(CAT_LST)) - set(data['Categories']):
                self.masterList[game]['Categories'][n] = 0
                update = True
            for n in set(TAG_TOG) - set(data['Tags']):
                self.masterList[game]['Tags'][n] = 0
                update = True
        return update

    def save(self):
        self.alphabetize()
        with open(PATH_LIST, 'w') as f:
            json.dump(self.masterList, f, indent=4)

    def alphabetize(self):
        titles = dict()
        for name, data in self.masterList.items():
            titles.update({data['Info']['Title']: name})
        alpha = list(titles)
        alpha.sort()
        names = [titles[title] for title in alpha]
        self.masterList = {name: self.masterList[name] for name in names}

    def checkForNewGames(self):
        newGames = list()
        for game in os_listdir():
            if game == os_path.basename(PATH_PROG):
                continue
            if not os_path.isdir(game):
                if os_path.splitext(game)[1] not in FILETYPES:
                    continue
            if game in self.masterList:
                continue
            newGames.append(game)
        if newGames:
            newGames.sort()
            print(len(newGames), 'new games')
            return EditGames(self.root, self, newGames, True)
        else:
            Mbox.showinfo("Notice", "No new games were found!")
            return False

    def saveRecent(self):
        with open(PATH_RECENT, 'w') as f:
            json.dump(self.recentList, f, indent=4)

    def saveNew(self):
        with open(PATH_NEW, 'w') as f:
            json.dump(self.newList, f, indent=4)
