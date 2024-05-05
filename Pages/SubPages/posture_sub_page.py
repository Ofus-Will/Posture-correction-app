import tkinter as tk
from tkinter import ttk

from Pages.monitoring import CameraView

from Data.data_handler import DataHandler

# main posture sub page for good and bad subpages to inherit
class PostureSubPage(ttk.Frame):
    def __init__(self, parent, app, title, index) -> None:
        super().__init__(parent)
        self.grid(row=0, column=0, sticky="nsew")

        self.parent = parent
        self.app = app
        self.index = index
        self.title = title

        self.addUI()

    # implement the UI for the base class
    def addUI(self) -> None:

        self.content_frame = ttk.Frame(self)  # Create an inner frame
        self.content_frame.pack(padx=30, pady=(20, 10), expand=True, fill='both')
        
        self.grid_columnconfigure(0, pad=50)

        self.camera_view = CameraView(self.content_frame, self.app, type(self.parent), self, width=420, height=280)
        self.camera_view.grid(row=0, column=0, padx=(0,20))

        self.btn_data = ttk.Button(self.content_frame, text="...")
        self.btn_data.grid(row=1, column=0, pady=(10,0), ipady=10, sticky="ew", padx=(0,20))

        self.btn_reset = ttk.Button(self.content_frame, text="...")
        self.btn_reset.grid(row=2, column=0, ipady=10, pady=(5,0), sticky="ew", padx=(0,20))

        btn_continue = ttk.Button(self.content_frame, text="Continue", command=lambda: self.parent.show_subpage(self.index + 1))
        btn_continue.grid(row=3, column=0, pady=5, ipady=10, sticky="ew", padx=(0,20))
        

        header = ttk.Label(self.content_frame, text=self.title, justify="left", style="Header.TLabel")
        header.grid(row=0, column=1, sticky="nw")

        self.text_holder = ttk.Frame(self.content_frame)
        self.text_holder.grid(row=0, column=1, pady=(30,10), sticky="nw")

    # add text dynamically to the page 
    # returns an instance of the posture sub page so can be called like: sub_page = PostureSubPage(...).add_text(...)
    def add_text(self, lines):
        for line in lines:
            ttk.Label(self.text_holder, text=line, justify="left").pack(anchor="w")

        return self
    
    # custom show method for the tkinter frame to handle on appearing logic
    def show(self) -> None:
        self.camera_view.break_loop = False
        self.camera_view.update_view()
        self.app.process_camera()

    # custom closing calls to stop camera_view from updating while page is not in focus
    def close(self) -> None:
        self.camera_view.break_loop = True

class GoodPostureSubPage(PostureSubPage):
    def __init__(self, parent, app, title, index) -> None:
        super().__init__(parent, app, title, index)

        self.app = app
        self.update_ui()

    # UI specific to good posture subpage 
    def update_ui(self) -> None:
        self.btn_data['text'] = "Capture good posture data"
        self.btn_data['command'] = lambda: self.app.data_handler.process_data(True, True)

        self.btn_reset['text'] = "Reset good posture data"
        self.btn_reset['command'] = lambda: self.app.data_handler.delete_data("good")


class BadPostureSubPage(PostureSubPage):
    def __init__(self, parent, app, title, index) -> None:
        super().__init__(parent, app, title, index)

        self.app = app
        self.update_ui()

    # UI specific to bad posture subpage
    def update_ui(self) -> None:
        self.btn_data['text'] = "Capture bad posture data"
        self.btn_data['command'] = lambda: self.app.data_handler.process_data(True, False)

        self.btn_reset['text'] = "Reset bad posture data"
        self.btn_reset['command'] = lambda: self.app.data_handler.delete_data("bad")

