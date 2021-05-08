GENERATE_DATA = False
SYNTHETICDATASTRATEGY = "concatenate"
COLLECTIONS = ["bps"]
TESTCOLLECTIONS = ["bps"]
EPOCHS = 60
INPUT_REPRESENTATIONS = ["Bass35", "Chromagram35", "Intervals39"]
OUTPUT_REPRESENTATIONS = [
    "LocalKey35",
    "PrimaryDegree22",
    "SecondaryDegree22",
    "Inversion4",
    "ChordQuality15",
    "ChordRoot35",
    "Bass35",
    "RomanNumeral76",
    "TonicizedKey35",
    "PitchClassSet94",
    "HarmonicRhythm2",
]
SEQUENCELENGTH = 640
BATCHSIZE = 16
DATAAUGMENTATION = True
MODEL = "simpleGRU"
SCRUTINIZEDATA = False
TESTSETON = False