import tkinter as tk
from tkinter import ttk

class Setting(ttk.Frame):
    def __init__(self, parent, app, data, index):
        super().__init__(parent) #, background="white", relief="solid", highlightbackground="grey", highlightcolor="grey", highlightthickness=1)

        self.app = app
        self.identifier = data[0]
        self.name = self.format_name(self.identifier)
        self.value = data[1]
        self.options = data[2]
        self.description = data[3]

        self.index = index

        self.init_ui()
        
    # add sub widgets to the settings frame
    def init_ui(self):
        self.grid(row=self.index, column=0, sticky="ew", padx=20, pady=(0,20))

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)

        lbl_name = ttk.Label(self, text=self.name)
        lbl_name.grid(row=0, column=0, sticky="nw")

        lbl_description = ttk.Label(self, text=self.description)
        lbl_description.grid(row=1, column=0, sticky="nw")

        self.selector = ttk.Combobox(self, values=self.options, state="readonly")
        self.selector.grid(row=0, column=1, sticky="ns")
        self.set_selector_value()

        # link combo box change event to update the settings
        self.selector.bind("<<ComboboxSelected>>", lambda event: self.update_setting())

    # set the currently selected option in the combo box to the one representing the current setting
    def set_selector_value(self):
        if self.value in self.options:
            index = self.options.index(self.value)
            self.selector.current(index)
        else:
            self.selector.current(0)

    # formatting this_naming to This Naming
    def format_name(self, name):
        words = name.split("_")
        result = " ".join(word.capitalize() for word in words)
        return result
    
    # trigger updates for specific settings (i.e., theme, text_size) that need live UI updates
    def update_setting(self):
        new_value = self.selector.get()
        if new_value != self.value:
            self.app.settings_handler.set_setting(self.identifier, new_value)

            if self.identifier == "theme": #or self.identifier == "font_size"):
                self.app.update_theme()

            elif self.identifier == "text_size":
                self.app.update_text()

            self.value = new_value