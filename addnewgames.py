from tkinter import Tk, Label, Entry, Button
from os import system as os_system
import json

from constants import *


class GetInput(Tk):
    def __init__(self):
        Tk.__init__(self)
        xpos = CENTER.x - ADD_WD / 2
        ypos = CENTER.y - ADD_HT / 2
        self.geometry('{}x{}+{:.0f}+{:.0f}'.format(ADD_WD, ADD_HT, xpos, ypos))
        self.title("Add Games")
        self.attributes('-topmost', 1)
        self.configure(padx=10, pady=10)
        self.bind_all('<Escape>', lambda e: self.destroy())
        self.bind_all('<Return>', lambda e: self.submit())
        self.columnconfigure(1, weight=1)

        with open(PATH_NEW, 'r') as f:
            self.addGameList = json.load(f)
        self.GUI()

    def GUI(self):
        self.ct = 0
        self.url = self.labelEntry("Site URL:")
        self.name = self.labelEntry("Game name:")
        self.folder = self.labelEntry("Game folder:")

        exitBtn = Button(self,
                         text="Close (Esc)",
                         command=self.destroy)
        exitBtn.place(anchor='se',
                      relx=0.4,
                      rely=0.9)

        saveBtn = Button(self,
                         text="Submit (Enter)",
                         command=self.submit)
        saveBtn.place(anchor='sw',
                      relx=0.6,
                      rely=0.9)
        self.url.focus()

    def labelEntry(self, txt):
        lbl = Label(self,
                    font=FONT_MD,
                    text=txt)
        lbl.grid(pady=10,
                 row=self.ct,
                 column=0,
                 sticky='e')
        ent = Entry(self,
                    font=FONT_MD)
        ent.grid(pady=10,
                 row=self.ct,
                 column=1,
                 sticky='ew')
        self.ct += 1
        return ent

    def submit(self):
        data = dict(name=self.name.get(),
                    url=self.url.get())
        self.addGameList.update({self.folder.get(): data})
        with open(PATH_NEW, 'w') as f:
            json.dump(self.addGameList, f, sort_keys=True, indent=4)

        os_system('nircmd stdbeep')
        self.folder.delete(0, 'end')
        self.name.delete(0, 'end')
        self.url.delete(0, 'end')
        self.url.focus()


if __name__ == "__main__":
    GetInput().mainloop()
