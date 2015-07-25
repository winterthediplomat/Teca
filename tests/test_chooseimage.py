import teca.generation as tecagen
import teca.ConfigHandler as tecaconf
import tests.test_filesystem as testfs
import unittest

class TestChooseImage(testfs.SameConfClass, unittest.TestCase):

    def test_selectOneFile(self):
        lst = ["roxas.png", "alchimist.gif", "nicola.webm"]
        self.assertTrue(tecagen.chooseImage("", lst, self.conf) in lst)

    def test_goDeepInTheFilesystem(self):
        # by definition of the fake filesystem, the root folder
        #   contains at least one image.
        self.assertNotEqual(tecagen.chooseImage("/tests/test_data/images", [], self.conf), "")
        self.assertNotEqual(tecagen.chooseImage("/tests/test_data/images", [], self.conf), self.conf.default_image)

    def test_emptyFolder(self):
        self.assertEqual(tecagen.chooseImage("/tests/test_data/emptyfolder", [], self.conf), self.conf.default_image)

class TestChooseCoverImage(testfs.SameConfClass, unittest.TestCase):

    def test_onlyOne(self):
        #chooseCoverImage(path, files, cfg)
        self.assertEqual(tecagen.chooseCoverImage("", ["foo"], self.conf), "foo")
