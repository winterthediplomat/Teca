import teca.utils as tecautils
import teca.ConfigHandler as tecaconf
import unittest

class TestFileFilter(unittest.TestCase):
    def setUp(self):
        self.conf = tecaconf.ConfigHandler(
            "tests/test_data/configuration.json",
            {"starting_path": "tests/test_data/images"}
        )
        self.files_list = [
          "foo.doc",
          "yukinon.jpg",
          "cuteflushadoingflushathings.webm"
        ]

    def test_dothefiltering(self):
        self.assertTrue("foo.doc" not in
                        tecautils.filterImages(self.files_list,
                                               self.conf))
        self.assertTrue("yukinon.jpg" in
                        tecautils.filterImages(self.files_list,
                                               self.conf))

    def test_nofiles(self):
        self.assertEqual(0, len(tecautils.filterImages([], self.conf)))
