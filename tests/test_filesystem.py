#^_^ coding: utf8 ^_^

import os
import mockfs
import teca.filesystem as tecafs
from six import next as _next
import teca.ConfigHandler as tecaconf
import unittest

class SameConfClass(object):
    def setUp(self):
        self.conf_path = "tests/test_data/configuration.json"
        self.conf_content = open(self.conf_path).read()
        self.starting_path = "tests/test_data/images/"
        self.conf = tecaconf.ConfigHandler(
            self.conf_path,
            {"starting_path": self.starting_path}
        )

        self.mfs = mockfs.replace_builtins()
        self.mfs.add_entries({
            "tests": {
                "test_data":{
                        "configuration.json" : self.conf_content,
                        "images": {
                            "cutegirlsarecute": {
                                "yukinon.jpg": "",
                                "charlotte.jpg": "",
                                "misato.bmp": ""
                            },
                            "hiddenfolder": {
                                "uselessdoc.txt": "useless content",
                                "uselessimage.png": ""
                            },
                            "emptyFolder": {},
                            "ohwait": {
                                "imagesonly": {
                                    "yukinon.jpg": "",
                                    "specialchàr.jpg": "",
                                    "thumb_lol.png": ""
                                }
                            },
                            "you": {
                               "shall": {
                                   "notpass": {
                                       "kaiki.gif": ""
                                   },
                                   "pass": {
                                       "eruna.jpg": ""
                                   }
                               }
                            }
                        }
                }
            }
        })

    def tearDown(self):
        mockfs.restore_builtins()

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

    def test_legitNamesOnly(self):
        fnames = tecafs.filesInFolder("ohwait/imagesonly", self.conf)
        self.assertTrue("thumb_lol.png" not in fnames)

    def test_specialFilenameInFolder(self):
        fnames = tecafs.filesInFolder("ohwait/imagesonly", self.conf)
        self.assertTrue("specialchàr.jpg" in fnames)
