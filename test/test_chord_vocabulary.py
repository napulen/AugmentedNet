"""Tests for AugmentedNet.chord_vocabulary."""

import unittest

from AugmentedNet.chord_vocabulary import frompcset
from AugmentedNet.feature_representation import KEYS, PCSETS


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
