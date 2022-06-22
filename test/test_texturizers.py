import unittest

from AugmentedNet.texturizers import (
    available_number_of_notes,
    available_templates,
    available_durations,
    applyTextureTemplate,
    _getRelevantTemplates,
)


basssplit_whole_triad = """\
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,2.0,,['C4'],[],[True]
2.0,2.0,,"['E-4', 'G-4']",['m3'],"[True, True]"
"""

basssplit_quarter_seventh = """\
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,0.5,,['C4'],[],[True]
0.5,0.5,,"['E-4', 'G-4', 'B--4']","['m3', 'd5']","[True, True, True]"
"""

alberti_half_triad = """\
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,0.5,,['C4'],[],[True]
0.5,0.5,,['G-4'],[],[True]
1.0,0.5,,['E-4'],[],[True]
1.5,0.5,,['G-4'],[],[True]
"""

alberti_whole_seventh = """\
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,1.0,,['C4'],[],[True]
1.0,1.0,,['B--4'],[],[True]
2.0,1.0,,['E-4'],[],[True]
3.0,1.0,,['G-4'],[],[True]
"""

syncopation_whole_triad = """\
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,1.0,,['G-4'],[],[True]
1.0,2.0,,['C4'],[],[True]
3.0,1.0,,['E-4'],[],[True]
"""

syncopation_half_seventh = """\
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,0.5,,['B--4'],[],[True]
0.5,1.0,,"['C4', 'E-4', 'G-4']","['m3', 'd5']","[True, True, True]"
1.5,0.5,,"['C4', 'E-4', 'G-4']","['m3', 'd5']","[True, True, True]"
"""

blockchord_quarter_triad = """\
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,1.0,,"['C4', 'E-4', 'G-4']","['m3', 'd5']","[True, True, True]"
"""

blockchord_half_seventh = """\
s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset
0.0,2.0,,"['C4', 'E-4', 'G-4', 'B--4']","['m3', 'd5', 'd7']","[True, True, True, True]"
"""


class TestTexturizers(unittest.TestCase):
    def test_available_number_of_notes(self):
        GT = [4, 3]
        self.assertEqual(available_number_of_notes, GT)

    def test_available_durations(self):
        GT = [4.0, 3.0, 2.0, 1.5, 1.0]
        self.assertEqual(available_durations, GT)

    def test_available_templates(self):
        GT = ["BassSplit", "Alberti", "Syncopation", "BlockChord"]
        self.assertEqual(list(available_templates.keys()), GT)

    def test_relevant_templates(self):
        templates1 = _getRelevantTemplates(4.0, 4)
        templates2 = _getRelevantTemplates(1.0, 4)
        self.assertEqual(len(templates1), 4)
        self.assertEqual(len(templates2), 3)

    def test_basssplit_whole_triad(self):
        GT = basssplit_whole_triad
        duration = 4.0
        notes = ["C4", "E-4", "G-4"]
        intervals = ["m3", "d5", "m3"]
        template = applyTextureTemplate(
            duration, notes, intervals, templateName="BassSplit"
        )
        self.assertEqual(template, GT)

    def test_basssplit_quarter_seventh(self):
        GT = basssplit_quarter_seventh
        duration = 1.0
        notes = ["C4", "E-4", "G-4", "B--4"]
        intervals = ["m3", "d5", "d7", "m3", "d5", "m3"]
        template = applyTextureTemplate(
            duration, notes, intervals, templateName="BassSplit"
        )
        self.assertEqual(template, GT)

    def test_alberti_half_triad(self):
        GT = alberti_half_triad
        duration = 2.0
        notes = ["C4", "E-4", "G-4"]
        intervals = ["m3", "d5", "m3"]
        template = applyTextureTemplate(
            duration, notes, intervals, templateName="Alberti"
        )
        self.assertEqual(template, GT)

    def test_alberti_whole_seventh(self):
        GT = alberti_whole_seventh
        duration = 4.0
        notes = ["C4", "E-4", "G-4", "B--4"]
        intervals = ["m3", "d5", "d7", "m3", "d5", "m3"]
        template = applyTextureTemplate(
            duration, notes, intervals, templateName="Alberti"
        )
        self.assertEqual(template, GT)

    def test_syncopation_whole_triad(self):
        GT = syncopation_whole_triad
        duration = 4.0
        notes = ["C4", "E-4", "G-4"]
        intervals = ["m3", "d5", "m3"]
        template = applyTextureTemplate(
            duration, notes, intervals, templateName="Syncopation"
        )
        self.assertEqual(template, GT)

    def test_syncopation_half_seventh(self):
        GT = syncopation_half_seventh
        duration = 2.0
        notes = ["C4", "E-4", "G-4", "B--4"]
        intervals = ["m3", "d5", "d7", "m3", "d5", "m3"]
        template = applyTextureTemplate(
            duration, notes, intervals, templateName="Syncopation"
        )
        self.assertEqual(template, GT)

    def test_blockchord_quarter_triad(self):
        GT = blockchord_quarter_triad
        duration = 1.0
        notes = ["C4", "E-4", "G-4"]
        intervals = ["m3", "d5", "m3"]
        template = applyTextureTemplate(
            duration, notes, intervals, templateName="BlockChord"
        )
        self.assertEqual(template, GT)

    def test_blockchord_half_seventh(self):
        GT = blockchord_half_seventh
        duration = 2.0
        notes = ["C4", "E-4", "G-4", "B--4"]
        intervals = ["m3", "d5", "d7", "m3", "d5", "m3"]
        template = applyTextureTemplate(
            duration, notes, intervals, templateName="BlockChord"
        )
        self.assertEqual(template, GT)


if __name__ == "__main__":
    unittest.main()
