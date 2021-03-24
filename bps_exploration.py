#!/usr/bin/env python
# coding: utf-8


from annotation_parser import parseAnnotation
from score_parser import parseScore
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from common import BPSVERSIONS


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
    "annotationFile\tclassicmanScore\tmeasureAlignment\tsappScore\tmeasureAlignment\talignedScore\tmeasureAlignment"
)

for annotation, scoreVersions in BPSVERSIONS.items():
    print(annotation, end="\t")
    for version, score in scoreVersions.items():
        print(score, end="\t")
        try:
            a = parseAnnotation(annotation)
            s = parseScore(score)
        except:
            print("FAILED", end="\t")
            pass
            continue
        alignmentdf = getAlignmentDataFrame(a, s)
        print(round(alignmentdf.misalignment.mean(), 2), end="\t")
    print()
