import unittest

import pandas as pd

from AugmentedNet import annotation_parser
from test import AuxiliaryFiles

aux = AuxiliaryFiles("annotation_parser")


def _load_dfgt(csvGT):
    dfGT = pd.read_csv(csvGT)
    dfGT.set_index("a_offset", inplace=True)
    for col in annotation_parser.A_LISTTYPE_COLUMNS:
        dfGT[col] = dfGT[col].apply(eval)
    return dfGT


class TestAnnotationParser(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_initial_dataframe(self):
        dfGT = _load_dfgt(aux.multiple_annotations_df1)
        s = annotation_parser._m21Parse(aux.multiple_annotations)
        df = annotation_parser._initialDataFrame(s)
        for rowGT, row in zip(dfGT.itertuples(), df.itertuples()):
            with self.subTest(gt_index=rowGT.Index, index=row.Index):
                self.assertEqual(rowGT._asdict(), row._asdict())

    def test_reindexed_dataframe(self):
        dfGT = _load_dfgt(aux.multiple_annotations_df2)
        s = annotation_parser._m21Parse(aux.multiple_annotations)
        df = annotation_parser._initialDataFrame(s)
        df = annotation_parser._reindexDataFrame(df, fixedOffset=0.25)
        for rowGT, row in zip(dfGT.itertuples(), df.itertuples()):
            with self.subTest(gt_index=rowGT.Index, index=row.Index):
                self.assertEqual(rowGT._asdict(), row._asdict())


if __name__ == "__main__":
    unittest.main()
