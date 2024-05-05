import unittest
from unittest.mock import MagicMock, patch

import cv2
from Pages.SubPages.posture_sub_page import GoodPostureSubPage
from Pages.SubPages.text_sub_page import TextSubPage
from Pages.calibration import CalibrationPage
from Pages.monitoring import MonitoringPage
from Widgets.camera_view import CameraView
import tkinter as tk

class TestCameraView(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = MagicMock()
        self.app.get_current_page.return_value = MonitoringPage
        self.camera_view = CameraView(self.root, self.app, MonitoringPage)
        self.camera_view.lbl_image = MagicMock()
        self.app.camera_handler.shared_frame = cv2.imread('Tests/test_image.jpg')

        self.root.withdraw()

    def test_update_view_correct_page(self):
        self.app.get_current_page.return_value = MonitoringPage(self.root, self.app)
        self.camera_view.update_view()
        self.assertTrue(self.camera_view.lbl_image.configure.called)

    def test_update_view_incorrect_page(self):
        self.app.get_current_page.return_value = CalibrationPage(self.root, self.app)
        self.camera_view.update_view()
        self.assertFalse(self.camera_view.lbl_image.configure.called)

    @patch.object(CalibrationPage, "get_subpage")
    def test_update_view_valid_subpage(self, mock_get_subpage):
        self.app.get_current_page.return_value = CalibrationPage(self.root, self.app)
        self.camera_view.page_class = CalibrationPage
        text_subpage = TextSubPage(self.root, self.app, "Test", 0)
        mock_get_subpage.return_value = text_subpage
        self.camera_view.subpage = text_subpage

        self.camera_view.update_view()
        self.assertTrue(self.camera_view.lbl_image.configure.called)

    @patch.object(CalibrationPage, "get_subpage")
    def test_update_view_valid_subpage(self, mock_get_subpage):
        self.app.get_current_page.return_value = CalibrationPage(self.root, self.app)
        self.camera_view.page_class = CalibrationPage
        mock_get_subpage.return_value = TextSubPage(self.root, self.app, "Test", 0)
        self.camera_view.subpage = GoodPostureSubPage(self.root, self.app, "Test", 1)

        self.camera_view.update_view()
        self.assertFalse(self.camera_view.lbl_image.configure.called)

# if __name__ == '__main__':
#     unittest.main()
