import os
import pandas as pd
import numpy as np
from pathlib import Path
from joint_parser import J_LISTTYPE_COLUMNS
from cache import TransposeKey
from common import (
    SEQUENCELENGTH,
    DATASETDIR,
    SYNTHDATASETDIR,
    DATASETSUMMARYFILE,
    INPUT_REPRESENTATION,
    OUTPUT_REPRESENTATION
)
from feature_representation import KEYS, INTERVALCLASSES
from input_representations import BassChromagram38, BassIntervals63
from output_representations import RomanNumeral76, LocalKey35, Inversion4


def _padToSequenceLength(arr):
    frames, features = arr.shape
    featuresPerSequence = SEQUENCELENGTH * features
    featuresInExample = frames * features
    padding = featuresPerSequence - (featuresInExample % featuresPerSequence)
    arr = np.pad(arr.reshape(-1), (0, padding))
    arr = arr.reshape(-1, SEQUENCELENGTH, features)
    return arr


def _getTranspositions(df):
    # return INTERVALCLASSES
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


def generateDataset(synthetic=False, dataAugmentation=False, collection=None):
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
        datasetSummary = datasetSummary[
            datasetSummary.collection == collection
        ]
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
            ]
            filteredIndex = len(df.index)
            print(f"\t({originalIndex}, {filteredIndex})")
        inputLayer = eval(INPUT_REPRESENTATION)(df)
        Xi = inputLayer.array
        Xi = _padToSequenceLength(Xi)
        if dataAugmentation and row.split == "training":
            transpositions = _getTranspositions(df)
            print('\t', transpositions)
            for transposition in inputLayer.dataAugmentation(
                transpositions
            ):
                Xi = np.concatenate((Xi, _padToSequenceLength(transposition)))
        outputLayer = eval(OUTPUT_REPRESENTATION)(df)
        yi = outputLayer.array
        yi = _padToSequenceLength(yi)
        # dataAug = list(inv.dataAugmentation(INTERVAL_TRANSPOSITIONS))
        if dataAugmentation and row.split == "training":
            for transposition in outputLayer.dataAugmentation(
                transpositions
            ):
                yi = np.concatenate((yi, _padToSequenceLength(transposition)))
        [splits[row.split]["X"].append(sequence) for sequence in Xi]
        [splits[row.split]["y"].append(sequence) for sequence in yi]
    for split in ["training", "validation", "test"]:
        for xy in ["X", "y"]:
            splits[split][xy] = np.array(splits[split][xy])
    np.save(f"{datasetDir}.npy", splits)


if __name__ == "__main__":
    generateDataset(synthetic=False, dataAugmentation=True, collection="bps")