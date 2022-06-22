import io
import random
import unittest

import music21
import pandas as pd

from AugmentedNet import score_parser

from test import AuxiliaryFiles

aux = AuxiliaryFiles("score_parser")


class TestScoreParser(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_octave_initial_dataframe(self):
        dfGT = score_parser.from_tsv(aux.octaveTestInitialDataFrame)
        s = score_parser._m21Parse(aux.octaveTest)
        df = score_parser._initialDataFrame(s)
        for rowGT, row in zip(dfGT.itertuples(), df.itertuples()):
            with self.subTest(gt_index=rowGT.Index, index=row.Index):
                self.assertEqual(rowGT._asdict(), row._asdict())

    def test_octave_reindexed_dataframe(self):
        dfGT = score_parser.from_tsv(aux.octaveTestReindexDataFrame)
        s = score_parser._m21Parse(aux.octaveTest)
        df = score_parser._initialDataFrame(s)
        df = score_parser._reindexDataFrame(df, fixedOffset=0.25)
        for rowGT, row in zip(dfGT.itertuples(), df.itertuples()):
            with self.subTest(gt_index=rowGT.Index, index=row.Index):
                self.assertEqual(rowGT._asdict(), row._asdict())

    def test_weird_rhythm_initial_dataframe(self):
        dfGT = score_parser.from_tsv(aux.weirdRhythmInitialDataFrame)
        s = score_parser._m21Parse(aux.weirdRhythm)
        df = score_parser._initialDataFrame(s)
        for rowGT, row in zip(dfGT.itertuples(), df.itertuples()):
            with self.subTest(gt_index=rowGT.Index, index=row.Index):
                self.assertEqual(rowGT._asdict(), row._asdict())

    def test_weird_rhythm_reindexed_dataframe(self):
        dfGT = score_parser.from_tsv(aux.weirdRhythmReindexDataFrame)
        s = score_parser._m21Parse(aux.weirdRhythm)
        df = score_parser._initialDataFrame(s)
        df = score_parser._reindexDataFrame(df, fixedOffset=0.25)
        for rowGT, row in zip(dfGT.itertuples(), df.itertuples()):
            with self.subTest(gt_index=rowGT.Index, index=row.Index):
                self.assertEqual(rowGT._asdict(), row._asdict())

    def test_parse_annotation_as_score(self):
        # The texturization is random, thus, set the seed here
        random.seed(1337)
        df = score_parser.parseAnnotationAsScore(
            aux.haydnOp20no4iAnnotation, texturize=True, eventBased=True
        )
        # This test is somewhat cheating, but I prefer the higher coverage
        # render the df into a m21 score, then compare scores (gt, generated)
        timeSignatures = {0.0: "3/4"}
        s = score_parser._engraveScore(df, timeSignatures)
        s = s.makeNotation()
        gt = music21.converter.parse(
            aux.texturizedHaydnOp20No4i, format="humdrum"
        )
        for c1, c2 in zip(s.chordify().flat.notes, gt.chordify().flat.notes):
            with self.subTest(c1=c1, c2=c2):
                self.assertEqual(c1.pitchNames, c2.pitchNames)


if __name__ == "__main__":
    unittest.main()
