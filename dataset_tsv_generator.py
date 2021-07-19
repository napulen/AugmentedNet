"""Combine all available (score, annotation) pairs into tsv files."""

import os
import pandas as pd
from pathlib import Path

import cli
from common import (
    ANNOTATIONSCOREDUPLES,
    DATASPLITS,
    DATASETDIR,
    SYNTHDATASETDIR,
    DATASETSUMMARYFILE,
)
from joint_parser import parseAnnotationAndScore, parseAnnotationAndAnnotation


def generateDataset(synthesize=False, texturize=False):
    statsdict = {
        "file": [],
        "annotation": [],
        "score": [],
        "collection": [],
        "split": [],
        "misalignmentMean": [],
        "qualityMean": [],
        "incongruentBassMean": [],
    }
    datasetDir = DATASETDIR if not synthesize else SYNTHDATASETDIR
    Path(datasetDir).mkdir(exist_ok=True)
    for split, files in DATASPLITS.items():
        Path(os.path.join(datasetDir, split)).mkdir(exist_ok=True)
        for nickname in files:
            print(nickname)
            annotation, score = ANNOTATIONSCOREDUPLES[nickname]
            if not synthesize:
                df = parseAnnotationAndScore(annotation, score)
            else:
                df = parseAnnotationAndAnnotation(
                    annotation, annotation, texturize=texturize
                )
            outpath = os.path.join(datasetDir, split, nickname + ".tsv")
            df.to_csv(outpath, sep="\t")
            collection = nickname.split("-")[0]
            statsdict["file"].append(nickname)
            statsdict["annotation"].append(annotation)
            statsdict["score"].append(score)
            statsdict["collection"].append(collection)
            statsdict["split"].append(split)
            misalignment = df.measureMisalignment.mean().round(2)
            statsdict["misalignmentMean"].append(misalignment)
            qualitySquaredSum = df.qualitySquaredSum.mean().round(2)
            statsdict["qualityMean"].append(qualitySquaredSum)
            incongruentBass = df.incongruentBass.mean().round(2)
            statsdict["incongruentBassMean"].append(incongruentBass)
            df = pd.DataFrame(statsdict)
            df.to_csv(os.path.join(datasetDir, DATASETSUMMARYFILE), sep="\t")
    return df


if __name__ == "__main__":
    parser = cli.tsv()
    args = parser.parse_args()
    kwargs = vars(args)
    generateDataset(**kwargs)
