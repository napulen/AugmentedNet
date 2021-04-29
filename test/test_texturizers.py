import unittest
from texturizers import (
    available_number_of_notes,
    available_templates,
    available_durations,
    applyTextureTemplate,
)


class TestTexturizers(unittest.TestCase):
    def test_available_number_of_notes(self):
        GT = [3, 4]
        self.assertEqual(available_number_of_notes, GT)

    def test_available_durations(self):
        GT = [1.0, 2.0, 4.0]
        self.assertEqual(available_durations, GT)

    def test_available_templates(self):
        GT = ["BassSplit", "Alberti", "BlockChord"]
        self.assertEqual(list(available_templates.keys()), GT)


if __name__ == "__main__":
    unittest.main()