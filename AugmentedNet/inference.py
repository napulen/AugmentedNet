"""Run the network to annotate an unseen musical input (inference)."""

import os

import music21
import numpy as np
import pandas as pd
import re
import tensorflow as tf
from tensorflow import keras

from . import __version__
from . import cli
from .chord_vocabulary import frompcset
from .cache import forceTonicization, getTonicizationScaleDegree
from .score_parser import parseScore
from .input_representations import available_representations as availableInputs
from .output_representations import (
    available_representations as availableOutputs,
)
from .utils import tensorflowGPUHack, disableGPU, padToSequenceLength


inversions = {
    "triad": {
        0: "",
        1: "6",
        2: "64",
    },
    "seventh": {
        0: "7",
        1: "65",
        2: "43",
        3: "2",
    },
}


def formatChordLabel(cl):
    """Format the chord label for end-user presentation."""
    # The only change I can think of: Cmaj -> C
    cl = cl.replace("maj", "") if cl.endswith("maj") else cl
    cl = cl.replace("-", "b")
    return cl


def formatRomanNumeral(rn, key):
    """Format the Roman numeral label for end-user presentation."""
    # Something of "I" and "I" of something
    if rn == "I/I":
        rn = "I"
    return rn


def solveChordSegmentation(df):
    return df.dropna()[df.HarmonicRhythm7 == 0]


def resolveRomanNumeral(b, t, a, s, pcs, key, tonicizedKey):
    chord = music21.chord.Chord(f"{b}2 {t}3 {a}4 {s}5")
    pcset = tuple(sorted(set(chord.pitchClasses)))
    # if the SATB notes don't make sense, use the pcset classifier
    if pcset not in frompcset:
        # which is guaranteed to exist in the chord vocabulary
        pcset = pcs
    # if the chord is nondiatonic to the tonicizedKey
    # force a tonicization where the chord does exist
    if tonicizedKey not in frompcset[pcset]:
        # print("Forcing a tonicization")
        candidateKeys = list(frompcset[pcset].keys())
        # prioritize modal mixture
        tonicizedKey = forceTonicization(key, candidateKeys)
    rnfigure = frompcset[pcset][tonicizedKey]["rn"]
    chord = frompcset[pcset][tonicizedKey]["chord"]
    quality = frompcset[pcset][tonicizedKey]["quality"]
    chordtype = "seventh" if len(pcset) == 4 else "triad"
    # if you can't find the predicted bass
    # in the pcset, assume root position
    inv = chord.index(b) if b in chord else 0
    invfigure = inversions[chordtype][inv]
    if invfigure in ["65", "43", "2"]:
        rnfigure = rnfigure.replace("7", invfigure)
    elif invfigure in ["6", "64"]:
        rnfigure += invfigure
    rn = rnfigure
    if tonicizedKey != key:
        denominator = getTonicizationScaleDegree(key, tonicizedKey)
        rn = f"{rn}/{denominator}"
    chordLabel = f"{chord[0]}{quality}"
    if inv != 0:
        chordLabel += f"/{chord[inv]}"
    return rn, chordLabel


def generateRomanText(h):
    metadata = h.metadata
    metadata.composer = metadata.composer or "Unknown"
    metadata.title = metadata.title or "Unknown"
    composer = metadata.composer.split("\n")[0]
    title = metadata.title.split("\n")[0]
    ts = {
        (ts.measureNumber, float(ts.beat)): ts.ratioString
        for ts in h.flat.getElementsByClass("TimeSignature")
    }
    rntxt = f"""\
Composer: {composer}
Title: {title}
Analyst: AugmentedNet v{__version__} - https://github.com/napulen/AugmentedNet
"""
    setKey = False
    currentMeasure = -1
    for n in h.flat.notes:
        if not n.lyric:
            continue
        rn = n.lyric.split()[0]
        key = ""
        measure = n.measureNumber
        beat = float(n.beat)
        if beat.is_integer():
            beat = int(beat)
        newts = ts.get((measure, beat), None)
        if newts:
            rntxt += f"\nTime Signature: {newts}\n"
        if ":" in rn:
            key, rn = rn.split(":")
        if measure != currentMeasure:
            rntxt += f"\nm{measure}"
            currentMeasure = measure
        if beat != 1:
            rntxt += f" b{round(beat, 3)}"
        if key:
            rntxt += f" {key.replace('-', 'b')}:"
        rntxt += f" {rn}"
    return rntxt


