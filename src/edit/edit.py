from commandline import openatfile
from typing import TYPE_CHECKING
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from re import sub as reSub
from subprocess import run
from os import startfile
from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFileDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QDialogButtonBox
)

from .ui_edit import Ui_EditDialog
from .getinfo import GetF95Info
from ..searchBoxes import SearchBoxes
from ..constants import *
from ..messageBox import Messagebox as Mbox

if TYPE_CHECKING:
    from ..gamelibrary import GameLibrary


class EditUI(Ui_EditDialog):
    dlg: QDialog
    show_ignore: bool
    # cancel, update, new, or ignore
    output: str = 'cancel'
    game_lib: "GameLibrary"
    pointer_info: dict[str, QLineEdit]
    pointer_program_paths: list[dict[str,
                                     U[QLineEdit, QLineEdit, QPushButton]]]
    pointer_categories_chkBox: dict[str, QCheckBox]
    pointer_categories_cmbBox: dict[str, QComboBox]
    pointer_tags_chkBox: dict[str, QCheckBox]
    pointer_tags_cmbBox: dict[str, QComboBox]
    game_path: Path
    orig_path: Path

#     _____  ____________
#    /  _/ |/ /  _/_  __/
#   _/ //    // /  / /
#  /___/_/|_/___/ /_/

    def __init__(self, game_lib: "GameLibrary", show_ignore: bool = False):
        self.game_lib = game_lib
        self.show_ignore = show_ignore
        self.dlg = QDialog(self.game_lib.main_win)
        self.dlg.setWindowIcon(QIcon(PATH_ICON))
        self.setupUi(self.dlg)
        self.initVars()
        self.initButtons()
        self.initProgPaths()

    def initVars(self):
        self.pointer_info = {
            'Title': self.lineEdit_title,
            'URL': self.lineEdit_url,
            'Image': self.lineEdit_image,
            'Version': self.lineEdit_version,
        }
        self.pointer_program_paths = [
            {'lbl': self.__dict__.get(f'label_progpths_{n:02d}'),
             'name': self.__dict__.get(f'lineEdit_progpths_name_{n:02d}'),
             'pth': self.__dict__.get(f'lineEdit_progpths_exe_{n:02d}')}
            for n in range(1, 31)
        ]
        ctg_srch = SearchBoxes(self.gBox_categories, self.gLayout_categories)
        tag_srch = SearchBoxes(self.gBox_tags, self.gLayout_tags)
        self.pointer_categories_cmbBox = {
            ttl: ctg_srch.createComboBox(ttl, ['', *cnt]) for ttl, cnt in CAT_SEL.items()
        }
        self.pointer_categories_chkBox = {
            txt: ctg_srch.createCheckBox(txt, False) for txt in CAT_TOG
        }
        self.pointer_tags_cmbBox = {
            ttl: tag_srch.createComboBox(ttl, ['', *cnt]) for ttl, cnt in TAG_SEL.items()
        }
        self.pointer_tags_chkBox = {
            txt: tag_srch.createCheckBox(txt, False) for txt in TAG_TOG
        }

    def initButtons(self):
        if self.show_ignore:
            self.buttonBox.setStandardButtons(
                QDialogButtonBox.Cancel | QDialogButtonBox.Ignore | QDialogButtonBox.Save)
        self.btn_open_game.clicked.connect(self.btnOpenGamePath)
        self.btn_edit_game.clicked.connect(self.btnEditGamePath)
        self.btn_url_open.clicked.connect(self.btnUrlOpen)
        self.btn_url_pull.clicked.connect(self.btnUrlPull)
        self.btn_image_search.clicked.connect(self.btnImgSearch)
        self.btn_progpths_remove.clicked.connect(self.btnPathsRemRow)
        self.btn_progpths_browse.clicked.connect(self.btnPathsBrowse)
        self.btn_progpths_find.clicked.connect(self.btnPathsFind)
        self.btn_progpths_add.clicked.connect(self.btnPathsAddRow)
        self.buttonBox.clicked.connect(lambda b: self.btnDlgClicked(b))

    def initProgPaths(self):
        self.label_progpths_name.hide()
        nm_field = self.pointer_program_paths[0]['name']
        nm_field.hide()
        for line in self.pointer_program_paths[1:]:
            line['lbl'].hide()
            line['name'].hide()
            line['pth'].hide()
        self.btn_progpths_remove.hide()

