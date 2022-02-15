import sys

sys.path.insert(0, "..")

from AugmentedNet.chord_vocabulary import frompcset
from AugmentedNet.feature_representation import KEYS
from AugmentedNet.cache import forceTonicization, getTonicizationScaleDegree

for pcs in frompcset:
    print(f"Chord {pcs} is called...")
    for key in KEYS:
        if key in frompcset[pcs]:
            rn = frompcset[pcs][key]["rn"]
            print(f"\t{key}:{rn} ---- diatonic")
        else:
            # Find a new tonicizedKey
            candidateKeys = list(frompcset[pcs].keys())
            tonicizedKey = forceTonicization(key, candidateKeys)
            numerator = frompcset[pcs][tonicizedKey]["rn"]
            rn = numerator
            if tonicizedKey != key:
                denominator = getTonicizationScaleDegree(key, tonicizedKey)
                rn += f"/{denominator}"
            print(f"\t{key}:{rn}")
