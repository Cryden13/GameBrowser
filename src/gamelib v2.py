from types import SimpleNamespace
from typing import TYPE_CHECKING
from PyQt5.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QVBoxLayout,
    QApplication
)
from json import (
    JSONEncoder,
    load as jsonLoad,
    dump as jsonDump
)

from .constants import *
from .messageBox import Messagebox as Mbox
from .edit import EditUI
from .browse.lineItem import UpdateLineItems
if TYPE_CHECKING:
    from .browse.lineItem import LineItem


class Game:
    def __init__(self, Dir: str, Info: dict[str, str], Categories: dict[str, U[int, str]], Tags: dict[str, U[int, str]]):
        self.Dir = FPATH_GAMES.joinpath(Dir)
        self.Info = self._Info(self.Dir, **Info)
        self.Categories = SimpleNamespace(**Categories)
        self.Tags = SimpleNamespace(**Tags)

    class _Info:
        def __init__(self, Dir: Path, Title: str, URL: str, Image: str, Version: str, Program_Path: U[str, dict[str, str]], Description: str):
            self.Title = Title
            self.URL = URL
            self.Image = Image
            self.Version = Version
            if isinstance(Program_Path, dict):
                self.Program_Path = {k: Dir.joinpath(v)
                                     for k, v in Program_Path.items()}
            else:
                self.Program_Path = Dir.joinpath(Program_Path)
            self.Description = Description

    @classmethod
    def _fromJson(cls, data):
        return cls(**data)


class GameLibrary:
    main_win: QMainWindow
    # all games
    master_list: list[Game]
    # all three recent games lists
    recent_list: dict[str, list[str]]
    # reference dict for the QVBoxLayouts within every recent tab, where {<layout_name>: <layout>}
    recent_tab_layouts: dict[str, QVBoxLayout]
    # reference dict for the QVBoxLayouts within every non-recent tab, where {<layout_letters>: <layout>}
    tab_layouts: dict[str, QVBoxLayout]
    # reference dict for all lineitems. [played, updated, added, alpha]
    lineitem_pointers: dict[Path, "list[LineItem]"]

    def __init__(self, win: QMainWindow):
        self.main_win = win
        self.recent_tab_layouts = dict()
        self.tab_layouts = dict()
        self.lineitem_pointers = dict()
        # master list
        with PATH_LIST.open('r') as f:
            json_data = jsonLoad(f)
        games = [Game._fromJson(d) for d in json_data]
        self.master_list = sorted(games, key=lambda d: d.Info.Title.casefold())
        # recent list
        with PATH_RECENT.open('r') as f:
            self.recent_list = jsonLoad(f)
        self.checkForMissingGames()

