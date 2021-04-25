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
import os
from dataset_pkl_generator import generateDataset

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

def train():
    (X_train, y_train), (X_val, y_val), (_, _) = loadData()

    model = models.simpleGRU(X_train, y_train)
    model.compile(
        optimizer="adam",
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )

    for yt, yv in zip(y_train, y_val):
        yt.array = np.argmax(yt.array, axis=2).reshape(-1, SEQUENCELENGTH, 1)
        yv.array = np.argmax(yv.array, axis=2).reshape(-1, SEQUENCELENGTH, 1)

    print(model.summary())
    model.fit(
        [xi.array for xi in X_train],
        [yi.array for yi in y_train],
        epochs=EPOCHS,
        shuffle=True,
        batch_size=BATCHSIZE,
        validation_data=(
            [xi.array for xi in X_val],
            [yi.array for yi in y_val],
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
    args = parser.parse_args()

    if args.nogpu:
        disableGPU()
    else:
        # Ideally, this shouldn't be necessary; but this is not an ideal world
        tensorflowGPUHack()

    mlflow.tensorflow.autolog()

    train()