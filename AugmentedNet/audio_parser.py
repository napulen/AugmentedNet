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


def _initialDataFrameCSV(s):
    """Parses a chroma CSV and produces a pandas dataframe."""
    dfdict = {col: [] for col in C_COLUMNS}
    with open(s) as fd:
        rows = fd.readlines()
    for r in rows:
        row = r.strip().split(",")
        t = row[0]
        basschroma = [float(pc) for pc in row[1:13]]
        basschroma = basschroma[3:] + basschroma[:3]
        basschroma = _normalizeChroma(basschroma)
        chroma = [float(pc) for pc in row[13:]]
        chroma = chroma[3:] + chroma[:3]
        chroma = _normalizeChroma(chroma)
        dfdict["c_offset"].append(round(float(t), FLOATSCALE))
        dfdict["c_basschroma"].append(basschroma)
        dfdict["c_chroma"].append(chroma)
    df = pd.DataFrame(dfdict)
    df.set_index("c_offset", inplace=True)
    return df

def _normalizeChroma(chroma):
    # chroma = [1.0 if pc > 1.0 else 0.0 for pc in chroma]
    chromaSum = sum(chroma)
    if chromaSum != 0:
        chroma = [round(pc / chromaSum, FLOATSCALE) for pc in chroma]
    return chroma

def _initialDataFrameARFF(s, column):
    """Parses a chroma ARFF and produces a pandas dataframe."""
    dfdict = {"c_offset": [], column: []}
    chroma = []
    with open(s) as fd:
        rows = fd.readlines()
    skip = True
    for r in rows:
        if "@DATA" in r:
            skip = False
            continue
        elif skip:
            continue
        row = r.strip().split(",")
        t = row[-1]
        chroma = [float(pc) for pc in row[0:12]]
        chroma = chroma[3:] + chroma[:3]
        chroma = _normalizeChroma(chroma)
        dfdict["c_offset"].append(round(float(t), FLOATSCALE))
        dfdict[column].append(chroma)
    df = pd.DataFrame(dfdict)
    df.set_index("c_offset", inplace=True)
    return df


def parseAudio(f, fixedOffset=FIXEDOFFSET):
    # Step 1: Parse and produce a dataframe of chromagrams
    if f.endswith(".csv"):
        df = _initialDataFrameCSV(f)
    elif f.endswith(".arff"):
        df = _initialDataFrameARFF(f, "c_chroma")
        fbass = f.replace("250.arff", "251.arff")
        dfbasschroma = _initialDataFrameARFF(fbass, "c_basschroma")
        df["c_basschroma"] = dfbasschroma.c_basschroma
    return df