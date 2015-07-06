import teca.generation as tecagen
import unittest

class TestTokenGeneration(unittest.TestCase):
    def test_isAlphaNum(self):
        self.assertTrue(tecagen.generateToken().isalnum())

    def test_onetokenleft(self):
        self.assertEqual("D", tecagen.generateToken("ABC", lenght=1, alphabet="ABCD"))

    def test_alltokenaretaken(self):
        with self.assertRaises(ValueError):
            tecagen.generateToken("ABCD", 1, "ABCD")
