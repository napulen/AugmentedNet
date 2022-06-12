"""Tonal representations used as inputs to the network."""

import numpy as np
import re

from .cache import (
    TransposePitch,
    m21Pitch,
    m21IntervalStr,
)
from .feature_representation import (
    INTERVALCLASSES,
    NOTEDURATIONS,
    NOTENAMES,
    PITCHCLASSES,
    SPELLINGS,
    FeatureRepresentation,
    FeatureRepresentationTI,
)

# NOTENAMEDEFAULTCLASS = {
#     "C": 0,
#     "D": 2,
#     "E": 4,
#     "F": 5,
#     "G": 7,
#     "A": 9,
#     "B": 11,
# }
# def _solvePitchSpelling(noteNames, pitchClasses):
#     if len(noteNames) != len(pitchClasses):
#         raise Exception
#     if not noteNames:
#         return
#     elif len(noteNames) == 1:
#     note = noteNames[0]
#     default = NOTENAMEDEFAULTCLASS[note]
#     bestMatch = 999999
#     for pc in pitchClasses:
#         diff = pc -


class Duration14(FeatureRepresentationTI):
    features = 2 * len(NOTEDURATIONS)
    pattern = [
        [1, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],  # eight
        [0, 1, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],  # quarter
        [0, 1, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 1, 1, 0, 1, 0, 0],
        [0, 0, 0, 1, 1, 0, 0],
        [0, 1, 0, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0],  # half
        [0, 1, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 1, 0],
        [0, 1, 1, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0],
        [0, 0, 1, 1, 0, 1, 0],
        [0, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 1, 0],
        [0, 1, 0, 0, 1, 1, 0],
        [0, 0, 1, 0, 1, 1, 0],
        [0, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 0],
        [0, 1, 0, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 1],  # whole
        [0, 1, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0, 1],
        [0, 1, 1, 0, 0, 0, 1],
        [0, 0, 0, 1, 0, 0, 1],
        [0, 1, 0, 1, 0, 0, 1],
        [0, 0, 1, 1, 0, 0, 1],
        [0, 1, 1, 1, 0, 0, 1],
        [0, 0, 0, 0, 1, 0, 1],
        [0, 1, 0, 0, 1, 0, 1],
        [0, 0, 1, 0, 1, 0, 1],
        [0, 1, 1, 0, 1, 0, 1],
        [0, 0, 0, 1, 1, 0, 1],
        [0, 1, 0, 1, 1, 0, 1],
        [0, 0, 1, 1, 1, 0, 1],
        [0, 1, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 1, 1],
        [0, 1, 0, 0, 0, 1, 1],
        [0, 0, 1, 0, 0, 1, 1],
        [0, 1, 1, 0, 0, 1, 1],
        [0, 0, 0, 1, 0, 1, 1],
        [0, 1, 0, 1, 0, 1, 1],
        [0, 0, 1, 1, 0, 1, 1],
        [0, 1, 1, 1, 0, 1, 1],
        [0, 0, 0, 0, 1, 1, 1],
        [0, 1, 0, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 1, 1],
        [0, 1, 1, 0, 1, 1, 1],
        [0, 0, 0, 1, 1, 1, 1],
        [0, 1, 0, 1, 1, 1, 1],
        [0, 0, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1],
    ]

    def run(self, transposition=None):
        array = np.zeros(self.shape, dtype=self.dtype)
        prev_measure = -1
        idx = 0
        for frame, measure in enumerate(self.df.s_measure):
            if measure != prev_measure:
                idx = 0
                prev_measure = measure
            pattern = self.pattern[idx]
            array[frame, 0:7] = pattern
            idx += 1
        idx = 0
        for frame, onset in enumerate(self.df.s_isOnset):
            if sum(onset) > 0:
                idx = 0
            pattern = self.pattern[idx]
            array[frame, 7:] = pattern
            idx += 1
        return array

    @classmethod
    def decode(cls, array):
        if len(array.shape) != 2 or array.shape[1] != cls.features:
            raise IndexError("Strange array shape.")
        ret = []
        for manyhot in array:
            measureOnset = [
                NOTEDURATIONS[x] for x in np.nonzero(manyhot[:7])[0]
            ]
            noteOnset = [NOTEDURATIONS[x] for x in np.nonzero(manyhot[7:])[0]]
            ret.append((tuple(measureOnset), tuple(noteOnset)))
        return ret


