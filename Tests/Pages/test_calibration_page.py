import unittest
from unittest.mock import MagicMock, patch

import tkinter as tk

from Pages.calibration import CalibrationPage


class TestCalibrationPage(unittest.TestCase):

    def setUp(self):
        self.app = MagicMock()
        self.root = tk.Tk()
        self.app.container = tk.Frame(self.root)
        self.page = CalibrationPage(self.app.container, self.app)

    def test_show_subpage_valid(self):
        self.page.current_subpage = None 
        self.page.show_subpage(2)

        self.assertIsNotNone(self.page.current_subpage)

    def test_show_subpage_invalid(self):
        self.page.current_subpage = None 
        self.page.show_subpage(500)

        self.assertIsNone(self.page.current_subpage)
