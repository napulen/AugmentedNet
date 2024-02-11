"""Templates for texturizing annotation files and turn them into scores."""

import random
from music21 import note
from music21 import interval


class TextureTemplate(object):
    """The base class for texturization templates."""

    supported_durations = [4.0, 3.0, 2.0, 1.5, 1.0]
    supported_number_of_notes = [1, 3, 4]

    def __init__(self, duration, notes, intervals):
        self.numberOfNotes = len(notes)
        if duration not in self.supported_durations:
            raise ValueError("Wrong duration value for this template.")
        if self.numberOfNotes not in self.supported_number_of_notes:
            raise ValueError(
                "This template doesn't support that number of notes."
            )
        self.duration = duration
        self.notes = notes
        self.intervals = intervals
        self.header = (
            "s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset\n"
        )
        if self.numberOfNotes == 1:
            self.template = self.templateNote
        if self.numberOfNotes == 3:
            self.template = self.templateTriad
        elif self.numberOfNotes == 4:
            self.template = self.templateSeventh

    def templateNote(self):
        if self.duration == 3.0:
            return self.templateNoteDottedHalf()
        elif self.duration == 1.5:
            return self.templateNoteDottedQuarter()
        else:
            return self.templateNoteBinary()

    def templateNoteDottedHalf(self):
        raise NotImplementedError()

    def templateNoteDottedQuarter(self):
        raise NotImplementedError()

    def templateNoteBinary(self):
        raise NotImplementedError()

    def templateTriad(self):
        if self.duration == 3.0:
            return self.templateTriadDottedHalf()
        elif self.duration == 1.5:
            return self.templateTriadDottedQuarter()
        else:
            return self.templateTriadBinary()

    def templateTriadDottedHalf(self):
        raise NotImplementedError()

    def templateTriadDottedQuarter(self):
        raise NotImplementedError()

    def templateTriadBinary(self):
        raise NotImplementedError()

    def templateSeventh(self):
        if self.duration == 3.0:
            return self.templateSeventhDottedHalf()
        elif self.duration == 1.5:
            return self.templateSeventhDottedQuarter()
        else:
            return self.templateSeventhBinary()

    def templateSeventhDottedHalf(self):
        raise NotImplementedError()

    def templateSeventhDottedQuarter(self):
        raise NotImplementedError()

    def templateSeventhBinary(self):
        raise NotImplementedError()

    def __str__(self):
        return self.header + self.template()

    def __repr__(self):
        return str(self)


class BassSplit(TextureTemplate):
    """Dividing the bass and remaining notes.

    The original chord duration is divided by half, playing
    the bass note in isolation during the first half,
    followed by the remaining upper notes."""

    supported_number_of_notes = [3, 4]

    def templateTriadBinary(self):
        dur = self.duration / 2
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,"['{self.notes[1]}', '{self.notes[2]}']",['{self.intervals[2]}'],"[True, True]"
"""

    def templateTriadDottedHalf(self):
        dur = 0.5
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,"['{self.notes[1]}', '{self.notes[2]}']",['{self.intervals[2]}'],"[True, True]"
{dur*2},{dur},,"['{self.notes[1]}', '{self.notes[2]}']",['{self.intervals[2]}'],"[True, True]"
{dur*3},{dur},,"['{self.notes[1]}', '{self.notes[2]}']",['{self.intervals[2]}'],"[True, True]"
{dur*4},{dur},,"['{self.notes[1]}', '{self.notes[2]}']",['{self.intervals[2]}'],"[True, True]"
{dur*5},{dur},,"['{self.notes[1]}', '{self.notes[2]}']",['{self.intervals[2]}'],"[True, True]"
"""

    def templateTriadDottedQuarter(self):
        dur = 0.5
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,"['{self.notes[1]}', '{self.notes[2]}']",['{self.intervals[2]}'],"[True, True]"
{dur*2},{dur},,"['{self.notes[1]}', '{self.notes[2]}']",['{self.intervals[2]}'],"[True, True]"
"""

    def templateSeventhBinary(self):
        dur = self.duration / 2
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,"['{self.notes[1]}', '{self.notes[2]}', '{self.notes[3]}']","['{self.intervals[3]}', '{self.intervals[4]}']","[True, True, True]"
"""

    def templateSeventhDottedHalf(self):
        dur = 0.5
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,"['{self.notes[1]}', '{self.notes[2]}', '{self.notes[3]}']","['{self.intervals[3]}', '{self.intervals[4]}']","[True, True, True]"
{dur*2},{dur},,"['{self.notes[1]}', '{self.notes[2]}', '{self.notes[3]}']","['{self.intervals[3]}', '{self.intervals[4]}']","[True, True, True]"
{dur*3},{dur},,"['{self.notes[1]}', '{self.notes[2]}', '{self.notes[3]}']","['{self.intervals[3]}', '{self.intervals[4]}']","[True, True, True]"
{dur*4},{dur},,"['{self.notes[1]}', '{self.notes[2]}', '{self.notes[3]}']","['{self.intervals[3]}', '{self.intervals[4]}']","[True, True, True]"
{dur*5},{dur},,"['{self.notes[1]}', '{self.notes[2]}', '{self.notes[3]}']","['{self.intervals[3]}', '{self.intervals[4]}']","[True, True, True]"
"""

    def templateSeventhDottedQuarter(self):
        dur = 0.5
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,"['{self.notes[1]}', '{self.notes[2]}', '{self.notes[3]}']","['{self.intervals[3]}', '{self.intervals[4]}']","[True, True, True]"
{dur*2},{dur},,"['{self.notes[1]}', '{self.notes[2]}', '{self.notes[3]}']","['{self.intervals[3]}', '{self.intervals[4]}']","[True, True, True]"
"""


