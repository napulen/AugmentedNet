import unittest
import music21
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


class ScoreParser(unittest.TestCase):
    def test_octave_test(self):
        notes = [
            ["C0", "B0"],
            ["C1", "B1"],
            ["C2", "B2"],
            ["C3", "B3"],
            #############
            ["C2", "B2"],
            ["C3", "B3"],
            ["C4", "B4"],
            ["C5", "B5"],
            #############
            ["C4", "B4"],
            ["C5", "B5"],
            ["C6", "B6"],
            ["C7", "B7"],
            #############
            ["C6", "B6"],
            ["C7", "B7"],
            ["C8", "B8"],
            #############
            #############
            ["C1", "B7"],
            ["C2", "B6"],
            ["C3", "B5"],
            ["C4", "B4"],
            #############
            #############
            ["C4"],
            ["B3", "D4"],
            ["A3", "E4"],
            ["G3", "F4"],
            #############
            ["F3", "G4"],
            ["E3", "G4"],
            ["F3", "A4"],
            ["G3", "A4"],
            ["A3", "G4"],
            ["G3", "G4"],
            ["F3", "F#4"],
            ["E3", "F#4"],
            ##############
            ["D3", "G4"],
        ]
        ties = [
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            #############
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            #############
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            #############
            [None, None],
            [None, None],
            [None, None],
            #############
            #############
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            #############
            #############
            [None],
            [None, None],
            [None, None],
            [None, None],
            #############
            [None, "start"],
            [None, "stop"],
            [None, "start"],
            [None, "stop"],
            [None, "start"],
            [None, "stop"],
            [None, "start"],
            [None, "stop"],
            ###############
            [None, None],
        ]
        measures = [
            1,
            1,
            1,
            1,
            #
            1,
            1,
            1,
            1,
            #
            1,
            1,
            1,
            1,
            #
            1,
            1,
            1,
            ##
            2,
            2,
            2,
            2,
            ##
            3,
            3,
            3,
            3,
            #
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            #
            3,
        ]
        offsets = [
            0.0,
            0.25,
            0.5,
            0.75,
            #####
            1.0,
            1.25,
            1.5,
            1.75,
            #####
            2.0,
            2.25,
            2.5,
            2.75,
            #####
            3.0,
            3.25,
            3.5,
            #####
            #####
            4.0,
            5.0,
            6.0,
            7.0,
            #####
            8.0,
            8.25,
            8.5,
            8.75,
            #####
            9.0,
            9.125,
            9.25,
            9.375,
            9.5,
            9.625,
            9.75,
            9.875,
            ######
            10.0,
        ]
        dfdictGT = {
            "offset": offsets,
            "measure": measures,
            "notes": notes,
            "ties": ties,
        }
        dfGT = pd.DataFrame(dfdictGT)
        dfdictGT = dfGT.to_dict()
        df = score_parser.parseScore(octaveTest)
        dfdict = df.to_dict()
        for k, vGT in dfdictGT.items():
            for frame, val in vGT.items():
                with self.subTest(property=k, frame=frame):
                    self.assertEqual(vGT[frame], dfdict[k][frame])

if __name__ == '__main__':
    unittest.main()