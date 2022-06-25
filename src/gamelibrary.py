
from json import (
    load as jsonLoad,
    dump as jsonDump
)
from copy import deepcopy
from typing import TYPE_CHECKING
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QVBoxLayout
)

from .browse.lineItem import UpdateLineItems
from .messageBox import Messagebox as Mbox
from .edit import EditUI
from .constants import *
if TYPE_CHECKING:
    from .browse.lineItem import LineItem


class GameLibrary:
    main_win: QMainWindow
    # all games
    master_list: dict[Path, GAMEDATA_TYPE]
    # all three recent games lists
    recent_list: dict[str, list[str]]
    # reference dict for the QVBoxLayouts within every recent tab, where {<layout_name>: <layout>}
    recent_tab_layouts: dict[str, QVBoxLayout]
    # reference dict for the QVBoxLayouts within every non-recent tab, where {<layout_letters>: <layout>}
    tab_layouts: dict[str, QVBoxLayout]
    # reference dict for all lineitems. [played, updated, added, alpha]
    lineitem_pointers: dict[Path, list["LineItem"]]

    def __init__(self, win: QMainWindow):
        self.main_win = win
        self.recent_tab_layouts = dict()
        self.tab_layouts = dict()
        self.lineitem_pointers = dict()
        # master list
        self.master_list = dict()
        with PATH_LIST.open('r') as f:
            raw_list: dict[str, GAMEDATA_TYPE] = jsonLoad(f)
        for game in list(raw_list):
            game_pth = FPATH_GAMES.joinpath(game)
            data = raw_list.pop(game)
            ppth = data['Info']['Program Path']
            if isinstance(ppth, dict):
                ppth_out = {nm: game_pth.joinpath(pth)
                            for nm, pth in ppth.items()}
            else:
                ppth_out = game_pth.joinpath(ppth)
            data['Info']['Program Path'] = ppth_out
            self.master_list[game_pth] = deepcopy(data)
        self.alphabetizeMaster()
        # recent list
        with PATH_RECENT.open('r') as f:
            self.recent_list = jsonLoad(f)
        self.checkForMissingGames()

