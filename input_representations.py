from cache import TransposePitch, m21Pitch, m21Key
from feature_representation import (
    PITCHCLASSES,
    NOTENAMES,
    INTERVALCLASSES,
    FeatureRepresentation,
)
import numpy as np

NOTENAMEDEFAULTCLASS = {
    "C": 0,
    "D": 2,
    "E": 4,
    "F": 5,
    "G": 7,
    "A": 9,
    "B": 11,
}


# def _solvePitchSpelling(noteNames, pitchClasses):
#     if len(noteNames) != len(pitchClasses):
#         raise Exception
#     if not noteNames:
#         return
#     elif len(noteNames) == 1:
#     note = noteNames[0]
#     default = NOTENAMEDEFAULTCLASS[note]
#     bestMatch = 999999
#     for pc in pitchClasses:
#         diff = pc -


class BassChromagram38(FeatureRepresentation):
    features = 2 * (len(NOTENAMES) + len(PITCHCLASSES))

    def run(self, transposition="P1"):
        array = np.zeros(self.shape, dtype=self.dtype)
        for frame, notes in enumerate(self.df.s_notes):
            for idx, note in enumerate(notes):
                transposedNote = TransposePitch(note, transposition)
                pitchObj = m21Pitch(transposedNote)
                pitchLetter = pitchObj.step
                pitchLetterIndex = NOTENAMES.index(pitchLetter)
                pitchClass = pitchObj.pitchClass
                array[frame, pitchLetterIndex + 19] = 1
                array[frame, pitchClass + 26] = 1
                if idx == 0:
                    array[frame, pitchLetterIndex] = 1
                    array[frame, pitchClass + 7] = 1
        return array

    @classmethod
    def decode(cls, array):
        if len(array.shape) != 2 or array.shape[1] != cls.features:
            raise IndexError("Strange array shape.")
        ret = []
        for manyhot in array:
            bassPitchName = NOTENAMES[np.argmax(manyhot[:7])]
            bassPitchClass = np.argmax(manyhot[7:19])
            chromagramPitchNames = [
                NOTENAMES[x] for x in np.nonzero(manyhot[19:26])[0]
            ]
            chromagramPitchClasses = np.nonzero(manyhot[26:])[0].tolist()
            ret.append(
                (
                    bassPitchName,
                    bassPitchClass,
                    tuple(chromagramPitchNames),
                    tuple(chromagramPitchClasses),
                )
            )
        return ret


class BassIntervals63(FeatureRepresentation):
    features = len(INTERVALCLASSES) + 19

    def run(self, transposition="P1"):
        array = np.zeros(self.shape, dtype=self.dtype)
        for frame, r in enumerate(self.df.iterrows()):
            _, row = r
            bass = row.s_notes[0]
            intervals = row.s_intervals
            transposedBass = TransposePitch(bass, transposition)
            pitchObj = m21Pitch(transposedBass)
            pitchLetter = pitchObj.step
            pitchLetterIndex = NOTENAMES.index(pitchLetter)
            pitchClass = pitchObj.pitchClass
            array[frame, pitchLetterIndex] = 1
            array[frame, 7 + pitchClass] = 1
            for interval in intervals:
                intervalIndex = INTERVALCLASSES.index(interval)
                array[frame, 19 + intervalIndex] = 1
        return array

    @classmethod
    def decode(cls, array):
        if len(array.shape) != 2 or array.shape[1] != cls.features:
            raise IndexError("Strange array shape.")
        ret = []
        for manyhot in array:
            bassPitchName = NOTENAMES[np.argmax(manyhot[:7])]
            bassPitchClass = np.argmax(manyhot[7:19])
            intervals = [
                INTERVALCLASSES[x] for x in np.nonzero(manyhot[19:])[0]
            ]
            ret.append(
                (
                    bassPitchName,
                    bassPitchClass,
                    tuple(intervals),
                )
            )
        return ret


