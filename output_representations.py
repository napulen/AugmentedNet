import numpy as np
import music21

NOTENAMES = ("C", "D", "E", "F", "G", "A", "B")

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
    ####
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


def bass19(df):
    """Encodes an Annotation DataFrame into a numpy array representation.

    Expects a DataFrame parsed by parseAnnotation(). Returns a numpy() array.
    """
    frames = len(df.index)
    ret = np.zeros((frames, 19))
    for frame, bass in enumerate(df.bass):
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
    for frame, bass in enumerate(df.bass):
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
    for frame, bass in enumerate(df.bass):
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
    for frame, bass in enumerate(df.bass):
        if bass == "E###":
            bass = "G"
        spellingIndex = SPELLINGS.index(bass)
        ret[frame, spellingIndex] = 1
    return ret


def inversion(df):
    """Encodes an Annotation DataFrame into a numpy array representation.

    Expects a DataFrame parsed by parseAnnotation(). Returns a numpy() array.
    """
    frames = len(df.index)
    ret = np.zeros((frames, 4))
    for frame, inversion in enumerate(df.inversion):
        if inversion > 3:
            # Any chord beyond sevenths is encoded as "root" position
            inversion = 0
        ret[frame, int(inversion)] = 1
    return ret


def degree1(df):
    """Encodes an Annotation DataFrame into a numpy array representation.

    Expects a DataFrame parsed by parseAnnotation(). Returns a numpy() array.
    """
    frames = len(df.index)
    ret = np.zeros((frames, 21))
    for frame, degree1 in enumerate(df.degree1):
        degreeIndex = DEGREES.index(degree1)
        ret[frame, degreeIndex] = 1
    return ret


def degree2(df):
    """Encodes an Annotation DataFrame into a numpy array representation.

    Expects a DataFrame parsed by parseAnnotation(). Returns a numpy() array.
    """
    frames = len(df.index)
    ret = np.zeros((frames, 22))
    for frame, degree2 in enumerate(df.degree2):
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
            tonicizedKey = row.tonicizedKey
        else:
            tonicizedKey = row.localKey
        tonicizedKeyIndex = KEYS.index(tonicizedKey)
        ret[frame, tonicizedKeyIndex] = 1
    return ret


def localKey(df):
    """Encodes an Annotation DataFrame into a numpy array representation.

    Expects a DataFrame parsed by parseAnnotation(). Returns a numpy() array.
    """
    frames = len(df.index)
    ret = np.zeros((frames, 30))
    for frame, localKey in enumerate(df.localKey):
        localKeyIndex = KEYS.index(localKey)
        ret[frame, localKeyIndex] = 1
    return ret


def chordRoot(df):
    """Encodes an Annotation DataFrame into a numpy array representation.

    Expects a DataFrame parsed by parseAnnotation(). Returns a numpy() array.
    """
    frames = len(df.index)
    ret = np.zeros((frames, 35))
    for frame, root in enumerate(df.root):
        spellingIndex = SPELLINGS.index(root)
        ret[frame, spellingIndex] = 1
    return ret


def chordQuality(df):
    """Encodes an Annotation DataFrame into a numpy array representation.

    Expects a DataFrame parsed by parseAnnotation(). Returns a numpy() array.
    """
    frames = len(df.index)
    ret = np.zeros((frames, len(CHORD_QUALITIES) + 1))
    for frame, quality in enumerate(df.quality):
        if not quality in CHORD_QUALITIES:
            qualityIndex = len(CHORD_QUALITIES) + 1
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
    for frame, isOnset in enumerate(df.isOnset):
        onset = 1 if isOnset else 0
        ret[frame, onset] = 1
    return ret


def romanNumeral(df):
    """Encodes an Annotation DataFrame into a numpy array representation.

    Expects a DataFrame parsed by parseAnnotation(). Returns a numpy() array.
    """
    frames = len(df.index)
    ret = np.zeros((frames, len(COMMON_ROMAN_NUMERALS) + 1))
    for frame, romanNumeral in enumerate(df.romanNumeral):
        if romanNumeral in COMMON_ROMAN_NUMERALS:
            rnIndex = COMMON_ROMAN_NUMERALS.index(romanNumeral)
            ret[frame, rnIndex] = 1
        else:
            ret[frame, len(COMMON_ROMAN_NUMERALS)] = 1
    return ret