#     ___  __  __________________  _  ______
#    / _ )/ / / /_  __/_  __/ __ \/ |/ / __/
#   / _  / /_/ / / /   / / / /_/ /    /\ \
#  /____/\____/ /_/   /_/  \____/_/|_/___/

    def btnDlgClicked(self, btn: QPushButton):
        txt = btn.text().strip('&')
        if txt == 'Save':
            self.trySaveInfo()
        if txt == 'Ignore':
            self.output = 'ignore'

    def btnOpenGamePath(self):
        openatfile(self.game_path)

    def btnEditGamePath(self):
        new_path_raw = QFileDialog.getExistingDirectory(
            caption="Select the game's directory",
            directory=str(FPATH_GAMES)
        )
        if new_path_raw:
            new_path = Path(new_path_raw).resolve()
            if self.game_path.exists() and not new_path.samefile(self.game_path):
                self.label_gamepath.setText(
                    str(new_path.relative_to(FPATH_GAMES)))
                self.game_path = new_path

    def btnUrlOpen(self):
        url = self.lineEdit_url.text().strip()
        if not url:
            Mbox.showinfo(title="Url Error",
                          message="No URL specified",
                          errorlevel=1)
        else:
            try:
                startfile(url)
            except Exception:
                Mbox.showinfo(title="Url Error",
                              message="Invalid URL",
                              errorlevel=1)

    def btnUrlPull(self):
        url = self.lineEdit_url.text().strip()
        if not url:
            Mbox.showinfo(title="Url Error",
                          message="No URL specified",
                          errorlevel=1)
        elif 'f95zone' in url:
            GetF95Info(pt_cats_chkBox=self.pointer_categories_chkBox,
                       pt_cats_cmbBox=self.pointer_categories_cmbBox,
                       pt_tags_chkBox=self.pointer_tags_chkBox,
                       pt_tags_cmbBox=self.pointer_tags_cmbBox,
                       pt_info=self.pointer_info,
                       pt_desc=self.textEdit_description,
                       url=url)
        elif Mbox.askquestion(title="Retrieval failed",
                              message="Only F95zone links supported. Would you like to open the link instead?") == 'Yes':
            startfile(url)

    def btnImgSearch(self):
        img_path_raw, _ = QFileDialog.getOpenFileName(
            caption=f"Select the image for '{self.game_path.stem}'",
            directory=str(FPATH_IMGS),
            filter="Images (*.png *.jpg *.gif)"
        )
        if img_path_raw:
            img_path = Path(img_path_raw)
            if img_path.is_relative_to(FPATH_IMGS):
                img_txt = str(img_path.relative_to(FPATH_IMGS))
            else:
                img_txt = str(img_path)
            self.lineEdit_image.setText(img_txt)

    def btnPathsRemRow(self):
        shown = [line for line in self.pointer_program_paths
                 if not line['pth'].isHidden()]
        if len(shown) == 2:
            self.pointer_program_paths[0]['name'].hide()
            self.btn_progpths_remove.hide()
            self.label_progpths_name.hide()
            self.btn_progpths_find.show()
        if len(shown) == 30:
            self.btn_progpths_add.show()
        old_line = self.pointer_program_paths[len(shown)-1]
        old_line['lbl'].hide()
        old_line['name'].hide()
        old_line['pth'].hide()
        self.pathsRowChange()

    def btnPathsAddRow(self) -> dict[str, U[QLabel, QLineEdit]]:
        shown = [line for line in self.pointer_program_paths
                 if not line['pth'].isHidden()]
        if len(shown) == 1:
            self.pointer_program_paths[0]['name'].show()
            self.btn_progpths_remove.show()
            self.label_progpths_name.show()
            self.btn_progpths_find.hide()
        if len(shown) == 29:
            self.btn_progpths_add.hide()
        new_line = self.pointer_program_paths[len(shown)]
        new_line['lbl'].show()
        new_line['name'].show()
        new_line['pth'].show()
        self.pathsRowChange()
        return new_line

    def btnPathsBrowse(self):
        raw_pths, _ = QFileDialog.getOpenFileNames(
            caption=f"Select executable(s) for '{self.game_path.stem}'",
            directory=str(self.game_path),
            filter=FILETYPENAMES
        )
        if raw_pths:
            paths = [Path(pth) for pth in raw_pths]
            self.addExes(paths)

    def btnPathsFind(self):
        def findExe(path: Path):
            return [pth for pth in path.iterdir() if pth.suffix in FILETYPES]

        if not self.game_path.is_dir():
            Mbox.showinfo(title='Error',
                          message=f'"{self.game_path.name}" is not a directory',
                          errorlevel=1)
            return
        paths = findExe(self.game_path)
        if not paths:
            for subdir in self.game_path.iterdir():
                if subdir.is_dir():
                    paths += findExe(subdir)
        if not paths:
            Mbox.showinfo(title='Error',
                          message="Couldn't find any executables",
                          errorlevel=1)
            return
        else:
            self.addExes(paths)