class ChromagramInterval(FeatureRepresentation):
    features = 19 + 19 + 44

    def run(self, transposition="P1"):
        array = np.zeros(self.shape, dtype=self.dtype)
        for frame, r in enumerate(self.df.iterrows()):
            _, row = r
            intervals = row.s_intervals
            notes = row.s_notes
            for idx, note in enumerate(notes):
                transposedNote = TransposePitch(note, transposition)
                pitchObj = m21Pitch(transposedNote)
                pitchLetter = pitchObj.step
                pitchLetterIndex = NOTENAMES.index(pitchLetter)
                pitchClass = pitchObj.pitchClass
                array[frame, pitchLetterIndex + 19] = 1
                array[frame, pitchClass + 26] = 1
                if idx == 0:
                    array[frame, pitchLetterIndex] = 1
                    array[frame, pitchClass + 7] = 1
            for interval in intervals:
                intervalIndex = INTERVALCLASSES.index(interval)
                array[frame, 38 + intervalIndex] = 1
        return array


# def pitchClassNoteName(df, minOctave=2, maxOctave=6):
#     """Encodes a Score DataFrame into a pianoroll-like representation.

#     Expects a DataFrame parsed by parseScore(). Returns a numpy() array.
#     """
#     octaves = maxOctave - minOctave + 1
#     frames = len(df.index)
#     ret = np.zeros((frames, 19 * octaves))
#     for frame, notes in enumerate(df.s_notes):
#         for note in notes:
#             m21Pitch = music21.pitch.Pitch(note)
#             pitchLetter = m21Pitch.step
#             pitchLetterIndex = NOTENAMES.index(pitchLetter)
#             pitchClass = m21Pitch.pitchClass
#             octave = m21Pitch.octave
#             if not minOctave <= octave <= maxOctave:
#                 continue
#             octave -= minOctave
#             ret[frame, pitchLetterIndex + 7 * octave] = 1
#             ret[frame, pitchClass + 7 * octaves + 12 * octave] = 1
#     return ret


# def salamiSliceWithHold(df, numberOfNotes=5):
#     """Encodes a Score DataFrame into a salami-slice representation.

#     Expects a DataFrame parsed by parseScore(). Returns a numpy() array.
#     """
#     frames = len(df.index)
#     ret = np.zeros((frames, (20 + 7) * numberOfNotes))
#     for frame, r in enumerate(df.iterrows()):
#         _, row = r
#         notes = row.s_notes
#         onsets = row.s_isOnset
#         noteIndex = 0
#         # print(notes, onsets)
#         for note, onset in zip(notes, onsets):
#             m21Pitch = music21.pitch.Pitch(note)
#             pitchLetter = m21Pitch.step
#             pitchLetterIndex = NOTENAMES.index(pitchLetter)
#             pitchClass = m21Pitch.pitchClass
#             octave = m21Pitch.octave
#             # print(frame, note, onset, pitchLetterIndex, pitchClass, octave)
#             ret[frame, pitchLetterIndex + 27 * noteIndex] = 1
#             ret[frame, pitchClass + 7 + 27 * noteIndex] = 1
#             ret[frame, octave + 19 + 27 * noteIndex] = 1
#             if not onset:
#                 ret[frame, 26 + 27 * noteIndex] = 1
#                 # print(note, onset, 'hold')
#             noteIndex += 1
#     return ret


# def compressedSalamiSliceWithHold(df, numberOfNotes=5):
#     """Encodes a Score DataFrame into a salami-slice representation.

#     Expects a DataFrame parsed by parseScore(). Returns a numpy() array.
#     """
#     frames = len(df.index)
#     ret = np.zeros((frames, 20 * numberOfNotes))
#     for frame, r in enumerate(df.iterrows()):
#         _, row = r
#         notes = row.s_notes
#         onsets = row.s_isOnset
#         noteIndex = 0
#         # print.s_notes, onsets)
#         pitchClasses = []
#         for note, onset in zip(notes, onsets):
#             if noteIndex == numberOfNotes:
#                 break
#             m21Pitch = music21.pitch.Pitch(note)
#             pitchLetter = m21Pitch.step
#             pitchLetterIndex = NOTENAMES.index(pitchLetter)
#             pitchClass = m21Pitch.pitchClass
#             if pitchClass in pitchClasses:
#                 continue
#             pitchClasses.append(pitchClass)
#             # print(frame, note, onset, pitchLetterIndex, pitchClass, octave)
#             ret[frame, pitchLetterIndex + 20 * noteIndex] = 1
#             ret[frame, pitchClass + 7 + 20 * noteIndex] = 1
#             if not onset:
#                 ret[frame, 19 + 20 * noteIndex] = 1
#                 # print(note, onset, 'hold')
#             noteIndex += 1
#     return ret


# def micchiChromagram(df):
#     """Encodes a 70-feature bass-chromagram, as in Micchi et al. 2020.

