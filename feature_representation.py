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
    for generic in [1, 4, 5, 8]
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


class FeatureRepresentation(object):
    features = 1

    def __init__(self, df):
        self.df = df
        self.frames = len(df.index)
        self.shape = (self.frames, self.features)
        self.dtype = "i8"
        self.array = self.run()

    def run(self, transposeByInterval=None):
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
