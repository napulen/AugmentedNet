import music21
import pandas as pd
import numpy as np
from common import FIXEDOFFSET, FLOATSCALE


def _m21Parse(f, fmt=None):
    return music21.converter.parse(f, format=fmt)


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
        "isOnset": [],
    }
    for c in s.chordify().flat.notes:
        dfdict["offset"].append(round(float(c.offset), FLOATSCALE))
        dfdict["duration"].append(round(float(c.quarterLength), FLOATSCALE))
        dfdict["measure"].append(c.measureNumber)
        dfdict["notes"].append([n.pitch.nameWithOctave for n in c])
        dfdict["isOnset"].append(
            [(not n.tie or n.tie.type == "start") for n in c]
        )
    # Make the last note to last for the entire measure
    lastMmNumber = dfdict["measure"][-1]
    lastMm = s.chordify().measure(lastMmNumber)
    lastMmDuration = round(float(lastMm.duration.quarterLength), FLOATSCALE)
    if lastMmDuration > dfdict["duration"][-1]:
        dfdict["duration"][-1] = lastMmDuration
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
