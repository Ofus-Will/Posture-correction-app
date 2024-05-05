import tkinter as tk
from tkinter import ttk

import json 
import os
from pathlib import Path

class SettingsHandler():

    def __init__(self, app, file_path:str="settings.json", values:dict=None) -> None:
        self.file_path = Path(os.getenv("LOCALAPPDATA")) / "Posture Correction" / file_path
        self.app = app

        # all the settings, their possible values and their descriptions
        self.meta_settings = {
            "theme": {
                "default": "Light", 
                "options": ["Light", "Dark"],
                "description": "Change the colour theme of the app!"
            },
            "alert_mode": {
                "default": "Notification",
                "options": ["Notification", "None"],
                "description": "Set your desired posture alert method!"
            },
            "text_size": {
                "default": "Medium",
                "options": ["Small", "Medium", "Large"],
                "description": "Update the size of the app's text!"
            }
        }

        if values != None:
            self.settings = values
        else:
            self.settings = {key: meta["default"] for key, meta in self.meta_settings.items()}

            self.load_settings()

    # load all settings from file
    def load_settings(self) -> None:
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                self.settings = json.load(file)
        else:
            self.save_settings()

    # save all settings to file
    def save_settings(self) -> None:
        with open(self.file_path, "w") as file:
            json.dump(self.settings, file, indent=4)

    # get a setting by a key
    def get_setting(self, key) -> dict[str, str]:
        return self.settings.get(key, None)
    
    # set the value of a setting and save it to file
    def set_setting(self, key, value) -> None:
        self.settings[key] = value 
        self.save_settings()

    # reset all settings to their default value
    def reset_defaults(self) -> None:
        for key in list(self.settings.keys()):
            self.settings[key] = self.meta_settings[key]["default"]
        self.save_settings()

    # get all settings in an exportable format
    def get_settings(self) -> None:
        # return self.settings.items()
        return [(key, self.settings.get(key), meta["options"], meta["description"]) for key, meta in self.meta_settings.items()]
    
