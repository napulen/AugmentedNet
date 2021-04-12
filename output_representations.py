from cache import TransposeKey, TransposePitch, m21Key, m21Pitch
from common import INTERVAL_TRANSPOSITIONS

import numpy as np
import music21

NOTENAMES = ("C", "D", "E", "F", "G", "A", "B")

PITCHCLASSES = [pc for pc in range(12)]

ACCIDENTALS = ("--", "-", "", "#", "##")

SPELLINGS = [
    f"{letter}{accidental}"
    for letter in NOTENAMES
    for accidental in ACCIDENTALS
]

NOTENAMES_LOWERCASE = [n.lower() for n in NOTENAMES]

DEGREES = (
    "-1",
    "-2",
    "-3",
    "-4",
    "-5",
    "-6",
    "-7",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "#1",
    "#2",
    "#3",
    "#4",
    "#5",
    "#6",
    "#7",
    "None",
)

KEYS = (
    "F-",
    "C-",
    "G-",
    "D-",
    "A-",
    "E-",
    "B-",
    "F",
    "C",
    "G",
    "D",
    "A",
    "E",
    "B",
    "F#",
    "C#",
    "G#",
    ####
    "d-",
    "a-",
    "e-",
    "b-",
    "f",
    "c",
    "g",
    "d",
    "a",
    "e",
    "b",
    "f#",
    "c#",
    "g#",
    "d#",
    "a#",
    "e#",
    "None",
)

CHORD_QUALITIES = [
    "major triad",
    "minor triad",
    "diminished triad",
    "augmented triad",
    "minor seventh chord",
    "major seventh chord",
    "dominant seventh chord",
    "incomplete dominant-seventh chord",
    "diminished seventh chord",
    "half-diminished seventh chord",
    "augmented sixth",
    "German augmented sixth chord",
    "French augmented sixth chord",
    "Italian augmented sixth chord",
    "minor-augmented tetrachord",
]

COMMON_ROMAN_NUMERALS = [
    "I",
    "V7",
    "V",
    "i",
    "IV",
    "ii",
    "vi",
    "iv",
    "viio7",
    "viio",
    "V7/V",
    "V7/IV",
    "viio7/V",
    "VI",
    "ii7",
    "V/V",
    "v",
    "V7/ii",
    "III",
    "iiø7",
    "iii",
    "iio",
    "viio/V",
    "V7/vi",
    "VII",
    "viio7/ii",
    "I/V",
    "V7/iv",
    "V/vi",
    "vi7",
    "Ger7",
    "N",
    "viio7/vi",
    "V/ii",
    "viiø7",
    "V9",
    "viio/ii",
    "V/iv",
    "Cad/V",
    "iv7",
    "viio7/iv",
    "IV7",
    "V7/III",
    "viiø7/V",
    "It",
    "viio7/v",
    "viio7/iii",
    "IV/V",
    "I+",
    "I7",
    "viio/IV",
    "V/III",
    "V7/iii",
    "viio/iv",
    "iio7",
    "VI7",
    "I/III",
    "V7/VI",
    "bVII",
    "bVI",
    "V+",
    "viio/vi",
    "III+",
    "V/iii",
    "ii/V",
    "I/-VI",
    "viio7/IV",
    "V7/v",
    "i7",
    "iii7",
    "Fr7",
    "V/IV",
    "vii",
    "V/v",
    "II",
]

INTERVAL_ENHARMONICS = {
    "A1": "m2",
    "M2": "D3",
    "A2": "m3",
    "M3": "D4",
    "A3": "P4",
    "A4": "D5",
    "P5": "D6",
    "A5": "m6",
    "M6": "D7",
    "A6": "m7",
    "M7": "D8",
    "m2": "A1",
    "D3": "M2",
    "m3": "A2",
    "D4": "M3",
    "P4": "A3",
    "D5": "A4",
    "D6": "P5",
    "m6": "A5",
    "D7": "M6",
    "m7": "A6",
    "D8": "M7",
}


class OutputRepresentation(object):
    def __init__(self, df, features=1):
        self.df = df
        self.frames = len(df.index)
        self.features = features
        self.shape = (self.frames, features)
        self.array = self.run()

    def run(self, transposeByInterval=None):
        array = np.zeros(self.shape)
        return array

    def dataAugmentation(self, intervals):
        for interval in intervals:
            yield self.run(transposeByInterval=interval)
        return


class OutputRepresentationTI(OutputRepresentation):
    """TI stands for Transposition Invariant.

    If a representation is TI, dataAugmentation consists of
    returning a copy of the array that was already computed.
    """

    def dataAugmentation(self, intervals):
        for _ in intervals:
            yield np.copy(self.array)
        return


