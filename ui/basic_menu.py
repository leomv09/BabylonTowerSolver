__author__ = 'BTCR'
from Tkinter import *


class AppUI(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master, relief=SUNKEN, bd=2)
        master.title("Babylon Tower")
        self.menu_bar = Menu(self)
        self.load_menu_bar()
        change_pageb = Button(self, text="ChangePage", compound=BOTTOM, command=self.change_pagef)
        change_pageb.pack()
        return_pageb = Button(self, text="Main", compound=BOTTOM, command=self.return_main_page)
        return_pageb.pack()
        self.main_page = Canvas(self, bg="red", width=700, height=400, bd=0, highlightthickness=0)
        self.main_page.pack()

        self.page2 = Canvas(self, bg="green", width=700, height=400, bd=0, highlightthickness=0)


    def change_pagef(self):
        self.main_page.pack_forget()
        self.page2.pack()

    def return_main_page(self):
        self.page2.pack_forget()
        self.main_page.pack()


    def load_menu_bar(self):
        menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=menu)
        menu.add_command(label="Save")
        menu.add_command(label="Load")
        menu.add_command(label="Reset")

        menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Theme", menu=menu)

        menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="About", menu=menu)

        self.master.config(menu=self.menu_bar)








def main():
    root = Tk()
    app = AppUI(root)
    app.pack()
    root.mainloop()


if __name__ == '__main__':
    main()

