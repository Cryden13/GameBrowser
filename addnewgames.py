from tkinter.ttk import Label, Entry, Button
from os import chdir, system as os_system, path as os_path
from tkinter import Tk

from gamelibrary import GameLib
from editlist import EditGames
from constants import *


class GUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry(f'{ADD_WD}'
                      f'x{ADD_HT}'
                      f'+{CENTER.x - EDIT_WD / 2:.0f}'
                      f'+{CENTER.y - EDIT_HT / 2:.0f}')
        self.title("Add Games")
        self.configure(padx=10, pady=10)
        self.bind_all('<Escape>', lambda _: self.destroy())
        self.bind_all('<Return>', lambda _: self.more())
        self.columnconfigure(1, weight=1)

    def start_main(self, gamelib: GameLib) -> None:
        self.gamelib = gamelib
        self.ct = int()
        self.url = self.labelEntry("Site URL:")
        self.name = self.labelEntry("Game name:")
        self.folder = self.labelEntry("Game folder:")

        exitBtn = Button(self,
                         text="Close (Esc)",
                         command=self.destroy)
        exitBtn.place(anchor='se',
                      relx=0.25,
                      rely=0.95)
        saveBtn = Button(self,
                         text="Save for Later",
                         command=self.save)
        saveBtn.place(anchor='s',
                      relx=0.5,
                      rely=0.95)
        moreBtn = Button(master=self,
                         text="Add More (Enter)",
                         command=self.more)
        moreBtn.place(anchor='sw',
                      relx=0.75,
                      rely=0.95)
        self.url.focus()

    def labelEntry(self, txt: str) -> Entry:
        lbl = Label(self,
                    font=FONT_MD,
                    text=txt)
        lbl.grid(column=0,
                 row=self.ct,
                 pady=10,
                 sticky='e')
        ent = Entry(self,
                    font=FONT_MD)
        ent.grid(column=1,
                 row=self.ct,
                 pady=10,
                 sticky='ew')
        self.ct += 1
        return ent

    def getInfo(self) -> bool:
        data = dict(name=self.name.get(),
                    url=self.url.get())
        fol = self.folder.get()
        if os_path.exists(fol):
            self.gamelib.newList[fol] = data
            return False
        else:
            Mbox.showerror(title="Error",
                           message=f"The folder '{fol}' does not exist!")
            return True

    def clearInfo(self) -> None:
        self.folder.delete(0, 'end')
        self.name.delete(0, 'end')
        self.url.delete(0, 'end')
        self.url.focus()
        os_system('nircmd stdbeep')

    def more(self) -> None:
        if self.getInfo():
            return
        EditGames(parent=self,
                  gamelib=self.gamelib,
                  allGames=[self.folder.get()],
                  adding=True)
        self.clearInfo()

    def save(self) -> None:
        if self.getInfo():
            return
        self.gamelib.saveNew()
        self.clearInfo()


if __name__ == "__main__":
    chdir(PATH_GAMES)
    root = GUI()
    lib = GameLib(root)
    root.start_main(lib)
    root.mainloop()
