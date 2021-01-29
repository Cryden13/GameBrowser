from window import *


class GameLib:
    def __init__(self, root):
        self.root = root
        self.masterList = {}
        if os_path.exists(PATH_LIST):
            with open(PATH_LIST, 'r') as f:
                self.masterList = json.load(f)
            self.checkForMissingGames()

    def checkForMissingGames(self):
        missingGames = [g for g in self.masterList if g not in os_listdir()]
        ttl = "Missing Reference ({} of {})"
        msg = "'{}' could not be found.\nPress <abort> to delete this item, <retry> to search for the file, or <ignore> to skip this check"
        update = False
        num = len(missingGames)
        for i, game in enumerate(missingGames):
            ans = mbox.askquestion(ttl.format(i+1, num),
                                   msg.format(game),
                                   icon='warning',
                                   type='abortretryignore')
            if ans == 'ignore':
                break
            elif ans == 'retry':
                exePaths = []
                more = True
                while more:
                    kwargs = dict(title="Select the executable(s) for '{}'".format(game),
                                  initialdir=PATH_GAMES)
                    newPaths = askopenfilenames(**kwargs)
                    exePaths += [os_path.relpath(p) for p in newPaths]
                    more = mbox.askyesno("More?",
                                         "Are there more executable(s) to add?")
                if exePaths:
                    data = self.masterList.pop(game)
                    paths = '; '.join(exePaths)
                    data['Info']['Program Path'] = paths
                    self.masterList.update({paths.split('\\')[0]: data})
                    update = True
            else:
                self.masterList.pop(game)
                update = True
        update = self.insertNewTags(update)
        self.root.deiconify()
        if update:
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
            mbox.showinfo("Notice", "No new games were found!")
            return False
