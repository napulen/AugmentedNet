import random

import music21

from AugmentedNet.common import ANNOTATIONSCOREDUPLES
from AugmentedNet.score_parser import (
    _m21Parse,
    _initialDataFrame,
    _texturizeAnnotationScore,
)
from AugmentedNet.score_parser import parseAnnotationAsScore


interesting = [
    "abc-op18-no1-1",
    "bps-22-op054-1",
    "bps-25-op079-sonatina-1",
    "haydnsun-no2-3",
    "haydnsun-no4-1",
    "tavern-beethoven-woo-69-b",
    "tavern-beethoven-woo-70-a",
    "tavern-beethoven-woo-70-b",
    "tavern-beethoven-woo-71-a",
    "wir-bach-chorales-12",
    "wir-bach-chorales-17",
    "wir-openscore-liedercorpus-chaminade-amoroso",
    "wir-openscore-liedercorpus-reichardt-zwolf-gesange-op-3-03-die-blume-der-blumen",
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-02-die-wetterfahne",
    "wir-openscore-liedercorpus-schubert-winterreise-d-911-05-der-lindenbau",
]


def _engraveScore(df, ts):
    """Useful for debugging _texturizeAnnotationScore."""
    chords = music21.stream.Stream()
    offset = 0.0
    for row in df.itertuples():
        if offset in ts:
            chords.append(music21.meter.TimeSignature(ts[offset]))
        if row.s_measure == 0:
            offset += row.s_duration
            continue
        pitches = row.s_notes
        duration = row.s_duration
        chord = music21.chord.Chord(pitches, quarterLength=duration)
        chords.append(chord)
        offset += duration
    return chords


def get_ts(score):
    s = music21.converter.parse(score)
    tss = {
        ts.offset: ts.ratioString
        for ts in s.flat.getElementsByClass("TimeSignature")
    }
    return tss


if __name__ == "__main__":
    random.shuffle(interesting)
    nickname = interesting[0]
    print(nickname)
    annotation, score = ANNOTATIONSCOREDUPLES[nickname]
    tss = get_ts(score)
    df = parseAnnotationAsScore(annotation, texturize=True, eventBased=True)
    _engraveScore(df, tss).show()
