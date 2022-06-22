import io
import unittest

import numpy as np
import pandas as pd

from AugmentedNet.feature_representation import CHORD_QUALITIES
from AugmentedNet.joint_parser import J_LISTTYPE_COLUMNS
from AugmentedNet.output_representations import (
    Bass35,
    Inversion4,
    RomanNumeral31,
    LocalKey38,
    PrimaryDegree22,
    SecondaryDegree22,
    ChordQuality11,
    ChordRoot35,
    TonicizedKey38,
    HarmonicRhythm7,
    PitchClassSet121,
)

from test import AuxiliaryFiles

aux = AuxiliaryFiles("output_representations")


def _load_dfgt(csvGT):
    dfGT = pd.read_csv(csvGT)
    dfGT.set_index("j_offset", inplace=True)
    for col in J_LISTTYPE_COLUMNS:
        dfGT[col] = dfGT[col].apply(eval)
    return dfGT


def _plot_array(arr):
    import matplotlib.pyplot as plt

    plt.pcolor(arr.T, edgecolors="k", linewidth=1, cmap="tab20")
    plt.show()


def _save(arr):
    np.savetxt("tmp.txt", arr, fmt="%i", delimiter=" ")


def _one_hot_encode(encoding, classList):
    timesteps = len(encoding)
    features = len(classList)
    array = np.zeros((timesteps, features), dtype="i8")
    for t, enc in enumerate(encoding):
        array[t, enc] = 1
    return array


class TestBass35(unittest.TestCase):
    clas = Bass35
    encodingGT = aux.haydnBass35GT
    dfFeature = "a_bass"
    transpositions = ["m2", "M6", "P5", "d7"]

    def setUp(self):
        self.maxDiff = None
        self.df = _load_dfgt(aux.haydn)
        self.timesteps = len(self.df.index)

    def test_encoding(self):
        encoding = self.clas(self.df).array.reshape(-1)
        encodingGT = np.loadtxt(self.encodingGT, dtype="i1")
        encodingGT = np.argmax(encodingGT, axis=1)
        for timestep in range(self.timesteps):
            with self.subTest(timestep=timestep):
                bass = encoding[timestep]
                bassGT = encodingGT[timestep]
                self.assertEqual(bass, bassGT)

    def test_decoding(self):
        encoding = self.clas(self.df).array
        decoded = self.clas.decode(encoding)
        for timestep, (gt, x) in enumerate(
            zip(self.df[self.dfFeature], decoded)
        ):
            with self.subTest(timestep=timestep):
                self.assertEqual(gt, x)

    # def test_data_augmentation(self):
    #     rep = self.clas(self.df)
    #     daArray = np.copy(rep.array)
    #     daGT = np.zeros(rep.shape)
    #     for idx, da in enumerate(
    #         rep.dataAugmentation(intervals=self.transpositions)
    #     ):
    #         daArray += (idx + 2) * da
    #     for timestep, (gt, x) in enumerate(zip(daArray, daGT)):
    #         with self.subTest(timestep=timestep):
    #             self.assertEqual(gt.tolist(), x.tolist())


class TestHarmonicRhythm7(TestBass35):
    clas = HarmonicRhythm7
    encodingGT = aux.haydnHarmonicRhythm7
    dfFeature = "a_harmonicRhythm"


class TestTonicizedKey38(TestBass35):
    clas = TonicizedKey38
    encodingGT = aux.haydnTonicizedKey38
    dfFeature = "a_tonicizedKey"


class TestPcSet94(TestBass35):
    clas = PitchClassSet121
    encodingGT = aux.haydnPitchClassSet121
    dfFeature = "a_pcset"

    # def test_encoding(self):
    #     super().test_encoding()

    # def test_decoding(self):
    #     super().test_decoding()

    # def test_data_augmentation(self):
    #     super().test_data_augmentation()


class TestInversion4(TestBass35):
    clas = Inversion4
    encodingGT = aux.haydnInversion4
    dfFeature = "a_inversion"


class TestRomanNumeral31(TestBass35):
    clas = RomanNumeral31
    encodingGT = aux.haydnRomanNumeral31
    dfFeature = "a_romanNumeral"


class TestLocalKey38(TestBass35):
    clas = LocalKey38
    encodingGT = aux.haydnLocalKey38
    dfFeature = "a_localKey"


class TestPrimaryDegree22(TestBass35):
    clas = PrimaryDegree22
    encodingGT = aux.haydnPrimaryDegree22
    dfFeature = "a_degree1"


class TestSecondaryDegree22(TestBass35):
    clas = SecondaryDegree22
    encodingGT = aux.haydnSecondaryDegree22
    dfFeature = "a_degree2"


class TestChordQuality11(TestBass35):
    clas = ChordQuality11
    encodingGT = aux.haydnChordQuality11
    dfFeature = "a_quality"

    def test_encoding(self):
        super().test_encoding()

    def test_decoding(self):
        super().test_decoding()


class TestChordRoot35(TestBass35):
    clas = ChordRoot35
    encodingGT = aux.haydnChordRoot35
    dfFeature = "a_root"
