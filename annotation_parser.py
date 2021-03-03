import music21
import pandas as pd
import numpy as np
from common import FIXEDOFFSET, FLOATSCALE
import re


def _m21Parse(f):
    return music21.converter.parse(f, format="romantext")


def _fixRnSynonyms(figure):
    ret = figure.replace("6/4", "64")
    ret = ret.replace("6/5", "65")
    ret = ret.replace("4/3", "43")
    ret = ret.replace("4/2", "42")
    ret = ret.replace("42", "2")
    ret = ret.replace("bII", "N")
    return ret


def _simplifyRomanNumeral(figure):
    missingAdd = re.compile("(\[.*\])")
    return missingAdd.sub("", figure)


def _preprocessRomanNumeral(figure):
    return _removeInversion(_simplifyRomanNumeral(_fixRnSynonyms(figure)))


def _removeInversion(figure):
    ret = figure.replace("65", "7")
    ret = ret.replace("43", "7")
    ret = ret.replace("64", "")
    ret = ret.replace("6", "")
    ret = ret.replace("2", "7")
    return ret


def _initialDataFrame(s):
    """Parses an annotation RomanText file and produces a pandas dataframe.

    Unpacking a roman numeral is slightly more complicated here than in
    previous approaches/papers, the reason is that some features do not
    seem to work well (e.g., inversion). It may be easier to predict others
    which may still serve to reconstruct the roman numeral.
    """
    dfdict = {
        "offset": [],
        "measure": [],
        "duration": [],
        "romanNumeral": [],
        "isOnset": [],
        "pitchNames": [],
        "bass": [],
        "root": [],
        "inversion": [],
        "quality": [],
        "pcset": [],
        "localKey": [],
        "tonicizedKey": [],
        "degree1": [],
        "degree2": [],
    }
    for rn in s.flat.getElementsByClass("RomanNumeral"):
        dfdict["offset"].append(round(float(rn.offset), FLOATSCALE))
        dfdict["measure"].append(rn.measureNumber)
        dfdict["duration"].append(round(float(rn.quarterLength), FLOATSCALE))
        dfdict["romanNumeral"].append(_preprocessRomanNumeral(rn.figure))
        dfdict["isOnset"].append(True)
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
            dfdict["tonicizedKey"].append("None")
        scaleDegree, alteration = rn.scaleDegreeWithAlteration
        if alteration:
            scaleDegree = f"{alteration.modifier}{scaleDegree}"
        else:
            scaleDegree = f"{scaleDegree}"
        dfdict["degree1"].append(str(scaleDegree))
        secondaryDegree = rn.secondaryRomanNumeral
        if secondaryDegree:
            scaleDegree, alteration = secondaryDegree.scaleDegreeWithAlteration
            if alteration:
                scaleDegree = f"{alteration.modifier}{scaleDegree}"
            else:
                scaleDegree = f"{scaleDegree}"
            dfdict["degree2"].append(scaleDegree)
        else:
            dfdict["degree2"].append("None")
    df = pd.DataFrame(dfdict)
    df.set_index("offset", inplace=True)
    return df


def _reindexDataFrame(df, fixedOffset=FIXEDOFFSET):
    """Reindexes a dataframe according to a fixed note-value.

    It could be said that the DataFrame produced by parseScore
    is a "salami-sliced" version of the score. This is intuitive
    for humans, but does not really work in machine learning.

    What works, is to slice the score in fixed note intervals,
    for example, a sixteenth note. This reindex function does
    exactly that.
    """
    firstRow = df.head(1)
    lastRow = df.tail(1)
    minOffset = firstRow.index.to_numpy()[0]
    maxOffset = (lastRow.index + lastRow.duration).to_numpy()[0]
    newIndex = np.arange(minOffset, maxOffset, fixedOffset)
    # All operations done over the full index, i.e., fixed-timesteps
    # plus original onsets. Later, original onsets (e.g., triplets)
    # are removed and just the fixed-timesteps are kept
    df = df.reindex(index=df.index.union(newIndex))
    # here onsets are easier, every "injected" index is not an onset
    df.isOnset.fillna(value=False, inplace=True)
    df.fillna(method="ffill", inplace=True)
    df = df.reindex(index=newIndex)
    return df


def parseAnnotation(f):
    # Step 0: Use music21 to parse the score
    s = _m21Parse(f)
    # Step 1: Parse and produce a salami-sliced dataset
    df = _initialDataFrame(s)
    # Step 2: Turn salami-slice into fixed-duration steps
    df = _reindexDataFrame(df)
    return df