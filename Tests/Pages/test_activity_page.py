import unittest
from unittest.mock import MagicMock, patch

import tkinter as tk
from tkinter import ttk

from Data.themes import Theme
from Pages.activity import ActivityPage
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TestActivityPage(unittest.TestCase):

    def setUp(self):
        self.app = MagicMock()
        self.root = tk.Tk()
        self.app.container = tk.Frame(self.root)
        self.page = ActivityPage(self.app.container, self.app)

        self.root.withdraw()

    def tearDown(self) -> None:
        self.root.destroy()

    @patch.object(ActivityPage, "get_graph_data")
    def test_draw_summary_graph(self, mock_get_graph_data):
        mock_get_graph_data.return_value = ([1, 2, 3, 4], [60, 30, 80, 55])

        self.page.draw_summary_graph(Theme.dark)

        found = False
        for widget in self.page.frame_summary.winfo_children():
            if isinstance(widget, tk.Canvas):
                found = True 
                break

        self.assertTrue(found)

    def test_get_graph_data(self):
        self.page.sessions = [{
        "start_time": "2024-04-25 13:56:10",
        "end_time": "2024-04-25 13:56:10",
        "duration": 0,
        "good_frame_count": 0,
        "bad_frame_count": 0
        }]

        graph_data = self.page.get_graph_data()

        self.assertIsNotNone(graph_data)

    def test_delete_sessions(self):
        self.app.get_theme.return_value = Theme.dark
        self.app.session_handler.sessions = []
        self.page.delete_sessions()

        children = self.page.frame_summary.winfo_children()
        found = len(children) == 1 and isinstance(children[0], ttk.Label)

        self.assertTrue(found)