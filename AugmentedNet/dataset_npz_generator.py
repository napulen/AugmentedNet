"""Generate pkl files for every tsv training example."""

import os
import pandas as pd
import numpy as np

from . import cli
from .cache import TransposeKey
from .common import DATASETSUMMARYFILE
from .feature_representation import KEYS, INTERVALCLASSES
from .input_representations import (
    available_representations as availableInputs,
)
from .joint_parser import J_LISTTYPE_COLUMNS
from .output_representations import (
    available_representations as availableOutputs,
)
from .utils import padToSequenceLength


def _getTranspositions(df):
    tonicizedKeys = df.a_localKey.to_list() + df.a_tonicizedKey.to_list()
    tonicizedKeys = set(tonicizedKeys)
    ret = []
    for interval in INTERVALCLASSES:
        if interval == "P1":
            continue
        transposed = [TransposeKey(k, interval) for k in tonicizedKeys]
        # Transpose to this interval if every modulation lies within
        # the set of KEY classes that we can classify
        if set(transposed).issubset(set(KEYS)):
            ret.append(interval)
    return ret


def generateDataset(
    synthetic,
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
    outputArrays = {}
    for split in ["training", "validation"]:
        for x in inputRepresentations:
            outputArrays[split + f"_X_{x}"] = []
        for y in outputRepresentations:
            outputArrays[split + f"_y_{y}"] = []
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
        split = row.split
        if testSetOn:
            if split == "validation":
                split = "training"
            elif split == "test":
                split = "validation"
        else:
            if split == "test":
                continue
        print(f"{row.split} -used-as-> {split}", row.file)
        tsvlocation = os.path.join(datasetDir, row.split, row.file)
        df = pd.read_csv(tsvlocation + ".tsv", sep="\t")
        for col in J_LISTTYPE_COLUMNS:
            df[col] = df[col].apply(eval)
        # Filter the bad quality annotations
        if scrutinizeData and split == "training":
            originalIndex = len(df.index)
            df = df[
                (df.qualitySquaredSum < 0.75)
                & (df.measureMisalignment == False)
                & (df.incongruentBass < 0.8)
            ]
            filteredIndex = len(df.index)
            print(f"\t({originalIndex}, {filteredIndex})")
        if dataAugmentation and split == "training":
            transpositions = _getTranspositions(df)
            print("\t", transpositions)
        else:
            transpositions = ["P1"]
        for inputRepresentation in inputRepresentations:
            inputLayer = availableInputs[inputRepresentation](df)
            Xi = inputLayer.array
            Xi = padToSequenceLength(Xi, sequenceLength)
            for transposition in transpositions:
                tr = inputLayer.run(transposition=transposition)
                tr = padToSequenceLength(tr, sequenceLength)
                Xi = np.concatenate((Xi, tr))
            npzfile = f"{split}_X_{inputRepresentation}"
            for sequence in Xi:
                outputArrays[npzfile].append(sequence)
        for outputRepresentation in outputRepresentations:
            outputLayer = availableOutputs[outputRepresentation](df)
            yi = outputLayer.array
            yi = padToSequenceLength(yi, sequenceLength)
            for transposition in transpositions:
                tr = outputLayer.run(transposition=transposition)
                tr = padToSequenceLength(tr, sequenceLength)
                yi = np.concatenate((yi, tr))
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
