from cache import TransposeKey, TransposePitch, m21Key, m21Pitch
from common import INTERVAL_TRANSPOSITIONS
from feature_representation import (
    CHORD_QUALITIES,
    COMMON_ROMAN_NUMERALS,
    FeatureRepresentation,
    FeatureRepresentationTI,
    NOTENAMES,
    PITCHCLASSES,
    SPELLINGS,
    COMMON_ROMAN_NUMERALS,
    DEGREES,
    KEYS,
    CHORD_QUALITIES,
)

import numpy as np


class Bass35(FeatureRepresentation):
    features = len(SPELLINGS)

    def run(self, transposition="P1"):
        array = np.zeros(self.shape)
        for frame, bass in enumerate(self.df.a_bass):
            transposedBass = TransposePitch(bass, transposition)
            spellingIndex = SPELLINGS.index(transposedBass)
            array[frame, spellingIndex] = 1
        return array

    @classmethod
    def decode(cls, array):
        if len(array.shape) != 2 or array.shape[1] != cls.features:
            raise IndexError("Strange array shape.")
        ret = [SPELLINGS[np.argmax(onehot)] for onehot in array]
        return ret


class Inversion4(FeatureRepresentationTI):
    features = 4

    def run(self):
        array = np.zeros(self.shape)
        for frame, inversion in enumerate(self.df.a_inversion):
            if inversion > 3:
                # Any chord beyond sevenths is encoded as "root" position
                inversion = 0
            array[frame] = inversion
        return array

    @classmethod
    def decode(cls, array):
        if len(array.shape) != 2 or array.shape[1] != cls.features:
            raise IndexError("Strange array shape.")
        ret = [np.argmax(onehot) for onehot in array]
        return ret


class RomanNumeral76(FeatureRepresentationTI):
    features = len(COMMON_ROMAN_NUMERALS) + 1

    def run(self):
        array = np.zeros(self.shape)
        for frame, romanNumeral in enumerate(self.df.a_romanNumeral):
            if romanNumeral in COMMON_ROMAN_NUMERALS:
                rnIndex = COMMON_ROMAN_NUMERALS.index(romanNumeral)
                array[frame] = rnIndex
            else:
                array[frame] = len(COMMON_ROMAN_NUMERALS)
        return array

    @classmethod
    def decode(cls, array):
        if len(array.shape) != 2 or array.shape[1] != cls.features:
            raise IndexError("Strange array shape.")
        ret = [COMMON_ROMAN_NUMERALS[np.argmax(onehot)] for onehot in array]
        return ret


class PrimaryDegree22(FeatureRepresentationTI):
    features = len(DEGREES) + 1

    def run(self):
        array = np.zeros(self.shape)
        for frame, degree1 in enumerate(self.df.a_degree1):
            if degree1 in DEGREES:
                degreeIndex = DEGREES.index(degree1)
                array[frame] = degreeIndex
            else:
                array[frame] = len(DEGREES)
        return array

    @classmethod
    def decode(cls, array):
        if len(array.shape) != 2 or array.shape[1] != cls.features:
            raise IndexError("Strange array shape.")
        ret = [DEGREES[np.argmax(onehot)] for onehot in array]
        return ret


class SecondaryDegree22(FeatureRepresentationTI):
    features = len(DEGREES) + 1

    def run(self):
        array = np.zeros(self.shape)
        for frame, degree2 in enumerate(self.df.a_degree2):
            if degree2 in DEGREES:
                degreeIndex = DEGREES.index(degree2)
                array[frame] = degreeIndex
            else:
                array[frame] = len(DEGREES)
        return array

    @classmethod
    def decode(cls, array):
        if len(array.shape) != 2 or array.shape[1] != cls.features:
            raise IndexError("Strange array shape.")
        ret = [DEGREES[np.argmax(onehot)] for onehot in array]
        return ret


class LocalKey35(FeatureRepresentation):
    features = len(KEYS)

    def run(self):
        array = np.zeros(self.shape)
        for frame, localKey in enumerate(self.df.a_localKey):
            if localKey in KEYS:
                degreeIndex = KEYS.index(localKey)
                array[frame] = degreeIndex
            else:
                array[frame] = len(KEYS)
        return array

    @classmethod
    def decode(cls, array):
        if len(array.shape) != 2 or array.shape[1] != cls.features:
            raise IndexError("Strange array shape.")
        ret = [KEYS[np.argmax(onehot)] for onehot in array]
        return ret


class ChordRoot35(FeatureRepresentation):
    features = len(SPELLINGS)

    def run(self):
        array = np.zeros(self.shape)
        for frame, root in enumerate(self.df.a_root):
            if root in SPELLINGS:
                rootIndex = SPELLINGS.index(root)
                array[frame] = rootIndex
            else:
                array[frame] = len(SPELLINGS)
        return array

    @classmethod
    def decode(cls, array):
        if len(array.shape) != 2 or array.shape[1] != cls.features:
            raise IndexError("Strange array shape.")
        ret = [KEYS[np.argmax(onehot)] for onehot in array]
        return ret


class ChordQuality15(FeatureRepresentation):
    features = len(CHORD_QUALITIES)

    def run(self):
        array = np.zeros(self.shape)
        for frame, quality in enumerate(self.df.a_quality):
            qualityIndex = CHORD_QUALITIES.index(quality)
            array[frame] = qualityIndex
        return array

    @classmethod
    def decode(cls, array):
        if len(array.shape) != 2 or array.shape[1] != cls.features:
            raise IndexError("Strange array shape.")
        ret = [CHORD_QUALITIES[np.argmax(onehot)] for onehot in array]
        return ret