from music21.roman import RomanNumeral

def parseRomanNumeral(rn, key):
    """Parse a roman numeral annotation and return a ground truth dictionary.

    Expects two strings, a roman numeral figure and the key context.
    Parses this annotation and turns it into a dictionary with all the
    features that are relevant for that annotation.
    """
    rn = RomanNumeral(rn, key)
    pitchNames = tuple(rn.pitchNames)
    bass = rn.pitchNames[0]
    root = rn.root().name
    inversion = rn.inversion()
    secondaryKey = rn.secondaryRomanNumeralKey
    quality = rn.commonName
    pcset = tuple(sorted(set(rn.pitchClasses)))
    degree = str(rn.scaleDegree)
    if rn.secondaryRomanNumeral:
        degree += f"/{rn.secondaryRomanNumeral.scaleDegree}"
    if secondaryKey:
        tonicizedKey = secondaryKey.tonicPitchNameWithCase
    else:
        tonicizedKey = None
    ret = {
        "pitchNames": pitchNames,
        "bass": bass,
        "root": root,
        "inversion": inversion,
        "quality": quality,
        "pcset": pcset,
        "tonicizedKey": tonicizedKey,
        "degree": degree,
    }
    return ret