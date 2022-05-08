import subprocess

import music21

from AugmentedNet.common import ANNOTATIONSCOREDUPLES


if __name__ == "__main__":
    for nick, (a, s) in ANNOTATIONSCOREDUPLES.items():
        if not nick.startswith("haydnop20"):
            continue
        print(nick)
        musicxml = s.replace(".krn", ".musicxml")
        # subprocess.run(["python3", "-m", "converter21", "-f", "humdrum", "-t", "musicxml", s, musicxml])
        s21 = music21.converter.parse(s)
        s21.write(fp=musicxml, fmt="musicxml")