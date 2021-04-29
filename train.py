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
from mlflow import log_metric, log_param, log_artifacts
from tensorflow.python.keras.callbacks import EarlyStopping, ModelCheckpoint


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


def printTrainingExample(x, y):
    import pandas as pd

    pd.set_option("display.max_rows", 640)
    ret = {}
    for xi in x:
        representationName = xi.name.split("_")[-1]
        decoded = availableInputs[representationName].decode(xi.array[0])
        ret[representationName] = decoded
    for yi in y:
        representationName = yi.name.split("_")[-1]
        decoded = availableOutputs[representationName].decode(yi.array[0])
        ret[representationName] = decoded
    df = pd.DataFrame(ret)
    print(df)


def train(
    syntheticDataStrategy=None,
    modelName="simpleGRU",
    monitoredMetric="val_training_y_LocalKey35_accuracy",
):
    if not syntheticDataStrategy:
        (X_train, y_train), (X_val, y_val), (_, _) = loadData(synthetic=False)
    elif syntheticDataStrategy == "syntheticOnly":
        (X_train, y_train), (X_val, y_val), (_, _) = loadData(synthetic=True)
    elif syntheticDataStrategy == "concatenate":
        (X_train, y_train), (X_val, y_val), (_, _) = loadData(synthetic=False)
        (Xs_train, ys_train), (_, _), (_, _) = loadData(synthetic=True)
        for x, xs in zip(X_train, Xs_train):
            x.array = np.concatenate((x.array, xs.array))
        for y, ys in zip(y_train, ys_train):
            y.array = np.concatenate((y.array, ys.array))
    elif syntheticDataStrategy == "transfer":
        (X_train, y_train), (X_val, y_val), (_, _) = loadData(synthetic=True)
        (Xtr_train, ytr_train), (Xtr_val, ytr_val), (_, _) = loadData(
            synthetic=False
        )

    printTrainingExample(X_train, y_train)

    model = models.available_models[modelName](X_train, y_train)

    model.compile(
        optimizer="adam",
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics="accuracy",
    )

    for yt, yv in zip(y_train, y_val):
        yt.array = np.argmax(yt.array, axis=2).reshape(-1, SEQUENCELENGTH, 1)
        yv.array = np.argmax(yv.array, axis=2).reshape(-1, SEQUENCELENGTH, 1)
        if modelName in ["micchi2020", "modifiedMicchi2020"]:
            yt.array = yt.array[:, ::4]
            yv.array = yv.array[:, ::4]

    print(model.summary())
    x = [xi.array for xi in X_train]
    y = [yi.array for yi in y_train]
    x = x if len(x) > 1 else x[0]
    y = y if len(y) > 1 else y[0]
    xv = [xi.array for xi in X_val]
    yv = [yi.array for yi in y_val]
    xv = xv if len(xv) > 1 else xv[0]
    yv = yv if len(yv) > 1 else yv[0]

    model.fit(
        x,
        y,
        epochs=EPOCHS,
        shuffle=True,
        batch_size=BATCHSIZE,
        validation_data=(
            xv,
            yv,
        ),
        callbacks=[
            EarlyStopping(
                monitor=monitoredMetric, patience=3
            ),
            ModelCheckpoint(
                "weights.{epoch:02d}-{val_loss:.2f}.hdf5",
                monitor=monitoredMetric,
                save_best_only=True,
            ),
        ],
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
        "--syntheticDataStrategy",
        choices=["syntheticOnly", "concatenate", "transfer"],
        default=globalArgs.SYNTHETICDATASTRATEGY,
        help="The strategy to use for synthetic training examples (if any).",
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
    parser.add_argument(
        "--model",
        default=globalArgs.MODEL,
        choices=list(models.available_models.keys()),
    )
    parser.add_argument(
        "--scrutinize_data",
        action="store_true",
        default=globalArgs.SCRUTINIZEDATA,
    )
    parser.add_argument(
        "--monitored_metric",
        type=str,
        default=globalArgs.MONITOREDMETRIC,
        help="Metric observed by EarlyStopping and ModelCheckpoint.",
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
            scrutinizeData=args.scrutinize_data,
        )
        log_artifacts(DATASETDIR, artifact_path="dataset")
    if args.syntheticDataStrategy:
        if args.generateData or not os.path.isfile(SYNTHDATASETDIR + ".npz"):
            generateDataset(
                synthetic=True,
                dataAugmentation=args.dataAugmentation,
                collection=args.collection,
                inputRepresentations=args.input_representations,
                outputRepresentations=args.output_representations,
                sequenceLength=args.sequence_length,
                scrutinizeData=args.scrutinize_data,
            )
            log_artifacts(SYNTHDATASETDIR, artifact_path="dataset-synth")

    mlflow.tensorflow.autolog()
    log_param("inputs", args.input_representations)
    log_param("outputs", args.output_representations)
    log_param("model", args.model)
    log_param("syntheticDataStrategy", args.syntheticDataStrategy)
    log_param("scrutinize_data", args.scrutinize_data)
    log_param("sequenceLength", args.sequence_length)
    log_param("monitoredMetric", args.monitored_metric)

    train(
        syntheticDataStrategy=args.syntheticDataStrategy,
        modelName=args.model,
        monitoredMetric=args.monitored_metric,
    )
