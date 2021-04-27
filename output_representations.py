from cache import (
    TransposeKey,
    TransposePitch,
    TransposePcSet,
    m21Key,
    m21Pitch,
)
from feature_representation import (
    CHORD_QUALITIES,
    COMMON_ROMAN_NUMERALS,
    FeatureRepresentation,
    FeatureRepresentationTI,
    SPELLINGS,
    COMMON_ROMAN_NUMERALS,
    DEGREES,
    KEYS,
    CHORD_QUALITIES,
    PCSETS,
)

import numpy as np


class OutputRepresentation(FeatureRepresentation):
    """Output representations are all one-hot encoded (no many-hots).

    That makes them easier to template.
    """

    classList = []
    classesNumber = len(classList)
    dfFeature = ""
    features = classesNumber
    transpositionFn = None

    def run(self, transposition="P1"):
        array = np.zeros(self.shape)
        for frame, dfFeature in enumerate(self.df[self.dfFeature]):
            transposed = eval(self.transpositionFn)(dfFeature, transposition)
            if transposed in self.classList:
                rnIndex = self.classList.index(transposed)
                array[frame, rnIndex] = 1
            else:
                array[frame, -1] = 1
        return array

    @classmethod
    def decode(cls, array):
        if len(array.shape) != 2 or array.shape[1] != len(cls.classList):
            raise IndexError("Strange array shape.")
        return [cls.classList[np.argmax(onehot)] for onehot in array]


class OutputRepresentationTI(FeatureRepresentationTI):
    """Output representations are all one-hot encoded (no many-hots).

    That makes them easier to template.
    """

    classList = []
    classesNumber = len(classList)
    dfFeature = ""
    features = classesNumber

    def run(self):
        array = np.zeros(self.shape)
        for frame, dfFeature in enumerate(self.df[self.dfFeature]):
            if dfFeature in self.classList:
                rnIndex = self.classList.index(dfFeature)
                array[frame, rnIndex] = 1
            else:
                array[frame, -1] = 1
        return array

    @classmethod
    def decode(cls, array):
        if len(array.shape) != 2 or array.shape[1] != len(cls.classList):
            raise IndexError("Strange array shape.")
        return [cls.classList[np.argmax(onehot)] for onehot in array]


class Bass35(OutputRepresentation):
    classList = SPELLINGS
    dfFeature = "a_bass"
    features = len(classList)
    transpositionFn = "TransposePitch"


class Inversion4(OutputRepresentationTI):
    classList = list(range(4))
    dfFeature = "a_inversion"
    features = len(classList)

    def run(self):
        array = np.zeros(self.shape)
        for frame, inversion in enumerate(self.df[self.dfFeature]):
            if inversion > 3:
                # Any chord beyond sevenths is encoded as "root" position
                inversion = 0
            array[frame, int(inversion)] = 1
        return array


class HarmonicRhythm2(OutputRepresentationTI):
    classList = [True, False]
    dfFeature = "a_isOnset"
    features = len(classList)


class RomanNumeral76(OutputRepresentationTI):
    classList = COMMON_ROMAN_NUMERALS
    dfFeature = "a_romanNumeral"
    features = len(classList)


class PrimaryDegree22(OutputRepresentationTI):
    classList = DEGREES
    dfFeature = "a_degree1"
    features = len(classList)


class SecondaryDegree22(OutputRepresentationTI):
    classList = DEGREES
    dfFeature = "a_degree2"
    features = len(classList)


class LocalKey35(OutputRepresentation):
    classList = KEYS
    dfFeature = "a_localKey"
    features = len(classList)
    transpositionFn = "TransposeKey"


class TonicizedKey35(OutputRepresentation):
    classList = KEYS
    dfFeature = "a_tonicizedKey"
    features = len(classList)
    transpositionFn = "TransposeKey"


class ChordRoot35(OutputRepresentation):
    classList = SPELLINGS
    dfFeature = "a_root"
    features = len(classList)
    transpositionFn = "TransposePitch"


class ChordQuality15(OutputRepresentationTI):
    classList = CHORD_QUALITIES
    dfFeature = "a_quality"
    features = len(classList)


class PitchClassSet94(OutputRepresentation):
    classList = PCSETS
    dfFeature = "a_pcset"
    features = len(classList)
    transpositionFn = "TransposePcSet"


available_representations = {
    "Bass35": Bass35,
    "Inversion4": Inversion4,
    "RomanNumeral76": RomanNumeral76,
    "PrimaryDegree22": PrimaryDegree22,
    "SecondaryDegree22": SecondaryDegree22,
    "LocalKey35": LocalKey35,
    "ChordRoot35": ChordRoot35,
    "ChordQuality15": ChordQuality15,
}