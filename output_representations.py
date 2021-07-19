"""The output tonal representations learned through multitask learning."""

import numpy as np

from cache import (
    TransposeKey,
    TransposePcSet,
    TransposePitch,
)
from feature_representation import (
    FeatureRepresentation,
    FeatureRepresentationTI,
    CHORD_QUALITIES,
    COMMON_ROMAN_NUMERALS,
    DEGREES,
    KEYS,
    PCSETS,
    SPELLINGS,
)


class OutputRepresentation(FeatureRepresentation):
    """Output representations are all one-hot encoded (no many-hots).

    That makes them easier to template.
    """

    classList = []
    dfFeature = ""
    transpositionFn = None

    def run(self, transposition="P1"):
        array = np.zeros(self.shape, dtype=self.dtype)
        for frame, dfFeature in enumerate(self.df[self.dfFeature]):
            transposed = self.transpositionFn(dfFeature, transposition)
            if transposed in self.classList:
                rnIndex = self.classList.index(transposed)
                array[frame] = rnIndex
            else:
                array[frame] = self.classesNumber() - 1
        return array

    @classmethod
    def classesNumber(cls):
        return len(cls.classList)

    @classmethod
    def decode(cls, array):
        return [cls.classList[index] for index in array.reshape(-1)]

    @classmethod
    def decodeOneHot(cls, array):
        if len(array.shape) != 2 or array.shape[1] != len(cls.classList):
            raise IndexError("Strange array shape.")
        return [cls.classList[np.argmax(onehot)] for onehot in array]


class OutputRepresentationTI(FeatureRepresentationTI):
    """Output representations are all one-hot encoded (no many-hots).

    That makes them easier to template.
    """

    classList = []
    dfFeature = ""

    def run(self):
        array = np.zeros(self.shape, dtype=self.dtype)
        for frame, dfFeature in enumerate(self.df[self.dfFeature]):
            if dfFeature in self.classList:
                rnIndex = self.classList.index(dfFeature)
                array[frame] = rnIndex
            else:
                array[frame] = self.classesNumber() - 1
        return array

    @classmethod
    def classesNumber(cls):
        return len(cls.classList)

    @classmethod
    def decode(cls, array):
        return [cls.classList[index] for index in array.reshape(-1)]

    @classmethod
    def decodeOneHot(cls, array):
        if len(array.shape) != 2 or array.shape[1] != len(cls.classList):
            raise IndexError("Strange array shape.")
        return [cls.classList[np.argmax(onehot)] for onehot in array]


class Bass35(OutputRepresentation):
    classList = SPELLINGS
    dfFeature = "a_bass"
    transpositionFn = staticmethod(TransposePitch)


class Inversion4(OutputRepresentationTI):
    classList = list(range(4))
    dfFeature = "a_inversion"

    def run(self):
        array = np.zeros(self.shape, dtype=self.dtype)
        for frame, inversion in enumerate(self.df[self.dfFeature]):
            if inversion > 3:
                # Any chord beyond sevenths is encoded as "root" position
                inversion = 0
            array[frame] = int(inversion)
        return array


class HarmonicRhythm2(OutputRepresentationTI):
    classList = [True, False]
    dfFeature = "a_isOnset"


class RomanNumeral76(OutputRepresentationTI):
    classList = COMMON_ROMAN_NUMERALS
    dfFeature = "a_romanNumeral"


class PrimaryDegree22(OutputRepresentationTI):
    classList = DEGREES
    dfFeature = "a_degree1"


class SecondaryDegree22(OutputRepresentationTI):
    classList = DEGREES
    dfFeature = "a_degree2"


class LocalKey35(OutputRepresentation):
    classList = KEYS
    dfFeature = "a_localKey"
    transpositionFn = staticmethod(TransposeKey)


class TonicizedKey35(OutputRepresentation):
    classList = KEYS
    dfFeature = "a_tonicizedKey"
    transpositionFn = staticmethod(TransposeKey)


class ChordRoot35(OutputRepresentation):
    classList = SPELLINGS
    dfFeature = "a_root"
    transpositionFn = staticmethod(TransposePitch)


class ChordQuality15(OutputRepresentationTI):
    classList = CHORD_QUALITIES
    dfFeature = "a_quality"


class PitchClassSet94(OutputRepresentation):
    classList = PCSETS
    dfFeature = "a_pcset"
    transpositionFn = staticmethod(TransposePcSet)


available_representations = {
    "Bass35": Bass35,
    "ChordQuality15": ChordQuality15,
    "ChordRoot35": ChordRoot35,
    "HarmonicRhythm2": HarmonicRhythm2,
    "Inversion4": Inversion4,
    "LocalKey35": LocalKey35,
    "PitchClassSet94": PitchClassSet94,
    "PrimaryDegree22": PrimaryDegree22,
    "RomanNumeral76": RomanNumeral76,
    "SecondaryDegree22": SecondaryDegree22,
    "TonicizedKey35": TonicizedKey35,
}
