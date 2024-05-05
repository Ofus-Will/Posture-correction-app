import unittest
from unittest.mock import MagicMock, patch
import cv2
import mediapipe as mp

from Data.camera_handler import CameraHandler
from Data.data_handler import DataHandler

class TestDataHandler(unittest.TestCase):
    
    def setUp(self):
        self.app = MagicMock()
        self.app.cap.read.return_value = (True, cv2.imread('Tests/test_image.jpg'))
        self.app.pose = mp.solutions.pose.Pose()
        self.app.camera_handler = CameraHandler(self.app)
        self.app.posture_classifier.visibility_threshold = 0.1

        self.data_handler = DataHandler(self.app)
        
    def load_landmarks(self):
        self.app.camera_handler.process_camera(False)

        return self.app.camera_handler.shared_landmarks

    def test_get_raw_data(self):
        self.load_landmarks()

        data = self.data_handler.get_raw_data()

        self.assertIsNotNone(data)

    def test_no_get_raw_data(self):
        self.app.camera_handler.shared_landmarks = None 

        data = self.data_handler.get_raw_data()

        self.assertIsNone(data)

    def test_process_data(self):
        self.load_landmarks()

        data = self.data_handler.process_data()

        self.assertIsNotNone(data)

    @patch.object(DataHandler, "get_raw_data")
    def test_no_process_data(self, mock_get_raw_data):
        self.load_landmarks()

        mock_get_raw_data.return_value = None

        data = self.data_handler.process_data()

        self.assertIsNone(data)

    def test_check_for_data(self):

        self.data_handler.good_posture = {"test": 1}
        self.data_handler.bad_posture = [{"test": 1}]
        
        has_data = self.data_handler.check_for_data()

        self.assertTrue(has_data)
        