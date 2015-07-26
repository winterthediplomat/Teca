import unittest
from teca import ConfigHandler

"""
tl;dr code should not ever use empty configuration handlers. also default values.

long version:
This test case documents all the shortcomings of 
not providing a configuration to Teca.
The most important thing that this test case does
is to show default values, when they're not set in the configuration.
"""

class DefaultConfigurationHandler(unittest.TestCase):

    def setUp(self):
        self.defConf = ConfigHandler.ConfigHandler()

    def test_image_formats(self):
        self.assertEqual(set(self.defConf.image_formats),
                         set(["jpg", "tiff", "png", "bmp"])
                         )

    def test_excluded_folders(self):
        self.assertEqual(self.defConf.excluded_folders(''), [])

    def test_starting_path(self):
        self.assertRaises(KeyError, lambda: self.defConf.starting_path)

    def test_use_verbose(self):
        self.assertRaises(KeyError, lambda: self.defConf.use_verbose)

    def test_excluded_file_formats(self):
        self.assertRaises(KeyError, lambda: self.defConf.excluded_file_formats("madalby.jpg"))
        self.assertRaises(KeyError, lambda: self.defConf.excluded_file_formats(""))

    def test_get_obj_from_path(self):
        """
        ConfigHandler._get_obj_from_path is an internal function.
        Testing it here, but client code should not use this directly.
        B
        """
        self.assertRaises(KeyError, lambda: self.defConf._get_obj_from_path("anime/yahari"))

    def test_cover_image_name(self):
        self.assertEqual(self.defConf.cover_image_name("tv/doctor/tennant"), "")

    def test_thumbnail_size(self):
        self.assertRaises(KeyError, lambda: self.defConf.thumbnail_size("drawings/doomfest"))

    def test_cover_size(self):
        self.assertRaises(KeyError, lambda: self.defConf.cover_size("drawings/notalfa"))

    def test_image_prefix_path(self):
        self.assertEqual(self.defConf.image_prefix_path("drawings/doomfest"), "")   

    def test_regenerate_thumbnails(self):
        self.assertRaises(KeyError, lambda: self.defConf.regenerate_thumbnails)

    def test_template_path(self):
        self.assertRaises(KeyError, lambda: self.defConf.template_path("projects_logos/Teca"))

    def test_directories_on_a_row(self):
        self.assertEqual(self.defConf.directories_on_a_row, 1)
