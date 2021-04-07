import os
import pandas as pd
from pathlib import Path
from common import ANNOTATIONSCOREDUPLES, DATASPLITS, DATASETDIR
from joint_parser import parseAnnotationAndScore

if __name__ == "__main__":
    statsdict = {
        "file": [],
        "annotation": [],
        "score": [],
        "split": [],
        "misalignmentMean": [],
        "qualityMean": [],
    }
    Path(DATASETDIR).mkdir(exist_ok=True)
    for split, files in DATASPLITS.items():
        Path(os.path.join(DATASETDIR, split)).mkdir(exist_ok=True)
        for nickname in files:
            print(nickname)
            annotation, score = ANNOTATIONSCOREDUPLES[nickname]
            df = parseAnnotationAndScore(annotation, score)
            outpath = os.path.join(DATASETDIR, split, nickname + ".tsv")
            df.to_csv(outpath, sep="\t")
            statsdict["file"].append(nickname)
            statsdict["annotation"].append(annotation)
            statsdict["score"].append(score)
            statsdict["split"].append(split)
            statsdict["misalignmentMean"].append(df.measureMisalignment.mean())
            statsdict["qualityMean"].append(df.qualitySquaredSum.mean())
            df = pd.DataFrame(statsdict)
            df.to_csv(os.path.join(DATASETDIR, "dataset_summary.tsv"), sep="\t")
