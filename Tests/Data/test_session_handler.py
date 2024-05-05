import unittest
from unittest.mock import MagicMock, patch
import cv2
import mediapipe as mp

from Data.camera_handler import CameraHandler
from Data.data_handler import DataHandler
from Data.session_handler import SessionHandler

from datetime import datetime

class TestSessionHandler(unittest.TestCase):
    
    def setUp(self):
        self.app = MagicMock()
        self.app.session_handler = SessionHandler(self.app)

    def test_start_session_deny(self):

        self.app.session_handler.start_time = datetime.now()

        self.assertFalse(self.app.session_handler.start_session())

    def test_start_session_success(self):

        self.app.session_handler.start_time = None 

        self.assertTrue(self.app.session_handler.start_session())

    def test_end_session_success(self):
        self.app.session_handler.start_time = datetime.now()
        self.assertTrue(self.app.session_handler.end_session())

    def test_end_session_deny(self):
        self.app.session_handler.start_time = None 
        self.assertFalse(self.app.session_handler.end_session())

    def test_delete_sessions_success(self):
        self.app.session_handler.sessions = ["example1", "example2", "example3"]

        self.app.session_handler.delete_sessions()

        self.assertEqual(self.app.session_handler.sessions, [])