#     Expects a DataFrame parsed by parseScore(). Returns a numpy() array.
#     """
#     frames = len(df.index)
#     ret = np.zeros((frames, 70))
#     for frame, notes in enumerate(df.s_notes):
#         for idx, note in enumerate(notes):
#             noOctave = music21.note.Note(note).name
#             spellingIndex = SPELLINGS.index(noOctave)
#             ret[frame, spellingIndex + 35] = 1
#             if idx == 0:
#                 ret[frame, spellingIndex] = 1
#     return ret


# def micchiChromagram19(df, dataAugmentation=False):
#     """Encodes a "compressed" bass-chromagram, similar to Micchi et al. 2020.

#     Expects a DataFrame parsed by parseScore(). Returns a numpy() array.
#     """
#     frames, classes = len(df.index), (19 * 2)
#     ret = np.zeros((frames, classes))
#     dataAug = None

#     for frame, notes in enumerate(df.s_notes):
#         for idx, note in enumerate(notes):
#             pitchObj = m21Pitch(note)
#             pitchLetter = pitchObj.step
#             pitchLetterIndex = NOTENAMES.index(pitchLetter)
#             pitchClass = pitchObj.pitchClass
#             ret[frame, pitchLetterIndex + 19] = 1
#             ret[frame, pitchClass + 19 + 7] = 1
#             if idx == 0:
#                 ret[frame, pitchLetterIndex] = 1
#                 ret[frame, pitchClass + 7] = 1

#     if not dataAugmentation:
#         return ret, dataAug

#     dataAug = np.zeros((len(INTERVAL_TRANSPOSITIONS), frames, classes))
#     for transposition, interval in enumerate(INTERVAL_TRANSPOSITIONS):
#         tr = dataAug[transposition]
#         for frame, notes in enumerate(df.s_notes):
#             for idx, note in enumerate(notes):
#                 pitchObj = TransposePitch(note, interval)
#                 pitchLetter = pitchObj.step
#                 pitchLetterIndex = NOTENAMES.index(pitchLetter)
#                 pitchClass = pitchObj.pitchClass
#                 tr[frame, pitchLetterIndex + 19] = 1
#                 tr[frame, pitchClass + 19 + 7] = 1
#                 if idx == 0:
#                     tr[frame, pitchLetterIndex] = 1
#                     tr[frame, pitchClass + 7] = 1

#     return ret, dataAug


# def intervalRepresentation(df, dataAugmentation=False):
#     """Encodes a "compressed" bass-chromagram, similar to Micchi et al. 2020.

#     Expects a DataFrame parsed by parseScore(). Returns a numpy() array.
#     """
#     frames, classes = len(df.index), (19 + len(INTERVALCLASSES))
#     ret = np.zeros((frames, classes))
#     dataAug = None

#     for frame, r in enumerate(df.iterrows()):
#         _, row = r
#         bass = row.s_notes[0]
#         intervals = row.s_intervals
#         pitchObj = m21Pitch(bass)
#         pitchLetter = pitchObj.step
#         pitchLetterIndex = NOTENAMES.index(pitchLetter)
#         pitchClass = pitchObj.pitchClass
#         ret[frame, pitchLetterIndex] = 1
#         ret[frame, 7 + pitchClass] = 1
#         for interval in intervals:
#             intervalIndex = INTERVALCLASSES.index(interval)
#             ret[frame, 19 + intervalIndex] = 1

#     if not dataAugmentation:
#         return ret, dataAug

#     dataAug = np.zeros((len(INTERVAL_TRANSPOSITIONS), frames, classes))
#     for transposition, interval in enumerate(INTERVAL_TRANSPOSITIONS):
#         tr = dataAug[transposition]
#         for frame, r in enumerate(df.iterrows()):
#             _, row = r
#             bass = row.s_notes[0]
#             transposed = TransposePitch(bass, interval)
#             pitchObj = m21Pitch(transposed)
#             intervals = row.s_intervals
#             pitchLetter = pitchObj.step
#             pitchLetterIndex = NOTENAMES.index(pitchLetter)
#             pitchClass = pitchObj.pitchClass
#             tr[frame, pitchLetterIndex] = 1
#             tr[frame, 7 + pitchClass] = 1
#             for interval in intervals:
#                 intervalIndex = INTERVALCLASSES.index(interval)
#                 tr[frame, 19 + intervalIndex] = 1

#     return ret, dataAug
