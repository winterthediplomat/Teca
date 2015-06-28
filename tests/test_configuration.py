import unittest
from teca import ConfigHandler as ch


class TestConfigHandler(unittest.TestCase):

    def test_excluded_folders_defaultparameter(self):
        defConf = ch.ConfigHandler()
        self.assertEqual(
            defConf.excluded_folders(),
            defConf.excluded_folders(""))
