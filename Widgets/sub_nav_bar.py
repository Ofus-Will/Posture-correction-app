import tkinter as tk
from tkinter import ttk

from Data.themes import Theme

class NavBar(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent, bd=0, relief="flat", background="green")
        self.grid(row=0, column=0, sticky="nsew", padx=15, pady=0)
        parent.grid_columnconfigure(0, weight=1)

        self.page = parent

        # add nav bar items to the parent widget
        self.nav_bar_items = {
            NavBarItem(self, "Intro", 0, parent.show_subpage),
            NavBarItem(self, "Tips", 1, parent.show_subpage),
            NavBarItem(self, "Good Posture", 2, parent.show_subpage),
            NavBarItem(self, "Bad Posture", 3, parent.show_subpage),
            NavBarItem(self, "Finished", 4, parent.show_subpage) 
        }

        self.update()

    # make sure the current nav bar item is correctly underlined
    def update(self):
        for nav_item in self.nav_bar_items:
            nav_item.update()

class NavBarItem(tk.Frame):
    def __init__(self, parent, title, index, command):
        super().__init__(parent)

        self.title = title
        self.parent = parent
        self.index = index
        self.command = command

        self.init_ui()

    # add buttons to widget which the user can press to switch pages
    def init_ui(self):
        btn_item = ttk.Button(self, text=self.title, style='Minimal.TButton', cursor="hand2", command= lambda:self.command(self.index))
        btn_item.pack(fill="both", expand=True, pady=(0, 2), ipady=10)

        self.grid(row=0, column=self.index, sticky="nsew")
        self.parent.grid_columnconfigure(self.index, weight=1)

    # underline for active sub page, background colour for inactive sub pages
    def update(self):
        if self.parent.page.current_subpage.title == self.title:
            self['background'] = "#2D78DB"
        else:  
            self["background"] = Theme.light["background-1"]