"""Turns an audio/chroma file into a pandas DataFrame."""

import pandas as pd

from .common import FIXEDOFFSET, FLOATSCALE

C_COLUMNS = [
    "c_offset",
    "c_basschroma",
    "c_chroma",
]

C_LISTTYPE_COLUMNS = [
    "c_basschroma",
    "c_chroma",
]


def from_tsv(tsv, sep="\t"):
    df = pd.read_csv(tsv, sep=sep)
    df.set_index("c_offset", inplace=True)
    for col in C_LISTTYPE_COLUMNS:
        df[col] = df[col].apply(eval)
    return df


def _initialDataFrame(s):
    """Parses a chroma and produces a pandas dataframe."""
    dfdict = {col: [] for col in C_COLUMNS}
    with open(s) as fd:
        rows = fd.readlines()
    for r in rows:
        row = r.strip().split(",")
        t = row[0]
        basschroma = [float(pc) for pc in row[1:13]]
        basschroma = basschroma[3:] + basschroma[:3]
        basschromaSum = sum(basschroma)
        if basschromaSum != 0:
            basschroma = [
                round(pc / basschromaSum, FLOATSCALE) for pc in basschroma
            ]
        chroma = [float(pc) for pc in row[13:]]
        chroma = chroma[3:] + chroma[:3]
        chromaSum = sum(chroma)
        if chromaSum != 0:
            chroma = [round(pc / chromaSum, FLOATSCALE) for pc in chroma]
        dfdict["c_offset"].append(round(float(t), FLOATSCALE))
        dfdict["c_basschroma"].append(basschroma)
        dfdict["c_chroma"].append(chroma)
    df = pd.DataFrame(dfdict)
    df.set_index("c_offset", inplace=True)
    return df


def parseAudio(f, fixedOffset=FIXEDOFFSET):
    # Step 1: Parse and produce a dataframe of chromagrams
    df = _initialDataFrame(f)
    return df