class Bass19(OutputRepresentation):
    def __init__(self, df):
        features = len(NOTENAMES) + len(PITCHCLASSES)
        super().__init__(df, features=features)

    def run(self, transposedByInterval=None):
        array = np.zeros(self.shape)
        for frame, bass in enumerate(self.df.a_bass):
            if transposedByInterval:
                transposedBass = TransposePitch(bass, transposedByInterval)
                pitchObj = m21Pitch(transposedBass)
            else:
                pitchObj = m21Pitch(bass)
            pitchLetter = pitchObj.step
            pitchLetterIndex = NOTENAMES.index(pitchLetter)
            pitchClass = m21Pitch.pitchClass
            array[frame, pitchLetterIndex] = 1
            array[frame, pitchClass + 7] = 1
        return array


class Inversion(OutputRepresentationTI):
    # def __init__(self, df):
    #     features = 4
    #     super().__init__(df, features=features)

    def run(self):
        array = np.zeros(self.shape)
        for frame, inversion in enumerate(self.df.a_inversion):
            if inversion > 3:
                # Any chord beyond sevenths is encoded as "root" position
                inversion = 0
            array[frame] = inversion
        return array


class RomanNumeral(OutputRepresentationTI):
    # def __init__(self, df):
    #     features = len(COMMON_ROMAN_NUMERALS) + 1
    #     super().__init__(df, features=features)

    def run(self):
        array = np.zeros(self.shape)
        for frame, romanNumeral in enumerate(self.df.a_romanNumeral):
            if romanNumeral in COMMON_ROMAN_NUMERALS:
                rnIndex = COMMON_ROMAN_NUMERALS.index(romanNumeral)
                array[frame] = rnIndex
            else:
                array[frame] = len(COMMON_ROMAN_NUMERALS)
        return array


def bass19(df):
    """Encodes an Annotation DataFrame into a numpy array representation.

    Expects a DataFrame parsed by parseAnnotation(). Returns a numpy() array.
    """
    frames = len(df.index)
    ret = np.zeros((frames, 19))
    for frame, bass in enumerate(df.a_bass):
        m21Pitch = music21.pitch.Pitch(bass)
        pitchLetter = m21Pitch.step
        pitchLetterIndex = NOTENAMES.index(pitchLetter)
        pitchClass = m21Pitch.pitchClass
        ret[frame, pitchLetterIndex] = 1
        ret[frame, pitchClass + 7] = 1
    return ret


def bass7(df):
    """Encodes an Annotation DataFrame into a numpy array representation.

    Expects a DataFrame parsed by parseAnnotation(). Returns a numpy() array.
    """
    frames = len(df.index)
    ret = np.zeros((frames, 7))
    for frame, bass in enumerate(df.a_bass):
        m21Pitch = music21.pitch.Pitch(bass)
        pitchLetter = m21Pitch.step
        pitchLetterIndex = NOTENAMES.index(pitchLetter)
        ret[frame, pitchLetterIndex] = 1
    return ret


def bass12(df):
    """Encodes an Annotation DataFrame into a numpy array representation.

    Expects a DataFrame parsed by parseAnnotation(). Returns a numpy() array.
    """
    frames = len(df.index)
    ret = np.zeros((frames, 12))
    for frame, bass in enumerate(df.a_bass):
        m21Pitch = music21.pitch.Pitch(bass)
        pitchClass = m21Pitch.pitchClass
        ret[frame, pitchClass] = 1
    return ret


def bass35(df):
    """Encodes an Annotation DataFrame into a numpy array representation.

    Expects a DataFrame parsed by parseAnnotation(). Returns a numpy() array.
    """
    frames = len(df.index)
    ret = np.zeros((frames, 35))
    for frame, bass in enumerate(df.a_bass):
        if bass == "E###":
            bass = "G"
        spellingIndex = SPELLINGS.index(bass)
        ret[frame, spellingIndex] = 1
    return ret


def inversion(df, dataAugmentation=False):
    """Encodes an Annotation DataFrame into a numpy array representation.

    Expects a DataFrame parsed by parseAnnotation(). Returns a numpy() array.
    """
    frames, classes = len(df.index), 4
    ret = np.zeros((frames, classes))
    dataAug = None

    for frame, inversion in enumerate(df.a_inversion):
        if inversion > 3:
            # Any chord beyond sevenths is encoded as "root" position
            inversion = 0
        ret[frame, int(inversion)] = 1

    if not dataAugmentation:
        return ret, dataAug

    dataAug = np.zeros((len(INTERVAL_TRANSPOSITIONS), frames, classes))
    for transposition, _ in enumerate(INTERVAL_TRANSPOSITIONS):
        dataAug[transposition] = ret

    return ret, dataAug


def degree1(df):
    """Encodes an Annotation DataFrame into a numpy array representation.

    Expects a DataFrame parsed by parseAnnotation(). Returns a numpy() array.
    """
    frames = len(df.index)
    ret = np.zeros((frames, 21))
    for frame, degree1 in enumerate(df.a_degree1):
        degreeIndex = DEGREES.index(degree1)
        ret[frame, degreeIndex] = 1
    return ret


