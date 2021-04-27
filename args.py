RANDOMSEED = 1337
GENERATE_DATA = True
SYNTHETICDATASTRATEGY = None
COLLECTION = "bps"
EPOCHS = 20
INPUT_REPRESENTATIONS = ["Bass19", "Chromagram19", "Intervals39"]
OUTPUT_REPRESENTATIONS = [
    "LocalKey35",
    "PrimaryDegree22",
    "SecondaryDegree22",
    "Inversion4",
    "ChordQuality15",
    "ChordRoot35",
]
SEQUENCELENGTH = 640
BATCHSIZE = 16
COLLECTION = "bps"
DATAAUGMENTATION = True
MODEL = "simpleGRU"
SCRUTINIZEDATA = True