class Bass19(FeatureRepresentation):
    features = len(NOTENAMES) + len(PITCHCLASSES)

    def run(self, transposition="P1"):
        array = np.zeros(self.shape, dtype=self.dtype)
        for frame, notes in enumerate(self.df.s_notes):
            bass = notes[0]
            transposed = TransposePitch(bass, transposition)
            pitchObj = m21Pitch(transposed)
            pitchLetter = pitchObj.step
            pitchLetterIndex = NOTENAMES.index(pitchLetter)
            pitchClass = pitchObj.pitchClass
            array[frame, pitchLetterIndex] = 1
            array[frame, pitchClass + len(NOTENAMES)] = 1
        return array

    @classmethod
    def decode(cls, array):
        if len(array.shape) != 2 or array.shape[1] != cls.features:
            raise IndexError("Strange array shape.")
        ret = []
        for manyhot in array:
            bassPitchName = NOTENAMES[np.argmax(manyhot[:7])]
            bassPitchClass = np.argmax(manyhot[7:19])
            ret.append((bassPitchName, bassPitchClass))
        return ret


class Chromagram19(FeatureRepresentation):
    features = len(NOTENAMES) + len(PITCHCLASSES)

    def run(self, transposition="P1"):
        array = np.zeros(self.shape, dtype=self.dtype)
        for frame, notes in enumerate(self.df.s_notes):
            for note in notes:
                transposedNote = TransposePitch(note, transposition)
                pitchObj = m21Pitch(transposedNote)
                pitchLetter = pitchObj.step
                pitchLetterIndex = NOTENAMES.index(pitchLetter)
                pitchClass = pitchObj.pitchClass
                array[frame, pitchLetterIndex] = 1
                array[frame, pitchClass + len(NOTENAMES)] = 1
        return array

    @classmethod
    def decode(cls, array):
        if len(array.shape) != 2 or array.shape[1] != cls.features:
            raise IndexError("Strange array shape.")
        ret = []
        for manyhot in array:
            chromagramPitchNames = [
                NOTENAMES[x] for x in np.nonzero(manyhot[:7])[0]
            ]
            chromagramPitchClasses = np.nonzero(manyhot[7:])[0].tolist()
            ret.append(
                (tuple(chromagramPitchNames), tuple(chromagramPitchClasses))
            )
        return ret


class Intervals19(FeatureRepresentationTI):
    features = len(NOTENAMES) + len(PITCHCLASSES)

    def run(self):
        array = np.zeros(self.shape, dtype=self.dtype)
        for frame, intervals in enumerate(self.df.s_intervals):
            for interval in intervals:
                intervalObj = m21IntervalStr(interval)
                chromatic = intervalObj.chromatic.mod12
                genericClass = intervalObj.generic.simpleUndirected - 1
                array[frame, genericClass] = 1
                array[frame, chromatic + len(NOTENAMES)] = 1
        return array

    @classmethod
    def decode(cls, array):
        if len(array.shape) != 2 or array.shape[1] != cls.features:
            raise IndexError("Strange array shape.")
        ret = []
        for manyhot in array:
            generics = (np.nonzero(manyhot[:7])[0] + 1).tolist()
            chromatics = np.nonzero(manyhot[7:])[0].tolist()
            ret.append((tuple(generics), tuple(chromatics)))
        return ret


class Intervals39(FeatureRepresentationTI):
    features = len(INTERVALCLASSES)

    def run(self):
        array = np.zeros(self.shape, dtype=self.dtype)
        for frame, intervals in enumerate(self.df.s_intervals):
            for interval in intervals:
                intervalIndex = INTERVALCLASSES.index(interval)
                array[frame, intervalIndex] = 1
        return array

    @classmethod
    def decode(cls, array):
        if len(array.shape) != 2 or array.shape[1] != cls.features:
            raise IndexError("Strange array shape.")
        ret = []
        for manyhot in array:
            intervals = [INTERVALCLASSES[x] for x in np.nonzero(manyhot)[0]]
            ret.append(tuple(intervals))
        return ret


