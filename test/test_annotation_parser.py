import unittest

from music21.roman import RomanNumeral
import pandas as pd

from AugmentedNet import annotation_parser
from test import AuxiliaryFiles

aux = AuxiliaryFiles("annotation_parser")


romanNumeralConversionsGT = {
    # bVII in a and bVII in C
    "bVI": ("C", (0, 3, 8), "c"),
    "bVII": ("C", (2, 5, 10), "F"),
    "VII": ("a", (2, 7, 11), "C"),
    # III in a
    "III": ("a", (0, 4, 7), "C"),
    # Secondary dominants in C
    "V/ii": ("C", (1, 4, 9), "d"),
    "V/iii": ("C", (3, 6, 11), "e"),
    "V/IV": ("C", (0, 4, 7), "F"),
    "V/V": ("C", (2, 6, 9), "G"),
    "V/vi": ("C", (4, 8, 11), "a"),
    # Secondary dominants in a
    "V/III": ("a", (2, 7, 11), "C"),
    "V/iv": ("a", (1, 4, 9), "d"),
    "V/V": ("a", (3, 6, 11), "E"),
    "V/VI": ("a", (0, 4, 7), "F"),
}


class TestAnnotationParser(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_initial_dataframe(self):
        dfGT = annotation_parser.from_tsv(aux.multiple_annotations_df1)
        s = annotation_parser._m21Parse(aux.multiple_annotations)
        df = annotation_parser._initialDataFrame(s)
        for rowGT, row in zip(dfGT.itertuples(), df.itertuples()):
            with self.subTest(gt_index=rowGT.Index, index=row.Index):
                self.assertEqual(rowGT._asdict(), row._asdict())

    def test_reindexed_dataframe(self):
        dfGT = annotation_parser.from_tsv(aux.multiple_annotations_df2)
        s = annotation_parser._m21Parse(aux.multiple_annotations)
        df = annotation_parser._initialDataFrame(s)
        df = annotation_parser._reindexDataFrame(df, fixedOffset=0.25)
        for rowGT, row in zip(dfGT.itertuples(), df.itertuples()):
            with self.subTest(gt_index=rowGT.Index, index=row.Index):
                self.assertEqual(rowGT._asdict(), row._asdict())

    def test_roman_numeral_secondary_dominants(self):
        for rn, (lkGT, pcsetGT, tkGT) in romanNumeralConversionsGT.items():
            rnobj = RomanNumeral(rn, lkGT)
            _, rndata = annotation_parser._extractRomanNumeralInformation(
                rnobj
            )
            rndata = annotation_parser._correctRomanNumeral(rndata)
            lk = rndata["localKey"]
            pcset = rndata["pcset"]
            tk = rndata["tonicizedKey"]
            with self.subTest(key=lkGT, rn=rn):
                self.assertEqual(lkGT, lk)
                self.assertEqual(pcsetGT, pcset)
                self.assertEqual(tkGT, tk)


if __name__ == "__main__":
    unittest.main()
