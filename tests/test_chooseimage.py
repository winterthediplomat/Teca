import teca.generation as tecagen
import teca.ConfigHandler as tecaconf
import unittest

class TestChooseImage(unittest.TestCase):
    def setUp(self):
        self.conf = tecaconf.ConfigHandler(
            "tests/test_data/configuration.json",
            {"starting_path": "./tests/test_data/images"}
        )

    def test_selectOneFile(self):
        lst = ["roxas.png", "alchimist.gif", "nicola.webm"]
        self.assertTrue(tecagen.chooseImage("", lst, self.conf) in lst)

class TestChooseCoverImage(unittest.TestCase):
    def setUp(self):
        self.conf = tecaconf.ConfigHandler(
            "tests/test_data/configuration.json",
            {"starting_path": "./tests/test_data/images"}
        )

    def test_onlyOne(self):
        #chooseCoverImage(path, files, cfg)
        self.assertEqual(tecagen.chooseCoverImage("", ["foo"], self.conf), "foo")
