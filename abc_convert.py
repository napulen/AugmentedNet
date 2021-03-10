import subprocess
import os
from common import ANNOTATIONSCOREMAP

museScoreBinary = "musescore-portable"

for score in ANNOTATIONSCOREMAP.values():
    folder = os.path.dirname(os.path.realpath(score))
    root, extension = os.path.splitext(score)
    if extension in [".mscz", ".mscx"]:
        destination = f"{root}.mxl"
        subprocess.run([museScoreBinary, score, "-o", destination])
