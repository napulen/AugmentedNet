import music21
import argparse
from AugmentedNet.score_parser import parseScore

if __name__ == "__main__":
    f = "/mnt/c/Users/nesto/OneDrive/Desktop/langscoreonly-encoding.mxl"
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_musicxml", help="An input file to encode/sonify."
    )
    args = parser.parse_args([f])
    df = parseScore(args.input_musicxml)
    bassPart = music21.stream.Part()
    chromaPart = music21.stream.Part()
    for n in df.s_notes:
        bass = f"{n[0][:-1]}3"
        chroma = list(dict.fromkeys([f"{x[:-1]}4" for x in n]))
        bassPart.append(music21.note.Note(bass, quarterLength=0.125))
        chromaPart.append(music21.chord.Chord(chroma, quarterLength=0.125))
        print(bass, chroma)
    s = music21.stream.Stream([chromaPart, bassPart])
    s.show("text")
    s.show()