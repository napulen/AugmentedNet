import os
import pandas as pd
import numpy as np
from pathlib import Path
from common import (
    SEQUENCELENGTH,
    DATASETDIR,
    SYNTHDATASETDIR,
    DATASETSUMMARYFILE,
)
from input_representations import (
    intervalRepresentation,
    pitchClassNoteName,
    salamiSliceWithHold,
    compressedSalamiSliceWithHold,
    micchiChromagram,
    micchiChromagram19,
)
from output_representations import (
    bass35,
    bass12,
    bass7,
    bass19,
    inversion,
    tonicizedKey,
    degree1,
    degree2,
    localKey,
    chordRoot,
    chordQuality,
    harmonicRhythm,
    romanNumeral,
)


def _padToSequenceLength(arr):
    frames, features = arr.shape
    featuresPerSequence = SEQUENCELENGTH * features
    featuresInExample = frames * features
    padding = featuresPerSequence - (featuresInExample % featuresPerSequence)
    arr = np.pad(arr.reshape(-1), (0, padding))
    arr = arr.reshape(-1, SEQUENCELENGTH, features)
    return arr


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
        for col in [
            "s_notes",
            "s_intervals",
            "s_isOnset",
            "a_pitchNames",
            "a_pcset",
            "qualityScoreNotes",
        ]:
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
        Xi, dataAug = intervalRepresentation(
            df, dataAugmentation=(row.split == "training" and dataAugmentation)
        )
        Xi = _padToSequenceLength(Xi)
        if dataAug is not None:
            for transposition in range(dataAug.shape[0]):
                print("transposition ", transposition)
                Xi = np.concatenate(
                    (Xi, _padToSequenceLength(dataAug[transposition]))
                )
        yi, dataAug = romanNumeral(
            df, dataAugmentation=(row.split == "training" and dataAugmentation)
        )
        yi = _padToSequenceLength(yi)
        if dataAug is not None:
            for transposition in range(dataAug.shape[0]):
                print("transposition ", transposition)
                yi = np.concatenate(
                    (yi, _padToSequenceLength(dataAug[transposition]))
                )
        [splits[row.split]["X"].append(sequence) for sequence in Xi]
        [splits[row.split]["y"].append(sequence) for sequence in yi]
    for split in ["training", "validation", "test"]:
        for xy in ["X", "y"]:
            splits[split][xy] = np.array(splits[split][xy])
    np.save(f"{datasetDir}.npy", splits)


if __name__ == "__main__":
    generateDataset(synthetic=True, dataAugmentation=True, collection="bps")