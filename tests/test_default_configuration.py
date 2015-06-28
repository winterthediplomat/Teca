import unittest
from teca import ConfigHandler


class DefaultConfigurationHandler(unittest.TestCase):

    def setUp(self):
        self.defConf = ConfigHandler.ConfigHandler()

    def test_defaultConfHander_imageformats(self):
        self.assertEqual(set(self.defConf.image_formats),
                         set(["jpg", "tiff", "png", "bmp"])
                         )

    def test_defaultConfHandler_excludedfolders(self):
        self.assertEqual(self.defConf.excluded_folders(''), [])

    def test_starting_path(self):
        self.assertRaises(KeyError, lambda: self.defConf.starting_path)
