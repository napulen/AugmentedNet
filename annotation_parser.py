import music21
import pandas as pd
from config import FRAMESPERQUARTERNOTE


def parseAnnotation(f):
    """Parses an annotation RomanText file and produces a pandas dataframe.

    Unpacking a roman numeral is slightly more complicated here than in
    previous approaches/papers, the reason is that some features do not
    seem to work well (e.g., inversion). It may be easier to predict others
    which may still serve to reconstruct the roman numeral.
    """
    s = music21.converter.parse(f, format="romantext")
    dfdict = {
        "offset": [],
        "measure": [],
        "pitchNames": [],
        "bass": [],
        "root": [],
        "inversion": [],
        "quality": [],
        "pcset": [],
        "localKey": [],
        "tonicizedKey": [],
        "degree": [],
    }
    for rn in s.flat.getElementsByClass("RomanNumeral"):
        dfdict["offset"].append(rn.offset)
        dfdict["measure"].append(rn.measureNumber)
        dfdict["pitchNames"].append(tuple(rn.pitchNames))
        dfdict["bass"].append(rn.pitchNames[0])
        dfdict["root"].append(rn.root().name)
        dfdict["inversion"].append(rn.inversion())
        dfdict["quality"].append(rn.commonName)
        dfdict["pcset"].append(tuple(sorted(set(rn.pitchClasses))))
        dfdict["localKey"].append(rn.key.tonicPitchNameWithCase)
        secondaryKey = rn.secondaryRomanNumeralKey
        if secondaryKey:
            dfdict["tonicizedKey"].append(secondaryKey.tonicPitchNameWithCase)
        else:
            dfdict["tonicizedKey"].append(None)
        secondaryDegree = rn.secondaryRomanNumeral
        if secondaryDegree:
            degree = f"{rn.scaleDegree}/{secondaryDegree.scaleDegree}"
        else:
            degree = f"{rn.scaleDegree}"
        dfdict["degree"].append(degree)
    df = pd.DataFrame(dfdict)
    return df