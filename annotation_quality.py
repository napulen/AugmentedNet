#!/usr/bin/env python
# coding: utf-8

from music21.note import Note
from annotation_parser import parseAnnotation
from score_parser import parseScore
import pandas as pd
from common import ANNOTATIONSCOREMAP


def getAnnotationOffsets(a):
    annotationIndexes = a[a.isOnset].pitchNames.index.to_list()
    annotationNotes = a[a.isOnset].pitchNames.to_list()
    annotationText = a[a.isOnset].romanNumeral.to_list()
    annotationIndexes.append("end")
    annotationRanges = [
        (
            annotationIndexes[i],
            annotationIndexes[i + 1],
            annotationNotes[i],
            annotationText[i],
        )
        for i in range(len(annotationNotes))
    ]
    return annotationRanges


def getNonChordSequence(annotationRanges, s):
    ret = []
    for start, end, annotationNotes, _ in annotationRanges:
        if end == "end":
            slices = s[start:]
        else:
            slices = s[start:end].iloc[:-1]
        originalNotes = slices.notes.to_list()
        originalNoteNames = [
            Note(n).name for chord in originalNotes for n in chord
        ]
        nonChordTones = set(originalNoteNames) - set(annotationNotes)
        missingNotes = set(annotationNotes) - set(originalNoteNames)
        originalNonChord = [n for n in originalNoteNames if n in nonChordTones]
        if not originalNotes:
            missingNotesRatio = 1.0
            nonChordToneRatio = 1.0
        else:
            missingNotesRatio = len(missingNotes) / len(set(annotationNotes))
            nonChordToneRatio = len(originalNonChord) / len(originalNoteNames)
        ret.append((originalNoteNames, nonChordToneRatio, missingNotesRatio))
    return ret


print(
    "annotationFile\tscoreFile\tnonChordRatio\tmissingNotesRatio\tannotationQuality\n"
)

for annotation, score in ANNOTATIONSCOREMAP.items():
    print(f"{annotation}\t{score}", end="\t")
    try:
        a = parseAnnotation(annotation)
        s = parseScore(score)
    except:
        print("FAILED")
        pass
        continue
    annotationRanges = getAnnotationOffsets(a)
    scoreMetrics = getNonChordSequence(annotationRanges, s)
    qualitydfdict = {
        "start": [],
        "end": [],
        "romanNumeral": [],
        "annotationPitchNames": [],
        "scorePitchNames": [],
        "nonChordRatio": [],
        "missingNotesRatio": [],
    }
    for i in range(len(annotationRanges)):
        start, end, annotationPitchNames, romanNumeral = annotationRanges[i]
        scorePitchNames, nonChordRatio, missingNotesRatio = scoreMetrics[i]
        qualitydfdict["start"].append(start)
        qualitydfdict["end"].append(end)
        qualitydfdict["romanNumeral"].append(romanNumeral)
        qualitydfdict["annotationPitchNames"].append(annotationPitchNames)
        qualitydfdict["scorePitchNames"].append(scorePitchNames)
        qualitydfdict["nonChordRatio"].append(nonChordRatio)
        qualitydfdict["missingNotesRatio"].append(missingNotesRatio)
    qualitydf = pd.DataFrame(qualitydfdict)
    qualitydf["score"] = (
        qualitydf.nonChordRatio + qualitydf.missingNotesRatio
    ) ** 2
    print(
        "{}\t{}\t{}".format(
            qualitydf.nonChordRatio.sum(),
            qualitydf.missingNotesRatio.sum(),
            qualitydf.score.sum(),
        )
    )