class Bass35(FeatureRepresentation):
    features = len(SPELLINGS)

    def run(self, transposition="P1"):
        array = np.zeros(self.shape, dtype=self.dtype)
        for frame, notes in enumerate(self.df.s_notes):
            bass = re.sub(r"\d", "", notes[0])
            transposed = TransposePitch(bass, transposition)
            if transposed in SPELLINGS:
                spellingIndex = SPELLINGS.index(transposed)
                array[frame, spellingIndex] = 1
        return array

    @classmethod
    def decode(cls, array):
        if len(array.shape) != 2 or array.shape[1] != len(SPELLINGS):
            raise IndexError("Strange array shape.")
        return [SPELLINGS[np.argmax(onehot)] for onehot in array]


class Chromagram35(FeatureRepresentation):
    features = len(SPELLINGS)

    def run(self, transposition="P1"):
        array = np.zeros(self.shape, dtype=self.dtype)
        for frame, notes in enumerate(self.df.s_notes):
            notes = [re.sub(r"\d", "", n) for n in notes]
            for note in notes:
                transposed = TransposePitch(note, transposition)
                if transposed in SPELLINGS:
                    spellingIndex = SPELLINGS.index(transposed)
                    array[frame, spellingIndex] = 1
        return array

    @classmethod
    def decode(cls, array):
        if len(array.shape) != 2 or array.shape[1] != len(SPELLINGS):
            raise IndexError("Strange array shape.")
        ret = []
        for manyhot in array:
            notes = [SPELLINGS[x] for x in np.nonzero(manyhot)[0]]
            ret.append(tuple(notes))
        return ret


class BassChromagram70(FeatureRepresentation):
    features = Bass35.features + Chromagram35.features

    def run(self, transposition="P1"):
        self.bass35 = Bass35(self.df).run(transposition)
        self.chromagram35 = Chromagram35(self.df).run(transposition)
        array = np.concatenate((self.bass35, self.chromagram35), axis=1)
        return array

    @classmethod
    def decode(cls, array):
        bass35 = Bass35.decode(array[:, : Bass35.features])
        chromagram35 = Chromagram35.decode(array[:, Bass35.features :])
        return [(b, ch) for b, ch in zip(bass35, chromagram35)]


class BassChromagram38(FeatureRepresentation):
    features = Bass19.features + Chromagram19.features

    def run(self, transposition="P1"):
        # super().__init__(df)
        self.bass19 = Bass19(self.df).run(transposition)
        self.chromagram19 = Chromagram19(self.df).run(transposition)
        array = np.concatenate((self.bass19, self.chromagram19), axis=1)
        return array

    @classmethod
    def decode(cls, array):
        bass19 = Bass19.decode(array[:, : Bass19.features])
        chromagram19 = Chromagram19.decode(array[:, Bass19.features :])
        return [(b[0], b[1], c[0], c[1]) for b, c in zip(bass19, chromagram19)]


class BassIntervals58(FeatureRepresentation):
    features = Bass19.features + Intervals39.features

    def run(self, transposition="P1"):
        self.bass19 = Bass19(self.df).run(transposition)
        self.intervals39 = Intervals39(self.df).run()
        array = np.concatenate((self.bass19, self.intervals39), axis=1)
        return array

    @classmethod
    def decode(cls, array):
        bass19 = Bass19.decode(array[:, : Bass19.features])
        intervals39 = Intervals39.decode(array[:, Bass19.features :])
        return [(b[0], b[1], i) for b, i in zip(bass19, intervals39)]


class BassChromagramIntervals77(FeatureRepresentation):
    features = BassChromagram38.features + Intervals39.features

    def run(self, transposition="P1"):
        self.bassChroma38 = BassChromagram38(self.df).run(transposition)
        self.intervals39 = Intervals39(self.df).run()
        array = np.concatenate((self.bassChroma38, self.intervals39), axis=1)
        return array

    @classmethod
    def decode(cls, array):
        bassChroma38 = BassChromagram38.decode(
            array[:, : BassChromagram38.features]
        )
        intervals39 = Intervals39.decode(array[:, BassChromagram38.features :])
        return [
            (bc[0], bc[1], bc[2], bc[3], i)
            for bc, i in zip(bassChroma38, intervals39)
        ]


available_representations = {
    "Bass19": Bass19,
    "Bass35": Bass35,
    "Chromagram19": Chromagram19,
    "Chromagram35": Chromagram35,
    "Duration14": Duration14,
    "Intervals39": Intervals39,
    "Intervals19": Intervals19,
    "BassChromagram38": BassChromagram38,
    "BassChromagram70": BassChromagram70,
    "BassIntervals58": BassIntervals58,
    "BassChromagramIntervals77": BassChromagramIntervals77,
}
