GENERATE_DATA = True
SYNTHETICDATASTRATEGY = "concatenate"
COLLECTIONS = ["bps"]
TESTCOLLECTIONS = ["bps"]
EPOCHS = 100
INPUT_REPRESENTATIONS = ["Bass19", "Chromagram19"]
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
MODEL = "AugmentedNet"
SCRUTINIZEDATA = False
TESTSETON = False
LR_BOUNDARIES = [40]
LR_VALUES = [0.01, 0.0001]