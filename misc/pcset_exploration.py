import json

import music21

from AugmentedNet.common import ANNOTATIONSCOREDUPLES


class PcSetNgram(object):
    def __init__(self, jsonfile="", max_pieces=10, transpose=True):
        self.ngrams = {}
        pieces = 0
        if jsonfile:
            with open(jsonfile) as fd:
                self.ngrams = json.loads(fd.read())
            return
        for _, (_, score) in ANNOTATIONSCOREDUPLES.items():
            pieces += 1
            if pieces > max_pieces:
                break
            print(score)
            s = music21.converter.parse(score)
            pcsets = [set(c.pitchClasses) for c in s.chordify().flat.notes]
            transpositions = range(1) if not transpose else range(12)
            for transp in transpositions:
                print(f"transp{transp}")
                previous = None
                for pcset in pcsets:
                    pcset = [(pc + transp) % 12 for pc in pcset]
                    ordered = str(tuple(sorted(pcset)))
                    if not previous:
                        previous = ordered
                    else:
                        if previous not in self.ngrams:
                            self.ngrams[previous] = {}
                        if ordered not in self.ngrams[previous]:
                            self.ngrams[previous][ordered] = 0
                        self.ngrams[previous][ordered] += 1
                        previous = ordered
        with open("data.json", "w") as fp:
            json.dump(self.ngrams, fp)

    def query(self, pcset, cardinalities=[]):
        if pcset not in self.ngrams:
            raise KeyError()
        if not cardinalities:
            cardinalities = list(range(13))
        resultsdict = self.ngrams[pcset]
        filteredresults = [
            (k, v)
            for k, v in resultsdict.items()
            if len(eval(k)) in cardinalities
        ]
        sortedresults = list(
            sorted(filteredresults, key=lambda t: t[1], reverse=True)
        )
        ngramstrength = sum([x[1] for x in sortedresults])
        print(f"from {pcset} (strength={ngramstrength}) to ->")
        for ngram, strength in sortedresults:
            deststrength = strength / ngramstrength
            if deststrength < 0.001:
                break
            print(f"\t{ngram} p={deststrength:.3f}")
        # print(sortedresults)


pcset_ngram = PcSetNgram("data.json", 500)

while True:
    # pcset_ngram.query("(0, 3, 6, 9)", [3])
    s = input("<query (e.g., 047)> [<cardinality (e.g., 3)>]+ --> ")
    sparsed = s.split()
    query, cardinalities = sparsed[0], sparsed[1:]
    cardinalities = [int(x) for x in cardinalities]
    encoding = "0123456789ab"
    querytransl = str(tuple([encoding.index(c) for c in query]))
    pcset_ngram.query(querytransl, cardinalities)