#     ______  ___  ___________
#    / __/ / / / |/ / ___/ __/
#   / _// /_/ /    / /___\ \
#  /_/  \____/_/|_/\___/___/

    def pathsRowChange(self):
        def updateScrollbar():
            vbar = self.scrollArea.verticalScrollBar()
            vbar.setValue(vbar.maximum())
        QTimer.singleShot(10, updateScrollbar)

    def addExes(self, exes: list[Path]):
        shown = [line for line in self.pointer_program_paths
                 if not line['pth'].isHidden()]
        new_line = self.pointer_program_paths[len(shown)-1]
        for raw_pth in exes:
            pth = raw_pth.relative_to(self.game_path)
            name = reSub(r'(?<=[a-z])(?=[A-Z])|_',
                         r' ',
                         pth.stem).strip()
            new_line['name'].setText(name)
            new_line['pth'].setText(str(pth))
            new_line = self.btnPathsAddRow()
        if len(exes) != 30:
            self.btnPathsRemRow()

#     _____  _____  __  ________
#    /  _/ |/ / _ \/ / / /_  __/
#   _/ //    / ___/ /_/ / / /
#  /___/_/|_/_/   \____/ /_/

    def simpleInfo(self, fol: U[str, Path], url: str = '', name: str = '', img: str = ''):
        if isinstance(fol, str):
            self.game_path = FPATH_GAMES.joinpath(fol)
        else:
            self.game_path = fol
            fol = str(fol.relative_to(FPATH_GAMES))
        self.orig_path = self.game_path
        self.label_gamepath.setText(fol)
        self.lineEdit_title.setText(name)
        self.lineEdit_url.setText(url)
        self.lineEdit_image.setText(img)
        self.dlg.exec()

    def fullInfo(self, gpath: Path, ginfo: GAMEDATA_TYPE):
        self.game_path = gpath
        self.orig_path = self.game_path
        self.label_gamepath.setText(
            str(self.game_path.relative_to(FPATH_GAMES)))
        # info
        for k, v in ginfo['Info'].items():
            if self.pointer_info.get(k):
                self.pointer_info[k].setText(str(v))
        self.textEdit_description.setPlainText(ginfo['Info']['Description'])
        # program paths
        ppths = ginfo['Info']['Program Path']
        if isinstance(ppths, Path):
            self.lineEdit_progpths_exe_01.setText(
                str(ppths.relative_to(self.game_path)))
        else:
            for i, (nm, pth) in enumerate(ppths.items()):
                line = self.pointer_program_paths[i]
                line['name'].setText(nm)
                line['pth'].setText(str(pth.relative_to(self.game_path)))
                self.btnPathsAddRow()
            self.btnPathsRemRow()
        # categories
        for k, field in self.pointer_categories_cmbBox.items():
            val = ginfo['Categories'][k]
            field.setCurrentText(val)
        for k, field in self.pointer_categories_chkBox.items():
            val = ginfo['Categories'][k]
            field.setChecked(val)
        # tags
        for k, field in self.pointer_tags_cmbBox.items():
            val = ginfo['Tags'][k]
            field.setCurrentText(val)
        for k, field in self.pointer_tags_chkBox.items():
            val = ginfo['Tags'][k]
            field.setChecked(val)
        self.dlg.exec()

