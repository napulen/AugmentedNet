import io
import random
import unittest

import music21
import pandas as pd

import AugmentedNet.score_parser

octaveTest = """
**kern	**kern
*part1	*part1
*staff2	*staff1
*I"Piano	*
*I'Pno.	*
*clefF4	*clefG2
*k[]	*k[]
*M4/4	*M4/4
=1	=1
16CCCCLL 16BBBB	4r
16CCC 16BBB	.
16CC 16BB	.
16CJJ 16B	.
16CCLL 16BB	16r
16C 16B	16r
16cJJ 16b	16r
16r	16cc 16bb
8r	16cLL 16b
.	16cc 16bb
8r	16ccc 16bbb
.	16ccccJJ 16bbbb
4r	16cccLL 16bbb
.	16ccccJ 16bbbb
.	8cccccJ 8bbbbb
=2	=2
4CCC	4bbbb
4CC	4bbb
4C	4bb
4c	4b
=3	=3
16cLL	16cLL
16B	16d
16A	16e
16GJJ	16fJJ
32FLLL	16gLL
32E	.
32F	16a
32G	.
32A	16g
32G	.
32F	16f#XJJ
32EJJJ	.
2D	2g
==	==
*-	*-
!!!system-decoration: {(s1,s2)}
"""

octaveTestInitialDataFrame = """
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,0.25,1,"['C0', 'B0']",['M7'],"[True, True]"
0.25,0.25,1,"['C1', 'B1']",['M7'],"[True, True]"
0.5,0.25,1,"['C2', 'B2']",['M7'],"[True, True]"
0.75,0.25,1,"['C3', 'B3']",['M7'],"[True, True]"
1.0,0.25,1,"['C2', 'B2']",['M7'],"[True, True]"
1.25,0.25,1,"['C3', 'B3']",['M7'],"[True, True]"
1.5,0.25,1,"['C4', 'B4']",['M7'],"[True, True]"
1.75,0.25,1,"['C5', 'B5']",['M7'],"[True, True]"
2.0,0.25,1,"['C4', 'B4']",['M7'],"[True, True]"
2.25,0.25,1,"['C5', 'B5']",['M7'],"[True, True]"
2.5,0.25,1,"['C6', 'B6']",['M7'],"[True, True]"
2.75,0.25,1,"['C7', 'B7']",['M7'],"[True, True]"
3.0,0.25,1,"['C6', 'B6']",['M7'],"[True, True]"
3.25,0.25,1,"['C7', 'B7']",['M7'],"[True, True]"
3.5,0.5,1,"['C8', 'B8']",['M7'],"[True, True]"
4.0,1.0,2,"['C1', 'B7']",['M7'],"[True, True]"
5.0,1.0,2,"['C2', 'B6']",['M7'],"[True, True]"
6.0,1.0,2,"['C3', 'B5']",['M7'],"[True, True]"
7.0,1.0,2,"['C4', 'B4']",['M7'],"[True, True]"
8.0,0.25,3,['C4'],[],[True]
8.25,0.25,3,"['B3', 'D4']",['m3'],"[True, True]"
8.5,0.25,3,"['A3', 'E4']",['P5'],"[True, True]"
8.75,0.25,3,"['G3', 'F4']",['m7'],"[True, True]"
9.0,0.125,3,"['F3', 'G4']",['M2'],"[True, True]"
9.125,0.125,3,"['E3', 'G4']",['m3'],"[True, False]"
9.25,0.125,3,"['F3', 'A4']",['M3'],"[True, True]"
9.375,0.125,3,"['G3', 'A4']",['M2'],"[True, False]"
9.5,0.125,3,"['A3', 'G4']",['m7'],"[True, True]"
9.625,0.125,3,"['G3', 'G4']",['P1'],"[True, False]"
9.75,0.125,3,"['F3', 'F#4']",['A1'],"[True, True]"
9.875,0.125,3,"['E3', 'F#4']",['M2'],"[True, False]"
10.0,2.0,3,"['D3', 'G4']",['P4'],"[True, True]"
"""

