import os
import pandas as pd
from pathlib import Path
from common import (
    ANNOTATIONSCOREDUPLES,
    DATASPLITS,
    DATASETDIR,
    SYNTHDATASETDIR,
    DATASETSUMMARYFILE,
)
from joint_parser import parseAnnotationAndScore, parseAnnotationAndAnnotation
from argparse import ArgumentParser


def generateDataset(wtcfold, synthetic=False, texturize=False):
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
    datasetDir = DATASETDIR if not synthetic else SYNTHDATASETDIR
    Path(datasetDir).mkdir(exist_ok=True)
    for split, files in DATASPLITS(wtcfold).items():
        Path(os.path.join(datasetDir, split)).mkdir(exist_ok=True)
        for nickname in files:
            print(nickname)
            annotation, score = ANNOTATIONSCOREDUPLES[nickname]
            if not synthetic:
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
    parser = ArgumentParser(
        description="Generate tsv files for every (annotation, score) pair."
    )
    parser.add_argument(
        "wtcfold",
        type=int,
        choices=range(4),
        help="The number of cross-validation fold of wtc to use.",
    )
    parser.add_argument(
        "--synthetic",
        action="store_true",
        help="Use (annotation, annotation) pairs, ignore the real scores.",
    )
    parser.add_argument(
        "--texturize",
        action="store_true",
        help="Texturize block chords. Ignored unless synthetic=True.",
    )
    args = parser.parse_args()
    generateDataset(
        args.wtcfold, synthetic=args.synthetic, texturize=args.texturize
    )
