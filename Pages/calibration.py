import tkinter as tk
from tkinter import ttk

from Pages.monitoring import MonitoringPage
from Pages.SubPages.text_sub_page import TextSubPage

from Pages.SubPages.posture_sub_page import GoodPostureSubPage, BadPostureSubPage, PostureSubPage

from Widgets.sub_nav_bar import NavBar

class CalibrationPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        # initiate all the sub pages for the calibration page
        self.sub_pages = [
            TextSubPage(self, app, "Intro", 0).add_text([
                "This is the calibration page! Here you",
                 "will allow us to figure out what good posture looks like on you",
                 "and in your environment."
            ]),
            TextSubPage(self, app, "Tips", 1).add_text([
                "It is important you know what is meant by good posture", 
                "Make sure the top of your computer screen is your eye level",
                "If using a laptop, a stand and separate keyboard and mouse will help a lot",
                "Sit with your hips in the back of your chair and keep your pelvis neutral to avoid rounding of the spine",
                "Keep your shoulders relaxed and done and make sure you are comfortable"
            ]),

            GoodPostureSubPage(self, app, "Good Posture", 2).add_text(["This is longer test text", "On to a second line that is longer", "And short"]),
            BadPostureSubPage(self, app, "Bad Posture", 3).add_text(["This is longer test text", "On to a second line that is longer", "And short"]),
            TextSubPage(self, app, "Finished", 4).add_text([
                "You're all set! You are now ready", 
                "To start monitoring your posture."
            ])
        ]

        for page in self.sub_pages:
            page.grid(row=1, column=0)

        self.sub_pages[0].tkraise()
        self.current_subpage = self.sub_pages[0]

        self.nav_bar = NavBar(self, app)

        self.grid_rowconfigure(1, weight=1)

        self.app = app

    # method for switching between sub pages
    def show_subpage(self, index):
        if len(self.sub_pages) >= index + 1:
            page = self.sub_pages[index]
            self.current_subpage = page
            page.tkraise()

            self.nav_bar.update()

            if hasattr(page, "show"):
                page.show()

    # custom appearing logic to handle showing first sub page as well
    def show(self):
        self.show_subpage(0)
        self.tkraise()

    # get the current subpage
    def get_subpage(self):
        return self.current_subpage