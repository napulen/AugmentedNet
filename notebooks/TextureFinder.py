
import sys

sys.path.insert(0, "..")
import music21
from music21.note import Note
from music21.interval import Interval
from AugmentedNet.common import ANNOTATIONSCOREDUPLES
import seaborn as sns
import matplotlib.pyplot as plt
from AugmentedNet.annotation_parser import parseAnnotation
from AugmentedNet.score_parser import parseScore
import pandas as pd
import pprint
from collections import Counter

# pd.set_option("display.max_rows", 6000)

texturecounter = Counter()

def getAnnotationOffsets(a):
    annotationIndexes = a[a.a_isOnset].a_pitchNames.index.to_list()
    annotationRoot = a[a.a_isOnset].a_root.to_list()
    annotationQuality = a[a.a_isOnset].a_quality.to_list()
    annotationKey = a[a.a_isOnset].a_tonicizedKey.to_list()
    annotationText = a[a.a_isOnset].a_romanNumeral.to_list()
    annotationIndexes.append("end")
    annotationRanges = [
        (
            annotationIndexes[i],
            annotationIndexes[i + 1],
            annotationRoot[i],
            annotationQuality[i],
            annotationKey[i],
            annotationText[i],
        )
        for i in range(len(annotationRoot))
    ]
    return annotationRanges


def getNonChordSequence(annotationRanges, s):
    ret = []
    for start, end, root, quality, key, rn in annotationRanges:
        s = s.dropna()
        s["s_onsets"] = s.s_isOnset.apply(sum)
        if end == "end":
            slices = s[start:]
        else:
            slices = s[start:end].iloc[:-1]
        # only care about slices where at least one onset occurs
        slices = slices[slices.s_onsets > 0]
        if slices.empty:
            continue
        notes = slices.s_notes.to_list()
        offsets = slices.s_notes.index.to_list() + [end]
        verticalIntervals = slices.s_intervals.to_list()
        # The interval between the annotated chord root and the first bass of the music sample
        rootInterval = Interval(Note(root), Note(notes[0][0]))
        firstnote = Note("C4").transpose(rootInterval)
        horizontalIntervals = [firstnote.name]
        for idx in range(1, len(notes)):
            previousBass = Note(notes[idx-1][0])
            thisBass = Note(notes[idx][0])
            horizontalInterval = Interval(previousBass, thisBass)
            horizontalIntervals.append(horizontalInterval.directedName)
        durations = []
        for idx in range(len(offsets) - 1):
            if offsets[idx+1] == "end":
                duration = 1.0
            else:
                duration = round(offsets[idx+1] - offsets[idx], 3)
            durations.append(duration)
        texture = []
        for idx in range(len(slices)):
            d = durations[idx]
            v = verticalIntervals[idx]
            h = horizontalIntervals[idx]
            t = f"{d}:{h}[{','.join(v)}];"
            texture.append(t)
            # print(t)
        texturestr = " ".join(texture)
        print(f"{quality}\t", texturestr)
        ret.append(texturestr)
    return ret


for _aPath, _sPath in ANNOTATIONSCOREDUPLES.values():
    # f = "bps-01-op002-no1-1"
    # _aPath, _sPath = ANNOTATIONSCOREDUPLES[f]
    aPath = f"../{_aPath}"
    sPath = f"../{_sPath}"


    aScore = music21.converter.parse(aPath, format="romantext")
    # sScore = music21.converter.parse(sPath).chordify().show("musicxml")

    a = parseAnnotation(aPath, eventBased=True)
    s = parseScore(sPath, eventBased=True)
    annotationRanges = getAnnotationOffsets(a)
    scoreMetrics = getNonChordSequence(annotationRanges, s)
    texturecounter.update(scoreMetrics)
    pprint.pprint(texturecounter.most_common(20))
    print(f"Number of texture patterns so far: {len(texturecounter)}")


# qualitydfdict = {
#     "start": [],
#     "end": [],
#     "romanNumeral": [],
#     "annotationPitchNames": [],
#     "scorePitchNames": [],
#     "nonChordRatio": [],
#     "missingNotesRatio": [],
# }

# for i in range(len(annotationRanges)):
#     start, end, annotationPitchNames, romanNumeral = annotationRanges[i]
#     scorePitchNames, nonChordRatio, missingNotesRatio = scoreMetrics[i]
#     qualitydfdict["start"].append(start)
#     qualitydfdict["end"].append(end)
#     qualitydfdict["romanNumeral"].append(romanNumeral)
#     qualitydfdict["annotationPitchNames"].append(annotationPitchNames)
#     qualitydfdict["scorePitchNames"].append(scorePitchNames)
#     qualitydfdict["nonChordRatio"].append(nonChordRatio)
#     qualitydfdict["missingNotesRatio"].append(missingNotesRatio)


# qualitydf = pd.DataFrame(qualitydfdict)




# qualitydf




# qualitydf["score"] = (
#     qualitydf.nonChordRatio + qualitydf.missingNotesRatio
# ) ** 2
# print(
#     qualitydf.nonChordRatio.sum(),
#     qualitydf.missingNotesRatio.sum(),
#     qualitydf.score.sum(),
# )
# print("Top problematic annotations:")
# display(qualitydf[qualitydf.score >= 1.0])
# plt.figure(figsize=(25, 10))
# sns.lineplot(data=qualitydf[["nonChordRatio", "missingNotesRatio", "score"]])
# plt.ylim(0, 4)


# plt.figure(figsize=(25, 10))
# sns.lineplot(data=qualitydf, x="romanNumeral", y="score")
