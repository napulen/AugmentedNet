import music21
import re
from common import ANNOTATIONSCOREMAP


def _measureDict(m21Score):
    tss = {}
    ms = {}
    for rn in m21Score.flat.getElementsByClass("RomanNumeral"):
        m = rn.measureNumber
        b = round(float(rn.beat), 2)
        b = int(b) if b.is_integer() else b
        if m not in ms:
            ms[m] = []
        key = rn.key.tonicPitchNameWithCase
        figure = rn.figure
        if (b, key, figure) not in ms[m]:
            ms[m].append((b, key, figure))
    for ts in m21Score.flat.getElementsByClass("TimeSignature"):
        m = ts.measureNumber
        tss[m] = ts.ratioString
    return tss, ms


def makeRntxtHeader(metadata):
    composer = metadata.composer
    title = metadata.title
    movementNumber = metadata.movementNumber
    movementName = metadata.movementName
    header = f"Composer: {composer}\n"
    header += f"Title: {title} - {movementNumber}: {movementName}\n"
    header += f"Analyst: Néstor Nápoles López, https://doi.org/10.5281/zenodo.1095617\n"
    header += f"Proofreader: Automated translation from **harm to RomanText\n"
    return header


def makeRntxtBody(tss, ms):
    body = ""
    allMeasures = list(sorted(set(list(tss.keys()) + list(ms.keys()))))
    currentKey = ""
    for m in allMeasures:
        if m in tss:
            body += f"\nTime Signature: {tss[m]}\n\n"
        if m in ms:
            line = f"m{m} "
            for b, key, rn in sorted(ms[m]):
                if rn == None:
                    continue
                beat = f"b{b} " if b != 1 else ""
                key = key.replace("-", "b")
                if key != currentKey:
                    currentKey = key
                    line += f"{beat}{currentKey}: {rn} "
                else:
                    line += f"{beat}{rn} "
            if re.match(r"m(\d)+ $", line):
                continue
            body += line[:-1] + "\n"
    return body


if __name__ == "__main__":
    for annotation, score in ANNOTATIONSCOREMAP.items():
        if "Quartets/Haydn" not in annotation:
            continue
        score = score.replace(".krn", ".hrm")
        print(score)
        harm = music21.converter.parse(score, format="humdrum")
        tss, ms = _measureDict(harm)
        rntxtHeader = makeRntxtHeader(harm.metadata)
        rntxtBody = makeRntxtBody(tss, ms)
        out = score.replace(".hrm", ".rntxt")
        with open(annotation, "w") as fd:
            fd.write(rntxtHeader)
            fd.write(rntxtBody)