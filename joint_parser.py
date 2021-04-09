from score_parser import parseScore
from annotation_parser import parseAnnotation
import pandas as pd
import numpy as np
import re


def _measureAlignmentScore(df):
    df["measureMisalignment"] = df.s_measure != df.a_measure
    return df


def _qualityMetric(df):
    df["qualityScoreNotes"] = np.nan
    df["qualityNonChordTones"] = np.nan
    df["qualityMissingChordTones"] = np.nan
    df["qualitySquaredSum"] = np.nan
    notesdf = df.explode("s_notes")
    annotations = df.a_annotationNumber.unique()
    for n in annotations:
        # All the rows spanning this annotation
        rows = notesdf[notesdf.a_annotationNumber == n]
        # No octave information; just pitch names
        scoreNotes = [re.sub(r"\d", "", n) for n in rows.s_notes]
        annotationNotes = rows.iloc[0].a_pitchNames
        missingChordTones = set(annotationNotes) - set(scoreNotes)
        nonChordTones = [n for n in scoreNotes if n not in annotationNotes]
        missingChordTonesScore = len(missingChordTones) / len(
            set(annotationNotes)
        )
        nonChordTonesScore = len(nonChordTones) / len(scoreNotes)
        squaredSumScore = (missingChordTonesScore + nonChordTonesScore) ** 2
        df.loc[df.a_annotationNumber == n, "qualityScoreNotes"] = str(
            scoreNotes
        )
        df.loc[
            df.a_annotationNumber == n, "qualityNonChordTones"
        ] = nonChordTonesScore
        df.loc[
            df.a_annotationNumber == n, "qualityMissingChordTones"
        ] = missingChordTonesScore
        df.loc[
            df.a_annotationNumber == n, "qualitySquaredSum"
        ] = squaredSumScore
    return df


def parseAnnotationAndScore(a, s, qualityAssessment=True):
    """Process a score an RomanText file simultaneously.

    s is a .mxl|.krn|.musicxml file
    a is a RomanText file

    Create the dataframes of both, generate a new one.
    """
    # Parse each file
    adf = parseAnnotation(a)
    sdf = parseScore(s)
    # Create the joint dataframe
    jointdf = pd.concat([sdf, adf], axis=1)
    # Sometimes, scores are longer than annotations (trailing empty measures)
    # In that case, ffill the annotation portion of the new dataframe
    jointdf["a_isOnset"].fillna(False, inplace=True)
    jointdf.fillna(method="ffill", inplace=True)
    if qualityAssessment:
        jointdf = _measureAlignmentScore(jointdf)
        jointdf = _qualityMetric(jointdf)
    return jointdf


def parseAnnotationAndAnnotation(a, qualityAssessment=True):
    adf = parseAnnotation(a)
    sdf = parseScore(a, fmt="romantext")
    jointdf = pd.concat([sdf, adf], axis=1)
    jointdf["a_isOnset"].fillna(False, inplace=True)
    jointdf.fillna(method="ffill", inplace=True)
    if qualityAssessment:
        jointdf = _measureAlignmentScore(jointdf)
        jointdf = _qualityMetric(jointdf)
    return jointdf