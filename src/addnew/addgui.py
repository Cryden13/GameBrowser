from tkinter.ttk import Label, Entry, Button, Style
from subprocess import Popen
from tkinter import Tk

try:
    from ..editlist import *
    from ..constants import *
except ImportError:
    from pathlib import Path
    pth = Path(__file__).parents[2]
    Popen(['py', '-m', pth.name, 'add', 'console'], cwd=pth.parent).wait()
    raise SystemExit

if TYPE_CHECKING:
    from ..gamelibrary import GameLib


class AddGUI(Tk):
    gamelib: "GameLib"
    ct: int
    url: Entry
    name: Entry
    folder: Entry

    def __init__(self):
        Tk.__init__(self)
        self.geometry(f'{ADD_WD}'
                      f'x{ADD_HT}'
                      f'+{CENTER_X - ADD_WD // 2}'
                      f'+{CENTER_Y - ADD_HT // 2}')
        self.title("Add Games")
        self.attributes('-topmost', True)
        self.configure(padx=10, pady=10)
        self.bind_class('addgame_class', '<Escape>', lambda _: self.destroy())
        self.bind_class('addgame_class', '<Return>', lambda _: self.more())
        self.columnconfigure(1, weight=1)
        Style().configure('.', font=FONT_DEF)
        self.option_add('*font', FONT_DEF)
        self.option_add('*TEntry.font', FONT_MD)
        self.option_add('*TCombobox.font', FONT_MD)
        self.update_idletasks()

    def start_main(self, gamelib: "GameLib") -> None:
        self.gamelib = gamelib
        self.ct = int()
        self.url = self.labelEntry("Site URL:")
        self.name = self.labelEntry("Game name:")
        self.folder = self.labelEntry("Game folder:")

        exitBtn = Button(master=self,
                         text="Close (Esc)",
                         command=self.destroy)
        exitBtn.place(anchor='se',
                      relx=0.25,
                      rely=0.95)
        saveBtn = Button(master=self,
                         text="Save for Later",
                         command=self.save)
        saveBtn.place(anchor='s',
                      relx=0.5,
                      rely=0.95)
        moreBtn = Button(master=self,
                         text="Add Info (Enter)",
                         command=self.more)
        moreBtn.place(anchor='sw',
                      relx=0.75,
                      rely=0.95)
        self.retag()
        self.url.focus()

    def labelEntry(self, txt: str) -> Entry:
        lbl = Label(self,
                    text=txt)
        lbl.grid(column=0,
                 row=self.ct,
                 pady=10,
                 sticky='e')
        ent = Entry(self)
        ent.grid(column=1,
                 row=self.ct,
                 pady=10,
                 sticky='ew')
        self.ct += 1
        return ent

    def retag(self) -> None:
        c = [self]
        [c.extend(w.winfo_children()) for w in c]
        [w.bindtags(('addgame_class',) + w.bindtags()) for w in c]

    def getInfo(self) -> bool:
        data = dict(name=self.name.get(),
                    url=self.url.get())
        fol = Path(self.folder.get()).resolve()
        if fol.exists():
            self.gamelib.newlist[fol] = data
            return False
        else:
            Mbox.showerror(title="Error",
                           message=f"The folder '{fol.name}' does not exist!")
            return True

    def clearInfo(self) -> None:
        self.folder.delete(0, 'end')
        self.name.delete(0, 'end')
        self.url.delete(0, 'end')
        self.url.focus()
        Popen(['powershell',
               '-command',
               '[system.media.systemsounds]::Beep.play()'])

    def more(self) -> None:
        if self.getInfo():
            return
        res = EditGames(parent=self,
                        gamelib=self.gamelib,
                        allGames=[Path(self.folder.get()).resolve()],
                        adding=True)
        if not res:
            self.save()
        self.clearInfo()

    def save(self) -> None:
        if self.getInfo():
            return
        self.gamelib.saveNew()
        self.clearInfo()
