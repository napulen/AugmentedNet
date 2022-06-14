"""Common hardcoded variables throughout the code."""

from .data import available_collections

# Number of decimals to the right of the decimal point
FLOATSCALE = 4

# Sixteenth notes
FRAMEBASENOTE = 32
FIXEDOFFSET = round(4.0 / FRAMEBASENOTE, FLOATSCALE)

DATASETSUMMARYFILE = "dataset_summary.tsv"

ANNOTATIONSCOREDUPLES = {}
DATASPLITS = {"training": [], "validation": [], "test": []}

for module in available_collections.values():
    ANNOTATIONSCOREDUPLES.update(module.annotation_score_duples)
    for split in DATASPLITS:
        DATASPLITS[split].extend(module.splits[split])
