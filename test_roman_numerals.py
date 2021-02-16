import unittest

from music21 import roman
import roman_numerals

class TestRomanNumeralParser(unittest.TestCase):

    def test_tonic_triad(self):
        rn, key = "I", "C"
        GT = {
            "pitchNames": ("C", "E", "G"),
            "bass": "C",
            "root": "C",
            "inversion": 0,
            "quality": "major triad",
            "pcset": (0, 4, 7),
            "tonicizedKey": None,
            "degree": "1",
        }
        ret = roman_numerals.parseRomanNumeral(rn, key)
        self.assertEqual(GT, ret)

    def test_dominant_seventh(self):
        rn, key = "V65", "d"
        GT = {
            "pitchNames": ("C#", "E", "G", "A"),
            "bass": "C#",
            "root": "A",
            "inversion": 1,
            "quality": "dominant seventh chord",
            "pcset": (1, 4, 7, 9),
            "tonicizedKey": None,
            "degree": "5",
        }
        ret = roman_numerals.parseRomanNumeral(rn, key)
        self.assertEqual(GT, ret)

    def test_tonicized_key(self):
        rn, key = "viio7/v", "c#"
        GT = {
            "pitchNames": ("F##", "A#", "C#", "E"),
            "bass": "F##",
            "root": "F##",
            "inversion": 0,
            "quality": "diminished seventh chord",
            "pcset": (1, 4, 7, 10),
            "tonicizedKey": "g#",
            "degree": "7/5",
        }
        ret = roman_numerals.parseRomanNumeral(rn, key)
        self.assertEqual(GT, ret)
