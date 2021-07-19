"""The argparse interfaces for the runnable scripts in AugmentedNet."""

import argparse
import json
import pathlib

from input_representations import available_representations as availableInputs
import models
from output_representations import (
    available_representations as availableOutputs,
)


class Defaults(object):
    _npz = {
        "synthetic": True,
        "dataAugmentation": True,
        "collections": ["bps"],
        "testCollections": ["bps"],
        "inputRepresentations": ["Bass19", "Chromagram19"],
        "outputRepresentations": [
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
        ],
        "sequenceLength": 640,
        "scrutinizeData": False,
        "testSetOn": False,
    }

    _train = {
        "nogpu": False,
        "generateData": True,
        "syntheticDataStrategy": "concatenate",
        "model": "AugmentedNet",
        "lr_boundaries": [40],
        "lr_values": [0.01, 0.0001],
        "epochs": 10,
        "batchsize": 16,
    }

    @classmethod
    def import_json(cls, filename="defaults.json"):
        jsonPath = pathlib.Path(filename)
        if jsonPath.exists():
            cls.jsonDefaults = json.load(open(jsonPath))
        else:
            cls.jsonDefaults = dict()

    @classmethod
    def npz(cls):
        ret = cls._npz
        if not hasattr(cls, "jsonDefaults"):
            cls.import_json()
        ret.update(cls.jsonDefaults["npz_defaults"])
        return ret

    @classmethod
    def train(cls):
        ret = cls._train
        if not hasattr(cls, "jsonDefaults"):
            cls.import_json()
        ret.update(cls.jsonDefaults["train_defaults"])
        return ret


def npz(is_parent_parser=False):
    if is_parent_parser:
        parser = argparse.ArgumentParser(add_help=False)
    else:
        description = "Generate pkl files for every tsv training example."
        parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--synthetic",
        action="store_true",
        help="Search for a synthetic dataset, not one from real scores.",
    )
    parser.add_argument(
        "--dataAugmentation",
        action="store_true",
        help="Perform data augmentation on the training set.",
    )
    parser.add_argument(
        "--collections",
        choices=["abc", "bps", "haydnop20", "wir", "wirwtc", "tavern"],
        nargs="+",
        help="Include training files from a specific corpus/collection.",
    )
    parser.add_argument(
        "--testCollections",
        choices=["abc", "bps", "haydnop20", "wir", "wirwtc", "tavern"],
        nargs="+",
        help="Include test files from a specific corpus/collection.",
    )
    parser.add_argument(
        "--inputRepresentations",
        choices=list(availableInputs.keys()),
        nargs="+",
        help="The input representations to be used.",
    )
    parser.add_argument(
        "--outputRepresentations",
        choices=list(availableOutputs.keys()),
        nargs="+",
        help="The output representations to be used.",
    )
    parser.add_argument(
        "--sequenceLength",
        choices=range(64, 640),
        type=int,
        help="The number of frames in each input sequence.",
    )
    parser.add_argument(
        "--scrutinizeData",
        action="store_true",
        help="Exclude bad-quality annotations from the training data.",
    )
    parser.add_argument(
        "--testSetOn",
        action="store_true",
        help="Use the real test set, and add the validation set to training.",
    )
    parser.set_defaults(**Defaults.npz())
    return parser


def train():
    parent = npz(is_parent_parser=True)
    description = "Train the AugmentedNet."
    parser = argparse.ArgumentParser(parents=[parent], description=description)
    parser.add_argument(
        "experiment_name",
        choices=["testset", "validationset", "prototyping", "debug"],
        help="A short name for this experiment.",
    )
    parser.add_argument(
        "run_name", type=str, help="A name for this experiment run."
    )
    parser.add_argument(
        "--nogpu",
        action="store_true",
        help="Disable the use of any GPU.",
    )
    parser.add_argument(
        "--generateData",
        action="store_true",
        help="Generate the numpy dataset, even if it exists.",
    )
    parser.add_argument(
        "--syntheticDataStrategy",
        choices=["syntheticOnly", "concatenate"],
        help="The strategy to use for synthetic training examples (if any).",
    )
    parser.add_argument(
        "--model",
        choices=list(models.available_models.keys()),
        help="The neural network architecture to use.",
    )
    parser.add_argument(
        "--lr_boundaries",
        nargs="+",
        help="The piecewise learning rate boundary points (in epochs).",
    )
    parser.add_argument(
        "--lr_values",
        nargs="+",
        help="The piecewise learning rate values for different boundaries.",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        help="Number of training epochs.",
    )
    parser.add_argument(
        "--batchsize",
        type=int,
        help="Number of training examples per batch",
    )
    parser.set_defaults(**Defaults.train())
    return parser
