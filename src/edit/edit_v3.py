from commandline import openatfile
from typing import TYPE_CHECKING
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from re import sub as reSub
from subprocess import run
from os import startfile
from PyQt5.QtWidgets import (
    QDialogButtonBox,
    QFileDialog,
    QPushButton,
    QVBoxLayout,
    QCheckBox,
    QComboBox,
    QLineEdit,
    QDialog,
    QWidget
)

from .ui_edit import Ui_EditDialog
from .ui_progpath import Ui_ProgramPath
from ..searchBoxes import SearchBoxes
from .getinfo import GetF95Info
from ..constants import *
from ..messageBox import (
    Messagebox as Mbox,
    SelectDialog
)

if TYPE_CHECKING:
    from ..gamelibrary_v3 import (
        Game as GameClass,
        GameLibrary
    )


class _EditDialog(QDialog):
    _block_close: bool

    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self._block_close = False

    def closeEvent(self, evnt):
        if self._block_close:
            self._block_close = False
            evnt.ignore()
        else:
            QDialog.closeEvent(self, evnt)


class _ProgLineItem(Ui_ProgramPath):
    wgt: QWidget
    parent_layout: QVBoxLayout
    pointers: list

    def __init__(self, parent_layout: QVBoxLayout, pointers: list, index=-1):
        self.wgt = QWidget()
        self.setupUi(self.wgt)

        self.parent_layout = parent_layout
        self.pointers = pointers

        self.btn_add.clicked.connect(self.addRowBefore)
        self.btn_rem.clicked.connect(self.remRow)

        self.parent_layout.insertWidget(index, self.wgt)

    def remRow(self):
        self.parent_layout.removeWidget(self.wgt)
        self.pointers.remove(self)
        self.wgt.deleteLater()

    def addRowBefore(self):
        i = self.pointers.index(self)
        li = _ProgLineItem(self.parent_layout, self.pointers, i)
        self.pointers.insert(i, li)


