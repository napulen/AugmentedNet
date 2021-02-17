import music21
import pandas as pd
from config import FRAMESPERQUARTERNOTE


def parseScore(f):
    """Parses a score and produces a pandas dataframe.

    The features obtained are the note names, their position in the score,
    measure number, and their ties (in case something fancy needs to be done,
    with the tie information).
    """
    s = music21.converter.parse(f)
    dfdict = {
        "offset": [],
        "measure": [],
        "notes": [],
        "ties": [],
    }
    for c in s.chordify().flat.notes:
        dfdict["offset"].append(c.offset)
        dfdict["measure"].append(c.measureNumber)
        dfdict["notes"].append([n.pitch.nameWithOctave for n in c])
        dfdict["ties"].append([n.tie.type if n.tie else None for n in c])
    df = pd.DataFrame(dfdict)
    return df
