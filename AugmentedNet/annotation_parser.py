"""Turns a RomanText file into a pandas DataFrame."""

import music21
import numpy as np
import pandas as pd
import re

from .cache import forceTonicization, getTonicizationScaleDegree
from .common import FIXEDOFFSET, FLOATSCALE
from .chord_vocabulary import frompcset, closestPcSet

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
        rn, rncorr = _extractRomanNumeralInformation(rn)
        rncorr = _correctRomanNumeral(rncorr)
        dfdict["a_offset"].append(round(float(rn.offset), FLOATSCALE))
        dfdict["a_measure"].append(rn.measureNumber)
        dfdict["a_duration"].append(round(float(rn.quarterLength), FLOATSCALE))
        dfdict["a_annotationNumber"].append(idx)
        dfdict["a_romanNumeral"].append(_removeInversion(rncorr["rn"]))
        dfdict["a_harmonicRhythm"].append(0)
        dfdict["a_pitchNames"].append(tuple(rncorr["pitchNames"]))
        dfdict["a_bass"].append(rncorr["pitchNames"][0])
        dfdict["a_tenor"].append(rncorr["pitchNames"][1])
        dfdict["a_alto"].append(rncorr["pitchNames"][2])
        if len(rncorr["pitchNames"]) == 4:
            dfdict["a_soprano"].append(rncorr["pitchNames"][3])
        else:
            dfdict["a_soprano"].append(rncorr["root"])
        dfdict["a_root"].append(rncorr["root"])
        dfdict["a_inversion"].append(rncorr["inversion"])
        dfdict["a_quality"].append(rn.commonName)
        dfdict["a_pcset"].append(rncorr["pcset"])
        dfdict["a_localKey"].append(rncorr["localKey"])
        dfdict["a_tonicizedKey"].append(rncorr["tonicizedKey"])
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


def _extractRomanNumeralInformation(rn):
    """Hacks and workarounds to retrieve the RomanNumeral from music21."""
    if (
        "Ger" not in rn.figure
        and "Fr" not in rn.figure
        and "It" not in rn.figure
    ):
        if rn.figure in ["I4", "iv4", "v4", "V4"]:
            rn.figure = rn.figure.replace("4", "")
        if rn.figure in ["V9", "V7M9"]:
            rn.figure = "V7"
        rn.figure = _preprocessRomanNumeral(rn.figure)
    romanNumeral = _removeInversion(rn.figure)
    pcset = tuple(sorted(set(rn.pitchClasses)))
    pitchNames = rn.pitchNames
    localKey = rn.key.tonicPitchNameWithCase
    secondaryKey = rn.secondaryRomanNumeralKey
    if secondaryKey:
        tonicizedKey = secondaryKey.tonicPitchNameWithCase
    else:
        tonicizedKey = localKey
    if localKey == "c-":
        # It happens for one measure in a piece by Wolf and c- is a stretch
        localKey = "b"
        tonicizedKey = "b"
    cleaned = {
        "rn": romanNumeral,
        "pcset": pcset,
        "pitchNames": pitchNames,
        "localKey": localKey,
        "tonicizedKey": tonicizedKey,
    }
    return rn, cleaned


def _correctRomanNumeral(rndata):
    """Trust nobody. Rewrite all Roman numerals based on chord vocabulary."""
    rn = rndata["rn"]
    pcset = rndata["pcset"]
    pitchNames = rndata["pitchNames"]
    localKey = rndata["localKey"]
    tonicizedKey = rndata["tonicizedKey"]
    # CHORD (PCSET)
    if not pcset in frompcset:
        # We get a valid pcset yes or yes
        pcset = closestPcSet(pcset)
    # TONICIZATION
    if tonicizedKey not in frompcset[pcset]:
        # Find a new tonicizedKey
        candidateKeys = list(frompcset[pcset].keys())
        tonicizedKey = forceTonicization(localKey, candidateKeys)
    chord = frompcset[pcset][tonicizedKey]["chord"]
    root = chord[0]
    numerator = frompcset[pcset][tonicizedKey]["rn"]
    myrn = numerator
    if tonicizedKey != localKey:
        denominator = getTonicizationScaleDegree(localKey, tonicizedKey)
        if denominator not in ["i", "I"]:
            myrn += f"/{denominator}"
    # INVERSION
    presumedBass = pitchNames[0]
    inversion = chord.index(presumedBass) if presumedBass in chord else 0
    pitchNames = chord[inversion:] + chord[:inversion]
    # CADENTIAL
    if "Cad" in rn and numerator in ["I", "i"] and inversion == 2:
        print("Found a cadential")
        myrn = myrn.replace(numerator, "Cad", 1)
        numerator = "Cad"
    if rn != myrn:
        mode = "minor" if localKey.islower() else "major"
        print(f"\t\t{rn} -> {myrn}\t{pcset}{mode}")
    rndata["rn"] = numerator # without tonicizations
    rndata["pcset"] = pcset
    rndata["tonicizedKey"] = tonicizedKey
    rndata["pitchNames"] = pitchNames
    rndata["root"] = root
    rndata["inversion"] = inversion
    return rndata


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
