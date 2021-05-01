import numpy as np

NOTENAMES = ("C", "D", "E", "F", "G", "A", "B")

NOTENAMES_LOWERCASE = [n.lower() for n in NOTENAMES]

PITCHCLASSES = [pc for pc in range(12)]

ACCIDENTALS = ("--", "-", "", "#", "##")

SPELLINGS = [
    f"{letter}{accidental}"
    for letter in NOTENAMES
    for accidental in ACCIDENTALS
]

INTERVALCLASSES = [
    f"{specific}{generic}"
    for generic in [2, 3, 6, 7]
    for specific in ["dd", "d", "m", "M", "A", "AA"]
] + [
    f"{specific}{generic}"
    for generic in [1, 4, 5]
    for specific in ["dd", "d", "P", "A", "AA"]
]

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
    "None",
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
    "None",
]

PCSETS = [
    (0, 1, 5, 8),
    (0, 2, 5, 9),
    (0, 2, 6),
    (0, 2, 6, 8),
    (0, 2, 6, 9),
    (0, 3, 5, 8),
    (0, 3, 5, 9),
    (0, 3, 6),
    (0, 3, 6, 8),
    (0, 3, 6, 9),
    (0, 3, 7),
    (0, 3, 7, 8),
    (0, 3, 7, 10),
    (0, 3, 8),
    (0, 3, 9),
    (0, 4, 5, 9),
    (0, 4, 6, 10),
    (0, 4, 7),
    (0, 4, 7, 9),
    (0, 4, 7, 10),
    (0, 4, 7, 11),
    (0, 4, 9),
    (0, 4, 10),
    (0, 5, 8),
    (0, 5, 9),
    (0, 6, 8),
    (0, 6, 9),
    (1, 2, 6, 9),
    (1, 3, 6, 10),
    (1, 3, 7),
    (1, 3, 7, 9),
    (1, 3, 7, 10),
    (1, 4, 6, 9),
    (1, 4, 6, 10),
    (1, 4, 7),
    (1, 4, 7, 9),
    (1, 4, 7, 10),
    (1, 4, 8),
    (1, 4, 8, 9),
    (1, 4, 8, 11),
    (1, 4, 9),
    (1, 4, 10),
    (1, 5, 6, 10),
    (1, 5, 7, 11),
    (1, 5, 8),
    (1, 5, 8, 10),
    (1, 5, 8, 11),
    (1, 5, 10),
    (1, 5, 11),
    (1, 6, 9),
    (1, 6, 10),
    (1, 7, 9),
    (1, 7, 10),
    (2, 3, 7, 10),
    (2, 4, 7, 11),
    (2, 4, 8),
    (2, 4, 8, 10),
    (2, 4, 8, 11),
    (2, 5, 7, 10),
    (2, 5, 7, 11),
    (2, 5, 8),
    (2, 5, 8, 10),
    (2, 5, 8, 11),
    (2, 5, 9),
    (2, 5, 9, 10),
    (2, 5, 10),
    (2, 5, 11),
    (2, 6, 7, 11),
    (2, 6, 9),
    (2, 6, 9, 11),
    (2, 6, 11),
    (2, 7, 10),
    (2, 7, 11),
    (2, 8, 10),
    (2, 8, 11),
    (3, 4, 8, 11),
    (3, 5, 9),
    (3, 5, 9, 11),
    (3, 6, 8, 11),
    (3, 6, 9),
    (3, 6, 9, 11),
    (3, 6, 10),
    (3, 6, 10, 11),
    (3, 6, 11),
    (3, 7, 10),
    (3, 8, 11),
    (3, 9, 11),
    (4, 6, 10),
    (4, 7, 10),
    (4, 7, 11),
    (4, 8, 11),
    (5, 7, 11),
    (5, 8, 11),
    "None",
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


class FeatureRepresentation(object):
    features = 1

    def __init__(self, df):
        self.df = df
        self.frames = len(df.index)
        self.dtype = "i8"
        self.array = self.run()

    @property
    def shape(self):
        return (self.frames, self.features)

    def run(self, tranposition=None):
        array = np.zeros(self.shape)
        return array

    def dataAugmentation(self, intervals):
        for interval in intervals:
            yield self.run(transposition=interval)
        return

    @classmethod
    def encodeManyHot(cls, array, timestep, index, value=1):
        if 0 <= index < cls.features:
            array[timestep, index] = value
        else:
            raise IndexError

    @classmethod
    def encodeCategorical(cls, array, timestep, classNumber):
        if 0 <= classNumber < cls.features:
            array[timestep] = classNumber
        else:
            raise IndexError


class FeatureRepresentationTI(FeatureRepresentation):
    """TI stands for Transposition Invariant.

    If a representation is TI, dataAugmentation consists of
    returning a copy of the array that was already computed.
    """

    def dataAugmentation(self, intervals):
        for _ in intervals:
            yield np.copy(self.array)
        return
