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
)
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

tf.random.set_seed(RANDOMSEED)

import os

# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
gpu_devices = tf.config.experimental.list_physical_devices("GPU")
for device in gpu_devices:
    tf.config.experimental.set_memory_growth(device, True)


def plotExample(pr, label):
    _, ax = plt.subplots(2, 1)
    sns.heatmap(pr.T, ax=ax[0])
    ax[0].invert_yaxis()
    sns.heatmap(label.T, ax=ax[1])
    ax[1].invert_yaxis()
    plt.show()


def manyhot_accuracy(y_true, y_pred):
    zero = tf.constant(0.0)
    nonzero = tf.not_equal(y_true, zero)
    manyhot_indices = tf.where(nonzero)
    manyhot_preds = tf.gather(y_pred, manyhot_indices)
    correct_preds = tf.math.reduce_sum(tf.cast(manyhot_preds > 0.5, tf.int32))
    return correct_preds / manyhot_preds.shape[0]


def train(synthetic=False):
    # datasetFile = SYNTHDATASETDIR if synthetic else DATASETDIR
    dataset = np.load(f"dataset.npy", allow_pickle=True).item()
    datasetDa = np.load("dataset-synth.npy", allow_pickle=True).item()
    X_train, y_train = dataset["training"]["X"], dataset["training"]["y"]
    X_val, y_val = dataset["validation"]["X"], dataset["validation"]["y"]
    X_test, y_test = dataset["test"]["X"], dataset["test"]["y"]

    Xda_train, yda_train = datasetDa["training"]["X"], datasetDa["training"]["y"]
    X_train, y_train = np.concatenate((X_train, Xda_train)), np.concatenate((y_train, yda_train))

    model = keras.Sequential(
        [
            keras.Input(shape=(SEQUENCELENGTH, X_train.shape[2])),
            layers.Dense(32),
            layers.BatchNormalization(),
            layers.Dense(32),
            layers.BatchNormalization(),
            layers.Bidirectional(layers.GRU(20, return_sequences=True)),
            layers.BatchNormalization(),
            layers.Bidirectional(layers.GRU(20, return_sequences=True)),
            layers.BatchNormalization(),
            layers.Dense(4),
        ]
    )
    model.compile(
        optimizer="rmsprop",
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics="accuracy",
    )
    y_train = np.argmax(y_train, axis=2).reshape(-1, SEQUENCELENGTH, 1)
    y_val = np.argmax(y_val, axis=2).reshape(-1, SEQUENCELENGTH, 1)
    print(model.summary())
    model.fit(
        X_train,
        y_train,
        epochs=50,
        shuffle=True,
        batch_size=BATCHSIZE,
        validation_data=(X_val, y_val),
    )

    # tl = keras.Sequential([
    #     keras.Input(shape=(SEQUENCELENGTH, train_x.shape[2])),
    #     model,
    #     # layers.GRU(20, return_sequences=True),
    #     layers.Dense(train_y.shape[2])
    # ])
    # model.trainable = False
    # tl.compile(
    #     optimizer="adam",
    #     loss=keras.losses.CategoricalCrossentropy(from_logits=True),
    #     metrics="categorical_accuracy",
    # )
    # tl.fit(
    #     train_x_real,
    #     train_y_real,
    #     epochs=1000,
    #     batch_size=BATCHSIZE,
    #     validation_data=(val_x, val_y)
    # )


if __name__ == "__main__":
    train(synthetic=True)