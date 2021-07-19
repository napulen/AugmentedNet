"""Turns a RomanText file into a pandas DataFrame."""

import music21
import pandas as pd
import numpy as np
from common import FIXEDOFFSET, FLOATSCALE
import re


A_COLUMNS = [
    "a_offset",
    "a_measure",
    "a_duration",
    "a_annotationNumber",
    "a_romanNumeral",
    "a_isOnset",
    "a_pitchNames",
    "a_bass",
    "a_root",
    "a_inversion",
    "a_quality",
    "a_pcset",
    "a_localKey",
    "a_tonicizedKey",
    "a_degree1",
    "a_degree2",
]


# These have to be made lists again if read from a csv. They're stored as str.
A_LISTTYPE_COLUMNS = [
    "a_pitchNames",
    "a_pcset",
]


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


def _removeInversion(figure):
    ret = figure.replace("65", "7")
    ret = ret.replace("43", "7")
    ret = ret.replace("64", "")
    ret = ret.replace("6", "")
    ret = ret.replace("2", "7")
    return ret


def _preprocessRomanNumeral(figure):
    return _removeInversion(_simplifyRomanNumeral(_fixRnSynonyms(figure)))


def _initialDataFrame(s):
    """Parses an annotation RomanText file and produces a pandas dataframe.

    Unpacking a roman numeral is slightly more complicated here than in
    previous approaches/papers, the reason is that I include more features
    than usual (e.g., inversion). It may be easier to predict which features
    lead to a better Roman numeral reconstruction this way.
    """
    dfdict = {col: [] for col in A_COLUMNS}
    for idx, rn in enumerate(s.flat.getElementsByClass("RomanNumeral")):
        dfdict["a_offset"].append(round(float(rn.offset), FLOATSCALE))
        dfdict["a_measure"].append(rn.measureNumber)
        dfdict["a_duration"].append(round(float(rn.quarterLength), FLOATSCALE))
        dfdict["a_annotationNumber"].append(idx)
        dfdict["a_romanNumeral"].append(_preprocessRomanNumeral(rn.figure))
        dfdict["a_isOnset"].append(True)
        dfdict["a_pitchNames"].append(tuple(rn.pitchNames))
        dfdict["a_bass"].append(rn.pitchNames[0])
        dfdict["a_root"].append(rn.root().name)
        dfdict["a_inversion"].append(rn.inversion())
        dfdict["a_quality"].append(rn.commonName)
        dfdict["a_pcset"].append(tuple(sorted(set(rn.pitchClasses))))
        localKey = rn.key.tonicPitchNameWithCase
        dfdict["a_localKey"].append(localKey)
        secondaryKey = rn.secondaryRomanNumeralKey
        if secondaryKey:
            tonicizedKey = secondaryKey.tonicPitchNameWithCase
            dfdict["a_tonicizedKey"].append(tonicizedKey)
        else:
            # if there is no tonicization, encode the local key
            dfdict["a_tonicizedKey"].append(localKey)
        scaleDegree, alteration = rn.scaleDegreeWithAlteration
        if alteration:
            scaleDegree = f"{alteration.modifier}{scaleDegree}"
        else:
            scaleDegree = f"{scaleDegree}"
        dfdict["a_degree1"].append(str(scaleDegree))
        secondaryDegree = rn.secondaryRomanNumeral
        if secondaryDegree:
            scaleDegree, alteration = secondaryDegree.scaleDegreeWithAlteration
            if alteration:
                scaleDegree = f"{alteration.modifier}{scaleDegree}"
            else:
                scaleDegree = f"{scaleDegree}"
            dfdict["a_degree2"].append(scaleDegree)
        else:
            dfdict["a_degree2"].append("None")
    df = pd.DataFrame(dfdict)
    df.set_index("a_offset", inplace=True)
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
    maxOffset = (lastRow.index + lastRow.a_duration).to_numpy()[0]
    newIndex = np.arange(minOffset, maxOffset, fixedOffset)
    # All operations done over the full index, i.e., fixed-timesteps
    # plus original onsets. Later, original onsets (e.g., triplets)
    # are removed and just the fixed-timesteps are kept
    df = df.reindex(index=df.index.union(newIndex))
    # here onsets are easier, every "injected" index is not an onset
    df.a_isOnset.fillna(value=False, inplace=True)
    df.fillna(method="ffill", inplace=True)
    df = df.reindex(index=newIndex)
    return df


def parseAnnotation(f, fixedOffset=FIXEDOFFSET, eventBased=False):
    """Generates the DataFrame from a RomanText file.

    Parses the file using music21. Creates an initial DataFrame
    with every onset event of the music21 stream. Finally,
    does the sampling at symbolically regular durations fixedOffset.
    """
    # Step 0: Use music21 to parse the score
    s = _m21Parse(f)
    # Step 1: Parse and produce a salami-sliced dataset
    df = _initialDataFrame(s)
    # Step 2: Turn salami-slice into fixed-duration steps
    if not eventBased:
        df = _reindexDataFrame(df, fixedOffset=fixedOffset)
    return df