#     ______  ___  ___________
#    / __/ / / / |/ / ___/ __/
#   / _// /_/ /    / /___\ \
#  /_/  \____/_/|_/\___/___/

    def alphabetize(self, data: U[dict[str], list[str], tuple[str]]) -> U[list[str], tuple[str], dict[str]]:
        def alphaKey(e: str):
            s = e[4:] if len(e) > 5 and e[:4].lower() == 'the ' else e
            return s.casefold()
        # create list of lowercase, alphabetized keys from 'data'
        alpha_lst = sorted(list(data), key=alphaKey)
        if isinstance(data, list):
            out = alpha_lst
        elif isinstance(data, tuple):
            out = tuple(alpha_lst)
        else:
            out = {k: v for a in alpha_lst
                   for k, v in data.items()
                   if k == a}
        return out

    def alphabetizeMaster(self):
        # create dict 'ttl2Fol' where {game_title: game_folder}
        ttl2Fol: dict[str, Path] = {data['Info']['Title']: fol
                                    for fol, data in self.master_list.items()}
        alphaTtls = self.alphabetize(ttl2Fol)
        alphaFols = [fol for fol in alphaTtls.values()]
        self.master_list = {fol: self.master_list[fol]
                            for fol in alphaFols}

    def checkForMissingGames(self):
        missing_games = {g: i['Info']['Title']
                         for g, i in self.master_list.items() if not g.exists()}
        ct = len(missing_games)
        for i, (fol, game) in enumerate(missing_games.items()):
            ans = Mbox.askquestion(title=f"({i+1}/{ct}) Missing Reference",
                                   message=(f"The folder for '{game}' Could not be found.\n"
                                            "Do you want to DELETE this item?"),
                                   buttons=('Ok', 'Open', 'Ignore', 'Cancel'))
            if ans == 'OK':
                chk = Mbox.askquestion(title="Delete Game",
                                       message=f"Are you sure you want to delete {game}? This is irreversible")
                if chk == 'Yes':
                    self.master_list.pop(fol)
                    self.save()
            elif ans == 'Open':
                new_path_raw: str = QFileDialog.getExistingDirectory(
                    caption=f"Select the main folder for '{fol.name}'",
                    directory=str(FPATH_GAMES))
                if new_path_raw:
                    new_path = Path(new_path_raw).resolve()
                    if new_path.samefile(FPATH_GAMES):
                        new_path_raw, *_ = QFileDialog.getOpenFileName(
                            caption=f"Select the file for '{fol.name}'",
                            directory=str(FPATH_GAMES),
                            filter=FILETYPENAMES
                        )
                        if new_path_raw:
                            new_path = Path(new_path_raw).resolve()
                        else:
                            continue
                    data = self.master_list.pop(fol)
                    ppth = data['Info']['Program Path']
                    if isinstance(ppth, dict):
                        ppth_out = {nm: new_path.joinpath(p.relative_to(fol))
                                    for nm, p in ppth.items()}
                    else:
                        ppth_out = new_path.joinpath(ppth.relative_to(fol))
                    data['Info']['Program Path'] = ppth_out
                    self.master_list.update({new_path: data})
                    self.save()
                    edit_ui = EditUI(game_lib=self)
                    edit_ui.fullInfo(gpath=new_path, ginfo=data)
            elif ans == 'Ignore':
                continue
            else:
                break

    def checkForNewGames(self):
        all_games = self.master_list
        new_games: list[Path] = list()
        for game in FPATH_GAMES.iterdir():
            if game == FPATH_PROG or game.stem[0] == '_':
                continue
            if not game.is_dir() and game.suffix not in FILETYPES:
                continue
            if game in all_games:
                continue
            new_games.append(game)
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
        for gdata in self.master_list.values():
            tags = gdata['Tags']
            for tag in tags.keys():
                if tag not in all_tags:
                    tags.pop(tag)
            for tag in all_tags:
                tags[tag] = tags.pop(tag, 0 if tag in TAG_TOG else '')
        QApplication.beep()

    def verifyExes(self):
        errors: dict[Path, list[Path]] = dict()
        for i, (gpath, data) in enumerate(self.master_list.items()):
            ppth = data['Info']['Program Path']
            if isinstance(ppth, dict):
                missing = [pth for pth in ppth.values() if not pth.exists()]
            else:
                missing = [ppth] if not ppth.exists() else []
            if missing:
                errors.update({gpath: missing})
        if errors:
            for i, (gpath, missing) in enumerate(errors.items()):
                ans = Mbox.askquestion(title=f"Missing/Incorrect Executables ({i+1}/{len(errors)})",
                                       message=(f"Game: <{gpath.relative_to(FPATH_GAMES)}>\n"
                                                f"Bad executables: <{'>, <'.join([str(m.relative_to(gpath)) for m in missing])}>\n"
                                                "Would you like to fix this issue?"),
                                       buttons=('Yes', 'No', 'Cancel'))
                if ans == 'Yes':
                    data = self.master_list[gpath]
                    edit_ui = EditUI(game_lib=self, show_ignore=True)
                    edit_ui.dlg.setWindowTitle(
                        f"Fixing Game ({i+1}/{len(errors)})")
                    edit_ui.fullInfo(gpath, data)
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
                          message="There were no incorrect/missing executables found!")

#     _______ _   ______
#    / __/ _ | | / / __/
#   _\ \/ __ | |/ / _/
#  /___/_/ |_|___/___/

    def save(self) -> None:
        print('TRYING TO SAVE MAIN')
        self.alphabetizeMaster()
        raw_list = dict()
        for game_path in self.master_list:
            game = str(game_path.relative_to(FPATH_GAMES))
            data = deepcopy(self.master_list[game_path])
            ppth = data['Info']['Program Path']
            if isinstance(ppth, dict):
                ppth_out = {nm: str(pth.relative_to(game_path))
                            for nm, pth in ppth.items()}
            else:
                ppth_out = str(ppth.relative_to(game_path))
            data['Info']['Program Path'] = ppth_out
            raw_list[game] = data
        with PATH_LIST.open('w') as f:
            jsonDump(raw_list, f, indent=4)

    def saveRecent(self) -> None:
        print('TRYING TO SAVE RECENT')
        with PATH_RECENT.open('w') as f:
            jsonDump(self.recent_list, f, indent=4)
