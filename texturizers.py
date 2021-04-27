import random

whole_triad_simple = """\
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,2.0,,['{notes[0]}'],[],[True]
2.0,2.0,,"['{notes[1]}', '{notes[2]}']",['{intervals[2]}'],"[True, True]"
"""

whole_seventh_simple = """
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,2.0,,['{notes[0]}'],[],[True]
2.0,2.0,,"['{notes[1]}', '{notes[2]}', '{notes[3]}']","['{intervals[3]}', '{intervals[4]}']","[True, True, True]"
"""

available_templates = {
    "whole": {
        "triad": [whole_triad_simple],
        "seventh": [whole_seventh_simple],
    },
}


def getTemplate(duration, numberOfNotes):
    if duration == 4.0:
        duration = "whole"
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