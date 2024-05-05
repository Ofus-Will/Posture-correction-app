import tkinter as tk
from tkinter import ttk
from typing import List, Tuple

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ActivityPage(ttk.Frame):
    def __init__(self, parent, app) -> None:
        super().__init__(parent)

        self.app = app
        self.parent = parent

        self.init_ui()

    # custom appearing logic for activity page (draw summary graph with relevant theme colour scheme)
    def show(self) -> None:
        theme = self.app.get_theme()
        self.tkraise()
        self.draw_summary_graph(theme)

    # destroy the summary graph on disappearing
    def close(self) -> None:
        for widget in self.frame_summary.winfo_children():
            widget.destroy()

    # add all the relevant UI widgets and configuration
    def init_ui(self) -> None:
        # Header at the top
        lbl_header = ttk.Label(self, text="Activity", style='Header.TLabel')
        lbl_header.grid(row=0, column=0, sticky="nw", padx=20, pady=(20, 10))

        btn_reset = ttk.Button(self, text="Reset Session Data", command=lambda: self.delete_sessions())
        btn_reset.grid(row=0, column=1, sticky="ne", padx=20, pady=(20,10))

        self.frame_summary = ttk.Frame(self, style="Secondary.TFrame")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.frame_summary.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0,20), padx=20)

    # method for drawing the summary graph showing session data
    def draw_summary_graph(self, theme):
        self.sessions = self.app.session_handler.sessions
        session_indexes = []
        good_percentage = []

        if self.sessions != []:

            session_indexes, good_percentage = self.get_graph_data()

            fig, ax = plt.subplots()
            ax.set_title("Posture Data", color=theme["foreground"])
            ax.set_xlabel("Session Index", color=theme["foreground"])
            ax.set_ylabel("Good Posture Percentage (%)", color=theme["foreground"])

            for spine in ax.spines.values():
                spine.set_color(theme["foreground"])
            ax.tick_params(axis='x', colors=theme["foreground"])
            ax.tick_params(axis='y', colors=theme["foreground"])

            ax.plot(session_indexes, good_percentage, label='Good Posture %', marker='o', linestyle='-') 
            ax.set_facecolor(theme["background-2"])
            fig.patch.set_facecolor(theme["background-2"])

            canvas = FigureCanvasTkAgg(fig, master=self.frame_summary)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH)

            plt.close(fig)
        
        else:

            ttk.Label(self.frame_summary, text="No session data found, go to monitoring!", style="Secondary.TLabel").pack(pady=20)

    # grab and format the session data in the way the graph expects it (session indexes, good posture percentage)
    def get_graph_data(self) -> Tuple[List[str], List[float]]:
        session_indexes = []
        good_percentage = []

        for index, session in enumerate(self.sessions):
            session_indexes.append(str(index))
            if session["good_frame_count"] + session["bad_frame_count"] > 0:  # Prevent division by zero
                percentage = 100 * (session["good_frame_count"] / (session["good_frame_count"] + session["bad_frame_count"]))
            else:
                percentage = 0
            good_percentage.append(percentage)

        return (session_indexes, good_percentage)

    # delete all session data
    def delete_sessions(self):
        self.app.session_handler.delete_sessions()    
        self.close()
        self.draw_summary_graph(self.app.get_theme())


        