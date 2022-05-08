from multiprocessing import Pool
import subprocess

from AugmentedNet.common import ANNOTATIONSCOREDUPLES

sonic_annotator = "/home/napulen/sonic-annotator-1.6-linux64-static/sonic-annotator"
nnlschroma = "/home/napulen/sonic-annotator-1.6-linux64-static/nnls_bothchroma.n3"

def chroma(wav):
    subprocess.run([sonic_annotator, "-t", nnlschroma, wav, "-w", "csv"])

if __name__ == "__main__":
    files = []
    for nick, (a, s) in ANNOTATIONSCOREDUPLES.items():
        wav = s.replace(".mxl", ".wav").replace(".krn", ".wav")
        files.append(wav)

    with Pool(6) as p:
        p.map(chroma, files)
