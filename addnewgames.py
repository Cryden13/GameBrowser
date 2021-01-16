import json
from tkinter import Tk, Label, Entry, Button, messagebox as mbox
from os import path as os_path
from constants import FONT_MD, PATH_NEW, NEW_DATA


class GetInput(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.configure(padx=10, pady=10)
        self.geometry('500x200+500+500')
        self.title("Add a game")
        self.attributes('-topmost', 1)
        self.columnconfigure(1, weight=1)
        self.bind_all('<Escape>', lambda e: self.destroy())
        self.bind_all('<Return>', lambda e: self.submit())

        self.GUI()

    def GUI(self):
        self.folder = self.labelEntry("Game folder:", 0)
        self.folder.focus()
        self.name = self.labelEntry("Game name:", 1)
        self.url = self.labelEntry("Site URL:", 2)

        Button(self, text="Close (Esc)", command=self.destroy).place(
            anchor='se', relx=0.4, rely=0.9)
        Button(self, text="Submit (Enter)", command=self.submit).place(
            anchor='sw', relx=0.6, rely=0.9)

    def labelEntry(self, txt, row):
        lbl = Label(self, font=FONT_MD, text=txt)
        lbl.grid(pady=10, row=row, column=0, sticky='e')
        ent = Entry(self, font=FONT_MD)
        ent.grid(pady=10, row=row, column=1, sticky='ew')
        return ent

    def submit(self):
        NEW_DATA.update(
            {self.folder.get(): {'name': self.name.get(), 'url': self.url.get()}})
        with open(PATH_NEW, 'w') as f:
            json.dump(NEW_DATA, f, sort_keys=True, indent=4)

        mbox.showinfo("Success", "Game was added successfully")
        self.folder.delete(0, 'end')
        self.name.delete(0, 'end')
        self.url.delete(0, 'end')
        self.folder.focus()


if __name__ == "__main__":
    GetInput().mainloop()
