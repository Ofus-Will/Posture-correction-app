from tkinter import ttk
from Widgets.setting import Setting

class SettingsPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        self.app = app

        self.grid_columnconfigure(0, weight=1)
        self.init_ui()

    # add the relevant settings widgets to the UI
    def init_ui(self):

        # Header at the top
        lbl_header = ttk.Label(self, text="Settings", style='Header.TLabel')
        lbl_header.grid(row=0, column=0, sticky="nw", padx=20, pady=(20,10))

        index = 1
        for setting_data in self.app.settings_handler.get_settings():
            Setting(self, self.app, setting_data, index)
            index += 1