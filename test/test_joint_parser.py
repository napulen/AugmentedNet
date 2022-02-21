import io
import unittest

import pandas as pd

from AugmentedNet import joint_parser

from test import AuxiliaryFiles

aux = AuxiliaryFiles("joint_parser")


class TestJointParser(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_haydn_annotation_and_score(self):
        dfGT = joint_parser.from_tsv(aux.haydnDataframeGT)
        df = joint_parser.parseAnnotationAndScore(
            aux.haydnRomanText, aux.haydnHumdrum, fixedOffset=0.25
        )
        for rowGT, row in zip(dfGT.itertuples(), df.itertuples()):
            with self.subTest(gt_index=rowGT.Index, index=row.Index):
                self.assertEqual(rowGT._asdict(), row._asdict())


if __name__ == "__main__":
    unittest.main()