def predict(model, inputPath):
    df = parseScore(inputPath)
    inputs = [l.name.rsplit("_")[1] for l in model.inputs]
    encodedInputs = [availableInputs[i](df) for i in inputs]
    outputLayers = [l.name.split("/")[0] for l in model.outputs]
    seqlen = model.inputs[0].shape[1]
    modelInputs = [
        padToSequenceLength(i.array, seqlen, value=-1) for i in encodedInputs
    ]
    predictions = model.predict(modelInputs)
    predictions = [p.reshape(1, -1, p.shape[2]) for p in predictions]
    dfdict = {}
    for outputRepr, pred in zip(outputLayers, predictions):
        print(outputRepr, pred.shape)
        predOnehot = np.argmax(pred[0], axis=1).reshape(-1, 1)
        decoded = availableOutputs[outputRepr].decode(predOnehot)
        dfdict[outputRepr] = decoded
    dfout = pd.DataFrame(dfdict)
    scoreLength = len(dfout.index)
    paddedIndex = np.full((scoreLength,), np.nan)
    paddedMeasure = np.full((scoreLength,), np.nan)
    paddedIndex[: len(df.index)] = df.index
    paddedMeasure[: len(df.s_measure)] = df.s_measure
    dfout["offset"] = paddedIndex
    dfout["measure"] = paddedMeasure
    chords = solveChordSegmentation(dfout)
    s = music21.converter.parse(inputPath)
    # remove all lyrics from score
    for note in s.recurse().notes:
        note.lyrics = []
    prevkey = ""
    for analysis in chords.itertuples():
        notes = []
        for n in s.flat.notes.getElementsByOffset(analysis.offset):
            if isinstance(n, music21.note.Note):
                notes.append((n, n.pitch.midi))
            elif isinstance(n, music21.chord.Chord) and not isinstance(
                n, music21.harmony.NoChord
            ):
                notes.append((n, n[0].pitch.midi))
        if not notes:
            continue
        bass = sorted(notes, key=lambda n: n[1])[0][0]
        thiskey = analysis.LocalKey38
        tonicizedKey = analysis.TonicizedKey38
        pcset = analysis.PitchClassSet121
        rn2, chordLabel = resolveRomanNumeral(
            analysis.Bass35,
            analysis.Tenor35,
            analysis.Alto35,
            analysis.Soprano35,
            pcset,
            thiskey,
            tonicizedKey,
        )
        if thiskey != prevkey:
            rn2fig = f"{thiskey}:{rn2}"
            prevkey = thiskey
        else:
            rn2fig = rn2
        bass.addLyric(formatRomanNumeral(rn2fig, thiskey))
        bass.addLyric(formatChordLabel(chordLabel))
    rntxt = generateRomanText(s)
    filename, _ = inputPath.rsplit(".", 1)
    annotatedScore = f"{filename}_annotated.musicxml"
    annotationCSV = f"{filename}_annotated.csv"
    annotatedRomanText = f"{filename}_annotated.rntxt"
    s.write(fp=annotatedScore)
    dfout.to_csv(annotationCSV)
    with open(annotatedRomanText, "w") as fd:
        fd.write(rntxt)


def batch(inputPath, dir, modelPath, useGpu):
    if useGpu:
        tensorflowGPUHack()
    else:
        disableGPU()
    model = keras.models.load_model(modelPath)
    if not dir and not os.path.isdir(inputPath):
        predict(model, inputPath)
    for root, _, files in os.walk(inputPath):
        for f in files:
            name, ext = os.path.splitext(f)
            if ext not in [".mxl", ".xml", ".musicxml", ".krn"]:
                continue
            if "_annotated" in name:
                # do not recursively annotate an annotated_file
                continue
            filepath = os.path.join(root, f)
            predict(model, inputPath=filepath)


if __name__ == "__main__":
    parser = cli.inference()
    args = parser.parse_args()
    kwargs = vars(args)
    batch(**kwargs)
