import os
import pandas as pd
import numpy as np
from pathlib import Path
from joint_parser import J_LISTTYPE_COLUMNS
from cache import TransposeKey
from common import (
    DATASETDIR,
    SYNTHDATASETDIR,
    DATASETSUMMARYFILE,
)
from feature_representation import KEYS, INTERVALCLASSES
from input_representations import available_representations as availableInputs
from output_representations import (
    available_representations as availableOutputs,
)
from argparse import ArgumentParser


def _padToSequenceLength(arr, sequenceLength):
    frames, features = arr.shape
    featuresPerSequence = sequenceLength * features
    featuresInExample = frames * features
    padding = featuresPerSequence - (featuresInExample % featuresPerSequence)
    arr = np.pad(arr.reshape(-1), (0, padding))
    arr = arr.reshape(-1, sequenceLength, features)
    return arr


def _getTranspositions(df):
    localKeys = df.a_localKey.to_list()
    localKeys = set(localKeys)
    ret = []
    for interval in INTERVALCLASSES:
        transposed = [TransposeKey(k, interval) for k in localKeys]
        # Transpose to this interval if every modulation lies within
        # the set of KEY classes that we can classify
        if set(transposed).issubset(set(KEYS)):
            ret.append(interval)
    return ret


def generateDataset(
    synthetic=False,
    dataAugmentation=False,
    collection=None,
    inputRepresentation="BassChromagram38",
    outputRepresentations=["Inversion4", "LocalKey35", "RomanNumeral76"],
    sequenceLength=64,
):
    splits = {
        "training": {"X": [], "y": []},
        "validation": {"X": [], "y": []},
        "test": {"X": [], "y": []},
    }
    datasetDir = DATASETDIR if not synthetic else SYNTHDATASETDIR
    summaryFile = os.path.join(datasetDir, DATASETSUMMARYFILE)
    if not os.path.exists(summaryFile):
        print("You need to generate the tsv files first.")
        exit()
    datasetSummary = pd.read_csv(summaryFile, sep="\t")
    if collection:
        datasetSummary = datasetSummary[datasetSummary.collection == collection]
    for row in datasetSummary.itertuples():
        print(row.split, row.file)
        tsvlocation = os.path.join(datasetDir, row.split, row.file)
        df = pd.read_csv(tsvlocation + ".tsv", sep="\t")
        for col in J_LISTTYPE_COLUMNS:
            df[col] = df[col].apply(eval)
        # Filter the bad content
        if row.split == "training":
            originalIndex = len(df.index)
            df = df[
                (df.qualitySquaredSum < 0.75)
                & (df.measureMisalignment == False)
                & (df.incongruentBass < 0.8)
            ]
            filteredIndex = len(df.index)
            print(f"\t({originalIndex}, {filteredIndex})")
        inputLayer = availableInputs[inputRepresentation](df)
        Xi = inputLayer.array
        Xi = _padToSequenceLength(Xi, sequenceLength)
        if dataAugmentation and row.split == "training":
            transpositions = _getTranspositions(df)
            print("\t", transpositions)
            for transposition in inputLayer.dataAugmentation(transpositions):
                Xi = np.concatenate(
                    (Xi, _padToSequenceLength(transposition, sequenceLength))
                )
        outputLayer = availableOutputs[outputRepresentations[0]](df)
        yi = outputLayer.array
        yi = _padToSequenceLength(yi, sequenceLength)
        # dataAug = list(inv.dataAugmentation(INTERVAL_TRANSPOSITIONS))
        if dataAugmentation and row.split == "training":
            for transposition in outputLayer.dataAugmentation(transpositions):
                yi = np.concatenate(
                    (yi, _padToSequenceLength(transposition, sequenceLength))
                )
        [splits[row.split]["X"].append(sequence) for sequence in Xi]
        [splits[row.split]["y"].append(sequence) for sequence in yi]
    for split in ["training", "validation", "test"]:
        for xy in ["X", "y"]:
            splits[split][xy] = np.array(splits[split][xy])
    np.save(f"{datasetDir}.npy", splits)


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Generate pkl files for every tsv training example."
    )
    parser.add_argument(
        "--synthetic",
        action="store_true",
        help="Search for a synthetic dataset, not one from real scores.",
    )
    parser.add_argument(
        "--dataAugmentation",
        action="store_true",
        help="Perform data augmentation on the training set.",
    )
    parser.add_argument(
        "--collection",
        choices=["abc", "bps", "haydnop20", "wir", "tavern"],
        help="Include files from a specific corpus/collection.",
    )
    parser.add_argument(
        "--input_representation",
        type=str,
        default="BassChromagram38",
        choices=list(availableInputs.keys()),
    )
    parser.add_argument(
        "--output_representations",
        nargs="+",
        default=["Inversion4", "LocalKey35", "RomanNumeral76"],
        choices=list(availableOutputs.keys()),
    )
    parser.add_argument(
        "--sequence_length",
        type=int,
        default=64,
        choices=range(16, 128),
    )
    args = parser.parse_args()
    generateDataset(
        synthetic=args.synthetic,
        dataAugmentation=args.dataAugmentation,
        collection=args.collection,
        inputRepresentation=args.input_representation,
        outputRepresentations=args.output_representations,
        sequenceLength=args.sequence_length,
    )
