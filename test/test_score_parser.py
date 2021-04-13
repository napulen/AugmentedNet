import unittest
import io
import score_parser
import pandas as pd

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
9.625,0.125,3,"['G3', 'G4']",['P8'],"[True, False]"
9.75,0.125,3,"['F3', 'F#4']",['A8'],"[True, True]"
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
9.75,0.125,3.0,"['F3', 'F#4']",['A8'],"[True, True]"
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
2.0,1.0,1,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P8']","[False, False, False, True]"
3.0,0.5,2,['B3'],[],[True]
3.5,1.0,2,"['B3', 'F4']",['d5'],"[False, True]"
4.5,1.0,2,"['B3', 'F4', 'G4']","['d5', 'm6']","[False, False, True]"
5.5,0.5,2,"['B3', 'F4', 'G4', 'D5']","['d5', 'm6', 'm3']","[False, False, False, True]"
6.0,3.0,3,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P8']","[True, True, True, True]"
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
2.0,1.0,1.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P8']","[False, False, False, True]"
2.25,1.0,1.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P8']","[False, False, False, False]"
2.5,1.0,1.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P8']","[False, False, False, False]"
2.75,1.0,1.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P8']","[False, False, False, False]"
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
6.0,3.0,3.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P8']","[True, True, True, True]"
6.25,3.0,3.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P8']","[False, False, False, False]"
6.5,3.0,3.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P8']","[False, False, False, False]"
6.75,3.0,3.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P8']","[False, False, False, False]"
7.0,3.0,3.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P8']","[False, False, False, False]"
7.25,3.0,3.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P8']","[False, False, False, False]"
7.5,3.0,3.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P8']","[False, False, False, False]"
7.75,3.0,3.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P8']","[False, False, False, False]"
8.0,3.0,3.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P8']","[False, False, False, False]"
8.25,3.0,3.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P8']","[False, False, False, False]"
8.5,3.0,3.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P8']","[False, False, False, False]"
8.75,3.0,3.0,"['C4', 'E4', 'G4', 'C5']","['M3', 'P5', 'P8']","[False, False, False, False]"
"""


def _load_dfgt(csvGT):
    csvGTF = io.StringIO(csvGT)
    dfGT = pd.read_csv(csvGTF)
    dfGT.set_index("s_offset", inplace=True)
    for col in score_parser.S_LISTTYPE_COLUMNS:
        # if col == "s_intervals":
        #     continue
        dfGT[col] = dfGT[col].apply(eval)
    return dfGT


class TestScoreParser(unittest.TestCase):
    def test_octave_initial_dataframe(self):
        dfGT = _load_dfgt(octaveTestInitialDataFrame)
        s = score_parser._m21Parse(octaveTest)
        df = score_parser._initialDataFrame(s)
        for rowGT, row in zip(dfGT.itertuples(), df.itertuples()):
            with self.subTest(gt_index=rowGT.Index, index=row.Index):
                self.assertEqual(rowGT._asdict(), row._asdict())

    def test_octave_reindexed_dataframe(self):
        dfGT = _load_dfgt(octaveTestReindexDataFrame)
        s = score_parser._m21Parse(octaveTest)
        df = score_parser._initialDataFrame(s)
        df = score_parser._reindexDataFrame(df)
        for rowGT, row in zip(dfGT.itertuples(), df.itertuples()):
            with self.subTest(gt_index=rowGT.Index, index=row.Index):
                self.assertEqual(rowGT._asdict(), row._asdict())

    def test_weird_rhythm_initial_dataframe(self):
        dfGT = _load_dfgt(weirdRhythmInitialDataFrame)
        s = score_parser._m21Parse(weirdRhythm)
        df = score_parser._initialDataFrame(s)
        for rowGT, row in zip(dfGT.itertuples(), df.itertuples()):
            with self.subTest(gt_index=rowGT.Index, index=row.Index):
                self.assertEqual(rowGT._asdict(), row._asdict())

    def test_weird_rhythm_reindexed_dataframe(self):
        dfGT = _load_dfgt(weirdRhythmReindexDataFrame)
        s = score_parser._m21Parse(weirdRhythm)
        df = score_parser._initialDataFrame(s)
        df = score_parser._reindexDataFrame(df)
        for rowGT, row in zip(dfGT.itertuples(), df.itertuples()):
            with self.subTest(gt_index=rowGT.Index, index=row.Index):
                self.assertEqual(rowGT._asdict(), row._asdict())


if __name__ == "__main__":
    unittest.main()