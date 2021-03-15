import common
from score_parser import parseScore
from annotation_parser import parseAnnotation
from common import TAVERNVERSIONS

# from common import ANNOTATIONSCOREMAP
import os
import sys

sys.path.append("./When-in-Rome/Code")
from romanUmpire import ScoreAndAnalysis

print(
    "annotationFile\toriginalScore\toverallPitchMatch\tmicchiScore\toverallPitchMatch"
)
skip = True
for annotation, scoreVersions in TAVERNVERSIONS.items():
    if not "K455" in annotation:
        continue
    print(f"{annotation}", end="\t")
    for version, score in scoreVersions.items():
        annotationFolder = os.path.dirname(os.path.realpath(annotation))
        print(f"{score}", end="\t")
        try:
            analysis = ScoreAndAnalysis(
                scoreOrData=score, analysisLocation=annotation
            )
        except:
            print("FAILED", end="\t")
            pass
            continue
        feedbackFile = f"feedback_on_analysis_{version}"
        analysisScoreFile = f"analysis_on_score_{version}"
        slicesFile = f"slices_{version}"
        try:
            analysis.writeScoreWithAnalysis(
                outPath=annotationFolder, outFile=analysisScoreFile
            )
        except:
            print("FAILED WRITING PAIRED ANALYSIS", end="\t")
            pass
            continue
        try:
            analysis.writeSlicesFromScore(
                outPath=annotationFolder, outFile=slicesFile
            )
        except:
            print("FAILED WRINT SLICES FILE")
            pass
            continue
        try:
            analysis.printFeedback(
                outPath=annotationFolder, outFile=feedbackFile
            )
        except:
            print("FAILED PRINTING FEEDBACK", end="\t")
            pass
            continue
        with open(os.path.join(annotationFolder, f"{feedbackFile}.txt")) as fd:
            for line in fd.readlines():
                if "Overall pitch match" in line:
                    pitchFeedback = line.replace(
                        "Overall pitch match:", ""
                    ).strip()
        print(pitchFeedback, end="\t")
    print()