#     ______  ___  ___________
#    / __/ / / / |/ / ___/ __/
#   / _// /_/ /    / /___\ \
#  /_/  \____/_/|_/\___/___/

    def getGameFromTitle(self, game_title: str):
        return next((g for g in self.master_list if g.Info.Title == game_title), None)

    def getIndexFromTitle(self, game_title: str):
        return next((self.master_list.index(g) for g in self.master_list if g.Info.Title == game_title), None)

    def getGameFromPath(self, game_path: Path):
        return next((g for g in self.master_list if g.Dir == game_path), None)

    def getIndexFromPath(self, game_path: Path):
        return next((self.master_list.index(g) for g in self.master_list if g.Dir == game_path), None)

    def checkForMissingGames(self):
        missing_games = [g for g in self.master_list if not g.Dir.exists()]
        ct = len(missing_games)
        for i, game in enumerate(missing_games):
            ans = Mbox.askquestion(title=f"Missing Reference ({i+1}/{ct})",
                                   message=(f"The folder for '{game.Info.Title}' could not be found.\n"
                                            "Do you want to DELETE this item?"),
                                   buttons=('OK', 'Open', 'Ignore', 'Cancel'))
            if ans == 'OK':
                idx = self.master_list.index(game)
                self.master_list.pop(idx)
                self.save()
            elif ans == 'Open':
                new_path_raw: str = QFileDialog.getExistingDirectory(
                    caption=f"Select the main folder for '{game.Info.Title}'",
                    directory=str(FPATH_GAMES))
                if new_path_raw:
                    new_path = Path(new_path_raw).resolve()
                    if new_path.samefile(FPATH_GAMES):
                        new_path_raw, *_ = QFileDialog.getOpenFileName(
                            caption=f"Select the file for '{game.Info.Title}'",
                            directory=str(FPATH_GAMES),
                            filter=FILETYPENAMES
                        )
                        if new_path_raw:
                            new_path = Path(new_path_raw).resolve()
                        else:
                            continue
                    ppth = game.Info.Program_Path
                    if isinstance(ppth, dict):
                        ppth_out = {nm: new_path.joinpath(p.relative_to(game.Dir))
                                    for nm, p in ppth.items()}
                    else:
                        ppth_out = new_path.joinpath(
                            ppth.relative_to(game.Dir))
                    game.Info.Program_Path = ppth_out
                    self.save()
            elif ans == 'Ignore':
                continue
            else:
                break

    def checkForNewGames(self):
        new_games: list[Path] = list()
        for game_dir in FPATH_GAMES.iterdir():
            if game_dir == FPATH_PROG or game_dir.stem[0] == '_':
                continue
            if not game_dir.is_dir() and game_dir.suffix not in FILETYPES:
                continue
            if self.getGameFromPath(game_dir):
                continue
            new_games.append(game_dir)
        if new_games:
            for i, new_game in enumerate(new_games):
                edit_ui = EditUI(game_lib=self, show_ignore=True)
                edit_ui.dlg.setWindowTitle(
                    f"Add New Game ({i+1}/{len(new_games)})")
                edit_ui.simpleInfo(fol=new_game)
                if edit_ui.output == 'ignore':
                    continue
                elif edit_ui.output == 'cancel':
                    break
                else:
                    UpdateLineItems(self, edit_ui)
        else:
            Mbox.showinfo(title="Notice",
                          message="No new games were found!")

    def verifyTags(self):
        all_tags = sorted(TAG_TOG | TAG_SEL.keys())
        for game in self.master_list:
            tags = game.Tags.__dict__
            for tag in tags.keys():
                if tag not in all_tags:
                    tags.pop(tag)
            for tag in all_tags:
                tags[tag] = tags.pop(tag, 0 if tag in TAG_TOG else '')
        QApplication.beep()

    def verifyExes(self):
        errors: dict[Game, list[Path]] = dict()
        for game in self.master_list:
            ppth = game.Info.Program_Path
            if isinstance(ppth, dict):
                missing = [pth for pth in ppth.values() if not pth.exists()]
            else:
                missing = [ppth] if not ppth.exists() else []
            if missing:
                errors.update({game: missing})
        if errors:
            for i, (game, missing) in enumerate(errors.items()):
                ans = Mbox.askquestion(title=f"Missing/Incorrect Executables ({i+1}/{len(errors)})",
                                       message=(f"Game: <{game.Info.Title}>\n"
                                                f"Bad executables: <{'>, <'.join([str(m.relative_to(game.Dir)) for m in missing])}>\n"
                                                "Would you like to fix this issue?"),
                                       buttons=('Yes', 'No', 'Cancel'))
                if ans == 'Yes':
                    edit_ui = EditUI(game_lib=self, show_ignore=True)
                    edit_ui.dlg.setWindowTitle(
                        f"Fixing Game ({i+1}/{len(errors)})")
                    edit_ui.fullInfo(game)
                    if edit_ui.output == 'ignore':
                        continue
                    elif edit_ui.output == 'cancel':
                        break
                    else:
                        UpdateLineItems(self, edit_ui)
                elif ans == 'Cancel':
                    break
            QApplication.beep()
        else:
            Mbox.showinfo(title="Missing Executables",
                          message="There were no incorrect executables found!")

#     _______ _   ______
#    / __/ _ | | / / __/
#   _\ \/ __ | |/ / _/
#  /___/_/ |_|___/___/

    class GameEncoder(JSONEncoder):
        def default(self, o):
            if isinstance(o, Path):
                return str(o.relative_to(FPATH_GAMES))
            else:
                return o.__dict__

    def save(self):
        print('TRYING TO SAVE MAIN')
        self.master_list.sort(key=lambda d: d.Info.Title.casefold())
        with PATH_LIST.open('w') as f:
            jsonDump(self.master_list, f, cls=self.GameEncoder, indent=4)

    def saveRecent(self):
        print('TRYING TO SAVE RECENT')
        with PATH_RECENT.open('w') as f:
            jsonDump(self.recent_list, f, indent=4)
