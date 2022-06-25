from . import abc_dcml, bps, haydnsun, mps, tavern, wir, wirwtc

available_collections = {
    "abc": abc_dcml,
    "bps": bps,
    "haydnsun": haydnsun,
    "mps": mps,
    "tavern": tavern,
    "wir": wir,
    "wirwtc": wirwtc,
}


def getAnnotationScoreDataset(collections=[]):
    """Return the available (annotation, score) pairs in the dataset."""
    allCollections = list(available_collections.keys())
    collections = collections or allCollections
    duples = {}
    splits = {"training": [], "validation": [], "test": []}
    for collection in collections:
        if collection not in allCollections:
            raise KeyError()
        module = available_collections[collection]
        duples.update(module.annotation_score_duples)
        for split in splits:
            splits[split].extend(module.splits[split])
    return duples, splits
