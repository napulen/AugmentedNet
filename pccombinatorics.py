import music21

majorkeys = [
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
]

minorkeys = [
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
]

degreesmajor = ["I", "ii", "iii", "IV", "V", "vi", "viio"]
degreesminor = ["i", "iio", "III", "iv", "V", "VI", "viio"]
degreesmajor7 = ["I7", "ii7", "iii7", "IV7", "V7", "vi7", "viio7"]
degreesminor7 = ["i7", "iio7", "III7", "iv7", "V7", "VI7", "viio7"]
degreesmajor7 = ["I7", "ii7", "iii7", "IV7", "V7", "vi7", "viiø7"]
special = ["N", "Ger7", "Fr7", "It"]

rns = []
pcsets = {}
pitchsets = {}


for key in majorkeys:
    for deg in degreesmajor + degreesmajor7 + special:
        rntext = f"{key}:{deg}"
        rn = music21.roman.RomanNumeral(deg, key)
        pcset = frozenset(rn.pitchClasses)
        pitchset = frozenset(rn.pitchNames)
        print(rntext, pcset, pitchset)
        rns.append(rntext)
        if not pcset in pcsets:
            pcsets[pcset] = []
        pcsets[pcset].append(rntext)
        if not pitchset in pitchsets:
            pitchsets[pitchset] = []
        pitchsets[pitchset].append(rntext)

for key in minorkeys:
    for deg in degreesminor + degreesminor7 + special:
        rntext = f"{key}:{deg}"
        rn = music21.roman.RomanNumeral(deg, key)
        pcset = frozenset(rn.pitchClasses)
        pitchset = frozenset(rn.pitchNames)
        print(rntext, pcset, pitchset)
        rns.append(rntext)
        if not pcset in pcsets:
            pcsets[pcset] = []
        pcsets[pcset].append(rntext)
        if not pitchset in pitchsets:
            pitchsets[pitchset] = []
        pitchsets[pitchset].append(rntext)

print("===================================")
print(len(rns), len(pcsets), len(pitchsets))

print(pcsets)
print(pitchsets)
