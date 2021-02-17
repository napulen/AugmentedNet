import unittest
import annotation_parser
import pandas as pd

multipleAnnotations = """
Composer: Néstor Nápoles López
Title: A unit test in C

Time signature: 3/4

m1 b1 C: I b2 ii b3 iii
m2 b1 IV b2 Cad64 b3 V
m3 vi b2 V6 b3 viio65/i
m4 b1 I6 b3 V
m5 b1 c: i b2 iio b3 III
m6 b1 N6 b2 Cad64 b3 V
m7 b1 It6 b3 V
m8 b1 Fr43 b3 V
m9 b1 Ger65
m10 b1 iv
m11 b1 V b3 V
m12 b1 I
"""


class TestInitialDataFrame(unittest.TestCase):
    def test_multiple_annotations(self):
        offsets = [
            0.0,
            1.0,
            2.0,
            ####
            3.0,
            4.0,
            5.0,
            ####
            6.0,
            7.0,
            8.0,
            ####
            9.0,
            11.0,
            ####
            12.0,
            13.0,
            14.0,
            ####
            15.0,
            16.0,
            17.0,
            ####
            18.0,
            20.0,
            ####
            21.0,
            23.0,
            ####
            24.0,
            ####
            27.0,
            ####
            30.0,
            32.0,
            ####
            33.0,
        ]
        measures = [
            1,
            1,
            1,
            2,
            2,
            2,
            3,
            3,
            3,
            4,
            4,
            5,
            5,
            5,
            6,
            6,
            6,
            7,
            7,
            8,
            8,
            9,
            10,
            11,
            11,
            12,
        ]
        durations = [
            1.0,
            1.0,
            1.0,
            ####
            1.0,
            1.0,
            1.0,
            ####
            1.0,
            1.0,
            1.0,
            ####
            2.0,
            1.0,
            ####
            1.0,
            1.0,
            1.0,
            ####
            1.0,
            1.0,
            1.0,
            ####
            2.0,
            1.0,
            ####
            2.0,
            1.0,
            ####
            3.0,
            ####
            3.0,
            ####
            2.0,
            1.0,
            ####
            3.0,
        ]
        areOnsets = [
            True,
            True,
            True,
            ####
            True,
            True,
            True,
            ####
            True,
            True,
            True,
            ####
            True,
            True,
            ####
            True,
            True,
            True,
            ####
            True,
            True,
            True,
            ####
            True,
            True,
            ####
            True,
            True,
            ####
            True,
            ####
            True,
            ####
            True,
            True,
            ####
            True,
        ]
        pitchNames = [
            ("C", "E", "G"),
            ("D", "F", "A"),
            ("E", "G", "B"),
            ################
            ("F", "A", "C"),
            ("G", "C", "E"),
            ("G", "B", "D"),
            ################
            ("A", "C", "E"),
            ("B", "D", "G"),
            ("D", "F", "A-", "B"),
            ################
            ("E", "G", "C"),
            ("G", "B", "D"),
            ################
            ("C", "E-", "G"),
            ("D", "F", "A-"),
            ("E-", "G", "B-"),
            ################
            ("F", "A-", "D-"),
            ("G", "C", "E-"),
            ("G", "B", "D"),
            ################
            ("A-", "C", "F#"),
            ("G", "B", "D"),
            ################
            ("A-", "C", "D", "F#"),
            ("G", "B", "D"),
            ################
            ("A-", "C", "E-", "F#"),
            ################
            ("F", "A-", "C"),
            ################
            ("G", "B", "D"),
            ("G", "B", "D"),
            ################
            ("C", "E", "G"),
        ]
        basses = [
            "C",
            "D",
            "E",
            ####
            "F",
            "G",
            "G",
            ####
            "A",
            "B",
            "D",
            ####
            "E",
            "G",
            ####
            "C",
            "D",
            "E-",
            ####
            "F",
            "G",
            "G",
            ####
            "A-",
            "G",
            ####
            "A-",
            "G",
            ####
            "A-",
            ####
            "F",
            ####
            "G",
            "G",
            ####
            "C",
        ]
        roots = [
            "C",
            "D",
            "E",
            ####
            "F",
            "C",
            "G",
            ####
            "A",
            "G",
            "B",
            ####
            "C",
            "G",
            ####
            "C",
            "D",
            "E-",
            ####
            "D-",
            "C",
            "G",
            ####
            "F#",
            "G",
            ####
            "D",
            "G",
            ####
            "F#",
            ####
            "F",
            ####
            "G",
            "G",
            ####
            "C",
        ]
        inversions = [
            0,
            0,
            0,
            ##
            0,
            2,
            0,
            ##
            0,
            1,
            1,
            ##
            1,
            0,
            ##
            0,
            0,
            0,
            ##
            1,
            2,
            0,
            ##
            1,
            0,
            ##
            2,
            0,
            ##
            1,
            ##
            0,
            ##
            0,
            0,
            ##
            0,
        ]
        qualities = [
            "major triad",
            "minor triad",
            "minor triad",
            ##############
            "major triad",
            "major triad",
            "major triad",
            ##############
            "minor triad",
            "major triad",
            "diminished seventh chord",
            ##############
            "major triad",
            "major triad",
            ##############
            "minor triad",
            "diminished triad",
            "major triad",
            ##############
            "major triad",
            "minor triad",
            "major triad",
            ##############
            "Italian augmented sixth chord",
            "major triad",
            ##############
            "French augmented sixth chord",
            "major triad",
            ##############
            "German augmented sixth chord",
            ##############
            "minor triad",
            ##############
            "major triad",
            "major triad",
            "major triad",
        ]
        pcsets = [
            (0, 4, 7),
            (2, 5, 9),
            (4, 7, 11),
            ##########
            (0, 5, 9),
            (0, 4, 7),
            (2, 7, 11),
            ##########
            (0, 4, 9),
            (2, 7, 11),
            (2, 5, 8, 11),
            ##########
            (0, 4, 7),
            (2, 7, 11),
            ##########
            (0, 3, 7),
            (2, 5, 8),
            (3, 7, 10),
            ##########
            (1, 5, 8),
            (0, 3, 7),
            (2, 7, 11),
            ##########
            (0, 6, 8),
            (2, 7, 11),
            ##########
            (0, 2, 6, 8),
            (2, 7, 11),
            ##########
            (0, 3, 6, 8),
            ##########
            (0, 5, 8),
            ##########
            (2, 7, 11),
            (2, 7, 11),
            ##########
            (0, 4, 7),
        ]
        localKeys = [
            "C",
            "C",
            "C",
            ####
            "C",
            "C",
            "C",
            ####
            "C",
            "C",
            "C",
            ####
            "C",
            "C",
            ####
            "c",
            "c",
            "c",
            ####
            "c",
            "c",
            "c",
            ####
            "c",
            "c",
            ####
            "c",
            "c",
            ####
            "c",
            ####
            "c",
            ####
            "c",
            "c",
            ####
            "c",
        ]
        tonicizedKeys = [
            None,
            None,
            None,
            #####
            None,
            None,
            None,
            #####
            None,
            None,
            "c",
            #####
            None,
            None,
            #####
            None,
            None,
            None,
            #####
            None,
            None,
            None,
            #####
            None,
            None,
            #####
            None,
            None,
            #####
            None,
            #####
            None,
            #####
            None,
            None,
            #####
            None,
        ]
        degrees = [
            "1",
            "2",
            "3",
            ####
            "4",
            "1",
            "5",
            ####
            "6",
            "5",
            "7/1",
            ####
            "1",
            "5",
            ####
            "1",
            "2",
            "3",
            ####
            "2",
            "1",
            "5",
            ####
            "4",
            "5",
            ####
            "2",
            "5",
            ####
            "4",
            ####
            "4",
            ####
            "5",
            "5",
            ####
            "1",
        ]
        dfdictGT = {
            "offset": offsets,
            "measure": measures,
            "duration": durations,
            "isOnset": areOnsets,
            "pitchNames": pitchNames,
            "bass": basses,
            "root": roots,
            "inversion": inversions,
            "quality": qualities,
            "pcset": pcsets,
            "localKey": localKeys,
            "tonicizedKey": tonicizedKeys,
            "degree": degrees,
        }
        dfGT = pd.DataFrame(dfdictGT)
        dfGT.set_index("offset", inplace=True)
        dfdictGT = dfGT.to_dict()
        df = annotation_parser._initialDataFrame(multipleAnnotations)
        dfdict = df.to_dict()
        for k, vGT in dfdictGT.items():
            for frame, val in vGT.items():
                with self.subTest(property=k, frame=frame):
                    self.assertEqual(vGT[frame], dfdict[k][frame])


if __name__ == "__main__":
    unittest.main()