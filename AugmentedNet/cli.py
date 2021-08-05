"""The argparse interfaces for the runnable scripts in AugmentedNet."""

from argparse import ArgumentParser

from . import models
from .dataset_npz_generator import __doc__ as npz_description
from .dataset_tsv_generator import __doc__ as tsv_description
from .train import __doc__ as train_description
from .input_representations import (
    available_representations as availableInputs,
)
from .output_representations import (
    available_representations as availableOutputs,
)


class DefaultArguments(object):
    base = {
        "tsvDir": "dataset",
    }
    tsv = {
        "synthesize": False,
        "texturize": False,
    }
    npz = {
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
        "npzOutput": "dataset",
    }
    train = {
        "nogpu": False,
        "generateData": True,
        "syntheticDataStrategy": None,
        "model": "AugmentedNet",
        "lr_boundaries": [40],
        "lr_values": [0.001, 0.001],
        "epochs": 100,
        "batchsize": 16,
    }


def _base(is_parent_parser=True):
    if is_parent_parser:
        parser = ArgumentParser(add_help=False)
    else:
        parser = ArgumentParser()
    parser.add_argument(
        "--tsvDir",
        type=str,
        help="A path to the directory where the tsvs will be located.",
    )
    parser.set_defaults(**DefaultArguments.base)
    return parser


def tsv():
    parents = [_base()]
    parser = ArgumentParser(description=tsv_description, parents=parents)
    parser.add_argument(
        "--synthesize",
        action="store_true",
        help="Instead of a real score, synthesize one from the RNA.",
    )
    parser.add_argument(
        "--texturize",
        action="store_true",
        help="If synthesizing a score, apply texturization to it.",
    )
    parser.set_defaults(**DefaultArguments.tsv)
    return parser


def npz(is_parent_parser=False):
    parents = [_base()]
    if is_parent_parser:
        parser = ArgumentParser(add_help=False, parents=parents)
    else:
        parser = ArgumentParser(description=npz_description, parents=parents)
    parser.add_argument(
        "--collections",
        choices=["abc", "bps", "haydnop20", "wir", "wirwtc", "tavern"],
        nargs="+",
        help="Include training files from a specific corpus/collection.",
    )
    parser.add_argument(
        "--dataAugmentation",
        action="store_true",
        help="Perform data augmentation on the training set.",
    )
    parser.add_argument(
        "--inputRepresentations",
        choices=list(availableInputs.keys()),
        nargs="+",
        help="The input representations to be used.",
    )
    parser.add_argument(
        "--npzOutput", type=str, help="The path of the output .npz file(s)."
    )
    parser.add_argument(
        "--outputRepresentations",
        choices=list(availableOutputs.keys()),
        nargs="+",
        help="The output representations to be used.",
    )
    parser.add_argument(
        "--scrutinizeData",
        action="store_true",
        help="Exclude bad-quality annotations from the training data.",
    )
    parser.add_argument(
        "--sequenceLength",
        choices=range(64, 640),
        type=int,
        help="The number of frames in each input sequence.",
    )
    parser.add_argument(
        "--synthetic",
        action="store_true",
        help="Search for a synthetic dataset, not one from real scores.",
    )
    parser.add_argument(
        "--testCollections",
        choices=["abc", "bps", "haydnop20", "wir", "wirwtc", "tavern"],
        nargs="+",
        help="Include test files from a specific corpus/collection.",
    )
    parser.add_argument(
        "--testSetOn",
        action="store_true",
        help="Use the real test set, and add the validation set to training.",
    )
    parser.set_defaults(**DefaultArguments.npz)
    return parser


def train():
    parents = [npz(is_parent_parser=True)]
    parser = ArgumentParser(description=train_description, parents=parents)
    parser.add_argument(
        "experiment_name",
        choices=["testset", "validationset", "prototyping", "debug"],
        help="A short name for this experiment.",
    )
    parser.add_argument(
        "run_name", type=str, help="A name for this experiment run."
    )
    parser.add_argument(
        "--batchsize",
        type=int,
        help="Number of training examples per batch",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        help="Number of training epochs.",
    )
    parser.add_argument(
        "--generateData",
        action="store_true",
        help="Generate the numpy dataset, even if it exists.",
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
        "--model",
        choices=list(models.available_models.keys()),
        help="The neural network architecture to use.",
    )
    parser.add_argument(
        "--nogpu",
        action="store_true",
        help="Disable the use of any GPU.",
    )
    parser.add_argument(
        "--syntheticDataStrategy",
        choices=["syntheticOnly", "concatenate"],
        help="The strategy to use for synthetic training examples (if any).",
    )
    parser.set_defaults(**DefaultArguments.train)
    return parser
