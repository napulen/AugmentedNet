"""Combine all available (score, annotation) pairs into tsv files."""

import os
import pandas as pd
from pathlib import Path

from . import cli
from .common import (
    ANNOTATIONSCOREDUPLES,
    DATASPLITS,
    DATASETSUMMARYFILE,
)
from .joint_parser import (
    parseAnnotationAndAudio,
)

nnls_postfix = "_vamp_nnls-chroma_nnls-chroma_bothchroma.csv"
fixedOffset = 0.04643990929705215419501133786848


def generateDataset(synthesize=False, texturize=False, tsvDir="dataset"):
    statsdict = {
        "file": [],
        "annotation": [],
        "chromacsv": [],
        "collection": [],
        "split": [],
        # "misalignmentMean": [],
        # "qualityMean": [],
        # "incongruentBassMean": [],
    }
    datasetDir = tsvDir
    Path(datasetDir).mkdir(exist_ok=True)
    for split, files in DATASPLITS.items():
        Path(os.path.join(datasetDir, split)).mkdir(exist_ok=True)
        for nickname in files:
            print(nickname)
            annotation, score = ANNOTATIONSCOREDUPLES[nickname]
            miditsv = score.replace(".mxl", ".csv").replace(".krn", ".csv")
            chromacsv = score.replace(".mxl", nnls_postfix).replace(
                ".krn", nnls_postfix
            )
            try:
                df = parseAnnotationAndAudio(
                    annotation, chromacsv, miditsv, fixedOffset=fixedOffset
                )
            except:
                print("\tErrored.")
                continue
            outpath = os.path.join(datasetDir, split, nickname + ".tsv")
            df.to_csv(outpath, sep="\t")
            collection = nickname.split("-")[0]
            statsdict["file"].append(nickname)
            statsdict["annotation"].append(annotation)
            statsdict["chromacsv"].append(chromacsv)
            statsdict["collection"].append(collection)
            statsdict["split"].append(split)
            # misalignment = round(df.measureMisalignment.mean(), 2)
            # statsdict["misalignmentMean"].append(misalignment)
            # qualitySquaredSum = round(df.qualitySquaredSum.mean(), 2)
            # statsdict["qualityMean"].append(qualitySquaredSum)
            # incongruentBass = round(df.incongruentBass.mean(), 2)
            # statsdict["incongruentBassMean"].append(incongruentBass)
            df = pd.DataFrame(statsdict)
            df.to_csv(os.path.join(datasetDir, DATASETSUMMARYFILE), sep="\t")
    return df


if __name__ == "__main__":
    parser = cli.tsv()
    args = parser.parse_args()
    kwargs = vars(args)
    generateDataset(**kwargs)
