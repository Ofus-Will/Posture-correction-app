import unittest
from unittest.mock import MagicMock, patch

from Data.settings_handler import SettingsHandler

class TestSettingsHandler(unittest.TestCase):
    
    def setUp(self):
        self.app = MagicMock()
        self.app.settings_handler = SettingsHandler(self.app)

    def test_get_setting_valid(self):
        setting = self.app.settings_handler.get_setting("theme")
        self.assertIsNotNone(setting)

    def test_get_setting_invalid(self):
        setting = self.app.settings_handler.get_setting("y98dstygfiau")
        self.assertIsNone(setting)

    def test_reset_defaults(self):
        self.app.settings_handler.reset_defaults()
        defaults = {key: meta["default"] for key, meta in self.app.settings_handler.meta_settings.items()}
        self.assertEqual(self.app.settings_handler.settings, defaults)
