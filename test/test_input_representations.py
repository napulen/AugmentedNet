import io
import re
import unittest

from music21.interval import Interval
import numpy as np
import pandas as pd

from AugmentedNet.input_representations import (
    BassChromagram38,
    BassChromagram70,
    BassIntervals58,
    MeasureNoteOnset14,
    Intervals19,
)
from AugmentedNet.joint_parser import J_LISTTYPE_COLUMNS

from test import AuxiliaryFiles

aux = AuxiliaryFiles("input_representations")


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


class TestMeasureNoteOnset14(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.df = _load_dfgt(aux.haydn)
        self.timesteps = len(self.df.index)
        self.transpositions = ["m2", "M6", "P5", "d7"]

    def test_encoding(self):
        encoding = MeasureNoteOnset14(self.df).array
        encodingGT = np.loadtxt(aux.haydnMeasureNoteOnset14GT, dtype="i1")
        for timestep in range(self.timesteps):
            with self.subTest(timestep=timestep):
                ar = np.nonzero(encoding[timestep])
                arGT = np.nonzero(encodingGT[timestep])
                self.assertEqual(tuple(ar[0]), tuple(arGT[0]))

    def test_decoding(self):
        encoding = MeasureNoteOnset14(self.df).array
        decoded = MeasureNoteOnset14.decode(encoding)
        decodedGT = aux.haydnMeasureNoteOnset14DecodedGT
        decodedGT = [(tuple(t[0]), tuple(t[1])) for t in decodedGT]
        for timestep in range(self.timesteps):
            with self.subTest(timestep=timestep):
                self.assertEqual(decoded[timestep], decodedGT[timestep])


class TestBassChromagram38(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.df = _load_dfgt(aux.haydn)
        self.timesteps = len(self.df.index)
        self.transpositions = ["m2", "M6", "P5", "d7"]

    def test_encoding(self):
        encoding = BassChromagram38(self.df).array
        encodingGT = np.loadtxt(aux.haydnBassChromagram38GT, dtype="i1")
        for timestep in range(self.timesteps):
            with self.subTest(timestep=timestep):
                ar = np.nonzero(encoding[timestep])
                arGT = np.nonzero(encodingGT[timestep])
                self.assertEqual(tuple(ar[0]), tuple(arGT[0]))

    def test_decoding(self):
        encoding = BassChromagram38(self.df).array
        decoded = BassChromagram38.decode(encoding)
        decodedGT = aux.haydnBassChromagram38DecodedGT
        for timestep in range(self.timesteps):
            decodedGT[timestep][2] = tuple(decodedGT[timestep][2])
            decodedGT[timestep][3] = tuple(decodedGT[timestep][3])
            with self.subTest(timestep=timestep):
                self.assertEqual(
                    tuple(decoded[timestep]), tuple(decodedGT[timestep])
                )

    def test_data_augmentation(self):
        bc38 = BassChromagram38(self.df)
        daArray = bc38.array
        daGT = np.loadtxt(aux.haydnBassChromagram38DA, dtype="i8")
        for idx, da in enumerate(
            bc38.dataAugmentation(intervals=self.transpositions)
        ):
            daArray += (idx + 2) * da
        for timestep, (gt, x) in enumerate(zip(daArray, daGT)):
            with self.subTest(timestep=timestep):
                self.assertEqual(gt.tolist(), x.tolist())


class TestBassIntervals58(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.df = _load_dfgt(aux.haydn)
        self.timesteps = len(self.df.index)
        self.transpositions = ["m2", "M6", "P5", "d7"]

    def test_encoding(self):
        encoding = BassIntervals58(self.df).array
        encodingGT = np.loadtxt(aux.haydnBassIntervals58GT, dtype="i1")
        for timestep in range(self.timesteps):
            with self.subTest(timestep=timestep):
                ar = np.nonzero(encoding[timestep])
                arGT = np.nonzero(encodingGT[timestep])
                self.assertEqual(tuple(ar[0]), tuple(arGT[0]))

    def test_decoding(self):
        encoding = BassIntervals58(self.df).array
        decoded = BassIntervals58.decode(encoding)
        for timestep, (gt, x) in enumerate(zip(self.df.s_intervals, decoded)):
            with self.subTest(timestep=timestep):
                self.assertEqual(set(gt), set(x[2]))

    def test_data_augmentation(self):
        bi63 = BassIntervals58(self.df)
        daArray = bi63.array
        daGT = np.loadtxt(aux.haydnBassIntervals58DA, dtype="i8")
        for idx, da in enumerate(
            bi63.dataAugmentation(intervals=self.transpositions)
        ):
            daArray += (idx + 2) * da
        for timestep, (gt, x) in enumerate(zip(daArray, daGT)):
            with self.subTest(timestep=timestep):
                self.assertEqual(gt.tolist(), x.tolist())


class TestIntervals19(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.df = _load_dfgt(aux.haydn)
        self.timesteps = len(self.df.index)
        self.transpositions = ["m2", "M6", "P5", "d7"]

    def test_encoding(self):
        encoding = Intervals19(self.df).array
        encodingGT = np.loadtxt(aux.haydnIntervals19GT, dtype="i1")
        for timestep in range(self.timesteps):
            with self.subTest(timestep=timestep):
                ar = np.nonzero(encoding[timestep])
                arGT = np.nonzero(encodingGT[timestep])
                self.assertEqual(tuple(ar[0]), tuple(arGT[0]))

    def test_decoding(self):
        encoding = Intervals19(self.df).array
        decoded = Intervals19.decode(encoding)
        for timestep, (gt, x) in enumerate(zip(self.df.s_intervals, decoded)):
            intervals = [Interval(i) for i in gt]
            generics = [i.generic.simpleUndirected for i in intervals]
            generics = tuple(sorted(set(generics)))
            chromatics = [i.semitones for i in intervals]
            chromatics = tuple(sorted(set(chromatics)))
            with self.subTest(timestep=timestep):
                self.assertEqual((generics, chromatics), x)

    # def test_data_augmentation(self):
    #     TODO: but it should be transposition invariant


class TestBassChromagram70(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.df = _load_dfgt(aux.haydn)
        self.timesteps = len(self.df.index)
        self.transpositions = ["m2", "M6", "P5", "d7"]

    def test_encoding(self):
        encoding = BassChromagram70(self.df).array
        encodingGT = np.loadtxt(aux.haydnBassChromagram70GT, dtype="i1")
        for timestep in range(self.timesteps):
            with self.subTest(timestep=timestep):
                ar = np.nonzero(encoding[timestep])
                arGT = np.nonzero(encodingGT[timestep])
                self.assertEqual(tuple(ar[0]), tuple(arGT[0]))

    def test_decoding(self):
        encoding = BassChromagram70(self.df).array
        decoded = BassChromagram70.decode(encoding)
        for timestep, (gt, x) in enumerate(zip(self.df.s_notes, decoded)):
            notes = [re.sub(r"\d", "", n) for n in gt]
            bassGT, chromagramGT = notes[0], set(sorted(notes))
            bass, chromagram = x[0], set(x[1])
            with self.subTest(timestep=timestep):
                self.assertEqual((bassGT, chromagramGT), (bass, chromagram))

    def test_data_augmentation(self):
        bc70 = BassChromagram70(self.df)
        daArray = bc70.array
        daGT = np.loadtxt(aux.haydnBassChromagram70DA, dtype="i8")
        for idx, da in enumerate(
            bc70.dataAugmentation(intervals=self.transpositions)
        ):
            daArray += (idx + 2) * da
        for timestep, (gt, x) in enumerate(zip(daArray, daGT)):
            with self.subTest(timestep=timestep):
                self.assertEqual(gt.tolist(), x.tolist())
