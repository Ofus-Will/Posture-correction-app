import unittest
from unittest.mock import MagicMock, patch
import cv2
import mediapipe as mp

from Data.camera_handler import CameraHandler
# from Pages.monitoring import MonitoringPage
# from Widgets.camera_view import CameraView

class TestCameraHandler(unittest.TestCase):

    def setUp(self):
        self.app = MagicMock()
        self.app.cap.read.return_value = (True, cv2.imread('Tests/test_image.jpg'))
        self.app.current_page = MagicMock()
        self.app.pose = mp.solutions.pose.Pose()
        # self.app.mp_pose = mp.solutions.pose
        # self.app.drawing_spec = mp.solutions.drawing_utils.DrawingSpec()
        self.camera_handler = CameraHandler(self.app)

    @patch.object(CameraHandler, "get_camera_view")
    def test_retrieves_landmarks(self, mock_get_camera_view):
        # mock_flip.return_value = cv2.flip(self.app.cap.read[1])
        # mock_cvtColor.return_value = cv2.cvtColor(mock_flip, cv2.COLOR_BGR2RGB)
        mock_camera_view = MagicMock()
        mock_get_camera_view.return_value = mock_camera_view
        self.app.monitoring = True
        mock_camera_view.landmark_bool.get.return_value = True
        self.camera_handler.process_camera(False)

        # print(self.camera_handler.shared_landmarks)
        self.assertIsNotNone(self.camera_handler.shared_landmarks, "Failed to get landmarks")


    @patch.object(CameraHandler, "get_camera_view")
    def test_no_retrieve_landmarks(self, mock_get_camera_view):
        mock_camera_view = MagicMock()
        mock_get_camera_view.return_value = mock_camera_view
        self.app.monitoring = False
        mock_camera_view.landmark_bool.get.return_value = False

        self.camera_handler.shared_landmarks = None

        self.camera_handler.process_camera()

        self.assertIsNone(self.camera_handler.shared_landmarks, "Wrongfully obtained landmarks")

    def test_get_page_camera_view(self):
        self.app.current_page.camera_view = MagicMock()
        camera_view = self.camera_handler.get_camera_view()
        self.assertIsInstance(camera_view, MagicMock)

    def test_get_subpage_camera_view(self):
        delattr(self.app.current_page, "camera_view")
        self.app.current_page.current_subpage = MagicMock()
        self.app.current_page.current_subpage.camera_view = MagicMock()

        camera_view = self.camera_handler.get_camera_view()

        self.assertIsInstance(camera_view, MagicMock)

    def test_no_get_page_camera_view(self):
        
        delattr(self.app.current_page, "camera_view")
        delattr(self.app.current_page, "current_subpage")

        camera_view = self.camera_handler.get_camera_view()

        self.assertIsNone(camera_view)

