import common
from score_parser import parseScore
from annotation_parser import parseAnnotation

# from common import ANNOTATIONSCOREMAP
import os
import sys

sys.path.append("./When-in-Rome/Code")
from romanUmpire import ScoreAndAnalysis


ANNOTATIONSCOREMAP = {
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/Op34/analysis_A.txt": {
        "original": "TAVERN/Beethoven/Opus34/Krn/Opus34.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/Opus34.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/Op34/analysis_B.txt": {
        "original": "TAVERN/Beethoven/Opus34/Krn/Opus34.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/Opus34.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/Op76/analysis_A.txt": {
        "original": "TAVERN/Beethoven/Opus76/Krn/Opus76.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/Opus76.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/Op76/analysis_B.txt": {
        "original": "TAVERN/Beethoven/Opus76/Krn/Opus76.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/Opus76.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_63/analysis_A.txt": {
        "original": "TAVERN/Beethoven/B063/Krn/Wo063.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B063.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_63/analysis_B.txt": {
        "original": "TAVERN/Beethoven/B063/Krn/Wo063.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B063.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_64/analysis_A.txt": {
        "original": "TAVERN/Beethoven/B064/Krn/Wo064.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B064.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_64/analysis_B.txt": {
        "original": "TAVERN/Beethoven/B064/Krn/Wo064.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B064.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_65/analysis_A.txt": {
        "original": "TAVERN/Beethoven/B065/Krn/Wo065.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B065.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_65/analysis_B.txt": {
        "original": "TAVERN/Beethoven/B065/Krn/Wo065.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B065.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_66/analysis_A.txt": {
        "original": "TAVERN/Beethoven/B066/Krn/Wo066.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B066.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_66/analysis_B.txt": {
        "original": "TAVERN/Beethoven/B066/Krn/Wo066.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B066.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_68/analysis_A.txt": {
        "original": "TAVERN/Beethoven/B068/Krn/Wo068.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B068.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_68/analysis_B.txt": {
        "original": "TAVERN/Beethoven/B068/Krn/Wo068.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B068.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_69/analysis_A.txt": {
        "original": "TAVERN/Beethoven/B069/Krn/Wo069.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B069.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_69/analysis_B.txt": {
        "original": "TAVERN/Beethoven/B069/Krn/Wo069.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B069.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_70/analysis_A.txt": {
        "original": "TAVERN/Beethoven/B070/Krn/Wo070.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B070.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_70/analysis_B.txt": {
        "original": "TAVERN/Beethoven/B070/Krn/Wo070.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B070.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_71/analysis_A.txt": {
        "original": "TAVERN/Beethoven/B071/Krn/Wo071.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B071.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_71/analysis_B.txt": {
        "original": "TAVERN/Beethoven/B071/Krn/Wo071.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B071.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_72/analysis_A.txt": {
        "original": "TAVERN/Beethoven/B072/Krn/Wo072.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B072.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_72/analysis_B.txt": {
        "original": "TAVERN/Beethoven/B072/Krn/Wo072.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B072.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_73/analysis_A.txt": {
        "original": "TAVERN/Beethoven/B073/Krn/Wo073.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B073.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_73/analysis_B.txt": {
        "original": "TAVERN/Beethoven/B073/Krn/Wo073.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B073.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_75/analysis_A.txt": {
        "original": "TAVERN/Beethoven/B075/Krn/Wo075.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B075.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_75/analysis_B.txt": {
        "original": "TAVERN/Beethoven/B075/Krn/Wo075.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B075.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_76/analysis_A.txt": {
        "original": "",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B076.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_76/analysis_B.txt": {
        "original": "",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B076.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_77/analysis_A.txt": {
        "original": "TAVERN/Beethoven/B077/Krn/Wo077.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B077.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_77/analysis_B.txt": {
        "original": "TAVERN/Beethoven/B077/Krn/Wo077.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B077.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_78/analysis_A.txt": {
        "original": "TAVERN/Beethoven/B078/Krn/Wo078.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B078.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_78/analysis_B.txt": {
        "original": "TAVERN/Beethoven/B078/Krn/Wo078.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B078.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_80/analysis_A.txt": {
        "original": "TAVERN/Beethoven/B080/Krn/Wo080.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B080.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Beethoven,_Ludwig_van/_/WoO_80/analysis_B.txt": {
        "original": "TAVERN/Beethoven/B080/Krn/Wo080.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Beethoven/scores/B080.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K025/analysis_A.txt": {
        "original": "TAVERN/Mozart/K025/Krn/K025.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Mozart/scores/K025.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K025/analysis_B.txt": {
        "original": "TAVERN/Mozart/K025/Krn/K025.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Mozart/scores/K025.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K179/analysis_A.txt": {
        "original": "TAVERN/Mozart/K179/Krn/K179.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Mozart/scores/K179.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K179/analysis_B.txt": {
        "original": "TAVERN/Mozart/K179/Krn/K179.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Mozart/scores/K179.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K265/analysis_A.txt": {
        "original": "TAVERN/Mozart/K265/Krn/K265.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Mozart/scores/K265.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K265/analysis_B.txt": {
        "original": "TAVERN/Mozart/K265/Krn/K265.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Mozart/scores/K265.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K353/analysis_A.txt": {
        "original": "TAVERN/Mozart/K353/Krn/K353.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Mozart/scores/K353.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K353/analysis_B.txt": {
        "original": "TAVERN/Mozart/K353/Krn/K353.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Mozart/scores/K353.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K354/analysis_A.txt": {
        "original": "TAVERN/Mozart/K354/Krn/K354.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Mozart/scores/K354.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K354/analysis_B.txt": {
        "original": "TAVERN/Mozart/K354/Krn/K354.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Mozart/scores/K354.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K398/analysis_A.txt": {
        "original": "TAVERN/Mozart/K398/Krn/K398.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Mozart/scores/K398.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K398/analysis_B.txt": {
        "original": "TAVERN/Mozart/K398/Krn/K398.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Mozart/scores/K398.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K455/analysis_A.txt": {
        "original": "TAVERN/Mozart/K455/Krn/K455.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Mozart/scores/K455.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K455/analysis_B.txt": {
        "original": "TAVERN/Mozart/K455/Krn/K455.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Mozart/scores/K455.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K501/analysis_A.txt": {
        "original": "TAVERN/Mozart/K501/Krn/K501.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Mozart/scores/K501.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K501/analysis_B.txt": {
        "original": "TAVERN/Mozart/K501/Krn/K501.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Mozart/scores/K501.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K573/analysis_A.txt": {
        "original": "TAVERN/Mozart/K573/Krn/K573.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Mozart/scores/K573.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K573/analysis_B.txt": {
        "original": "TAVERN/Mozart/K573/Krn/K573.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Mozart/scores/K573.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K613/analysis_A.txt": {
        "original": "TAVERN/Mozart/K613/Krn/K613.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Mozart/scores/K613.mxl",
    },
    "When-in-Rome/Corpus/Variations_and_Grounds/Mozart,_Wolfgang_Amadeus/_/K613/analysis_B.txt": {
        "original": "TAVERN/Mozart/K613/Krn/K613.krn",
        "micchi": "functional-harmony-micchi/data/Tavern/Mozart/scores/K613.mxl",
    },
}

tavernSets = ["original", "micchi"]

print(
    "annotationFile\toriginalScore\toverallPitchMatch\tmicchiScore\toverallPitchMatch"
)
skip = True
for annotation, scoreVersions in ANNOTATIONSCOREMAP.items():
    print(f"{annotation}", end="\t")
    for version, score in scoreVersions.items():
        annotationFolder = os.path.dirname(os.path.realpath(annotation))
        print(f"{score}", end="\t")
        analysis = ScoreAndAnalysis(
            scoreOrData=score, analysisLocation=annotation
        )
        feedbackFile = f"feedback_on_analysis_{version}"
        analysisScoreFile = f"analysis_on_score_{version}"
        analysis.writeScoreWithAnalysis(
            outPath=annotationFolder, outFile=analysisScoreFile
        )
        analysis.printFeedback(outPath=annotationFolder, outFile=feedbackFile)
        with open(os.path.join(annotationFolder, f"{feedbackFile}.txt")) as fd:
            for line in fd.readlines():
                if "Overall pitch match" in line:
                    pitchFeedback = line.replace(
                        "Overall pitch match:", ""
                    ).strip()
        print(pitchFeedback, end="\t")
    print()