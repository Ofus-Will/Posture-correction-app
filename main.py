import tkinter as tk
from tkinter import ttk
import mediapipe as mp
import cv2
from winotify import Notification as WinNotification
from datetime import datetime

from Data.session_handler import SessionHandler
from Data.camera_handler import CameraHandler
from Data.settings_handler import SettingsHandler
from Data.data_handler import DataHandler
from Data.posture_classifier import PostureClassifier
from Data.data_handler import DataHandler
from Data.posture_classifier import PostureClassifier
from Data.themes import Theme

from Pages.settings import SettingsPage
from Pages.monitoring import MonitoringPage
from Pages.calibration import CalibrationPage
from Pages.activity import ActivityPage

from Widgets.notification import Notification
from Widgets.nav_bar import NavBar

class PostureApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("1024x600")
        self.resizable(False, False)
        self.title("Posture Correction Application")
        self.last_notification = None

        self.init_ui()
        self.init_mp()

        self.data_handler = DataHandler(self)
        self.posture_classifier = PostureClassifier(self)
        self.camera_handler = CameraHandler(self)
        self.settings_handler = SettingsHandler(self)
        self.session_handler = SessionHandler(self)

        self.current_page = "" 
        self.pages = {}
        self.camera_port = 0
        self.monitoring = False

        self.style = ttk.Style(self)

        for Class in (MonitoringPage, CalibrationPage, ActivityPage, SettingsPage):
            page = Class(self.container, self)
            self.pages[Class] = page
            page.grid(row=1, column=1, sticky="nsew") 

        self.update_theme()
        self.update_text()
        self.show_page(MonitoringPage)

    # add the container and the nav bar to the page
    def init_ui(self):
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.nav_bar = NavBar(self.container, self)
    
    def init_mp(self):
        self.cap = cv2.VideoCapture(0)
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.7, model_complexity=2)
        self.drawing_spec = mp.solutions.drawing_utils.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)
        # self.utils = mp.solutions.drawing_utils

    def get_current_page(self):
        return self.current_page

    # method for showing pages, handling custom close and show methods from each page
    def show_page(self, Page):
        if self.current_page != Page:
            
            if hasattr(self.current_page, "close"):
                self.current_page.close()

            self.current_page = self.pages[Page]

            if hasattr(self.current_page, 'show'):
                self.current_page.show()
            else:
                self.current_page.tkraise()

    # method for showing notifications
    # either custom notification widget or use a framework to send a windows notification
    def show_notification(self, text, windows=False, temporary=False, background="#d64541"):
        if windows:
            if self.last_notification is None or (datetime.now() - self.last_notification).seconds > 10:
                self.last_notification = datetime.now()
                title, msg = text.split("-")
                notification = WinNotification(app_id="Posture Correction", title=title, msg=msg, duration="short")
                notification.show()
        else:
            if hasattr(self, 'notification') and self.notification is not None: # and (self.notification.text != text):
                if text != self.notification.text:
                    self.notification.update_text(text)
            else:
                self.notification = Notification(self.container, text, self, background=background)
                self.notification.grid(row=0, column=1, sticky='ew', ipady=5)

            if temporary:
                self.after(1000, self.notification.destroy)

    # sets the current index for the VideoCapture method (cv2)
    # called when switching between cameras from the camera selector widget
    def set_camera_port(self, index):
        self.cap.release()
        self.camera_port = index
        self.cap = cv2.VideoCapture(index)

    # toggle the app's monitoring state
    # called by the monitoring page's "start monitoring" button 
    def toggle_monitoring(self):

        if not self.data_handler.check_for_data():
            return
        
        self.monitoring = not self.monitoring
        if self.monitoring == True:
            self.posture_classifier.classify_posture(True)

        elif self.session_handler.start_time is not None:
            self.session_handler.end_session()

        if isinstance(self.current_page, MonitoringPage):
            self.current_page.change_state()


    # intermediate process camera method
    # if another class tries to start the camera_handler process_camera recursive method and its already subscribed to,
    # dont call the camera handler's process camera method
    def process_camera(self, recursive = True):
        if self.camera_handler.subscribed and recursive:
            # print("debug: processer already active")
            return 
        
        self.camera_handler.process_camera(recursive)
    
    # get the theme respective to the current theme setting value
    def get_theme(self):
        return Theme.dark if self.settings_handler.get_setting("theme") == "Dark" else Theme.light
    
    # update the theme, called when the theme setting combo box is updated (another value selected)
    def update_theme(self):
        theme = self.get_theme()
        self.style.theme_use("clam")

        self.style.configure("TFrame", background=theme["background-1"])
        self.style.configure("Secondary.TFrame", background=theme["background-2"])
        self.style.configure("Secondary.TLabel", background=theme["background-2"])
        self.style.configure("TButton", background=theme["background-2"], foreground=theme["foreground"], focuscolor="none", relief="flat", padx=0, pady=0)
        self.style.configure("Header.TLabel", font=("Helvetica", 14, "bold"))
        self.style.configure("TLabel", background=theme["background-1"], foreground=theme["foreground"])
        self.style.configure("TCheckbutton", focuscolor="none")
        self.style.layout('Minimal.TButton', [('Button.label', {'sticky': 'nswe'})])
        self.style.configure("Minimal.TButton", anchor="center", background=theme["background-1"])

        self.style.map("TCheckbutton",
              background=[('active', theme["background-1"]), ("!active", theme["background-1"])],
              foreground=[('active', theme["foreground"]), ("!active", theme["foreground"])])

    # update the text size, called when the text size setting combo box is updated (another value selected)
    def update_text(self):
        curr_size = self.settings_handler.get_setting("text_size")
        text_sizes = { "Small": ("Segoe UI", 10), "Medium": ("Segoe UI", 12), "Large": ("Segoe UI", 14) }
        font = text_sizes.get(curr_size, text_sizes["Medium"])

        self.style.theme_use('clam')
        self.style.configure("TLabel", font=font)
        self.style.configure("Header.TLabel", font=(font[0], (font[1] + 4), "bold"))
        self.style.configure("TButton", font=font)
        self.style.configure("TCheckbutton", font=font)
        self.style.configure("TCombobox", font=font)

if __name__ == "__main__":
    app = PostureApp()
    app.mainloop()