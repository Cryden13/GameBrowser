from tkinter.simpledialog import Dialog
from shutil import move as move_file
from winnotify import PlaySound

from tkinter import (
    StringVar,
    Frame,
    Tk
)
from tkinter.ttk import (
    Button,
    Label,
    Entry,
    Style
)

try:
    from ..constants import *
    from ..editlist import *
except ImportError:
    from subprocess import run
    from pathlib import Path
    pth = Path(__file__).parents[2]
    run(['py', '-m', pth.name, 'add', 'console'], cwd=pth.parent)
    raise SystemExit

if TYPE_CHECKING:
    from ..gamelibrary import GameLib


class AddDialog(Dialog):
    parent: Tk
    gamelib: "GameLib"
    updated: bool
    bodyfrm: Frame
    ct: int
    url: StringVar
    wgt: Entry
    name: StringVar
    folder: StringVar
    image: StringVar

    def __init__(self, parent: Tk, gamelib: "GameLib"):
        self.parent = parent
        self.gamelib = gamelib
        self.updated = False
        Dialog.__init__(self,
                        parent=self.parent,
                        title="Add Games")

    def body(self, master: Frame) -> Entry:
        self.bind_class('addgame_class', '<Escape>', lambda _: self.destroy())
        self.bind_class('addgame_class', '<Return>', self.more)
        Style().configure('.', font=FONT_DEF)
        self.option_add('*font', FONT_DEF)
        self.option_add('*TEntry.font', FONT_MD)
        self.option_add('*TCombobox.font', FONT_MD)
        self.configure(padx=(PAD * 4),
                       pady=(PAD * 3))

        master.pack(ipady=PAD)
        master.columnconfigure(1, weight=1)
        self.bodyfrm = master

        self.ct = 0
        self.url, self.wgt = self.labelEntry("Site URL:")
        self.name, _ = self.labelEntry("Game name:")
        self.folder, _ = self.labelEntry("Game folder:")
        self.image, _ = self.labelEntry("Image name (opt):")
        return self.wgt

    def buttonbox(self) -> None:
        btnfrm = Frame(master=self)
        btnfrm.pack()
        kw = dict(row=0,
                  padx=PAD)
        # close btn
        exitBtn = Button(master=btnfrm,
                         text="Close (Esc)",
                         command=self.destroy)
        exitBtn.grid(column=0,
                     **kw)
        # save btn
        saveBtn = Button(master=btnfrm,
                         text="Save for Later",
                         command=self.save)
        saveBtn.grid(column=1,
                     **kw)
        # add info btn
        moreBtn = Button(master=btnfrm,
                         text="Add Info (Enter)",
                         command=self.more)
        moreBtn.grid(column=2,
                     **kw)
        self.retag()
        self.update_idletasks()
        win_x = CENTER_X - self.winfo_width() // 2
        win_y = CENTER_Y - self.winfo_height() // 2
        self.after_idle(self.geometry, f'+{win_x}+{win_y}')

    def labelEntry(self, txt: str) -> tuple[StringVar, Entry]:
        lbl = Label(master=self.bodyfrm,
                    text=txt)
        lbl.grid(column=0,
                 row=self.ct,
                 pady=PAD,
                 sticky='e')
        var = StringVar(self)
        ent = Entry(master=self.bodyfrm,
                    width=50,
                    textvariable=var)
        ent.grid(column=1,
                 row=self.ct,
                 pady=PAD,
                 sticky='ew')
        self.ct += 1
        return (var, ent)

    def retag(self) -> None:
        c = [self]
        [c.extend(w.winfo_children()) for w in c]
        [w.bindtags(('addgame_class',) + w.bindtags()) for w in c]

    def getInfo(self) -> bool:
        cont = self.getImage()
        data = dict(name=self.name.get(),
                    url=self.url.get(),
                    image=self.image.get())
        fol = Path(self.folder.get()).resolve()
        if fol.exists():
            self.gamelib.newlist[fol] = data
            return cont
        else:
            Mbox.showerror(title="Error",
                           message=f'The folder "{fol.name}" does not exist!')
            return False

    def getImage(self) -> bool:
        def findImg(pth: Path) -> O[Path]:
            image = pth.joinpath(imgstr)
            if not image.suffix:
                for i in pth.iterdir():
                    if i.stem == image.stem:
                        return i
            else:
                return image if image.exists() else None

        imgstr = self.image.get()
        if not imgstr:
            return True
        img = findImg(PATH_IMGS)
        if not img:
            img = findImg(Path.home().joinpath('desktop'))
            if img:
                img = Path(move_file(img, PATH_IMGS.joinpath(img.name)))
            else:
                Mbox.showerror(title='Image Path Error',
                               message=f'The image "{img}" could not be found')
                return False
        if img.suffix != ".jpg" and (img.stat().st_size > (1000**2) or img.suffix == '.gif'):
            new = img.with_suffix(".jpg")
            run(f'magick "{img}[0]" "{new}"')
            img.unlink()
            self.image.set(new.name)
        else:
            self.image.set(img.name)
        return True

    def clearInfo(self) -> None:
        self.image.set('')
        self.folder.set('')
        self.name.set('')
        self.url.set('')
        self.wgt.focus()
        PlaySound('Beep')
        self.updated = True

    def more(self) -> None:
        if not self.getInfo():
            return
        res = EditGames(parent=self,
                        gamelib=self.gamelib,
                        allGames=[Path(self.folder.get()).resolve()],
                        adding=True)
        if res:
            self.clearInfo()
        else:
            self.save()

    def save(self) -> None:
        if not self.getInfo():
            return
        self.gamelib.saveNew()
        self.clearInfo()


class AddGUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.withdraw()

    def start_main(self, gamelib: "GameLib") -> None:
        AddDialog(self, gamelib)
        self.destroy()
