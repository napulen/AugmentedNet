import music21
import re
from common import ANNOTATIONSCOREMAP


def _isInitialKey(token):
    return re.match(r"\.[a-gA-G][b#]*\.[b#]*[ivIV]+", token)


def _isKeyChange(token):
    return re.match(r"[.]?[b#]*[ivIV]+\.[b#]*[ivIV]+", token)


def _isHalfDiminishedSeventh(token):
    return "%" in token


def _isPhraseEnding(token):
    return "\\" in token


def _isCadenceEnding(token):
    return "\\\\" in token


def _isCad64(token):
    return token == "V(64)"


def _hasSquareBracket(token):
    return "[" in token or "]" in token


def _hasAddedIntervals(token):
    return re.match(".*\(.*\).*", token)


def _isAugmentedSixth(token):
    return [aug6 for aug6 in ["Ger", "It", "Fr"] if aug6 in token]


def _isDiminishedSeventh(token):
    return "#viio" in token


def _processABCToken(token, globalKey):
    key = None
    figure = token
    if _isInitialKey(figure):
        _, keyStr, figure = figure.split(".")
        key = music21.key.Key(keyStr).tonicPitchNameWithCase
    if _isKeyChange(figure):
        keyChange = figure.split(".")
        if len(keyChange) == 3:
            _, keyStr, figure = keyChange
        elif len(keyChange) == 2:
            keyStr, figure = keyChange
        key = music21.roman.RomanNumeral(keyStr, globalKey).root().name
        if keyStr.islower():
            key = key.lower()
    if _isHalfDiminishedSeventh(figure):
        figure = figure.replace("%", "ø")
    if _isCadenceEnding(figure):
        figure = figure.replace("\\\\", "")
    if _isPhraseEnding(figure):
        figure = figure.replace("\\", "")
    if _isCad64(figure):
        figure = "Cad64"
    if _hasSquareBracket(figure):
        figure = figure.replace("]", "").split("[")[0]
    if _hasAddedIntervals(figure):
        figure = re.sub(r"\(.*\)", "", figure)
    if _isAugmentedSixth(figure):
        figure = figure[1:]
        figure = figure.replace("Ger6", "Ger65")
        figure = figure.replace("Fr6", "Fr65")
    if _isDiminishedSeventh(figure):
        figure = figure.replace("#", "")
    if key:
        key = key.replace("-", "b")
    return figure, key


def _measureDict(m21Score):
    tss = {}
    ms = {}
    globalKey = None
    for harm in m21Score.flat.getElementsByClass("Harmony"):
        m = harm.measureNumber
        b = round(float(harm.beat), 2)
        b = int(b) if b.is_integer() else b
        annotation = harm.chordKindStr
        if annotation == "@none":
            continue
        if m not in ms:
            ms[m] = {}
        # print(annotation)
        figure, key = _processABCToken(annotation, globalKey)
        if key and not globalKey:
            globalKey = key
        if b not in ms[m]:
            ms[m][b] = (key, figure)
        else:
            print(f"Collission! m{m} b{b}")
        # if key:
        #     print(f"{annotation} -> {key}:{figure}")
        # else:
        #     print(f"{annotation} -> {figure}")
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
    header += f"Analyst: Neuwirth et al. ABC dataset. See https://github.com/DCMLab/ABC\n"
    header += f"Proofreader: Automated translation by Néstor Nápoles López\n"
    return header


def makeRntxtBody(tss, ms):
    body = ""
    allMeasures = list(sorted(set(list(tss.keys()) + list(ms.keys()))))
    for m in allMeasures:
        if m in tss:
            body += f"\nTime Signature: {tss[m]}\n\n"
        if m in ms:
            line = f"m{m} "
            for b, (key, rn) in ms[m].items():
                beat = f"b{b} " if b != 1 else ""
                if key:
                    key = key.replace("-", "b")
                    line += f"{beat}{key}: {rn} "
                else:
                    line += f"{beat}{rn} "
            if re.match(r"m(\d)+ $", line):
                continue
            body += line[:-1] + "\n"
    return body


if __name__ == "__main__":
    for annotation, score in ANNOTATIONSCOREMAP.items():
        # if "Quartets/Beethoven" not in annotation:
        if "Quartets/Beethoven" not in annotation:
            continue
        score = score.replace(".mscx", ".mxl")
        print(score)
        harm = music21.converter.parse(score)
        tss, ms = _measureDict(harm)
        rntxtHeader = makeRntxtHeader(harm.metadata)
        rntxtBody = makeRntxtBody(tss, ms)
        out = score.replace(".mxl", ".rntxt")
        with open(out, "w") as fd:
            fd.write(rntxtHeader)
            fd.write(rntxtBody)