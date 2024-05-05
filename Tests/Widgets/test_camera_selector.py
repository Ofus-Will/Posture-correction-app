import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from tkinter import ttk

from Widgets.camera_selector import CameraSelector

class TestCameraSelector(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = MagicMock()

        # self.selector = CameraSelector(self.root, self.app)

        self.root.withdraw()

    def tearDown(self):
        self.root.destroy()

    @patch('Widgets.camera_selector.get_cam_ports')
    def test_init(self, mock_get_cam_ports):
        mock_get_cam_ports.return_value = [0, 1, 2]

        selector = CameraSelector(self.root, self.app)

        expected_ports = ('Camera 1', 'Camera 2', 'Camera 3')
        self.assertEqual(selector['values'], expected_ports)

    @patch('Widgets.camera_selector.get_cam_ports')
    def test_change_camera_port(self, mock_get_cam_ports):

        mock_get_cam_ports.return_value = [0, 1]
        selector = CameraSelector(self.root, self.app)

        selector.set("Camera 2")
        selector.event_generate("<<ComboboxSelected>>")

        self.app.set_camera_port.assert_called_once_with(1)
