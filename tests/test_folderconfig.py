import unittest
from teca import ConfigHandler as ch


class TestFolderConfig(unittest.TestCase):

    def setUp(self):
        self.parameters = {"test": [1, 2, 3], "foo": "bar", "baz": 3}
        self.default_fc = ch.FolderConfig()
        self.parameter_fc = ch.FolderConfig(self.parameters)

    def test_no_parameters(self):
        self.assertEqual(self.default_fc.config, dict())

    def test_with_parameters(self):
        self.assertEqual(self.parameter_fc.config, self.parameters)

    def test_getitem_withparameters(self):
        self.assertEqual(self.parameter_fc["foo"], "bar")
        self.assertEqual(self.parameter_fc["baz"], 3)
        self.assertRaises(KeyError, lambda: self.parameter_fc["alfapls"])

    def test_merge_empty_with_empty(self):
        self.default_fc.merge_with(self.default_fc)
        self.assertEqual(self.default_fc.config, dict())

    def test_merge_with_none(self):
        """
        this method should just request a parameter.
        leaving this test there to document this behaviour, but
        it's going to change (very) soon.
        """
        try:
            self.assertRaises(
                AttributeError,
                lambda: self.parameter_fc.merge_with())
        except:
            self.assertTrue(False)

    def test_merge_empty_with_parameter(self):
        self.default_fc.merge_with(self.parameter_fc)
        self.assertEqual(self.default_fc.config, self.parameter_fc.config)

    def test_merge_parameter_with_empty(self):
        self.parameter_fc.merge_with(self.default_fc)
        self.assertEqual(self.parameter_fc.config, self.parameters)

    def test_merge_parameter_with_parameter(self):
        yafc = ch.FolderConfig(self.parameters)
        yafc.merge_with(self.parameter_fc)
        self.assertEqual(self.parameter_fc.config, yafc.config)
