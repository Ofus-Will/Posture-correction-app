# import tkinter as tk
from tkinter import ttk

from Pages.monitoring import MonitoringPage
from Pages.calibration import CalibrationPage
from Pages.activity import ActivityPage
from Pages.settings import SettingsPage

class NavBar(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, style="Secondary.TFrame")
        self.grid(row=0, column=0, rowspan=2, sticky="ns")

        self.app = app 

        self.init_ui()

    # add widgets to nav bar frame
    def init_ui(self):
        btn_monitoring = ttk.Button(self, text="Monitoring", command=lambda: self.app.show_page(MonitoringPage))
        btn_calibration = ttk.Button(self, text="Calibration", command=lambda: self.app.show_page(CalibrationPage))
        btn_progress = ttk.Button(self, text="Activity", command=lambda: self.app.show_page(ActivityPage))
        btn_settings = ttk.Button(self, text="Settings", command=lambda: self.app.show_page(SettingsPage))

        btn_monitoring.pack(side="top", fill="x", pady=(60,4), padx=10, ipadx=4, ipady=4)
        btn_calibration.pack(side="top", fill="x", pady=4, padx=10, ipadx=4, ipady=4)
        btn_progress.pack(side="top", fill="x", pady=4, padx=10, ipadx=4, ipady=4)
        btn_settings.pack(side="bottom", fill="x", pady=10, padx=10, ipadx=4, ipady=4)

