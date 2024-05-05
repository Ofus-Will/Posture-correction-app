import unittest
from unittest.mock import MagicMock, patch

import tkinter as tk

from Pages.monitoring import MonitoringPage


class TestMonitoringPage(unittest.TestCase):

    def setUp(self):
        self.app = MagicMock()
        self.root = tk.Tk()
        self.app.container = tk.Frame(self.root)
        self.page = MonitoringPage(self.app.container, self.app)

    def test_update_ui_active(self):
        self.app.monitoring = True 

        self.page.update_ui()

        self.assertEqual(self.page.lbl_status["text"], "Status: Active")

    def test_update_ui_inactive(self):
        self.app.monitoring = False 

        self.page.update_ui()

        self.assertEqual(self.page.lbl_status["text"], "Status: Inactive")