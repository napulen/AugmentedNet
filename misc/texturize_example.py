from common import ANNOTATIONSCOREDUPLES
from score_parser import (
    _m21Parse,
    _initialDataFrame,
    _texturizeAnnotationScore,
)
from joint_parser import parseAnnotationAndAnnotation
import music21


def _engraveScore(df):
    """Useful for debugging _texturizeAnnotationScore."""
    chords = music21.stream.Stream()
    for row in df.itertuples():
        if row.s_measure == 0:
            continue
        pitches = row.s_notes
        duration = row.s_duration
        chord = music21.chord.Chord(pitches, quarterLength=duration)
        chords.append(chord)
    return chords


f = "bps-01-op002-no1-1"

annotation, score = ANNOTATIONSCOREDUPLES[f]

df = parseAnnotationAndAnnotation(annotation)

_engraveScore(df).show()

