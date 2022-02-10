"""Turns a RomanText file into a pandas DataFrame."""

import music21
import numpy as np
import pandas as pd
import re

from .common import FIXEDOFFSET, FLOATSCALE
from .chord_vocabulary import frompcset

A_COLUMNS = [
    "a_offset",
    "a_measure",
    "a_duration",
    "a_annotationNumber",
    "a_romanNumeral",
    "a_harmonicRhythm",
    "a_pitchNames",
    "a_bass",
    "a_tenor",
    "a_alto",
    "a_soprano",
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
    ret = ret.replace("N", "bII")
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
    return _fixRnSynonyms(_simplifyRomanNumeral(figure))


def _initialDataFrame(s):
    """Parses an annotation RomanText file and produces a pandas dataframe.

    Unpacking a roman numeral is slightly more complicated here than in
    previous approaches/papers, the reason is that I include more features
    than usual (e.g., inversion). It may be easier to predict which features
    lead to a better Roman numeral reconstruction this way.
    """
    dfdict = {col: [] for col in A_COLUMNS}
    for idx, rn in enumerate(s.flat.getElementsByClass("RomanNumeral")):
        if (
            "Ger" not in rn.figure
            and "Fr" not in rn.figure
            and "It" not in rn.figure
        ):
            if rn.figure == "I4":
                # found in wir-monteverdi-madrigals-book-3-10
                rn.figure = "I"
            if rn.figure == "iv4":
                rn.figure = "iv"
            if rn.figure == "v4":
                rn.figure = "v"
            if rn.figure == "V4":
                rn.figure = "V"
            rn.figure = _preprocessRomanNumeral(rn.figure)
        dfdict["a_offset"].append(round(float(rn.offset), FLOATSCALE))
        dfdict["a_measure"].append(rn.measureNumber)
        dfdict["a_duration"].append(round(float(rn.quarterLength), FLOATSCALE))
        dfdict["a_annotationNumber"].append(idx)
        dfdict["a_romanNumeral"].append(_removeInversion(rn.figure))
        dfdict["a_harmonicRhythm"].append(0)
        dfdict["a_pitchNames"].append(tuple(rn.pitchNames))
        dfdict["a_bass"].append(rn.pitchNames[0])
        dfdict["a_tenor"].append(rn.pitchNames[1])
        dfdict["a_alto"].append(rn.pitchNames[2])
        if len(rn.pitchNames) == 4:
            dfdict["a_soprano"].append(rn.pitchNames[3])
        else:
            dfdict["a_soprano"].append(rn.root().name)
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
        rntextrn = dfdict['a_romanNumeral'][-1]
        pcset = dfdict["a_pcset"][-1]
        harmalysisrn = "!!!!!!!!!!!!!!!!!!!!!"
        key = dfdict["a_tonicizedKey"][-1]
        if pcset in frompcset:
            if key in frompcset[pcset]:
                harmalysisrn = frompcset[pcset][key]["rn"]
            else:
                harmalysisrn = "?????????????????????????"
        print(f"RomanText: {rntextrn} -> Harmalysis: {harmalysisrn}\t{key} {pcset}")
    df = pd.DataFrame(dfdict)
    df.set_index("a_offset", inplace=True)
    return df


def _harmonicRhythmPostprocessing(a_harmonicRhythm):
    """This is a new approach for harmonic rhythm to balance the classes.

    Instead of providing 'is_onset' True/False kind of annotations,
    log the duration elapsed since the last chord.

    0 - this is a chord onset
    1 - a 32nd note has passed since the last chord
    2 - a 16th note has passed since the last chord
    3 - an eighth note has passed since the last chord
    4 - a quarter note has passed since the last chord
    5 - a half note has passed since the last chord
    6 - a whole note has passed since the last chord"""
    template = [1, 2, 2, 3, 3, 3, 3] + ([4] * 8) + ([5] * 16) + ([6] * 32)
    hr = a_harmonicRhythm.to_list()
    t = 62
    for i in range(len(a_harmonicRhythm)):
        if hr[i] == 0:
            t = 0
        else:
            hr[i] = template[min(t, 62)]
            t += 1
    return hr


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
    # the harmonic rhythm is postprocessed to reduce class imbalance
    harmRhythm = _harmonicRhythmPostprocessing(df.a_harmonicRhythm)
    df["a_harmonicRhythm"] = harmRhythm
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
