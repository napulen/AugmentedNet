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
offset,measure,notes,isOnset
0.0,1,"['C0', 'B0']","[True, True]"
0.25,1,"['C1', 'B1']","[True, True]"
0.5,1,"['C2', 'B2']","[True, True]"
0.75,1,"['C3', 'B3']","[True, True]"
1.0,1,"['C2', 'B2']","[True, True]"
1.25,1,"['C3', 'B3']","[True, True]"
1.5,1,"['C4', 'B4']","[True, True]"
1.75,1,"['C5', 'B5']","[True, True]"
2.0,1,"['C4', 'B4']","[True, True]"
2.25,1,"['C5', 'B5']","[True, True]"
2.5,1,"['C6', 'B6']","[True, True]"
2.75,1,"['C7', 'B7']","[True, True]"
3.0,1,"['C6', 'B6']","[True, True]"
3.25,1,"['C7', 'B7']","[True, True]"
3.5,1,"['C8', 'B8']","[True, True]"
4.0,2,"['C1', 'B7']","[True, True]"
5.0,2,"['C2', 'B6']","[True, True]"
6.0,2,"['C3', 'B5']","[True, True]"
7.0,2,"['C4', 'B4']","[True, True]"
8.0,3,['C4'],[True]
8.25,3,"['B3', 'D4']","[True, True]"
8.5,3,"['A3', 'E4']","[True, True]"
8.75,3,"['G3', 'F4']","[True, True]"
9.0,3,"['F3', 'G4']","[True, True]"
9.125,3,"['E3', 'G4']","[True, False]"
9.25,3,"['F3', 'A4']","[True, True]"
9.375,3,"['G3', 'A4']","[True, False]"
9.5,3,"['A3', 'G4']","[True, True]"
9.625,3,"['G3', 'G4']","[True, False]"
9.75,3,"['F3', 'F#4']","[True, True]"
9.875,3,"['E3', 'F#4']","[True, False]"
10.0,3,"['D3', 'G4']","[True, True]"
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
4r	2.c	4.r
[8e	.	.
*	*	*^
4.e]	.	8r	4.g
.	.	4cc	.
*	*	*v	*v
=2	=2	=2
8r	2.B	4.r
[4f	.	.
*	*	*^
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
offset,measure,notes,isOnset
0.0,1,['C4'],[True]
1.0,1,"['C4', 'E4']","[False, True]"
1.5,1,"['C4', 'E4', 'G4']","[False, False, True]"
2.0,1,"['C4', 'E4', 'G4', 'C5']","[False, False, False, True]"
3.0,2,['B3'],[True]
3.5,2,"['B3', 'F4']","[False, True]"
4.5,2,"['B3', 'F4', 'G4']","[False, False, True]"
5.5,2,"['B3', 'F4', 'G4', 'D5']","[False, False, False, True]"
6.0,3,"['C4', 'E4', 'G4', 'C5']","[True, True, True, True]"
"""


def _load_dfdict_gt(gt):
    csvGT = io.StringIO(gt)
    dfGT = pd.read_csv(csvGT)
    dfGT.set_index("offset", inplace=True)
    dfGT["notes"] = dfGT["notes"].apply(eval)
    dfGT["isOnset"] = dfGT["isOnset"].apply(eval)
    dfdictGT = dfGT.to_dict()
    return dfdictGT


class TestInitialDataFrame(unittest.TestCase):
    def test_octave(self):
        dfdictGT = _load_dfdict_gt(octaveTestInitialDataFrame)
        s = score_parser._m21Parse(octaveTest)
        df = score_parser._initialDataFrame(s)
        dfdict = df.to_dict()
        for k, vGT in dfdictGT.items():
            for frame, val in vGT.items():
                with self.subTest(property=k, frame=frame):
                    self.assertEqual(vGT[frame], dfdict[k][frame])

    def test_weird_rhythm(self):
        dfdictGT = _load_dfdict_gt(weirdRhythmInitialDataFrame)
        s = score_parser._m21Parse(weirdRhythm)
        df = score_parser._initialDataFrame(s)
        dfdict = df.to_dict()
        for k, vGT in dfdictGT.items():
            for frame, val in vGT.items():
                with self.subTest(property=k, frame=frame):
                    self.assertEqual(vGT[frame], dfdict[k][frame])


if __name__ == "__main__":
    unittest.main()