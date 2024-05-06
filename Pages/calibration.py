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
                "What is meant by good posture:", 
                "- The top of your monitor should be roughly inline with your eyes",
                "- If using a laptop consider buying a stand, keyboard, and mouse",
                "- Make sure your hips are in the back of your chair and keep your pelvis in a neutral position",
                "- Ensure your spine is straight while remaining in a comfortable position",
                "- Keep your shoulders relaxed"
            ]),

            GoodPostureSubPage(self, app, "Good Posture", 2).add_text([
                "Here you will capture good posture data",
                "Follow the tips on the previous page",
                "",
                "Click the 'Capture good posture data'",
                "button when you're ready",
                "",
                "You can also reset all good posture data",
                "By clicking the reset button",
                "",
                "Click 'Continue' to advance to the next page"]),
            BadPostureSubPage(self, app, "Bad Posture", 3).add_text([
                "Here you will capture all the bad posture data",
                "There should ideally be multiple instances",
                "",
                "Examples include:",
                "- Slouching",
                "- Leaning to the left",
                "- Leaning to the right",
                "- Any other bad habits you know you have",
                "",
                "Click 'Continue' to advance to the next page"]),
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