class EditUI(Ui_EditDialog):
    dlg: _EditDialog
    show_ignore: bool
    # cancel, update, new, or ignore
    output: str = 'cancel'
    game_lib: "GameLibrary"
    pointer_info: dict[str, QLineEdit]
    pointer_program_paths: list[_ProgLineItem]
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
        self.dlg = _EditDialog(self.game_lib.main_win)
        self.dlg.setWindowIcon(QIcon(PATH_ICON))
        self.setupUi(self.dlg)
        self.initVars()
        self.initButtons()

    def initVars(self):
        self.pointer_info = {
            'Title': self.lineEdit_title,
            'URL': self.lineEdit_url,
            'Image': self.lineEdit_image,
            'Version': self.lineEdit_version
        }
        self.pointer_program_paths = list()
        self.btnPathsAddRow()
        ctg_srch = SearchBoxes(self.gBox_categories,
                               self.gLayout_categories,
                               len(CAT_SEL)+len(CAT_TOG))
        tag_srch = SearchBoxes(self.gBox_tags,
                               self.gLayout_tags,
                               len(TAG_SEL)+len(TAG_TOG))
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
        self.btn_progpths_browse.clicked.connect(self.btnPathsBrowse)
        self.btn_progpths_find.clicked.connect(self.btnPathsFind)
        self.btn_progpths_add.clicked.connect(self.btnPathsAddRow)
        self.buttonBox.clicked.connect(lambda b: self.btnDlgClicked(b))

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
        self.dlg.close()

    def btnOpenGamePath(self):
        openatfile(self.game_path)

    def btnEditGamePath(self):
        new_path_raw = QFileDialog.getExistingDirectory(
            caption="Select the game's directory",
            directory=str(FPATH_GAMES)
        )
        if new_path_raw:
            new_path = Path(new_path_raw)
            if not self.game_path.exists() or not new_path.samefile(self.game_path):
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
        elif Mbox.askquestion(title="Retrieval Failed",
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

    def btnPathsAddRow(self) -> _ProgLineItem:
        def updateScrollbar():
            vbar = self.scrollArea.verticalScrollBar()
            vbar.setValue(vbar.maximum())
        li = _ProgLineItem(self.vLayout_progpths_scrollArea_items,
                           self.pointer_program_paths)
        self.pointer_program_paths.append(li)
        QTimer.singleShot(10, updateScrollbar)
        return li

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
            if self.game_path.suffix in FILETYPES:
                paths = [self.game_path]
                self.addExes(paths)
                return
            else:
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
        elif len(paths) == 1:
            self.addExes(paths)
        else:
            fields = [str(pth.relative_to(self.game_path)) for pth in paths]
            res = SelectDialog(parent=self.dlg,
                               title='Pick executables',
                               fields=fields).ans
            if res:
                paths = [self.game_path.joinpath(pth)
                         for pth in res]
                self.addExes(paths)

#     ______  ___  ___________
#    / __/ / / / |/ / ___/ __/
#   / _// /_/ /    / /___\ \
#  /_/  \____/_/|_/\___/___/

    def addExes(self, exes: list[Path]):
        if len(self.pointer_program_paths):
            new_line = self.pointer_program_paths[-1]
        else:
            new_line = self.btnPathsAddRow()
        for raw_pth in exes:
            pth = raw_pth.relative_to(self.game_path)
            new_line.lineEdit_exe.setText(str(pth))
            name = reSub(r'(?<=[a-z])(?=[A-Z])|_',
                         r' ',
                         pth.stem).strip()
            new_line.lineEdit_name.setText(name)
            new_line = self.btnPathsAddRow()
        self.pointer_program_paths[-1].remRow()

    def askMissingInfo(self, missing_pts: list[str]):
        ans = Mbox.askquestion(title='Missing input',
                               message=f'The following fields are blank:\n{",".join(missing_pts)}\nWould you like to continue anyway?')
        if ans == 'No':
            self.dlg._block_close = True
            return True
        else:
            return False

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

    def fullInfo(self, ginfo: "GameClass"):
        self.game_path = ginfo.Dir
        self.orig_path = self.game_path
        self.label_gamepath.setText(
            str(self.game_path.relative_to(FPATH_GAMES)))
        # info
        for k, v in ginfo.Info.__dict__.items():
            if self.pointer_info.get(k):
                self.pointer_info[k].setText(str(v))
        self.textEdit_description.setPlainText(ginfo.Info.Description)
        # program paths
        ppths = ginfo.Info.Program_Path
        if isinstance(ppths, Path):
            self.pointer_program_paths[0].lineEdit_exe.setText(
                str(ppths.relative_to(self.game_path)))
        else:
            for nm, pth in ppths.items():
                line = self.btnPathsAddRow()
                line.lineEdit_name.setText(nm)
                line.lineEdit_exe.setText(str(pth.relative_to(self.game_path)))
            QTimer.singleShot(10, self.pointer_program_paths[0].remRow)
        # categories
        for k, field in self.pointer_categories_cmbBox.items():
            val = ginfo.Categories.__dict__.get(k)
            field.setCurrentText(val)
        for k, field in self.pointer_categories_chkBox.items():
            val = ginfo.Categories.__dict__.get(k)
            field.setChecked(val)
        # tags
        for k, field in self.pointer_tags_cmbBox.items():
            val = ginfo.Tags.__dict__.get(k)
            field.setCurrentText(val)
        for k, field in self.pointer_tags_chkBox.items():
            val = ginfo.Tags.__dict__.get(k)
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
        if None in (info_input, info_game_path, info_paths, categories, tags):
            return
        new_data = {
            'Dir': info_game_path,
            'Info': (info_input | info_paths),
            'Categories': categories,
            'Tags': tags
        }
        new_game = GameClass._fromJson(**new_data)
        # check if data is new
        old_game = self.game_lib.getGameFromPath(self.orig_path)
        if not old_game:
            # game is new
            self.output = 'new'
            self.game_lib.recent_list['added'].insert(
                0, new_data['Info']['Title'])
            self.game_lib.saveRecent()
            self.checkUpdatedData(info_game_path, old_game, new_data)
        elif new_data != old_game._toDict():
            if new_data['Info']['Version'] != old_game.Info.Version:
                # game is updated
                self.output = 'update'
            else:
                # game is changed
                self.output = 'change'
            self.checkUpdatedData(info_game_path, old_game, new_data)
        else:
            self.output = 'cancel'

    def checkUpdatedData(self, gpath: Path, old_game: O[GameClass], new_data: GAMEDATA_TYPE):
        path_is_new = (not self.game_path.samefile(gpath)
                       if self.game_path.exists() else True)

    def getInputsInfo(self) -> dict[str, str]:
        def moveResizeImage(img: str) -> str:
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
        data = {k: v.text().strip()
                for k, v in self.pointer_info.items()}
        if 'f95zone' in data['URL']:
            url = reSub(pattern=r'(?<=threads/).+?\.(?=\d+/$)',
                        repl='',
                        string=data['URL'])
            data['URL'] = url
        data['Image'] = moveResizeImage(data['Image'])
        data['Description'] = self.textEdit_description.toPlainText()
        missing_pts = [k for k, v in data.items() if k != 'Image' and not v]
        if missing_pts:
            stop = self.askMissingInfo(missing_pts)
            if stop:
                return None
        return data

    def getInputsPaths(self) -> tuple[Path, U[Path, dict[str, Path]]]:
        top_path = FPATH_GAMES.joinpath(self.label_gamepath.text())
        data = {line.lineEdit_name.text(): top_path.joinpath(line.lineEdit_exe.text())
                for line in self.pointer_program_paths
                if line.lineEdit_exe.text()}
        if len(data) == 1:
            data = list(data.values())[0]
            if not data:
                stop = self.askMissingInfo(['Program Path(s)'])
                if stop:
                    return None, None
        return top_path, {'Program_Path': data}

    def getInputs(self, chkBox_pointer: dict[str, QCheckBox], cmbBox_pointer: dict[str, QComboBox]) -> dict[str, U[str, int]]:
        chkBox = {k: int(v.isChecked())
                  for k, v in chkBox_pointer.items()}
        cmbBox = {k: v.currentText()
                  for k, v in cmbBox_pointer.items()}
        missing_pts = [k for k, v in cmbBox.items() if not v]
        if missing_pts:
            stop = self.askMissingInfo(missing_pts)
            if stop:
                return None
        data = (chkBox | cmbBox)
        return data

    def getInputsCategories(self) -> dict[str, U[str, int]]:
        return self.getInputs(self.pointer_categories_chkBox, self.pointer_categories_cmbBox)

    def getInputsTags(self) -> dict[str, U[str, int]]:
        return self.getInputs(self.pointer_tags_chkBox, self.pointer_tags_cmbBox)
