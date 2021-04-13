import unittest
from common import ANNOTATIONSCOREDUPLES, DATASPLITS

class TestDataset(unittest.TestCase):
    def test_dataset_and_splits_length(self):
        """ This one checks there are no duplicate entries. """
        train, val, test = DATASPLITS.values()
        allAnnotations = list(ANNOTATIONSCOREDUPLES.keys())
        allSplits = train + val + test
        self.assertEqual(len(allAnnotations), len(allSplits))

    def test_dataset_and_splits_equal(self):
        """ This one checks there are no missing/distinct entries."""
        train, val, test = DATASPLITS.values()
        allAnnotations = list(ANNOTATIONSCOREDUPLES.keys())
        allSplits = train + val + test
        self.assertEqual(set(allAnnotations), set(allSplits))