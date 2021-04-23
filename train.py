from tensorflow.python.eager.context import disable_graph_collection
from tensorflow.python.keras.layers.normalization import BatchNormalization
from score_parser import parseScore
from annotation_parser import parseAnnotation
from common import (
    SEQUENCELENGTH,
    BATCHSIZE,
    RANDOMSEED,
    INPUT_REPRESENTATION,
    OUTPUT_REPRESENTATION,
    DATASETDIR,
    SYNTHDATASETDIR,
    EPOCHS,
)
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import models
import args

tf.random.set_seed(RANDOMSEED)

import mlflow
import mlflow.tensorflow


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
    dataset = np.load(f"dataset.npy", allow_pickle=True).item()
    datasetDa = np.load("dataset-synth.npy", allow_pickle=True).item()
    X_train, y_train = dataset["training"]["X"], dataset["training"]["y"]
    X_val, y_val = dataset["validation"]["X"], dataset["validation"]["y"]
    X_test, y_test = dataset["test"]["X"], dataset["test"]["y"]

    Xda_train, yda_train = (
        datasetDa["training"]["X"],
        datasetDa["training"]["y"],
    )
    outputClasses = y_train.shape[2]
    # X_train, y_train = np.concatenate((X_train, Xda_train)), np.concatenate(
    #     (y_train, yda_train)
    # )

    model = models.simpleGRU(X_train.shape[2], y_train.shape[2])
    model.compile(
        optimizer="adam",
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )

    y_train = np.argmax(y_train, axis=2).reshape(-1, SEQUENCELENGTH, 1)
    yda_train = np.argmax(yda_train, axis=2).reshape(-1, SEQUENCELENGTH, 1)
    y_val = np.argmax(y_val, axis=2).reshape(-1, SEQUENCELENGTH, 1)

    print(model.summary())
    model.fit(
        X_train,
        y_train,
        epochs=EPOCHS,
        shuffle=True,
        batch_size=BATCHSIZE,
        validation_data=(X_val, y_val),
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
    parser = ArgumentParser(
        description="Train the AugmentedNet."
    )
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