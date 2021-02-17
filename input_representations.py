import numpy as np
import music21

NOTENAMES = ("C", "D", "E", "F", "G", "A", "B")


def pitchClassNoteName(df, minOctave=2, maxOctave=6):
    """Encodes a Score DataFrame into a pianoroll-like representation.

    Expects a DataFrame parsed by parseScore(). Returns a numpy() array.
    """
    octaves = maxOctave - minOctave + 1
    frames = len(df.index)
    ret = np.zeros((frames, 19 * octaves))
    for frame, notes in enumerate(df.notes):
        for note in notes:
            m21Pitch = music21.pitch.Pitch(note)
            pitchLetter = m21Pitch.step
            pitchLetterIndex = NOTENAMES.index(pitchLetter)
            pitchClass = m21Pitch.pitchClass
            octave = m21Pitch.octave
            if not minOctave <= octave <= maxOctave:
                continue
            octave -= minOctave
            ret[frame, pitchLetterIndex + 7 * octave] = 1
            ret[frame, pitchClass + 7 * octaves + 12 * octave] = 1
    return ret
