import numpy as np
import tensorflow as tf
from tensorflow import keras
from train import loadData
from input_representations import available_representations as availableInputs
from output_representations import (
    available_representations as availableOutputs,
)
import pandas as pd


def tensorflowGPUHack():
    # https://github.com/tensorflow/tensorflow/issues/37942
    gpu_devices = tf.config.experimental.list_physical_devices("GPU")
    for device in gpu_devices:
        tf.config.experimental.set_memory_growth(device, True)


def evaluate(modelHdf5, X_test, y_true):
    model = keras.models.load_model(modelHdf5)
    X = [xi.array for xi in X_test]
    X = X if len(X) > 1 else X[0]
    y_preds = model.predict(X)
    dfdict = {}
    features = []
    for y, ypred in zip(y_true, y_preds):
        name = y.name.replace("validation_y_", "")
        print(name)
        features.append(name)
        dfdict["true_" + name] = []
        dfdict["pred_" + name] = []
        for true, preds in zip(y.array, ypred):
            decodedTrue = availableOutputs[name].decode(true)
            dfdict["true_" + name].extend(decodedTrue)
            decodedPreds = availableOutputs[name].decode(preds)
            dfdict["pred_" + name].extend(decodedPreds)
    df = pd.DataFrame(dfdict)
    for feature in features:
        df[feature] = df["true_" + feature] == df["pred_" + feature]
        print(f"{feature}: {df[feature].mean().round(3)}")
    # Some custom features
    df["Degree"] = df.PrimaryDegree22 & df.SecondaryDegree22
    df["RomanNumeral"] = (
        df.LocalKey35
        & df.ChordQuality15
        & df.ChordRoot35
        & df.Inversion4
        & df.Degree
    )
    print(f"Degree: {df.Degree.mean().round(3)}")
    print(f"RomanNumeral: {df.RomanNumeral.mean().round(3)}")
    df.to_csv("results.csv")


if __name__ == "__main__":
    tensorflowGPUHack()
    (_, _), (X_test, y_test) = loadData(synthetic=False)
    evaluate(".model_checkpoint/testset/bps-47-3.81.hdf5", X_test, y_test)