import io
import random
import unittest

import music21
import pandas as pd

import AugmentedNet.score_parser

from test import AuxiliaryFiles

aux = AuxiliaryFiles("score_parser")


def _load_dfgt(csvGT):
    dfGT = pd.read_csv(csvGT)
    dfGT.set_index("s_offset", inplace=True)
    for col in AugmentedNet.score_parser.S_LISTTYPE_COLUMNS:
        dfGT[col] = dfGT[col].apply(eval)
    return dfGT


class TestScoreParser(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_octave_initial_dataframe(self):
        dfGT = _load_dfgt(aux.octaveTestInitialDataFrame)
        s = AugmentedNet.score_parser._m21Parse(aux.octaveTest)
        df = AugmentedNet.score_parser._initialDataFrame(s)
        for rowGT, row in zip(dfGT.itertuples(), df.itertuples()):
            with self.subTest(gt_index=rowGT.Index, index=row.Index):
                self.assertEqual(rowGT._asdict(), row._asdict())

    def test_octave_reindexed_dataframe(self):
        dfGT = _load_dfgt(aux.octaveTestReindexDataFrame)
        s = AugmentedNet.score_parser._m21Parse(aux.octaveTest)
        df = AugmentedNet.score_parser._initialDataFrame(s)
        df = AugmentedNet.score_parser._reindexDataFrame(df, fixedOffset=0.25)
        for rowGT, row in zip(dfGT.itertuples(), df.itertuples()):
            with self.subTest(gt_index=rowGT.Index, index=row.Index):
                self.assertEqual(rowGT._asdict(), row._asdict())

    def test_weird_rhythm_initial_dataframe(self):
        dfGT = _load_dfgt(aux.weirdRhythmInitialDataFrame)
        s = AugmentedNet.score_parser._m21Parse(aux.weirdRhythm)
        df = AugmentedNet.score_parser._initialDataFrame(s)
        for rowGT, row in zip(dfGT.itertuples(), df.itertuples()):
            with self.subTest(gt_index=rowGT.Index, index=row.Index):
                self.assertEqual(rowGT._asdict(), row._asdict())

    def test_weird_rhythm_reindexed_dataframe(self):
        dfGT = _load_dfgt(aux.weirdRhythmReindexDataFrame)
        s = AugmentedNet.score_parser._m21Parse(aux.weirdRhythm)
        df = AugmentedNet.score_parser._initialDataFrame(s)
        df = AugmentedNet.score_parser._reindexDataFrame(df, fixedOffset=0.25)
        for rowGT, row in zip(dfGT.itertuples(), df.itertuples()):
            with self.subTest(gt_index=rowGT.Index, index=row.Index):
                self.assertEqual(rowGT._asdict(), row._asdict())

    def test_parse_annotation_as_score(self):
        # The texturization is random, thus, set the seed here
        random.seed(1337)
        df = AugmentedNet.score_parser.parseAnnotationAsScore(
            aux.haydnOp20no4iAnnotation, texturize=True, eventBased=True
        )
        # This test is somewhat cheating, but I prefer the higher coverage
        # render the df into a m21 score, then compare scores (gt, generated)
        s = AugmentedNet.score_parser._engraveScore(df)
        s = s.makeNotation()
        gt = music21.converter.parse(
            aux.texturizedHaydnOp20No4i, format="humdrum"
        )
        for c1, c2 in zip(s.chordify().flat.notes, gt.chordify().flat.notes):
            with self.subTest(c1=c1, c2=c2):
                self.assertEqual(c1.pitchNames, c2.pitchNames)


if __name__ == "__main__":
    unittest.main()
