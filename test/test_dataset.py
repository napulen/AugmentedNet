import unittest
from common import ANNOTATIONSCOREMAP, DATASPLITS

class TestDataset(unittest.TestCase):
    def test_dataset_and_splits_length(self):
        train, val, test = DATASPLITS.values()
        allAnnotations = list(ANNOTATIONSCOREMAP.keys())
        allSplits = train + val + test
        self.assertEqual(len(allAnnotations), len(allSplits))

    def test_dataset_and_splits_equal(self):
        train, val, test = DATASPLITS.values()
        allAnnotations = list(ANNOTATIONSCOREMAP.keys())
        allSplits = train + val + test
        self.assertEqual(set(allAnnotations), set(allSplits))