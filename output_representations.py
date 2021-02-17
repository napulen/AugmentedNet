import numpy as np
import music21

NOTENAMES = ("C", "D", "E", "F", "G", "A", "B")


def bass(df):
    """Encodes an Annotation DataFrame into a numpy array representation.

    Expects a DataFrame parsed by parseAnnotation(). Returns a numpy() array.
    """
    frames = len(df.index)
    ret = np.zeros((frames, 19))
    for frame, bass in enumerate(df.bass):
        m21Pitch = music21.pitch.Pitch(bass)
        pitchLetter = m21Pitch.step
        pitchLetterIndex = NOTENAMES.index(pitchLetter)
        pitchClass = m21Pitch.pitchClass
        ret[frame, pitchLetterIndex] = 1
        ret[frame, pitchClass + 7] = 1
    return ret


def inversion(df):
    """Encodes an Annotation DataFrame into a numpy array representation.

    Expects a DataFrame parsed by parseAnnotation(). Returns a numpy() array.
    """
    frames = len(df.index)
    ret = np.zeros((frames, 4))
    for frame, inversion in enumerate(df.inversion):
        ret[frame, int(inversion)] = 1
    return ret