octaveTestReindexDataFrame = """
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,0.25,1.0,"['C0', 'B0']",['M7'],"[True, True]"
0.25,0.25,1.0,"['C1', 'B1']",['M7'],"[True, True]"
0.5,0.25,1.0,"['C2', 'B2']",['M7'],"[True, True]"
0.75,0.25,1.0,"['C3', 'B3']",['M7'],"[True, True]"
1.0,0.25,1.0,"['C2', 'B2']",['M7'],"[True, True]"
1.25,0.25,1.0,"['C3', 'B3']",['M7'],"[True, True]"
1.5,0.25,1.0,"['C4', 'B4']",['M7'],"[True, True]"
1.75,0.25,1.0,"['C5', 'B5']",['M7'],"[True, True]"
2.0,0.25,1.0,"['C4', 'B4']",['M7'],"[True, True]"
2.25,0.25,1.0,"['C5', 'B5']",['M7'],"[True, True]"
2.5,0.25,1.0,"['C6', 'B6']",['M7'],"[True, True]"
2.75,0.25,1.0,"['C7', 'B7']",['M7'],"[True, True]"
3.0,0.25,1.0,"['C6', 'B6']",['M7'],"[True, True]"
3.25,0.25,1.0,"['C7', 'B7']",['M7'],"[True, True]"
3.5,0.5,1.0,"['C8', 'B8']",['M7'],"[True, True]"
3.75,0.5,1.0,"['C8', 'B8']",['M7'],"[False, False]"
4.0,1.0,2.0,"['C1', 'B7']",['M7'],"[True, True]"
4.25,1.0,2.0,"['C1', 'B7']",['M7'],"[False, False]"
4.5,1.0,2.0,"['C1', 'B7']",['M7'],"[False, False]"
4.75,1.0,2.0,"['C1', 'B7']",['M7'],"[False, False]"
5.0,1.0,2.0,"['C2', 'B6']",['M7'],"[True, True]"
5.25,1.0,2.0,"['C2', 'B6']",['M7'],"[False, False]"
5.5,1.0,2.0,"['C2', 'B6']",['M7'],"[False, False]"
5.75,1.0,2.0,"['C2', 'B6']",['M7'],"[False, False]"
6.0,1.0,2.0,"['C3', 'B5']",['M7'],"[True, True]"
6.25,1.0,2.0,"['C3', 'B5']",['M7'],"[False, False]"
6.5,1.0,2.0,"['C3', 'B5']",['M7'],"[False, False]"
6.75,1.0,2.0,"['C3', 'B5']",['M7'],"[False, False]"
7.0,1.0,2.0,"['C4', 'B4']",['M7'],"[True, True]"
7.25,1.0,2.0,"['C4', 'B4']",['M7'],"[False, False]"
7.5,1.0,2.0,"['C4', 'B4']",['M7'],"[False, False]"
7.75,1.0,2.0,"['C4', 'B4']",['M7'],"[False, False]"
8.0,0.25,3.0,['C4'],[],[True]
8.25,0.25,3.0,"['B3', 'D4']",['m3'],"[True, True]"
8.5,0.25,3.0,"['A3', 'E4']",['P5'],"[True, True]"
8.75,0.25,3.0,"['G3', 'F4']",['m7'],"[True, True]"
9.0,0.125,3.0,"['F3', 'G4']",['M2'],"[True, True]"
9.25,0.125,3.0,"['F3', 'A4']",['M3'],"[True, True]"
9.5,0.125,3.0,"['A3', 'G4']",['m7'],"[True, True]"
9.75,0.125,3.0,"['F3', 'F#4']",['A1'],"[True, True]"
10.0,2.0,3.0,"['D3', 'G4']",['P4'],"[True, True]"
10.25,2.0,3.0,"['D3', 'G4']",['P4'],"[False, False]"
10.5,2.0,3.0,"['D3', 'G4']",['P4'],"[False, False]"
10.75,2.0,3.0,"['D3', 'G4']",['P4'],"[False, False]"
11.0,2.0,3.0,"['D3', 'G4']",['P4'],"[False, False]"
11.25,2.0,3.0,"['D3', 'G4']",['P4'],"[False, False]"
11.5,2.0,3.0,"['D3', 'G4']",['P4'],"[False, False]"
11.75,2.0,3.0,"['D3', 'G4']",['P4'],"[False, False]"
"""

