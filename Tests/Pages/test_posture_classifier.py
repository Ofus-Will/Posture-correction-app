import unittest
from unittest.mock import MagicMock, patch
import cv2
import mediapipe as mp

from Data.camera_handler import CameraHandler
from Data.data_handler import DataHandler
from Data.posture_classifier import PostureClassifier

class TestPostureClassifier(unittest.TestCase):
    
    def setUp(self):
        self.app = MagicMock()
        self.app.posture_classifier = PostureClassifier(self.app)
        self.app.data_handler = DataHandler(self.app)
        self.app.camera_handler = CameraHandler(self.app)
        self.app.pose = mp.solutions.pose.Pose()

    def test_update_classification_good(self):
        self.app.cap.read.return_value = (True, cv2.imread('Tests/test_image.jpg'))
        self.app.camera_handler.process_camera(False)
        self.app.data_handler.good_posture = self.app.data_handler.process_data()

        self.app.posture_classifier.update_classification()

        # print("Classification: ", self.app.posture_classifier.classification)

        self.assertTrue(self.app.posture_classifier.classification == "Good")

    def test_update_classification_bad(self):
        self.app.data_handler.bad_posture = []

        self.app.cap.read.return_value = (True, cv2.imread('Tests/test_image_bad.jpg'))
        self.app.camera_handler.process_camera(False)
        self.app.data_handler.bad_posture.append(self.app.data_handler.process_data())
        self.app.cap.read.return_value = (True, cv2.imread('Tests/test_image.jpg'))
        self.app.camera_handler.process_camera(False)
        self.app.data_handler.good_posture = self.app.data_handler.process_data()

        self.app.cap.read.return_value = (True, cv2.imread('Tests/test_image_bad.jpg'))
        self.app.camera_handler.process_camera(False)

        self.app.posture_classifier.consecutive_bad_frames = 100

        self.app.posture_classifier.update_classification()

        self.assertEqual(self.app.posture_classifier.classification, "Bad")