class Alberti(TextureTemplate):
    """An Alberti-bass-like texturization of a chord.

    A  4-note  melodic  pattern with the contour
    lowest, highest, middle, highest."""

    supported_number_of_notes = [3, 4]

    def templateTriadBinary(self):
        dur = self.duration / 4
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,['{self.notes[2]}'],[],[True]
{dur*2},{dur},,['{self.notes[1]}'],[],[True]
{dur*3},{dur},,['{self.notes[2]}'],[],[True]
"""

    def templateTriadDottedHalf(self):
        dur = 0.5
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,['{self.notes[2]}'],[],[True]
{dur*2},{dur},,['{self.notes[1]}'],[],[True]
{dur*3},{dur},,['{self.notes[2]}'],[],[True]
{dur*4},{dur},,['{self.notes[1]}'],[],[True]
{dur*5},{dur},,['{self.notes[2]}'],[],[True]
"""

    def templateTriadDottedQuarter(self):
        dur = 0.5
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,['{self.notes[2]}'],[],[True]
{dur*2},{dur},,['{self.notes[1]}'],[],[True]
"""

    def templateSeventhBinary(self):
        dur = self.duration / 4
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,['{self.notes[3]}'],[],[True]
{dur*2},{dur},,['{self.notes[1]}'],[],[True]
{dur*3},{dur},,['{self.notes[2]}'],[],[True]
"""

    def templateSeventhDottedHalf(self):
        dur = 0.5
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,['{self.notes[3]}'],[],[True]
{dur*2},{dur},,['{self.notes[1]}'],[],[True]
{dur*3},{dur},,['{self.notes[2]}'],[],[True]
{dur*4},{dur},,['{self.notes[1]}'],[],[True]
{dur*5},{dur},,['{self.notes[2]}'],[],[True]
"""

    def templateSeventhDottedQuarter(self):
        dur = 0.5
        return f"""\
0.0,{dur},,"['{self.notes[0]}', '{self.notes[3]}']",['{self.intervals[2]}'],[True]
{dur},{dur},,['{self.notes[1]}'],[],[True]
{dur*2},{dur},,['{self.notes[2]}'],[],[True]
"""


class Syncopation(TextureTemplate):
    """A syncopated pattern to separate the upper voice from the rest.

    The highest note is played in isolation,
    followed by the remaining lower notes,
    played in syncopation."""

    supported_durations = [4.0, 2.0]
    supported_number_of_notes = [3, 4]

    def templateTriad(self):
        dur = self.duration / 4
        return f"""\
