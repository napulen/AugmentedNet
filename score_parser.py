import music21
from music21.interval import Interval
import pandas as pd
import numpy as np
from common import FIXEDOFFSET, FLOATSCALE


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
    dfdict = {
        "offset": [],
        "duration": [],
        "measure": [],
        "notes": [],
        "intervals": [],
        "isOnset": [],
    }
    measureNumberShift = _measureNumberShift(s)
    for c in s.chordify().flat.notesAndRests:
        dfdict["offset"].append(round(float(c.offset), FLOATSCALE))
        dfdict["duration"].append(round(float(c.quarterLength), FLOATSCALE))
        dfdict["measure"].append(c.measureNumber + measureNumberShift)
        if 'Rest' in c.classes:
            # We need dummy entries for rests at the beginning of a measure
            dfdict["notes"].append(np.nan)
            dfdict["intervals"].append(np.nan)
            dfdict["isOnset"].append(np.nan)
            continue
        dfdict["notes"].append([n.pitch.nameWithOctave for n in c])
        dfdict["intervals"].append(
            [Interval(c[0].pitch, p).semiSimpleName for p in c.pitches[1:]]
        )
        dfdict["isOnset"].append(
            [(not n.tie or n.tie.type == "start") for n in c]
        )

    df = pd.DataFrame(dfdict)
    currentLastOffset = float(df.tail(1).offset) + float(df.tail(1).duration)
    deltaDuration = _lastOffset(s) - currentLastOffset
    df.loc[len(df) - 1, 'duration'] += deltaDuration
    df.set_index("offset", inplace=True)
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
    maxOffset = (lastRow.index + lastRow.duration).to_numpy()[0]
    newIndex = np.arange(minOffset, maxOffset, fixedOffset)
    # All operations done over the full index, i.e., fixed-timesteps
    # plus original onsets. Later, original onsets (e.g., triplets)
    # are removed and just the fixed-timesteps are kept
    df = df.reindex(index=df.index.union(newIndex))
    df.notes.fillna(method="ffill", inplace=True)
    # the "isOnset" column is hard to generate in fixed-timesteps
    # however, it allows us to encode a "hold" symbol if we wanted to
    newCol = pd.Series(
        [[False] * n for n in df.notes.str.len().to_list()], index=df.index
    )
    df.isOnset.fillna(value=newCol, inplace=True)
    df.fillna(method="ffill", inplace=True)
    df = df.reindex(index=newIndex)
    return df


def parseScore(f, fmt=None):
    # Step 0: Use music21 to parse the score
    s = _m21Parse(f, fmt)
    # Step 1: Parse and produce a salami-sliced dataset
    df = _initialDataFrame(s, fmt)
    # Step 2: Turn salami-slice into fixed-duration steps
    df = _reindexDataFrame(df)
    return df
