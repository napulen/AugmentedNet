"""Tests for AugmentedNet.keydistance."""

import unittest

from AugmentedNet.keydistance import weberEuclidean


GT = [
    ("C", 0.0),
    ("G", 1.0),
    ("F", 1.0),
    ("c", 1.0),
    ("a", 1.0),
    ("g", 1.41),
    ("e", 1.41),
    ("d", 1.41),
    ("f", 1.41),
    ("D", 2.0),
    ("E-", 2.0),
    ("B-", 2.0),
    ("A", 2.0),
    ("b", 2.24),
    ("E", 2.24),
    ("A-", 2.24),
    ("b-", 2.24),
    ("D-", 2.83),
    ("B", 2.83),
    ("e-", 3.0),
    ("f#", 3.0),
    ("c#", 3.16),
    ("a-", 3.16),
    ("d-", 3.61),
    ("G-", 3.61),
    ("F#", 3.61),
    ("g#", 3.61),
    ("C-", 4.12),
    ("C#", 4.12),
    ("d#", 4.24),
    ("G#", 4.47),
    ("F-", 4.47),
    ("a#", 5.0),
    ("e#", 5.39),
]


class TestKeyDistance(unittest.TestCase):
    def test_key_distances_for_c_major(self):
        keys = [pair[0] for pair in GT]
        distancesGT = [pair[1] for pair in GT]
        distances = []
        for key in keys:
            distance = round(weberEuclidean("C", key), 2)
            distances.append(distance)
        self.assertEqual(distancesGT, distances)