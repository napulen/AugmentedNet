from multiprocessing import Pool
import subprocess
from AugmentedNet.common import ANNOTATIONSCOREDUPLES

musescore_bin = "/mnt/c/Program Files/MuseScore 3/bin/MuseScore3.exe"

def mscore(inout):
    print(inout)
    inn, out = inout
    subprocess.run([musescore_bin, inn, "-o", out])
    

files = []
for nick, (a, s) in ANNOTATIONSCOREDUPLES.items():
    print(nick, s)
    if not nick.startswith("haydnop20"):
        continue
    if s.endswith(".krn"):
        inn = s.replace(".mxl", ".musicxml").replace(".krn", ".musicxml")
        out = s.replace(".mxl", ".wav").replace(".krn", ".wav")
        files.append((inn, out))

with Pool(6) as p:
    p.map(mscore, files)
