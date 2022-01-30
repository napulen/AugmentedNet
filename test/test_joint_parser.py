import io
import unittest

import pandas as pd

import AugmentedNet.joint_parser

from test import AuxiliaryFiles

aux = AuxiliaryFiles("joint_parser")


def _load_dfgt(csvGT):
    dfGT = pd.read_csv(csvGT)
    dfGT.set_index("j_offset", inplace=True)
    for col in AugmentedNet.joint_parser.J_LISTTYPE_COLUMNS:
        dfGT[col] = dfGT[col].apply(eval)
    return dfGT


class TestScoreParser(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_haydn_annotation_and_score(self):
        dfGT = _load_dfgt(aux.haydnDataframeGT)
        df = AugmentedNet.joint_parser.parseAnnotationAndScore(
            aux.haydnRomanText, aux.haydnHumdrum, fixedOffset=0.25
        )
        for rowGT, row in zip(dfGT.itertuples(), df.itertuples()):
            with self.subTest(gt_index=rowGT.Index, index=row.Index):
                self.assertEqual(rowGT._asdict(), row._asdict())


if __name__ == "__main__":
    unittest.main()