weirdRhythm = """
**kern	**kern
*part1	*part1
*staff2	*staff1
*I"Piano	*
*I'Pno.	*
*clefF4	*clefG2
*k[]	*k[]
*M6/8	*M6/8
*MM180	*MM180
=1	=1
*^	*
*	*	*^
4r	2.c	4.r	4.r
[8e	.	.	.
4.e]	.	8r	4.g
.	.	4cc	.
=2	=2	=2	=2
8r	2.B	4.r	4.r
[4f	.	.	.
4.f]	.	4r	4.g
.	.	8dd	.
*	*	*v	*v
*v	*v	*
=3	=3
2.c 2.e	2.g 2.cc
=:|!	=:|!
*-	*-
!!!system-decoration: {(s1,s2)}
"""

weirdRhythmInitialDataFrame = """
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,1.0,1,['C4'],[],[True]
1.0,0.5,1,"['C4', 'E4']",['M3'],"[False, True]"
1.5,0.5,1,"['C4', 'E4', 'G4']","['M3', 'P5']","[False, False, True]"
2.0,1.0,1,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P1']","[False, False, False, True]"
3.0,0.5,2,['B3'],[],[True]
3.5,1.0,2,"['B3', 'F4']",['d5'],"[False, True]"
4.5,1.0,2,"['B3', 'F4', 'G4']","['d5', 'm6']","[False, False, True]"
5.5,0.5,2,"['B3', 'F4', 'G4', 'D5']","['d5', 'm6', 'm3']","[False, False, False, True]"
6.0,3.0,3,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P1']","[True, True, True, True]"
"""

weirdRhythmReindexDataFrame = """
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,1.0,1.0,['C4'],[],[True]
0.25,1.0,1.0,['C4'],[],[False]
0.5,1.0,1.0,['C4'],[],[False]
0.75,1.0,1.0,['C4'],[],[False]
1.0,0.5,1.0,"['C4', 'E4']",['M3'],"[False, True]"
1.25,0.5,1.0,"['C4', 'E4']",['M3'],"[False, False]"
1.5,0.5,1.0,"['C4', 'E4', 'G4']","['M3', 'P5']","[False, False, True]"
1.75,0.5,1.0,"['C4', 'E4', 'G4']","['M3', 'P5']","[False, False, False]"
2.0,1.0,1.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P1']","[False, False, False, True]"
2.25,1.0,1.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P1']","[False, False, False, False]"
2.5,1.0,1.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P1']","[False, False, False, False]"
2.75,1.0,1.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P1']","[False, False, False, False]"
3.0,0.5,2.0,['B3'],[],[True]
3.25,0.5,2.0,['B3'],[],[False]
3.5,1.0,2.0,"['B3', 'F4']",['d5'],"[False, True]"
3.75,1.0,2.0,"['B3', 'F4']",['d5'],"[False, False]"
4.0,1.0,2.0,"['B3', 'F4']",['d5'],"[False, False]"
4.25,1.0,2.0,"['B3', 'F4']",['d5'],"[False, False]"
4.5,1.0,2.0,"['B3', 'F4', 'G4']","['d5', 'm6']","[False, False, True]"
4.75,1.0,2.0,"['B3', 'F4', 'G4']","['d5', 'm6']","[False, False, False]"
5.0,1.0,2.0,"['B3', 'F4', 'G4']","['d5', 'm6']","[False, False, False]"
5.25,1.0,2.0,"['B3', 'F4', 'G4']","['d5', 'm6']","[False, False, False]"
5.5,0.5,2.0,"['B3', 'F4', 'G4', 'D5']","['d5', 'm6', 'm3']","[False, False, False, True]"
5.75,0.5,2.0,"['B3', 'F4', 'G4', 'D5']","['d5', 'm6', 'm3']","[False, False, False, False]"
6.0,3.0,3.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P1']","[True, True, True, True]"
6.25,3.0,3.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P1']","[False, False, False, False]"
6.5,3.0,3.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P1']","[False, False, False, False]"
6.75,3.0,3.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P1']","[False, False, False, False]"
7.0,3.0,3.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P1']","[False, False, False, False]"
7.25,3.0,3.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P1']","[False, False, False, False]"
7.5,3.0,3.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P1']","[False, False, False, False]"
7.75,3.0,3.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P1']","[False, False, False, False]"
8.0,3.0,3.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P1']","[False, False, False, False]"
8.25,3.0,3.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P1']","[False, False, False, False]"
8.5,3.0,3.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P1']","[False, False, False, False]"
8.75,3.0,3.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P1']","[False, False, False, False]"
"""