#     _______ _   ______
#    / __/ _ | | / / __/
#   _\ \/ __ | |/ / _/
#  /___/_/ |_|___/___/

    def trySaveInfo(self):
        info_input = self.getInputsInfo()
        info_game_path, info_paths = self.getInputsPaths()
        categories = self.getInputsCategories()
        tags = self.getInputsTags()
        # check if data is new
        new_data = {
            'Info': (info_input | info_paths),
            'Categories': categories,
            'Tags': tags
        }
        old_data = self.game_lib.master_list.get(self.game_path)
        if not old_data:
            # game is new
            self.output = 'new'
            self.game_lib.recent_list['added'].insert(
                0, new_data['Info']['Title'])
            self.game_lib.saveRecent()
            self.checkUpdatedData(info_game_path, old_data, new_data)
        elif new_data != old_data:
            # game is updated
            self.output = 'update'
            self.checkUpdatedData(info_game_path, old_data, new_data)
        else:
            self.output = 'cancel'

    def checkUpdatedData(self, gpath: Path, old_data: O[GAMEDATA_TYPE], new_data: GAMEDATA_TYPE):
        path_is_new = (not self.game_path.samefile(gpath)
                       if self.game_path.exists() else True)
        old_ver = old_data['Info']['Version'] if old_data else ''
        new_ver = new_data['Info']['Version']
        if path_is_new or not old_data or old_ver != new_ver:
            old_title = old_data['Info']['Title'] if old_data else ''
            new_title = new_data['Info']['Title']
            # update recent lists
            old_list = 'updated' if old_data else 'added'
            cur_list = self.game_lib.recent_list[old_list].copy()
            if old_title in cur_list:
                cur_list.remove(old_title)
            if new_title in cur_list:
                cur_list.remove(new_title)
            cur_list.insert(0, new_title)
            while len(cur_list) > MAX_RECENT_GAMES:
                cur_list.pop()
            if cur_list != self.game_lib.recent_list[old_list]:
                self.game_lib.recent_list[old_list] = cur_list
                self.game_lib.saveRecent()
            # check if path has changed
            if path_is_new:
                self.game_lib.master_list.pop(self.game_path, None)
                self.game_path = gpath
        # update master list
        self.game_lib.master_list[self.game_path] = new_data
        self.game_lib.save()

    def getInputsInfo(self) -> dict[str, str]:
        data = {k: v.text().strip()
                for k, v in self.pointer_info.items()}
        if 'f95zone' in data['URL']:
            url = reSub(pattern=r'(?<=threads/).+?\.(?=\d+/$)',
                        repl='',
                        string=data['URL'])
            data['URL'] = url
        data['Image'] = self.moveResizeImage(data['Image'])
        data['Description'] = self.textEdit_description.toPlainText()
        return data

    def moveResizeImage(self, img: str) -> str:
        if not img:
            return ''
        img_path = Path(img)
        if not img_path.exists():
            img_path = FPATH_IMGS.joinpath(img_path)
        if not img_path.exists():
            return img
        # process
        new_path = FPATH_IMGS.joinpath(f'{img_path.stem}.jpg')
        run(f'magick convert "{img_path}[0]" -resize 1280x720> "{new_path}"')
        if str(img_path) != str(new_path):
            img_path.unlink()
        return str(new_path.relative_to(FPATH_IMGS))

    def getInputsPaths(self) -> tuple[Path, U[Path, dict[str, Path]]]:
        top_path = FPATH_GAMES.joinpath(self.label_gamepath.text())
        data = {line['name'].text(): top_path.joinpath(line['pth'].text())
                for line in self.pointer_program_paths
                if not line['pth'].isHidden()
                and line['pth'].text()}
        if len(data) == 1:
            data = list(data.values())[0]
        return top_path, {'Program Path': data}

    @staticmethod
    def getInputs(chkBox_pointer: dict[str, QCheckBox], cmbBox_pointer: dict[str, QComboBox]) -> dict[str, U[str, int]]:
        chkBox = {k: int(v.isChecked())
                  for k, v in chkBox_pointer.items()}
        cmbBox = {k: v.currentText()
                  for k, v in cmbBox_pointer.items()}
        data = (chkBox | cmbBox)
        return data

    def getInputsCategories(self) -> dict[str, U[str, int]]:
        return self.getInputs(self.pointer_categories_chkBox, self.pointer_categories_cmbBox)

    def getInputsTags(self) -> dict[str, U[str, int]]:
        return self.getInputs(self.pointer_tags_chkBox, self.pointer_tags_cmbBox)
