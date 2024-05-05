import tkinter as tk
from tkinter import ttk

from Pages.monitoring import MonitoringPage

# text-based subpage
class TextSubPage(ttk.Frame):
    def __init__(self, parent, app, title, index):
        super().__init__(parent)

        self.grid(row=1, column=0, sticky="nsew")
        self.index = index
        self.parent = parent
        self.app = app
        self.title = title

        self.button = ttk.Button(self, padding=(25,10))
        label = ttk.Label(self, text=title, style="Header.TLabel")
        label.pack(pady=(20, 20))

    # add text dynamically to the page 
    # returns an instance of the text sub page so can be called like: sub_page = TextSubPage(...).add_text(...)
    def add_text(self, lines):
        for line in lines:
            ttk.Label(self, text=line).pack()
        
        self.update_button()

        return self
    
    # applies the relevant button action for the sub page (either continue or return to monitoring)
    def update_button(self):

        if self.index != 4:
            self.button['text'] = 'Continue'
            self.button['command'] = lambda: self.parent.show_subpage(self.index + 1)
            
        else:
            self.button['text'] = 'Go to Monitoring'
            self.button['command'] = lambda: self.app.show_page(MonitoringPage)

        self.button.pack(pady=(30, 0))
