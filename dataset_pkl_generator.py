import os
import pandas as pd
import numpy as np
from pathlib import Path
from common import (
    SEQUENCELENGTH,
    DATASETDIR,
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


if __name__ == "__main__":
    splits = {
        "training": {"X": [], "y": []},
        "validation": {"X": [], "y": []},
        "test": {"X": [], "y": []},
    }
    if not os.path.exists(DATASETSUMMARYFILE):
        print("You need to generate the tsv files first.")
        exit()
    datasetSummary = pd.read_csv(DATASETSUMMARYFILE, sep="\t")
    for row in datasetSummary.itertuples():
        tsvlocation = os.path.join(DATASETDIR, row.split, row.file)
        df = pd.read_csv(tsvlocation + ".tsv", sep="\t")
        print(df)
        Xi = intervalRepresentation(df)
        Xi = _padToSequenceLength(Xi)
        yi = romanNumeral(df)
        yi = _padToSequenceLength(yi)
        [splits[row.split]["X"].append(sequence) for sequence in Xi]
        [splits[row.split]["y"].append(sequence) for sequence in yi]
    for split in ["training", "validation", "test"]:
        for xy in ["X", "y"]:
            splits[split][xy] = np.array(splits[split][xy])
    np.save("dataset.npy", splits)