0.0,{dur},,['{self.notes[2]}'],[],[True]
{dur},{dur*2},,['{self.notes[0]}'],[],[True]
{dur*3},{dur},,['{self.notes[1]}'],[],[True]
"""

    def templateSeventh(self):
        dur = self.duration / 4
        return f"""\
0.0,{dur},,['{self.notes[3]}'],[],[True]
{dur},{dur*2},,"['{self.notes[0]}', '{self.notes[1]}', '{self.notes[2]}']","['{self.intervals[0]}', '{self.intervals[1]}']","[True, True, True]"
{dur*3},{dur},,"['{self.notes[0]}', '{self.notes[1]}', '{self.notes[2]}']","['{self.intervals[0]}', '{self.intervals[1]}']","[True, True, True]"
"""


class Arpeggio(TextureTemplate):
    """A simple arpeggio pattern that climbs and descends the chord.

    The lowest note to the highest note of the chord is played in isolation,
    then the highest note to the lowest note is played in isolation."""

    supported_number_of_notes = [3, 4]

    def templateTriadBinary(self):
        dur = self.duration / 4
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,['{self.notes[1]}'],[],[True]
{dur*2},{dur},,['{self.notes[2]}'],[],[True]
{dur*3},{dur},,['{self.notes[1]}'],[],[True]
"""

    def templateTriadDottedHalf(self):
        dur = 0.25
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,['{self.notes[1]}'],[],[True]
{dur*2},{dur},,['{self.notes[2]}'],[],[True]
{dur*3},{dur},,['{self.notes[1]}'],[],[True]
{dur*4},{dur},,['{self.notes[0]}'],[],[True]
{dur*5},{dur},,['{self.notes[1]}'],[],[True]
{dur*6},{dur},,['{self.notes[2]}'],[],[True]
{dur*7},{dur},,['{self.notes[1]}'],[],[True]
{dur*8},{dur},,['{self.notes[0]}'],[],[True]
{dur*9},{dur},,['{self.notes[1]}'],[],[True]
{dur*10},{dur},,['{self.notes[2]}'],[],[True]
{dur*11},{dur},,['{self.notes[1]}'],[],[True]
"""

    def templateTriadDottedQuarter(self):
        dur = 0.25
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,['{self.notes[1]}'],[],[True]
{dur*2},{dur},,['{self.notes[2]}'],[],[True]
{dur*3},{dur},,['{self.notes[1]}'],[],[True]
{dur*4},{dur},,['{self.notes[0]}'],[],[True]
{dur*5},{dur},,['{self.notes[1]}'],[],[True]
"""

    def templateSeventhBinary(self):
        dur = self.duration / 4
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,['{self.notes[1]}'],[],[True]
{dur*2},{dur},,['{self.notes[3]}'],[],[True]
{dur*3},{dur},,['{self.notes[1]}'],[],[True]
"""

    def templateSeventhDottedHalf(self):
        dur = 0.25
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,['{self.notes[1]}'],[],[True]
{dur*2},{dur},,['{self.notes[3]}'],[],[True]
{dur*3},{dur},,['{self.notes[1]}'],[],[True]
{dur*4},{dur},,['{self.notes[0]}'],[],[True]
{dur*5},{dur},,['{self.notes[1]}'],[],[True]
{dur*6},{dur},,['{self.notes[3]}'],[],[True]
{dur*7},{dur},,['{self.notes[1]}'],[],[True]
{dur*8},{dur},,['{self.notes[0]}'],[],[True]
{dur*9},{dur},,['{self.notes[1]}'],[],[True]
{dur*10},{dur},,['{self.notes[3]}'],[],[True]
{dur*11},{dur},,['{self.notes[1]}'],[],[True]
"""

    def templateSeventhDottedQuarter(self):
        dur = 0.25
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,['{self.notes[1]}'],[],[True]
{dur*2},{dur},,['{self.notes[3]}'],[],[True]
{dur*3},{dur},,['{self.notes[1]}'],[],[True]
{dur*4},{dur},,['{self.notes[0]}'],[],[True]
{dur*5},{dur},,['{self.notes[1]}'],[],[True]
"""


    def templateSeventh(self):
        dur = self.duration / 6
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,['{self.notes[1]}'],[],[True]
{dur*2},{dur},,['{self.notes[2]}'],[],[True]
{dur*3},{dur},,['{self.notes[3]}'],[],[True]
{dur*4},{dur},,['{self.notes[2]}'],[],[True]
{dur*5},{dur},,['{self.notes[1]}'],[],[True]
"""


