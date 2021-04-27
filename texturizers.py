import random

########
# Triads
########
whole_triad_basssplit = """
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,2.0,,['{notes[0]}'],[],[True]
2.0,2.0,,"['{notes[1]}', '{notes[2]}']",['{intervals[2]}'],"[True, True]"
"""

half_triad_basssplit = """
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,1.0,,['{notes[0]}'],[],[True]
1.0,1.0,,"['{notes[1]}', '{notes[2]}']",['{intervals[2]}'],"[True, True]"
"""

quarter_triad_basssplit = """
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,0.5,,['{notes[0]}'],[],[True]
0.5,0.5,,"['{notes[1]}', '{notes[2]}']",['{intervals[2]}'],"[True, True]"
"""


whole_triad_alberti = """
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,1.0,,['{notes[0]}'],[],[True]
1.0,1.0,,['{notes[2]}'],[],[True]
2.0,1.0,,['{notes[1]}'],[],[True]
3.0,1.0,,['{notes[2]}'],[],[True]
"""

half_triad_alberti = """
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,0.5,,['{notes[0]}'],[],[True]
0.5,0.5,,['{notes[2]}'],[],[True]
1.0,0.5,,['{notes[1]}'],[],[True]
1.5,0.5,,['{notes[2]}'],[],[True]
"""

quarter_triad_alberti = """
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,0.25,,['{notes[0]}'],[],[True]
0.25,0.25,,['{notes[2]}'],[],[True]
0.5,0.25,,['{notes[1]}'],[],[True]
0.75,0.25,,['{notes[2]}'],[],[True]
"""


whole_triad_block = """
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,4.0,,"['{notes[0]}', '{notes[1]}', '{notes[2]}']","['{intervals[0]}', '{intervals[1]}']","[True, True, True]"
"""

half_triad_block = """
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,2.0,,"['{notes[0]}', '{notes[1]}', '{notes[2]}']","['{intervals[0]}', '{intervals[1]}']","[True, True, True]"
"""

quarter_triad_block = """
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,1.0,,"['{notes[0]}', '{notes[1]}', '{notes[2]}']","['{intervals[0]}', '{intervals[1]}']","[True, True, True]"
"""


##########
# Sevenths
##########
whole_seventh_basssplit = """
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,2.0,,['{notes[0]}'],[],[True]
2.0,2.0,,"['{notes[1]}', '{notes[2]}', '{notes[3]}']","['{intervals[3]}', '{intervals[4]}']","[True, True, True]"
"""

half_seventh_basssplit = """
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,1.0,,['{notes[0]}'],[],[True]
1.0,1.0,,"['{notes[1]}', '{notes[2]}', '{notes[3]}']","['{intervals[3]}', '{intervals[4]}']","[True, True, True]"
"""

quarter_seventh_basssplit = """
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,0.5,,['{notes[0]}'],[],[True]
0.5,0.5,,"['{notes[1]}', '{notes[2]}', '{notes[3]}']","['{intervals[3]}', '{intervals[4]}']","[True, True, True]"
"""


whole_seventh_alberti = """
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,1.0,,['{notes[0]}'],[],[True]
1.0,1.0,,['{notes[3]}'],[],[True]
2.0,1.0,,['{notes[1]}'],[],[True]
3.0,1.0,,['{notes[2]}'],[],[True]
"""

half_seventh_alberti = """
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,0.5,,['{notes[0]}'],[],[True]
0.5,0.5,,['{notes[3]}'],[],[True]
1.0,0.5,,['{notes[1]}'],[],[True]
1.5,0.5,,['{notes[2]}'],[],[True]
"""

quarter_seventh_alberti = """
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,0.25,,['{notes[0]}'],[],[True]
0.25,0.25,,['{notes[3]}'],[],[True]
0.5,0.25,,['{notes[1]}'],[],[True]
0.75,0.25,,['{notes[2]}'],[],[True]
"""


whole_seventh_block = """
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,4.0,,"['{notes[0]}', '{notes[1]}', '{notes[2]}', '{notes[3]}']","['{intervals[0]}', '{intervals[1]}', '{intervals[2]}']","[True, True, True, True]"
"""

half_seventh_block = """
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,2.0,,"['{notes[0]}', '{notes[1]}', '{notes[2]}', '{notes[3]}']","['{intervals[0]}', '{intervals[1]}', '{intervals[2]}']","[True, True, True, True]"
"""

quarter_seventh_block = """
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,1.0,,"['{notes[0]}', '{notes[1]}', '{notes[2]}', '{notes[3]}']","['{intervals[0]}', '{intervals[1]}', '{intervals[2]}']","[True, True, True, True]"
"""


available_templates = {
    "whole": {
        "triad": [
            whole_triad_basssplit,
            whole_triad_alberti,
            whole_triad_block,
        ],
        "seventh": [
            whole_seventh_basssplit,
            whole_seventh_alberti,
            whole_seventh_block,
        ],
    },
    "half": {
        "triad": [
            half_triad_basssplit,
            half_triad_alberti,
            half_triad_block,
        ],
        "seventh": [
            half_seventh_basssplit,
            half_seventh_alberti,
            half_seventh_block,
        ],
    },
    "quarter": {
        "triad": [
            quarter_triad_basssplit,
            quarter_triad_alberti,
            quarter_triad_block,
        ],
        "seventh": [
            quarter_seventh_basssplit,
            quarter_seventh_alberti,
            quarter_seventh_block,
        ],
    },
}


def getTemplate(duration, numberOfNotes):
    if duration == 4.0:
        duration = "whole"
    elif duration == 2.0:
        duration = "half"
    elif duration == 1.0:
        duration = "quarter"

    if numberOfNotes == 3:
        numberOfNotes = "triad"
    elif numberOfNotes == 4:
        numberOfNotes = "seventh"
    if (
        not duration in available_templates
        or not numberOfNotes in available_templates[duration]
    ):
        raise KeyError(
            f"Cannot find a template for {duration}, {numberOfNotes}"
        )
    available = available_templates[duration][numberOfNotes]
    return random.choice(available)