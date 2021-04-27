import music21
from music21.interval import Interval
from music21.pitch import Pitch
from numpy.lib.ufunclike import fix
import pandas as pd
import numpy as np
from common import FIXEDOFFSET, FLOATSCALE
import io
from itertools import combinations
from texturizers import getTemplate

S_COLUMNS = [
    "s_offset",
    "s_duration",
    "s_measure",
    "s_notes",
    "s_intervals",
    "s_isOnset",
]

S_LISTTYPE_COLUMNS = [
    "s_notes",
    "s_intervals",
    "s_isOnset",
]


def _m21Parse(f, fmt=None):
    return music21.converter.parse(f, format=fmt)


def _measureNumberShift(m21Score):
    firstMeasure = m21Score.parts[0].measure(0) or m21Score.parts[0].measure(1)
    isAnacrusis = True if firstMeasure.paddingLeft > 0.0 else False
    if isAnacrusis and firstMeasure.number == 1:
        measureNumberShift = -1
    else:
        measureNumberShift = 0
    return measureNumberShift


def _lastOffset(m21Score):
    lastMeasure = m21Score.parts[0].measure(-1)
    filledDuration = lastMeasure.duration.quarterLength / float(
        lastMeasure.barDurationProportion()
    )
    lastOffset = lastMeasure.offset + filledDuration
    return lastOffset


def _initialDataFrame(s, fmt=None):
    """Parses a score and produces a pandas dataframe.

    The features obtained are the note names, their position in the score,
    measure number, and their ties (in case something fancy needs to be done,
    with the tie information).
    """
    dfdict = {col: [] for col in S_COLUMNS}
    measureNumberShift = _measureNumberShift(s)
    for c in s.chordify().flat.notesAndRests:
        dfdict["s_offset"].append(round(float(c.offset), FLOATSCALE))
        dfdict["s_duration"].append(round(float(c.quarterLength), FLOATSCALE))
        dfdict["s_measure"].append(c.measureNumber + measureNumberShift)
        if "Rest" in c.classes:
            # We need dummy entries for rests at the beginning of a measure
            dfdict["s_notes"].append(np.nan)
            dfdict["s_intervals"].append(np.nan)
            dfdict["s_isOnset"].append(np.nan)
            continue
        dfdict["s_notes"].append([n.pitch.nameWithOctave for n in c])
        intvs = [Interval(c[0].pitch, p).simpleName for p in c.pitches[1:]]
        dfdict["s_intervals"].append(intvs)
        onsets = [(not n.tie or n.tie.type == "start") for n in c]
        dfdict["s_isOnset"].append(onsets)
    df = pd.DataFrame(dfdict)
    currentLastOffset = float(df.tail(1).s_offset) + float(
        df.tail(1).s_duration
    )
    deltaDuration = _lastOffset(s) - currentLastOffset
    df.loc[len(df) - 1, "s_duration"] += deltaDuration
    df.set_index("s_offset", inplace=True)
    df = df[~df.index.duplicated()]
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
    maxOffset = (lastRow.index + lastRow.s_duration).to_numpy()[0]
    newIndex = np.arange(minOffset, maxOffset, fixedOffset)
    # All operations done over the full index, i.e., fixed-timesteps
    # plus original onsets. Later, original onsets (e.g., triplets)
    # are removed and just the fixed-timesteps are kept
    df = df.reindex(index=df.index.union(newIndex))
    df.s_notes.fillna(method="ffill", inplace=True)
    df.s_notes.fillna(method="bfill", inplace=True)
    # the "isOnset" column is hard to generate in fixed-timesteps
    # however, it allows us to encode a "hold" symbol if we wanted to
    newCol = pd.Series(
        [[False] * n for n in df.s_notes.str.len().to_list()], index=df.index
    )
    df.s_isOnset.fillna(value=newCol, inplace=True)
    df.fillna(method="ffill", inplace=True)
    df.fillna(method="bfill", inplace=True)
    df = df.reindex(index=newIndex)
    return df


def _texturizeAnnotationScore(df, duration, numberOfNotes):
    # Preemptively, remove any notion of held notes in an annotation file
    df["s_isOnset"] = df.s_isOnset.apply(lambda l: [True for _ in l])
    outputdf = df.copy()
    # A copy because we don't want these two temporary columns in the output
    df["notesNumber"] = df.s_notes.apply(len)
    df["allOnsets"] = df.s_isOnset.apply(all)
    # Which block chords can we replace with a more complex texture
    replaceable = df[
        (df.s_duration == duration)
        & (df.notesNumber == numberOfNotes)
        & (df.allOnsets)
    ]
    for row in replaceable.itertuples():
        offset = row.Index
        measure = row.s_measure
        notes = row.s_notes
        intervals = [
            Interval(Pitch(n1), Pitch(n2)).simpleName
            for n1, n2 in combinations(notes, 2)
        ]
        template = getTemplate(duration, len(notes))
        texture = template.format(notes=notes, intervals=intervals)
        textureF = io.StringIO(texture)
        texturedf = pd.read_csv(textureF)
        texturedf["s_offset"] += offset
        texturedf["s_measure"] = measure
        for col in S_LISTTYPE_COLUMNS:
            texturedf[col] = texturedf[col].apply(eval)
        texturedf.set_index("s_offset", inplace=True)
        for index, row in texturedf.iterrows():
            outputdf.loc[index] = row
    outputdf.sort_index(inplace=True)
    return outputdf


def parseScore(f, fmt=None, fixedOffset=FIXEDOFFSET):
    # Step 0: Use music21 to parse the score
    s = _m21Parse(f, fmt)
    # Step 1: Parse and produce a salami-sliced dataset
    df = _initialDataFrame(s, fmt)
    # Step 2: Turn salami-slice into fixed-duration steps
    df = _reindexDataFrame(df, fixedOffset=fixedOffset)
    return df


def parseAnnotationAsScore(f, texturize=False, fixedOffset=FIXEDOFFSET):
    fmt = "romantext"
    if not texturize:
        return parseScore(f, fmt=fmt, fixedOffset=fixedOffset)
    # Step 0: Use music21 to parse the score
    s = _m21Parse(f, fmt=fmt)
    # Step 1: Parse and produce a salami-sliced dataset
    df = _initialDataFrame(s, fmt=fmt)
    # Step 2: Texturize the dataframe
    for duration in [4.0, 2.0, 1.0]:
        for numberOfNotes in [3, 4]:
            df = _texturizeAnnotationScore(df, duration, numberOfNotes)
    # Step 3: Turn salami-slice into fixed-duration steps
    df = _reindexDataFrame(df, fixedOffset=fixedOffset)
    return df
