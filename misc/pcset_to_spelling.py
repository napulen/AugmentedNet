import music21
from pprint import pprint
import json

pcsets = {}

QUALITIES = {
    "Cad": "cad",
    "Fr7": "aug6",
    "Ger7": "aug6",
    "I": "maj",
    "I7": "maj7",
    "III+": "aug",
    "III+7": "aug7",
    "IV": "maj",
    "IV7": "maj7",
    "It": "aug6",
    "N": "maj",
    "V": "maj",
    "V+": "aug",
    "V7": "7",
    "VI": "maj",
    "VI7": "maj7",
    "i": "min",
    "i7": "min7",  # should this be minmaj7?
    "ii": "min",
    "ii7": "min7",
    "iii": "min",
    "iii7": "min7",
    "iio": "dim",
    "iiø7": "hdim7",
    "iv": "min",
    "iv7": "min7",
    "vi": "min",
    "vi7": "min7",
    "viio": "dim",
    "viio7": "dim7",
    "viiø7": "hdim7",
}


def line_of_fifths(x, mode="major"):
    fifths_major = ["C", "G", "D", "A", "E", "B", "F#"]
    fourths_major = ["C", "F", "B-", "E-", "A-", "D-", "G-"]
    fifths_minor = ["a", "e", "b", "f#", "c#", "g#", "d#"]
    fourths_minor = ["a", "d", "g", "c", "f", "b-", "e-"]

    fifths = fifths_major if mode == "major" else fifths_minor
    fourths = fourths_major if mode == "major" else fourths_minor

    if x == 0:
        return fifths[0]
    elif x > 0:
        accidentals = x // 7
        return f"{fifths[x % 7]}{'#' * accidentals}"
    elif x < 0:
        x *= -1
        accidentals = x // 7
        return f"{fourths[x % 7]}{'-' * accidentals}"


def range_lof(start, end, mode="major"):
    for n in range(start, end + 1):
        yield line_of_fifths(n, mode=mode)


def fillpcset(key, deg):
    rntext = f"{key}:{deg}"
    rn = music21.roman.RomanNumeral(deg.replace("bVII", "VII"), key)
    pcset = tuple(sorted(set(rn.pitchClasses)))
    if not pcset in pcsets:
        pcsets[pcset] = {}
    if key in pcsets[pcset]:
        print(f"COLLISION between {rntext} and {pcsets[pcset][key]}")
        return
    pcsets[pcset][key] = {}
    pcsets[pcset][key]["chord"] = rn.pitchNames
    if deg == "bII":
        deg = "N"
    pcsets[pcset][key]["rn"] = deg
    pcsets[pcset][key]["quality"] = QUALITIES[deg]


if __name__ == "__main__":
    start, end = -9, 9
    majorkeys = range_lof(start, end, mode="major")
    minorkeys = range_lof(start, end, mode="minor")
    degreesmajor = ["I", "ii", "iii", "IV", "V", "V+", "vi", "viio"]
    degreesminor = [
        "i",
        "iio",
        # "III",
        "III+",
        "iv",
        "V",
        "VI",
        # "bVII",
        "viio",
    ]
    degreesmajor7 = [f"{c}7".replace("viio7", "viiø7") for c in degreesmajor]
    degreesmajor7.remove("V+7")
    degreesminor7 = [f"{c}7" if c != "iio" else "iiø7" for c in degreesminor]
    special = ["bII", "Ger7", "Fr7", "It"]

    for key in majorkeys:
        for deg in degreesmajor + degreesmajor7 + special:
            fillpcset(key, deg)
    for key in minorkeys:
        for deg in degreesminor + degreesminor7 + special:
            fillpcset(key, deg)
    print(len(pcsets))
    pprint(pcsets)
