import numpy as np
import music21

NOTENAMES = ("C", "D", "E", "F", "G", "A", "B")

ACCIDENTALS = ("--", "-", "", "#", "##")

SPELLINGS = [
    f"{letter}{accidental}"
    for letter in NOTENAMES
    for accidental in ACCIDENTALS
]


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


def salamiSliceWithHold(df, numberOfNotes=5):
    """Encodes a Score DataFrame into a salami-slice representation.

    Expects a DataFrame parsed by parseScore(). Returns a numpy() array.
    """
    frames = len(df.index)
    ret = np.zeros((frames, (20 + 7) * numberOfNotes))
    for frame, r in enumerate(df.iterrows()):
        _, row = r
        notes = row.notes
        onsets = row.isOnset
        noteIndex = 0
        # print(notes, onsets)
        for note, onset in zip(notes, onsets):
            m21Pitch = music21.pitch.Pitch(note)
            pitchLetter = m21Pitch.step
            pitchLetterIndex = NOTENAMES.index(pitchLetter)
            pitchClass = m21Pitch.pitchClass
            octave = m21Pitch.octave
            # print(frame, note, onset, pitchLetterIndex, pitchClass, octave)
            ret[frame, pitchLetterIndex + 27 * noteIndex] = 1
            ret[frame, pitchClass + 7 + 27 * noteIndex] = 1
            ret[frame, octave + 19 + 27 * noteIndex] = 1
            if not onset:
                ret[frame, 26 + 27 * noteIndex] = 1
                # print(note, onset, 'hold')
            noteIndex += 1
    return ret


def compressedSalamiSliceWithHold(df, numberOfNotes=5):
    """Encodes a Score DataFrame into a salami-slice representation.

    Expects a DataFrame parsed by parseScore(). Returns a numpy() array.
    """
    frames = len(df.index)
    ret = np.zeros((frames, 20*numberOfNotes))
    for frame, r in enumerate(df.iterrows()):
        _, row = r
        notes = row.notes
        onsets = row.isOnset
        noteIndex = 0
        # print(notes, onsets)
        pitchClasses = []
        for note, onset in zip(notes, onsets):
            if noteIndex == numberOfNotes:
                break
            m21Pitch = music21.pitch.Pitch(note)
            pitchLetter = m21Pitch.step
            pitchLetterIndex = NOTENAMES.index(pitchLetter)
            pitchClass = m21Pitch.pitchClass
            if pitchClass in pitchClasses:
                continue
            pitchClasses.append(pitchClass)
            # print(frame, note, onset, pitchLetterIndex, pitchClass, octave)
            ret[frame, pitchLetterIndex + 20 * noteIndex] = 1
            ret[frame, pitchClass + 7 + 20 * noteIndex] = 1
            if not onset:
                ret[frame, 19 + 20 * noteIndex] = 1
                # print(note, onset, 'hold')
            noteIndex += 1
    return ret


def micchiChromagram(df):
    """Encodes a 70-feature bass-chromagram, as in Micchi et al. 2020.

    Expects a DataFrame parsed by parseScore(). Returns a numpy() array.
    """
    frames = len(df.index)
    ret = np.zeros((frames, 70))
    for frame, notes in enumerate(df.notes):
        for idx, note in enumerate(notes):
            noOctave = music21.note.Note(note).name
            spellingIndex = SPELLINGS.index(noOctave)
            ret[frame, spellingIndex + 35] = 1
            if idx == 0:
                ret[frame, spellingIndex] = 1
    return ret


def micchiChromagram19(df):
    """Encodes a "compressed" bass-chromagram, similar to Micchi et al. 2020.

    Expects a DataFrame parsed by parseScore(). Returns a numpy() array.
    """
    frames = len(df.index)
    ret = np.zeros((frames, 38))
    for frame, notes in enumerate(df.notes):
        for idx, note in enumerate(notes):
            m21Pitch = music21.pitch.Pitch(note)
            pitchLetter = m21Pitch.step
            pitchLetterIndex = NOTENAMES.index(pitchLetter)
            pitchClass = m21Pitch.pitchClass
            ret[frame, pitchLetterIndex + 19] = 1
            ret[frame, pitchClass + 19 + 7] = 1
            if idx == 0:
                ret[frame, pitchLetterIndex] = 1
                ret[frame, pitchClass + 7] = 1
    return ret