"""Tests for AugmentedNet.chord_vocabulary."""

import unittest

from AugmentedNet.chord_vocabulary import frompcset, closestPcSet
from AugmentedNet.feature_representation import KEYS, PCSETS

romanGT = {
    ((0, 3, 8), "G#"): (["G#", "B#", "D#"], "I"),
    ((1, 4, 8), "d-"): (["D-", "F-", "A-"], "i"),
    ((1, 6, 9), "F-"): (["G-", "B--", "D-"], "ii"),
    ((1, 7, 10), "e#"): (["F##", "A#", "C#"], "iio"),
    ((0, 5, 8), "C#"): (["E#", "G#", "B#"], "iii"),
    ((3, 7, 11), "a-"): (["C-", "E-", "G"], "III+"),
    ((4, 8, 11), "C-"): (["F-", "A-", "C-"], "IV"),
    ((3, 6, 10), "a#"): (["D#", "F#", "A#"], "iv"),
    ((1, 5, 8), "F#"): (["C#", "E#", "G#"], "V"),
    ((2, 5, 10), "e-"): (["B-", "D", "F"], "V"),
    ((3, 6, 10), "G-"): (["E-", "G-", "B-"], "vi"),
    ((3, 6, 11), "d#"): (["B", "D#", "F#"], "VI"),
    ((1, 4, 10), "B"): (["A#", "C#", "E"], "viio"),
    ((0, 3, 9), "b-"): (["A", "C", "E-"], "viio"),
}

pcsetsGT = {
    # V7, V9, Vb9
    (2, 5, 7, 11): (2, 5, 7, 11),
    (2, 5, 7, 9, 11): (2, 5, 7, 11),
    (2, 5, 7, 8, 11): (2, 5, 7, 11),
    # V+, V+7
    (3, 7, 11): (3, 7, 11),
    (3, 5, 7, 11): (3, 7, 11),
}


class TestChordVocabulary(unittest.TestCase):
    def test_vocabulary_size(self):
        """The vocabulary should have 121 items."""
        self.assertEqual(len(frompcset), 121)

    def test_keys_in_vocabulary(self):
        """There should only be 34 keys."""
        keys = []
        for pcset, k in frompcset.items():
            keys.extend(list(k.keys()))
        self.assertEqual(frozenset(keys), frozenset(KEYS))

    def test_pcsets_in_vocabulary(self):
        """The pcsets in the vocabulary and PCSETS should be the same."""
        pcsets = set(frompcset.keys())
        self.assertEqual(pcsets, set(PCSETS))

    def test_roman_numerals(self):
        """Verify that some Roman numerals are correct."""
        for (pcset, key), (chordGT, rnGT) in romanGT.items():
            chord = frompcset[pcset][key]["chord"]
            rn = frompcset[pcset][key]["rn"]
            with self.subTest(pcset=pcset, key=key):
                self.assertEqual(chordGT, chord)
                self.assertEqual(rnGT, rn)

    def test_closest_pcset(self):
        """Verify that you get sensible pcset matches."""
        for pcset, pcsGT in pcsetsGT.items():
            pcs = closestPcSet(pcset)
            with self.subTest(pcset=pcset, closest_match=pcsGT):
                self.assertEqual(pcs, pcsGT)
