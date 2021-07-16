import music21
from pprint import pprint
import itertools


def _line_of_fifths(x, mode="major"):
    fifths_major = ["C", "G", "D", "A", "E", "B", "F#"]
    fourths_major = ["C", "F", "Bb", "Eb", "Ab", "Db", "Gb"]
    fifths_minor = ["a", "e", "b", "f#", "c#", "g#", "d#"]
    fourths_minor = ["a", "d", "g", "c", "f", "bb", "eb"]

    fifths = fifths_major if mode == "major" else fifths_minor
    fourths = fourths_major if mode == "major" else fourths_minor

    if x == 0:
        return fifths[0]
    elif x > 0:
        accidentals = x // 7
        return f"{fifths[x%7]}{'#' * accidentals}"
    elif x < 0:
        x *= -1
        accidentals = x // 7
        return f"{fourths[x%7]}{'-' * accidentals}"


def range_lof(start, end, mode="major"):
    for n in range(start, end + 1):
        yield _line_of_fifths(n, mode=mode)


start, end = -6, 5
majorkeys = range_lof(start, end, mode="major")
minorkeys = range_lof(start, end, mode="minor")

degreesmajor = ["I", "ii", "iii", "IV", "V", "vi", "viio"]
degreesminor = ["i", "iio", "III", "iv", "V", "VI", "viio"]
degreesmajor7 = ["I7", "ii7", "iii7", "IV7", "V7", "vi7", "viio7"]
degreesminor7 = ["i7", "iiø7", "III7", "iv7", "V7", "VI7", "viio7"]
degreesmajor7 = ["I7", "ii7", "iii7", "IV7", "V7", "vi7", "viiø7"]
special = ["N", "Ger7", "Fr7", "It"]

rns = []
pcsets = {}
pitchsets = {}
pcset_pitchset = {}
pitchset_pcset = {}

for key in majorkeys:
    for deg in degreesmajor + degreesmajor7 + special:
        rntext = f"{key}:{deg}"
        rn = music21.roman.RomanNumeral(deg, key)
        pcset = frozenset(rn.pitchClasses)
        pitchset = frozenset([p.replace("-", "b") for p in rn.pitchNames])
        # print(rntext, pcset, pitchset)
        rns.append(rntext)
        if not pcset in pcsets:
            pcsets[pcset] = []
        pcsets[pcset].append(rntext)
        if not pitchset in pitchsets:
            pitchsets[pitchset] = []
        pitchsets[pitchset].append(rntext)
        if not pcset in pcset_pitchset:
            pcset_pitchset[pcset] = []
        pcset_pitchset[pcset].append(pitchset)
        if not pitchset in pitchset_pcset:
            pitchset_pcset[pitchset] = []
        if not pcset in pitchset_pcset[pitchset]:
            pitchset_pcset[pitchset].append(pcset)

for key in minorkeys:
    for deg in degreesminor + degreesminor7 + special:
        rntext = f"{key}:{deg}"
        rn = music21.roman.RomanNumeral(deg, key)
        pcset = frozenset(rn.pitchClasses)
        pitchset = frozenset([p.replace("-", "b") for p in rn.pitchNames])
        # print(rntext, pcset, pitchset)
        rns.append(rntext)
        if not pcset in pcsets:
            pcsets[pcset] = []
        pcsets[pcset].append(rntext)
        if not pitchset in pitchsets:
            pitchsets[pitchset] = []
        pitchsets[pitchset].append(rntext)
        if not pcset in pcset_pitchset:
            pcset_pitchset[pcset] = []
        pcset_pitchset[pcset].append(pitchset)
        if not pitchset in pitchset_pcset:
            pitchset_pcset[pitchset] = []
        if not pcset in pitchset_pcset[pitchset]:
            pitchset_pcset[pitchset].append(pcset)

# print("===================================")
# print(len(rns), len(pcsets), len(pitchsets))

# pprint(pcsets)
# pprint(pitchsets)

print("graph G {")
for pitchset, keys_roman in pitchsets.items():
    # keys = [k.split(":")[0] for k in keys_roman]
    keys = keys_roman
    pitchsetstr = str(set(pitchset)).replace("'", "")
    print(f'\t"{pitchsetstr}"[shape=rect];')
    for key in keys:
        print(f'\t"{key}"[shape=plain]')
        print(f'\t"{pitchsetstr}" -- "{key}";')
    for pcset in pitchset_pcset[pitchset]:
        print(
            f'\t"{tuple(sorted(set(pcset)))}"[shape=oval, fixedsize=true, width=1, height=0.5];'
        )
        print(
            f'\t"{pitchsetstr}" -- "{tuple(sorted(set(pcset)))}"[weight=10];'
        )

    # for key in itertools.combinations(keys, 2):
    #     k1, k2 = key
    #     # print(pcset, k1, k2)
    #     print(f'\t"{k1}" -- "{k2}"#[label="{set(pcset)}"]')
print("}")


# print("graph H {")
# keys_over_keys = {}
# for pitchset, keys_roman in pitchsets.items():
#     keys = [k.split(":")[0] for k in keys_roman]
#     for key_pair in itertools.combinations(keys, 2):
#         if key_pair not in keys_over_keys:
#             keys_over_keys[key_pair] = 0
#         keys_over_keys[key_pair] += 1
# for key_pair, strength in keys_over_keys.items():
#     k1, k2 = key_pair
#     print(f'\t"{k1}" -- "{k2}"[weight = {strength}, penwidth = {strength/5}]')
# print("}")