def degree2(df):
    """Encodes an Annotation DataFrame into a numpy array representation.

    Expects a DataFrame parsed by parseAnnotation(). Returns a numpy() array.
    """
    frames = len(df.index)
    ret = np.zeros((frames, 22))
    for frame, degree2 in enumerate(df.a_degree2):
        if degree2:
            degreeIndex = DEGREES.index(degree2)
        else:
            degreeIndex = 21
        ret[frame, degreeIndex] = 1
    return ret


def tonicizedKey(df):
    """Encodes an Annotation DataFrame into a numpy array representation.

    Expects a DataFrame parsed by parseAnnotation(). Returns a numpy() array.
    """
    frames = len(df.index)
    ret = np.zeros((frames, 31))
    for frame, r in enumerate(df.iterrows()):
        _, row = r
        if row.tonicizedKey != "None":
            tonicizedKey = row.a_tonicizedKey
        else:
            tonicizedKey = row.a_localKey
        tonicizedKeyIndex = KEYS.index(tonicizedKey)
        ret[frame, tonicizedKeyIndex] = 1
    return ret


def localKey(df, dataAugmentation=False):
    """Encodes an Annotation DataFrame into a numpy array representation.

    Expects a DataFrame parsed by parseAnnotation(). Returns a numpy() array.
    """
    frames, classes = len(df.index), (len(KEYS) - 1)
    ret = np.zeros((frames, classes))
    dataAug = None

    for frame, localKey in enumerate(df.a_localKey):
        localKeyIndex = KEYS.index(localKey)
        ret[frame, localKeyIndex] = 1

    if not dataAugmentation:
        return ret, dataAug

    dataAug = np.zeros((len(INTERVAL_TRANSPOSITIONS), frames, classes))
    for transposition, interval in enumerate(INTERVAL_TRANSPOSITIONS):
        tr = dataAug[transposition]
        enharmonicInterval = INTERVAL_ENHARMONICS[interval]
        for frame, localKey in enumerate(df.a_localKey):
            transposedKey = TransposeKey(localKey, interval)
            if transposedKey not in KEYS:
                print("x")
                transposedKey = TransposeKey(localKey, enharmonicInterval)
            localKeyIndex = KEYS.index(transposedKey)
            tr[frame, localKeyIndex] = 1

    return ret, dataAug


def chordRoot(df):
    """Encodes an Annotation DataFrame into a numpy array representation.

    Expects a DataFrame parsed by parseAnnotation(). Returns a numpy() array.
    """
    frames = len(df.index)
    ret = np.zeros((frames, 35))
    for frame, root in enumerate(df.a_root):
        spellingIndex = SPELLINGS.index(root)
        ret[frame, spellingIndex] = 1
    return ret


def chordQuality(df):
    """Encodes an Annotation DataFrame into a numpy array representation.

    Expects a DataFrame parsed by parseAnnotation(). Returns a numpy() array.
    """
    frames = len(df.index)
    ret = np.zeros((frames, len(CHORD_QUALITIES) + 1))
    for frame, quality in enumerate(df.a_quality):
        if not quality in CHORD_QUALITIES:
            qualityIndex = len(CHORD_QUALITIES)
        else:
            qualityIndex = CHORD_QUALITIES.index(quality)
        ret[frame, qualityIndex] = 1
    return ret


def harmonicRhythm(df):
    """Encodes an Annotation DataFrame into a numpy array representation.

    Expects a DataFrame parsed by parseAnnotation(). Returns a numpy() array.
    """
    frames = len(df.index)
    ret = np.zeros((frames, 2))
    for frame, isOnset in enumerate(df.a_isOnset):
        onset = 1 if isOnset else 0
        ret[frame, onset] = 1
    return ret


def romanNumeral(df, dataAugmentation=False):
    """Encodes an Annotation DataFrame into a numpy array representation.

    Expects a DataFrame parsed by parseAnnotation(). Returns a numpy() array.
    """
    frames, classes = len(df.index), (len(COMMON_ROMAN_NUMERALS) + 1)
    ret = np.zeros((frames, classes))
    dataAug = None

    for frame, romanNumeral in enumerate(df.a_romanNumeral):
        if romanNumeral in COMMON_ROMAN_NUMERALS:
            rnIndex = COMMON_ROMAN_NUMERALS.index(romanNumeral)
            ret[frame, rnIndex] = 1
        else:
            ret[frame, len(COMMON_ROMAN_NUMERALS)] = 1

    if not dataAugmentation:
        return ret, dataAug

    dataAug = np.zeros((len(INTERVAL_TRANSPOSITIONS), frames, classes))
    for transposition, _ in enumerate(INTERVAL_TRANSPOSITIONS):
        dataAug[transposition] = ret

    return ret, dataAug