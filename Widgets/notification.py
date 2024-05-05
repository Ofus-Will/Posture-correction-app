import tkinter as tk
from tkinter import ttk

class Notification(tk.Frame):
    def __init__(self, parent, text, app, background, *args, **kwargs):
        tk.Frame.__init__(self, parent, background=background, *args, **kwargs)

        self.text = text
        self.app = app
        self.background = background

        self.init_ui()

    # add the widgets to the notification frame
    def init_ui(self):
        font = ("Helvetica", 10, "bold")
        self.label = tk.Label(self, text=self.text, background=self.background, foreground="white", font=font)
        self.label.pack(side='left', expand=True, fill='both')

        button = tk.Button(self, text="X", background=self.background, foreground='white', 
                           cursor="hand2", relief="flat", command= lambda:self.close(), font=font, 
                           highlightthickness=0, bd=0, activeforeground="white", activebackground=self.background)
        button.pack(side='right', padx=5, ipadx=5)

    # update the text of the label (called when the notification already exists instead of creating a new one)
    def update_text(self, text):
        self.text = text 
        self.label['text'] = self.text

    # handle disposal of notification
    def close(self):
        self.destroy()
        self.app.notification = None