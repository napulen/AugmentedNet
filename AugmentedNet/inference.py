"""Run the network to annotate an unseen musical input (inference)."""

import os

import music21
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras

from . import cli
from .chord_vocabulary import frompcset
from .cache import forceTonicization, getTonicizationScaleDegree
from .score_parser import parseScore
from .input_representations import available_representations as availableInputs
from .output_representations import (
    available_representations as availableOutputs,
)


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


def tensorflowGPUHack():
    # https://github.com/tensorflow/tensorflow/issues/37942
    gpu_devices = tf.config.experimental.list_physical_devices("GPU")
    for device in gpu_devices:
        tf.config.experimental.set_memory_growth(device, True)


def disableGPU():
    # Disabling the GPU
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def _padToSequenceLength(arr, sequenceLength):
    frames, features = arr.shape
    featuresPerSequence = sequenceLength * features
    featuresInExample = frames * features
    padding = featuresPerSequence - (featuresInExample % featuresPerSequence)
    arr = np.pad(arr.reshape(-1), (0, padding))
    arr = arr.reshape(-1, sequenceLength, features)
    return arr


def solveChordSegmentation(df):
    return df.dropna()[df.HarmonicRhythm7 == 0]


def resolveRomanNumeral(b, t, a, s, pcs, key, tonicizedKey):
    chord = music21.chord.Chord(f"{b}2 {t}3 {a}4 {s}5")
    pcset = tuple(sorted(set(chord.pitchClasses)))
    # if the SATB notes don't make sense, use the pcset classifier
    if pcset not in frompcset:
        # which is guaranteed to exist in the chord vocabulary
        pcset = pcs if pcs != "None" else (0, 4, 7)
    # if the chord is nondiatonic to the tonicizedKey
    # force a tonicization where the chord does exist
    if tonicizedKey not in frompcset[pcset]:
        print("Forcing a tonicization")
        candidateKeys = list(frompcset[pcset].keys())
        # prioritize modal mixture
        parallel = tonicizedKey.lower()
        if parallel in candidateKeys:
            print(f"\tTonicizing the parallel, {parallel}")
            tonicizedKey = parallel
        else:
            tonicizedKey = forceTonicization(key, candidateKeys)
    rnfigure = frompcset[pcset][tonicizedKey]["rn"]
    chord = frompcset[pcset][tonicizedKey]["chord"]
    chordtype = "seventh" if len(pcset) == 4 else "triad"
    # if you can't find the predicted bass
    # in the pcset, assume root position
    inv = chord.index(b) if b in chord else 0
    invfigure = inversions[chordtype][inv]
    if invfigure in ["65", "43", "2"]:
        rnfigure = rnfigure.replace("7", invfigure)
    elif invfigure in ["6", "64"]:
        rnfigure += invfigure
    rn = music21.roman.RomanNumeral(rnfigure, tonicizedKey)
    if tonicizedKey != key:
        denominator = getTonicizationScaleDegree(key, tonicizedKey)
        rn = music21.roman.RomanNumeral(f"{rn.figure}/{denominator}", key)
    return rn


def simplifyChordLabel(label):
    label = label.replace("-incomplete ", "-")
    label = label.replace("-major triad", "")
    label = label.replace("-minor triad", "min")
    label = label.replace("-diminished triad", "dim")
    label = label.replace("-augmented triad", "aug")
    label = label.replace("-dominant seventh chord", "7")
    label = label.replace("-major seventh chord", "maj7")
    label = label.replace("-minor seventh chord", "min7")
    label = label.replace("-minor-seventh chord", "min7")
    label = label.replace("-half-diminished seventh chord", "hdim7")
    label = label.replace("-diminished seventh chord", "dim7")
    label = label.replace("-German augmented sixth chord", "Ger")
    return label


def simplifyArabicNumerals(figure):
    # Diminished seventh of a major key
    figure = figure.replace("b753", "7")
    figure = figure.replace("6b5", "65")
    figure = figure.replace("64b3", "43")
    # Another diminished seventh case
    figure = figure.replace("#653", "65")
    figure = figure.replace("6#43", "65")
    figure = figure.replace("64#2", "65")
    # Dominant seventh of a minor key
    figure = figure.replace("75#3", "7")
    figure = figure.replace("#643", "43")
    figure = figure.replace("6#42", "2")
    return figure


def predict(modelPath, inputFile, useGpu=False):
    if useGpu:
        tensorflowGPUHack()
    else:
        disableGPU()
    model = keras.models.load_model(modelPath)
    df = parseScore(inputFile)
    inputs = [l.name.rsplit("_")[1] for l in model.inputs]
    encodedInputs = [availableInputs[i](df) for i in inputs]
    outputLayers = [l.name.split("/")[0] for l in model.outputs]
    # TODO: How to decide the sequence length?
    modelInputs = [_padToSequenceLength(i.array, 640) for i in encodedInputs]
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
    s = music21.converter.parse(inputFile)
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
        thiskey = analysis.LocalKey35
        tonicizedKey = analysis.TonicizedKey35
        pcset = analysis.PitchClassSet121
        rn2 = resolveRomanNumeral(
            analysis.Bass35,
            analysis.Tenor35,
            analysis.Alto35,
            analysis.Soprano35,
            pcset,
            thiskey,
            tonicizedKey,
        )
        pcset = tuple(sorted(set(rn2.pitchClasses)))
        if thiskey != prevkey:
            rn2fig = f"{thiskey}:{rn2.figure}"
            prevkey = thiskey
        else:
            rn2fig = rn2.figure
        bass.addLyric(simplifyArabicNumerals(rn2fig))
        bass.addLyric(simplifyChordLabel(rn2.pitchedCommonName))
    filename, extension = inputFile.rsplit(".")
    annotatedScore = f"{filename}_annotated.musicxml"
    annotationCSV = f"{filename}_annotated.csv"
    s.write(fp=annotatedScore)
    dfout.to_csv(annotationCSV)


if __name__ == "__main__":
    parser = cli.inference()
    args = parser.parse_args()
    kwargs = vars(args)
    predict(**kwargs)
