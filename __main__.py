from traceback import format_exc
from window import *


class GameLib:
    def __init__(self):
        self.masterList = {}
        if os_path.exists(PATH_LIST):
            with open(PATH_LIST, 'r') as f:
                self.masterList = json.load(f)
            self.alphabetize()
            self.checkMissing()

    def checkMissing(self):
        missingGames = [g for g in self.masterList if g not in os_listdir()]
        if missingGames:
            for game in missingGames:
                ans = mbox.askyesnocancel(
                    "Missing reference", "'{}'\ncould not be found.\nPress 'yes' to delete the reference, 'no' to browse for the file, or 'cancel' to do nothing".format(game))
                if ans:
                    self.masterList.pop(game)
                elif ans == False:
                    exePaths = []
                    more = True
                    while more:
                        newPaths = askopenfilenames(
                            title="Select the executable(s) for '{}'".format(game), initialdir=PATH_GAMES)
                        exePaths += [os_path.relpath(p) for p in newPaths]
                        more = mbox.askyesno(
                            "More?", "Are there more executable(s) to add?")
                    if exePaths:
                        data = self.masterList.pop(game)
                        paths = '||'.join(exePaths)
                        data['Info']['Program Path'] = paths
                        self.masterList.update({paths.split('\\')[0]: data})
                        root.deiconify()
                    else:
                        continue
                else:
                    continue
                self.save()
        self.checkNewTags()

    def checkNewTags(self):
        i = 0
        for game, data in self.masterList.items():
            for n in set(INFO_ENT)-set(data['Info']):
                self.masterList[game]['Info'][n] = 0
                i += 1
            for n in (set(CAT_TOG) | set(CAT_LST))-set(data['Categories']):
                self.masterList[game]['Categories'][n] = 0
                i += 1
            for n in set(TAG_TOG)-set(data['Tags']):
                self.masterList[game]['Tags'][n] = 0
                i += 1
        if i:
            self.save()

    def save(self):
        self.alphabetize()
        with open(os_path.join(PATH_DIR, 'Game List.json'), 'w') as f:
            json.dump(self.masterList, f, indent=4)

    def alphabetize(self):
        titles = {data['Info']['Title']: name for name,
                  data in self.masterList.items()}
        alpha = list(titles)
        alpha.sort()
        self.masterList = {name: self.masterList[name] for name in [
            titles[title] for title in alpha]}

    def checkGames(self):
        newGames = [g for g in os_listdir() if (os_path.isdir(g) or os_path.splitext(
            g)[1] in FILETYPES) and g not in self.masterList and g != os_path.basename(PATH_DIR)]
        if newGames:
            addNew = EditGames(root, self, newGames, True)
            try:
                root.wait_window(addNew)
            except Exception:
                pass
        else:
            mbox.showinfo("Notice", "No new games were found!")
        return


os_chdir(PATH_GAMES)
root = GUI()
gamelib = GameLib()
root.start_main(gamelib)
root.mainloop()
if format_exc()[:14] != "NoneType: None":
    input("Fatal Exception occured. Press Enter to continue: ")
