from tensorflow.python.eager.context import disable_graph_collection
from tensorflow.python.keras.layers.normalization import BatchNormalization
from score_parser import parseScore
from annotation_parser import parseAnnotation
from args import (
    SEQUENCELENGTH,
    BATCHSIZE,
    RANDOMSEED,
    INPUT_REPRESENTATION,
    OUTPUT_REPRESENTATION,
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
import args
from argparse import ArgumentParser

tf.random.set_seed(RANDOMSEED)

import mlflow
import mlflow.tensorflow


class InputOutput(object):
    def __init__(self, name, array):
        self.name = name
        self.array = array


def tensorflowGPUHack():
    # https://github.com/tensorflow/tensorflow/issues/37942
    gpu_devices = tf.config.experimental.list_physical_devices("GPU")
    for device in gpu_devices:
        tf.config.experimental.set_memory_growth(device, True)


def disableGPU():
    # Disabling the GPU
    import os

    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def train():
    dataset = np.load(f"dataset.npz")
    training = {f: dataset[f] for f in dataset.files if "training" in f}
    X_train = [InputOutput(x, arr) for x, arr in training.items() if "X" in x]
    y_train = [InputOutput(y, arr) for y, arr in training.items() if "y" in y]

    model = models.simpleGRU(X_train, y_train)
    model.compile(
        optimizer="adam",
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )

    for y in y_train:
        y.array = np.argmax(y.array, axis=2).reshape(-1, SEQUENCELENGTH, 1)

    print(model.summary())
    model.fit(
        [xi.array for xi in X_train],
        [yi.array for yi in y_train],
        epochs=EPOCHS,
        shuffle=True,
        batch_size=BATCHSIZE,
        # validation_data=(X_val, y_val),
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
    args = parser.parse_args()

    if args.nogpu:
        disableGPU()
    else:
        # Ideally, this shouldn't be necessary; but this is not an ideal world
        tensorflowGPUHack()

    mlflow.tensorflow.autolog()

    train()