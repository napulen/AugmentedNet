"""Generate pkl files for every tsv training example."""

import os
import pandas as pd
import numpy as np

from . import cli
from . import joint_parser
from .cache import TransposeKey
from .common import DATASETSUMMARYFILE, ANNOTATIONSCOREDUPLES
from .feature_representation import KEYS, INTERVALCLASSES
from .input_representations import (
    available_representations as availableInputs,
)
from .output_representations import (
    available_representations as availableOutputs,
)
from .utils import padToSequenceLength


def _getTranspositions(df):
    tonicizedKeys = df.a_localKey.to_list() + df.a_tonicizedKey.to_list()
    tonicizedKeys = set(tonicizedKeys)
    ret = []
    CONSTRAINEDKEYS = (
        "G-",
        "e-",
        "D-",
        "b-",
        "A-",
        "f",
        "E-",
        "c",
        "B-",
        "g",
        "F",
        "d",
        "C",
        "a",
        "G",
        "e",
        "D",
        "b",
        "A",
        "f#",
        "E",
        "c#",
        "B",
        "g#",
        "F#",
        "d#",
    )
    for interval in INTERVALCLASSES:
        transposed = [TransposeKey(k, interval) for k in tonicizedKeys]
        # Transpose to this interval if every modulation lies within
        # the set of KEY classes that we can classify
        if set(transposed).issubset(set(CONSTRAINEDKEYS)):
            ret.append(interval)
    return ret


def initializeArrays(inputRepresentations, outputRepresentations):
    """Each array becomes a dict entry with the name of the input/output"""
    outputArrays = {}
    for split in ["training", "validation"]:
        for x in inputRepresentations:
            outputArrays[split + f"_X_{x}"] = []
        for y in outputRepresentations:
            outputArrays[split + f"_y_{y}"] = []
    return outputArrays


def scrutinize(df, qualityThresh=0.75, bassThresh=0.8):
    """Filter 'bad quality' annotations."""
    originalIndex = len(df.index)
    df = df[
        (df.qualitySquaredSum < qualityThresh)
        & (df.measureMisalignment == False)
        & (df.incongruentBass < bassThresh)
    ]
    filteredIndex = len(df.index)
    print(f"\t({originalIndex}, {filteredIndex})")


def correctSplit(split, testSetOn):
    """Correct the split of this file according to 'testSetOn' parameter."""
    if testSetOn:
        if split == "validation":
            return "training"
        elif split == "test":
            return "validation"
    return split


def generateDataset(
    synthetic,
    texturizeEachTransposition,
    dataAugmentation,
    collections,
    testCollections,
    inputRepresentations,
    outputRepresentations,
    sequenceLength,
    scrutinizeData,
    testSetOn,
    tsvDir,
    npzOutput,
):
    outputArrays = initializeArrays(
        inputRepresentations, outputRepresentations
    )
    training = ["training", "validation"] if testSetOn else ["training"]
    validation = ["test"] if testSetOn else ["validation"]
    datasetDir = f"{tsvDir}-synth" if synthetic else tsvDir
    summaryFile = os.path.join(datasetDir, DATASETSUMMARYFILE)
    if not os.path.exists(summaryFile):
        print("You need to generate the tsv files first.")
        exit()
    datasetSummary = pd.read_csv(summaryFile, sep="\t")
    trainingdf = datasetSummary[
        (datasetSummary.collection.isin(collections))
        & (datasetSummary.split.isin(training))
    ]
    validationdf = datasetSummary[
        (datasetSummary.collection.isin(testCollections))
        & (datasetSummary.split.isin(validation))
    ]
    df = pd.concat([trainingdf, validationdf])
    for row in df.itertuples():
        split = correctSplit(row.split, testSetOn)
        if split == "test":
            # Preemptive measure just to avoid a potential disaster
            continue
        print(f"{row.split} -used-as-> {split}", row.file)
        tsvlocation = os.path.join(datasetDir, row.split, f"{row.file}.tsv")
        df = joint_parser.from_tsv(tsvlocation)
        if scrutinizeData and split == "training":
            df = scrutinize(df)
        if dataAugmentation and split == "training":
            transpositions = _getTranspositions(df)
            print("\t", transpositions)
        else:
            transpositions = ["P1"]
        if synthetic:
            if not texturizeEachTransposition:
                # once per file
                try:
                    df = joint_parser.retexturizeSynthetic(df)
                except:
                    continue
            else:
                # once per transposition
                dfsynth = df.copy()
        for transposition in transpositions:
            if synthetic and texturizeEachTransposition:
                df = joint_parser.retexturizeSynthetic(dfsynth)
            print("Original length:", len(df.index))
            for inputRepresentation in inputRepresentations:
                inputLayer = availableInputs[inputRepresentation](df)
                Xi = inputLayer.run(transposition=transposition)
                if len(Xi) <= (sequenceLength / 2):
                    Xi = np.concatenate((Xi, Xi), axis=0)
                Xi = padToSequenceLength(Xi, sequenceLength, value=-1)
                npzfile = f"{split}_X_{inputRepresentation}"
                for sequence in Xi:
                    outputArrays[npzfile].append(sequence)
            for outputRepresentation in outputRepresentations:
                outputLayer = availableOutputs[outputRepresentation](df)
                yi = outputLayer.run(transposition=transposition)
                if len(yi) <= (sequenceLength / 2):
                    yi = np.concatenate((yi, yi), axis=0)
                if outputRepresentation == "HarmonicRhythm7":
                    yi = padToSequenceLength(yi, sequenceLength, value=6)
                else:
                    yi = padToSequenceLength(yi, sequenceLength)
                npzfile = f"{split}_y_{outputRepresentation}"
                for sequence in yi:
                    outputArrays[npzfile].append(sequence)
    # drop the extension, we'll overwrite it to .npz
    filename, _ = os.path.splitext(npzOutput)
    outputFile = f"{filename}-synth" if synthetic else filename
    np.savez_compressed(outputFile, **outputArrays)


if __name__ == "__main__":
    parser = cli.npz()
    args = parser.parse_args()
    generateDataset(**vars(args))