haydnOp20no4iAnnotation = """
Composer: Haydn, Franz Joseph
Title: String Quartet in D Major - No.1: Allegro di molto
Analyst: Néstor Nápoles López, https://doi.org/10.5281/zenodo.1095617
Proofreader: Automated translation from **harm to RomanText

Time Signature: 3/4

m1 a: i
m3 Ger7
m5 V b3 viio/V
m6 V b3 V2
m7 A: I6
m8 V
m9 I b2 IV b3 viio/V
m10 V
m11 I
m12 ii
m13 V2 b3 I6
m14 V7 b3 I
m15 V2 b3 I6
m16 V7 b3 I
m17 ii65
m18 V2
m19 I6
m20 IV
m21 ii6
m22 I6
m25 V43
m27 I6
m28 b3 I6
m29 V43 b3 I
m30 ii6 b3 V7
m31 I
"""

texturizedHaydnOp20No4i = """
**kern
*clefG2
*k[]
*M4/4
=1
2.a 2.cc 2.ee
[4a [4cc [4ee
=2
2a] 2cc] 2ee]
[2dd#X [2ff [2aa [2ccc
=3
4dd#] 4ff] 4aa] 4ccc]
2.dd#X 2.ff 2.aa 2.ccc
=4
8bb
4ee
8gg#X
4dd#X 4ff#X 4aa
[4ee [4gg# [4bb
=5
4ee] 4gg#] 4bb]
8ddnL
8eeJ 8gg#X 8bb
[2cc#X [2ee [2aa
=6
4cc#] 4ee] 4aa]
2.ee 2.gg#X 2.bb
=7
16aLL
16ee
16cc#X
16eeJJ
8ddL
8ff#XJ 8aa
4dd#X 4ff# 4aa
[4ee [4gg#X [4bb
=8
2ee] 2gg#] 2bb]
[2a [2cc#X [2ee
=9
4a] 4cc#] 4ee]
2.b 2.dd 2.ff#X
=10
8bb
4dd 4ee 4gg#X
8dd 8ee 8gg#
4cc#X 4ee 4aa
8eeL
8dddJ
=11
8gg#XL
8bbJ
16aLL
16ee
16cc#X
16eeJJ
8bbL
16ddL
16gg#JJ
16eeLL
16gg#J
8ddJ 8ee 8gg#
=12
16cc#XLL
16aa
16ee
16aaJJ
2ee 2gg#X 2bb 2ddd
4a 4cc# 4ee
=13
2.dd 2.ff#X 2.aa 2.bb
[4dd [4ee [4gg#X [4bb
=14
2dd] 2ee] 2gg#] 2bb]
[2cc#X [2ee [2aa
=15
4cc#] 4ee] 4aa]
2.dd 2.ff#X 2.aa
=16
2.dd 2.ff#X 2.bb
[4cc#X [4ee [4aa
=17
2cc#] 2ee] 2aa]
[2cc#X [2ee [2aa
=18
4cc#] 4ee] 4aa]
2.cc#X 2.ee 2.aa
=19
2.b 2.dd 2.ee 2.gg#X
[4b [4dd [4ee [4gg#
=20
2b] 2dd] 2ee] 2gg#]
[2cc#X [2ee [2aa
=21
4cc#] 4ee] 4aa]
8cc#XL
8aaJ
8eeL
8aaJ
16cc#LL
16aa
16ee
16aaJJ
=22
8gg#X
4b 4dd 4ee
8b 8dd 8ee
8aL
8cc#XJ 8ee
8bbL
[8ddJ
=23
8ddL]
8ff#XJ
16eeLL
16ddd
16gg#X
16bbJJ
[2a [2cc#X [2ee
=24
4a] 4cc#] 4ee]
==
*-
"""