class AuxiliaryNotes(TextureTemplate):
    """A pitch pattern that creates a minor second interval in the middle of the chord.
    """

    supported_durations = [4.0, 2.0, 1.5, 1.0]
    supported_number_of_notes = [1]


    def templateNoteBinary(self):
        transposed_note_up = note.Note(self.notes[0]).transpose(1)
        transposed_name_up = transposed_note_up.nameWithOctave
        transposed_note_down = note.Note(self.notes[0]).transpose(-1)
        transposed_name_down = transposed_note_down.nameWithOctave
        dur = self.duration / 4
        return f"""\
0.0,{dur},,['{transposed_name_up}'],[],[True]
{dur},{dur},,['{self.notes[0]}'],[],[True]
{dur*2},{dur},,['{transposed_name_down}'],[],[True]
{dur*3},{dur},,['{self.notes[0]}'],[],[True]
"""

    def templateNoteDottedQuarter(self):
        transposed_note_up = note.Note(self.notes[0]).transpose(1)
        transposed_name_up = transposed_note_up.nameWithOctave
        transposed_note_down = note.Note(self.notes[0]).transpose(-1)
        transposed_name_down = transposed_note_down.nameWithOctave
        dur = 0.25
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,['{transposed_name_up}'],[],[True]
{dur*2},{dur},,['{self.notes[0]}'],[],[True]
{dur*3},{dur},,['{transposed_name_down}'],[],[True]
{dur*5},{dur*2},,['{self.notes[0]}'],[],[True]
"""


class BlockChord(TextureTemplate):
    """A block-chord texture. The default texture in music21-generated scores."""

    supported_number_of_notes = [3, 4]

    def templateTriad(self):
        dur = self.duration
        return f"""\
0.0,{dur},,"['{self.notes[0]}', '{self.notes[1]}', '{self.notes[2]}']","['{self.intervals[0]}', '{self.intervals[1]}']","[True, True, True]"
"""

    def templateSeventh(self):
        dur = self.duration
        return f"""\
0.0,{dur},,"['{self.notes[0]}', '{self.notes[1]}', '{self.notes[2]}', '{self.notes[3]}']","['{self.intervals[0]}', '{self.intervals[1]}', '{self.intervals[2]}']","[True, True, True, True]"
"""


available_templates = {
    "BassSplit": BassSplit,
    "Alberti": Alberti,
    "Syncopation": Syncopation,
    "BlockChord": BlockChord,
    "Arpeggio": Arpeggio,
    "AuxiliaryNotes": AuxiliaryNotes,
}

available_durations = list(
    reversed(
        sorted(
            set(
                [
                    d
                    for t in available_templates.values()
                    for d in t.supported_durations
                ]
            )
        )
    )
)

available_number_of_notes = list(
    reversed(
        sorted(
            set(
                [
                    n
                    for t in available_templates.values()
                    for n in t.supported_number_of_notes
                ]
            )
        )
    )
)


def _getRelevantTemplates(duration, numberOfNotes):
    ret = []
    for template in available_templates.values():
        if (
            duration in template.supported_durations
            and numberOfNotes in template.supported_number_of_notes
        ):
            ret.append(template)
    return ret


def applyTextureTemplate(duration, notes, intervals, templateName=None):
    """Apply a random texture to a chord with the given duration and notes."""

    numberOfNotes = len(notes)
    if templateName:
        if templateName not in available_templates:
            raise KeyError()
        else:
            template = available_templates[templateName]
            return str(template(duration, notes, intervals))
    if (
        duration not in available_durations
        or numberOfNotes not in available_number_of_notes
    ):
        raise KeyError()
    relevantTemplates = _getRelevantTemplates(duration, numberOfNotes)
    return str(random.choice(relevantTemplates)(duration, notes, intervals))
