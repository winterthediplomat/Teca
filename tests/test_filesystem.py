import teca.filesystem as tecafs
from teca.utils import _next
import teca.ConfigHandler as tecaconf
import unittest

class SameConfClass(object):
    def setUp(self):
        self.conf = tecaconf.ConfigHandler(
            "tests/test_data/configuration.json",
            {"starting_path": "tests/test_data/images/"}
        )
    
class TestWalk(SameConfClass, unittest.TestCase):
    
    def test_foldersAtRoot(self):
        _, folders, _ = _next(tecafs.walk("", self.conf))
        self.assertEqual(set(["emptyFolder", "you", "ohwait", "cutegirlsarecute"]),
                         set(folders))

class TestDirectoryIsEmpty(SameConfClass, unittest.TestCase):

    def test_rootIsNotEmpty(self):
        res = tecafs.isDirectoryEmpty("", self.conf)
        self.assertEqual(res, False)

    def test_folderIsEmptyIndeed(self):
        res = tecafs.isDirectoryEmpty("emptyFolder", self.conf)
        self.assertEqual(res, True)

class TestFilesInDirectory(SameConfClass, unittest.TestCase):

    def test_noFilesInEmptyFolder(self):
        fnames = tecafs.filesInDirectory("emptyFolder", self.conf)
        self.assertEqual(len(fnames), 0)

    def test_noFilesInHiddenFolder(self):
        fnames = tecafs.filesInDirectory("hiddenfolder", self.conf)
        self.assertEqual(len(fnames), 0)

        fnames = tecafs.filesInDirectory("you/shall/notpass", self.conf)
        self.assertEqual(len(fnames), 0)

    def test_filesInNonHiddenFolder(self):
        fnames = tecafs.filesInDirectory("you/shall/pass", self.conf)
        self.assertNotEqual(len(fnames), 0)

    def test_noFilesInLegitButDocsFolder(self):
        fnames = tecafs.filesInDirectory("ohwait/documents", self.conf)
        self.assertEqual(len(fnames), 0)

    def test_filesInOnlyImagesFolder(self):
        fnames = tecafs.filesInFolder("ohwait/imagesonly", self.conf)
        self.assertNotEqual(len(fnames), 0)
