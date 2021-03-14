#!/usr/bin/env python
# coding: utf-8


from annotation_parser import parseAnnotation
from score_parser import parseScore
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from common import ANNOTATIONSCOREMAP


def getAlignmentDataFrame(a, s):
    alignmentdf = pd.concat(
        [a.measure, s.measure],
        axis=1,
        keys=["annotationMeasure", "scoreMeasure"],
    )
    alignmentdf["misalignment"] = (
        alignmentdf.annotationMeasure != alignmentdf.scoreMeasure
    )
    return alignmentdf


print(
    "annotationFile\tscoreFile\tmeasureAlignment\n"
)

for annotation, score in ANNOTATIONSCOREMAP.items():
    # For ABC scores, which are pre-converted from .mscz to .mxl
    if score.endswith(".mscx"):
        score = score.replace(".mscx", ".mxl")
    print(f"{annotation}\t{score}", end="\t")
    try:
        a = parseAnnotation(annotation)
        s = parseScore(score)
    except:
        print("FAILED")
        pass
        continue
    alignmentdf = getAlignmentDataFrame(a, s)
    print(round(alignmentdf.misalignment.mean(), 2))