def _load_dfgt(csvGT):
    csvGTF = io.StringIO(csvGT)
    dfGT = pd.read_csv(csvGTF)
    dfGT.set_index("s_offset", inplace=True)
    for col in AugmentedNet.score_parser.S_LISTTYPE_COLUMNS:
        dfGT[col] = dfGT[col].apply(eval)
    return dfGT


class TestScoreParser(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_octave_initial_dataframe(self):
        dfGT = _load_dfgt(octaveTestInitialDataFrame)
        s = AugmentedNet.score_parser._m21Parse(octaveTest)
        df = AugmentedNet.score_parser._initialDataFrame(s)
        for rowGT, row in zip(dfGT.itertuples(), df.itertuples()):
            with self.subTest(gt_index=rowGT.Index, index=row.Index):
                self.assertEqual(rowGT._asdict(), row._asdict())

    def test_octave_reindexed_dataframe(self):
        dfGT = _load_dfgt(octaveTestReindexDataFrame)
        s = AugmentedNet.score_parser._m21Parse(octaveTest)
        df = AugmentedNet.score_parser._initialDataFrame(s)
        df = AugmentedNet.score_parser._reindexDataFrame(df, fixedOffset=0.25)
        for rowGT, row in zip(dfGT.itertuples(), df.itertuples()):
            with self.subTest(gt_index=rowGT.Index, index=row.Index):
                self.assertEqual(rowGT._asdict(), row._asdict())

    def test_weird_rhythm_initial_dataframe(self):
        dfGT = _load_dfgt(weirdRhythmInitialDataFrame)
        s = AugmentedNet.score_parser._m21Parse(weirdRhythm)
        df = AugmentedNet.score_parser._initialDataFrame(s)
        for rowGT, row in zip(dfGT.itertuples(), df.itertuples()):
            with self.subTest(gt_index=rowGT.Index, index=row.Index):
                self.assertEqual(rowGT._asdict(), row._asdict())

    def test_weird_rhythm_reindexed_dataframe(self):
        dfGT = _load_dfgt(weirdRhythmReindexDataFrame)
        s = AugmentedNet.score_parser._m21Parse(weirdRhythm)
        df = AugmentedNet.score_parser._initialDataFrame(s)
        df = AugmentedNet.score_parser._reindexDataFrame(df, fixedOffset=0.25)
        for rowGT, row in zip(dfGT.itertuples(), df.itertuples()):
            with self.subTest(gt_index=rowGT.Index, index=row.Index):
                self.assertEqual(rowGT._asdict(), row._asdict())

    def test_parse_annotation_as_score(self):
        # The texturization is random, thus, set the seed here
        random.seed(1337)
        df = AugmentedNet.score_parser.parseAnnotationAsScore(
            haydnOp20no4iAnnotation, texturize=True, eventBased=True
        )
        # This test is somewhat cheating, but I prefer the higher coverage
        # render the df into a m21 score, then compare scores (gt, generated)
        s = AugmentedNet.score_parser._engraveScore(df)
        s = s.makeNotation()
        gt = music21.converter.parse(texturizedHaydnOp20No4i, fmt="humdrum")
        for c1, c2 in zip(s.chordify().flat.notes, gt.chordify().flat.notes):
            with self.subTest(c1=c1, c2=c2):
                self.assertEqual(c1.pitchNames, c2.pitchNames)


if __name__ == "__main__":
    unittest.main()
