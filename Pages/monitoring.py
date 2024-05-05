import tkinter as tk
from tkinter import ttk

from Widgets.camera_view import CameraView
from Widgets.camera_selector import CameraSelector

from datetime import datetime

class MonitoringPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        self.app = app

        self.init_ui()

    # add the widgets for the monitoring page
    def init_ui(self):
        header_font = ("Helvetica", 14, "bold")
        style = ttk.Style(self.app)
        style.configure('Custom.TLabel', background="white", font=header_font)

        # Header at the top
        lbl_header = ttk.Label(self, text="Monitoring", style='Header.TLabel')
        lbl_header.grid(row=0, column=0, sticky="nw", padx=20, pady=(20,10))

        # Camera view at the top left
        self.camera_view = CameraView(self, self.app, MonitoringPage)
        self.camera_view.grid(row=1, column=0, sticky="nsew", padx=20)

        # Dropdown menu for camera selection at the top right
        self.camera_selector = CameraSelector(self, self.app)
        self.camera_selector.grid(row=0, column=0, sticky="ne", padx=20, pady=(20,10))

        data_container = ttk.Frame(self)
        data_container.grid(row=1, column=1, sticky="nsew", padx=15, pady=(50, 20))
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.lbl_status = ttk.Label(data_container, text="Status: Inactive", style='Custom.TLabel')
        self.lbl_duration = ttk.Label(data_container, text="Duration: 00:00", style='Custom.TLabel')
        self.lbl_posture = ttk.Label(data_container, text="Posture: ...", style='Custom.TLabel')
        self.btn_monitor = ttk.Button(data_container, text="Start Monitoring", padding=(25, 10), command= lambda: self.app.toggle_monitoring())

        self.lbl_status.grid(row=0, column=0, padx=10, pady=5)
        self.lbl_duration.grid(row=1, column=0, padx=10, pady=5)
        self.lbl_posture.grid(row=2, column=0, padx=10, pady=5)
        self.btn_monitor.grid(row=3, column=0, padx=10, pady=10)

        data_container.grid_columnconfigure(0, weight=1)
        data_container.grid_columnconfigure(1, weight=1)

    # update the UI based off the current monitoring state
    def change_state(self):

        if self.app.monitoring == True:
            self.camera_view.lbl_image['background'] = 'light green'
            self.btn_monitor['text'] = 'End Monitoring'
        else:
            self.camera_view.lbl_image['background'] = 'red'
            self.btn_monitor['text'] = 'Start Monitoring'

            self.update_ui()

    # Called every frame (when monitoring page is open)
    # Shows the current monitoring state, duration, and posture classification
    def update_ui(self):

        if self.app.monitoring == True:
            self.lbl_status['text'] = "Status: Active"
            self.lbl_posture['text'] = f"Posture: {self.app.posture_classifier.classification}"

            duration = (datetime.now() - self.app.session_handler.start_time)
            # Get the total number of seconds
            total_seconds = int(duration.total_seconds())

            # Calculate hours, minutes, and seconds
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Format as "hh:mm:ss" if hours > 0, otherwise "mm:ss"
            if hours:
                duration_str = f"{hours}:{minutes:02}:{seconds:02}"
            else:
                duration_str = f"{minutes:02}:{seconds:02}"

            self.lbl_duration['text'] = f"Duration: {duration_str}"
        else:
            self.lbl_status['text'] = "Status: Inactive"
            self.lbl_duration['text'] = "Duration: 00:00"
            self.lbl_posture['text'] = "Posture: ..."

    # custom show method to handle updating the camera viewing and processing the feed
    def show(self):
        self.tkraise()
        self.camera_view.update_view()
        self.app.process_camera()
