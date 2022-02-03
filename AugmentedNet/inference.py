"""Run the network to annotate an unseen musical input (inference)."""

import os

import music21
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras

from . import cli
from .score_parser import parseScore
from .input_representations import available_representations as availableInputs
from .output_representations import (
    available_representations as availableOutputs,
)


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


def resolveRomanNumeral75(rn75, inversion):
    seventh = True if "7" in rn75 else False
    inv = ""
    if inversion == 1:
        inv = "65" if seventh else "6"
    elif inversion == 2:
        inv = "43" if seventh else "64"
    elif inversion == 3:
        inv = "2"
    if seventh:
        rn = rn75.replace("7", inv)
    else:
        rn = rn75 + inv
    return rn


def resolveSATB(b, t, a, s, key):
    chord = music21.chord.Chord(f"{b}2 {t}3 {a}4 {s}5")
    return music21.roman.romanNumeralFromChord(chord, key)


def simplifyChordLabel(label):
    label = label.replace("-major triad", "")
    label = label.replace("-minor triad", "min")
    label = label.replace("-diminished triad", "dim")
    label = label.replace("-augmented triad", "aug")
    label = label.replace("-dominant seventh chord", "7")
    label = label.replace("-major seventh chord", "maj7")
    label = label.replace("-minor seventh chord", "min7")
    label = label.replace("-half-diminished seventh chord", "hdim7")
    return label


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
        # print(analysis.offset, notes)
        bass = sorted(notes, key=lambda n: n[1])[0][0]
        thiskey = analysis.LocalKey35
        rn2 = resolveSATB(
            analysis.Bass35,
            analysis.Tenor35,
            analysis.Alto35,
            analysis.Soprano35,
            thiskey,
        )
        if thiskey != prevkey:
            # rn1 = f"{thiskey}:{rn1}"
            rn2fig = f"{thiskey}:{rn2.figure}"
            prevkey = thiskey
        else:
            rn2fig = rn2.figure
        # bass.addLyric(rn1)
        bass.addLyric(rn2fig)
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
