from tensorflow.python.eager.context import disable_graph_collection
from tensorflow.python.keras.layers.normalization import BatchNormalization
from score_parser import parseScore
from annotation_parser import parseAnnotation
from args import (
    SEQUENCELENGTH,
    BATCHSIZE,
    RANDOMSEED,
    INPUT_REPRESENTATIONS,
    OUTPUT_REPRESENTATIONS,
    EPOCHS,
)
from common import DATASETDIR, SYNTHDATASETDIR
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import models
import args as globalArgs
from argparse import ArgumentParser
import os
from dataset_pkl_generator import generateDataset
from input_representations import available_representations as availableInputs
from output_representations import (
    available_representations as availableOutputs,
)

tf.random.set_seed(RANDOMSEED)

import mlflow
import mlflow.tensorflow


class InputOutput(object):
    def __init__(self, name, array):
        self.name = name
        self.array = array

    def __str__(self):
        return f"{self.name} {self.array.shape}"

    def __repr__(self):
        return str(self)


def tensorflowGPUHack():
    # https://github.com/tensorflow/tensorflow/issues/37942
    gpu_devices = tf.config.experimental.list_physical_devices("GPU")
    for device in gpu_devices:
        tf.config.experimental.set_memory_growth(device, True)


def disableGPU():
    # Disabling the GPU
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def loadData(synthetic=False):
    datasetFile = f"{SYNTHDATASETDIR if synthetic else DATASETDIR}.npz"
    dataset = np.load(datasetFile)
    X_train, y_train = [], []
    X_val, y_val = [], []
    X_test, y_test = [], []
    for name in dataset.files:
        array = dataset[name]
        if "training_X" in name:
            X_train.append(InputOutput(name, array))
        elif "training_y" in name:
            y_train.append(InputOutput(name, array))
        elif "validation_X" in name:
            X_val.append(InputOutput(name, array))
        elif "validation_y" in name:
            y_val.append(InputOutput(name, array))
        elif "test_X" in name:
            X_test.append(InputOutput(name, array))
        elif "test_y" in name:
            y_test.append(InputOutput(name, array))
    return (X_train, y_train), (X_val, y_val), (X_test, y_test)


def train(synthetic=False):
    (X_train, y_train), (X_val, y_val), (_, _) = loadData(synthetic=False)
    if synthetic:
        (Xs_train, ys_train), (Xs_val, ys_val), (_, _) = loadData(
            synthetic=True
        )

    model = models.simpleGRU(X_train, y_train)
    model.compile(
        optimizer="adam",
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics="accuracy",
    )

    for yt, yv in zip(y_train, y_val):
        yt.array = np.argmax(yt.array, axis=2).reshape(-1, SEQUENCELENGTH, 1)
        yv.array = np.argmax(yv.array, axis=2).reshape(-1, SEQUENCELENGTH, 1)

    print(model.summary())
    model.fit(
        [xi.array for xi in X_train],
        y_train[0].array,
        epochs=EPOCHS,
        shuffle=True,
        batch_size=BATCHSIZE,
        validation_data=(
            [xi.array for xi in X_val],
            y_val[0].array,
        ),
    )

    # tl = keras.Sequential([
    #     keras.Input(shape=(SEQUENCELENGTH, X_train.shape[2])),
    #     model,
    #     layers.Dense(32),
    #     layers.Dense(y_train.shape[2])
    # ])

    # model.trainable = False

    # tl.compile(
    #     optimizer="adam",
    #     loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    #     metrics=["accuracy"],
    # )
    # tl.fit(
    #     X_train,
    #     y_train,
    #     epochs=EPOCHS,
    #     batch_size=BATCHSIZE,
    #     validation_data=(X_val, y_val)
    # )


if __name__ == "__main__":
    parser = ArgumentParser(description="Train the AugmentedNet.")
    parser.add_argument(
        "--nogpu",
        action="store_true",
        help="Disable the use of any GPU.",
    )
    parser.add_argument(
        "--generateData",
        action="store_true",
        default=globalArgs.GENERATE_DATA,
        help="Generate the numpy dataset, even if it exists.",
    )
    parser.add_argument(
        "--synthetic",
        action="store_true",
        default=globalArgs.SYNTHETIC,
        help="Use (and generate) the dataset of synthetic examples.",
    )
    parser.add_argument(
        "--dataAugmentation",
        action="store_true",
        default=globalArgs.DATAAUGMENTATION,
        help="If generating the numpy arrays, whether to do data augmentation.",
    )
    parser.add_argument(
        "--collection",
        choices=["abc", "bps", "haydnop20", "wir", "tavern"],
        default=globalArgs.COLLECTION,
        help="Include files from a specific corpus/collection.",
    )
    parser.add_argument(
        "--input_representations",
        nargs="+",
        default=globalArgs.INPUT_REPRESENTATIONS,
        choices=list(availableInputs.keys()),
    )
    parser.add_argument(
        "--output_representations",
        nargs="+",
        default=globalArgs.OUTPUT_REPRESENTATIONS,
        choices=list(availableOutputs.keys()),
    )
    parser.add_argument(
        "--sequence_length",
        type=int,
        default=globalArgs.SEQUENCELENGTH,
        choices=range(16, 128),
    )

    args = parser.parse_args()

    if args.nogpu:
        disableGPU()
    else:
        # Ideally, this shouldn't be necessary; but this is not an ideal world
        tensorflowGPUHack()

    if args.generateData or not os.path.isfile(DATASETDIR + ".npz"):
        generateDataset(
            synthetic=False,
            dataAugmentation=args.dataAugmentation,
            collection=args.collection,
            inputRepresentations=args.input_representations,
            outputRepresentations=args.output_representations,
            sequenceLength=args.sequence_length,
        )
    if args.synthetic:
        if args.generateData or not os.path.isfile(SYNTHDATASETDIR + ".npz"):
            generateDataset(
                synthetic=True,
                dataAugmentation=args.dataAugmentation,
                collection=args.collection,
                inputRepresentations=args.input_representations,
                outputRepresentations=args.output_representations,
                sequenceLength=args.sequence_length,
            )

    mlflow.tensorflow.autolog()

    train(synthetic=args.synthetic)