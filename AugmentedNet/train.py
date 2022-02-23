"""Train the AugmentedNet."""

import datetime
import gc
import math
from pathlib import Path
import os

import mlflow
import mlflow.tensorflow
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import optimizers
from tensorflow.keras import utils

from . import cli
from . import models
from .dataset_npz_generator import generateDataset
from .input_representations import (
    available_representations as availableInputs,
)
from .output_representations import (
    available_representations as availableOutputs,
)
from .utils import tensorflowGPUHack, disableGPU


class InputOutput(object):
    def __init__(self, name, array):
        self.name = name
        self.array = array
        if "y" in name:
            self.shortname = name.split("_")[-1]
            self.clas = availableOutputs[self.shortname]
            self.outputFeatures = self.clas.classesNumber()

    def __str__(self):
        return f"{self.name} {self.array.shape}"

    def __repr__(self):
        return str(self)


def _loadNpz(npzPath, synthetic=False):
    datasetFile = f"{npzPath}-synth.npz" if synthetic else f"{npzPath}.npz"
    dataset = np.load(datasetFile, mmap_mode="r")
    X_train, y_train = [], []
    X_test, y_test = [], []
    for name in dataset.files:
        array = dataset[name]
        if "training_X" in name:
            X_train.append(InputOutput(name, array))
        elif "training_y" in name:
            y_train.append(InputOutput(name, array))
        elif "validation_X" in name:
            X_test.append(InputOutput(name, array))
        elif "validation_y" in name:
            y_test.append(InputOutput(name, array))
    return (X_train, y_train), (X_test, y_test)


def loadData(npzPath, syntheticDataStrategy=None, modelName="AugmentedNet"):
    if not syntheticDataStrategy:
        (X_train, y_train), (X_test, y_test) = _loadNpz(
            npzPath, synthetic=False
        )
    elif syntheticDataStrategy == "syntheticOnly":
        (X_train, y_train), (X_test, y_test) = _loadNpz(
            npzPath, synthetic=True
        )
    elif syntheticDataStrategy == "concatenate":
        (X_train, y_train), (X_test, y_test) = _loadNpz(
            npzPath, synthetic=False
        )
        # Test portion of synthetic data is NEVER used in this case
        (Xs_train, ys_train), (_, _) = _loadNpz(npzPath, synthetic=True)
        for x, xs in zip(X_train, Xs_train):
            x.array = np.concatenate((x.array, xs.array))
        for y, ys in zip(y_train, ys_train):
            y.array = np.concatenate((y.array, ys.array))
    for yt, yv in zip(y_train, y_test):
        if modelName in ["Micchi2020"]:
            yt.array = yt.array[:, ::4]
            yv.array = yv.array[:, ::4]

    return (X_train, y_train), (X_test, y_test)


def printTrainingExample(x, y):
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


def findBestModel(checkpointPath=".model_checkpoint/"):
    models = [f for f in os.listdir(checkpointPath)]
    accuracies = [f.replace(".hdf5", "").split("-")[-1] for f in models]
    best = accuracies.index(max(accuracies))
    return models[best]


class ModdedModelCheckpoint(keras.callbacks.ModelCheckpoint):
    def on_epoch_end(self, epoch, logs={}):
        monitored = list(availableOutputs.keys())
        nonMonitored = [
            "ChordQuality11",
            "ChordRoot35",
            "Inversion4",
            "PrimaryDegree22",
            "RomanNumeral31",
            "SecondaryDegree22",
        ]
        monitored = [a for a in monitored if a not in nonMonitored]
        print(f"monitored_outputs: {monitored}")
        accuracies = [logs.get(f"val_{k}_accuracy", 0.0) for k in monitored]
        monitoredAcc = sum(accuracies) / len(monitored)
        losses = [logs.get(f"val_{k}_loss", 0.0) for k in monitored]
        monitoredLoss = sum(losses)
        print(f"monitored accuracy: {monitoredAcc}")
        print(f"monitored loss: {monitoredLoss}")
        logs["val_monitored_accuracy"] = monitoredAcc
        logs["val_monitored_loss"] = monitoredLoss
        super().on_epoch_end(epoch, logs=logs)


def evaluate(modelHdf5, X_test, y_true):
    model = keras.models.load_model(modelHdf5)
    X = [xi.array for xi in X_test]
    X = X if len(X) > 1 else X[0]
    y_preds = model.predict(X)
    dfdict = {}
    summary = {}
    features = []
    for y, ypred in zip(y_true, y_preds):
        name = y.name.replace("validation_y_", "")
        features.append(name)
        dfdict["true_" + name] = []
        dfdict["pred_" + name] = []
        for true, preds in zip(y.array, ypred):
            predsCategorical = np.argmax(preds, axis=1).reshape(-1, 1)
            decodedTrue = availableOutputs[name].decode(true)
            dfdict["true_" + name].extend(decodedTrue)
            decodedPreds = availableOutputs[name].decode(predsCategorical)
            dfdict["pred_" + name].extend(decodedPreds)
    df = pd.DataFrame(dfdict)
    for feature in features:
        df[feature] = df["true_" + feature] == df["pred_" + feature]
        summary[feature] = df[feature].mean().round(3)
        print(f"{feature}: {summary[feature]}")
    # Some custom features, all optional depending on outputs
    if "PrimaryDegree22" in df and "SecondaryDegree22" in df:
        df["Degree"] = df.PrimaryDegree22 & df.SecondaryDegree22
        summary["Degree"] = df.Degree.mean().round(3)
        print(f"Degree: {summary['Degree']}")
    if (
        "LocalKey35" in df
        and "ChordQuality11" in df
        and "ChordRoot35" in df
        and "Inversion4" in df
        and "Degree" in df
    ):
        df["RomanNumeral"] = (
            df.LocalKey35
            & df.ChordQuality11
            & df.ChordRoot35
            & df.Inversion4
            & df.Degree
        )
        summary["RomanNumeral"] = df.RomanNumeral.mean().round(3)
        print(f"RomanNumeral: {summary['RomanNumeral']}")
    # The alternative approach proposed in Napoles Lopez et al. (2021)
    if "RomanNumeral31" in df and "LocalKey35" in df and "Inversion4" in df:
        df["AltRomanNumeral"] = (
            df.RomanNumeral31 & df.LocalKey35 & df.Inversion4
        )
        summary["AltRomanNumeral"] = df.AltRomanNumeral.mean().round(3)
        print(f"AltRomanNumeral: {summary['AltRomanNumeral']}")
    # An alternative version in closed-form chord outputs
    if (
        "Bass35" in df
        and "Tenor35" in df
        and "Alto35" in df
        and "Soprano35" in df
        and "LocalKey35" in df
    ):
        df["satbRomanNumeral"] = (
            df.Bass35 & df.Tenor35 & df.Alto35 & df.Soprano35 & df.LocalKey35
        )
        summary["satbRomanNumeral"] = df.satbRomanNumeral.mean().round(3)
        print(f"satbRomanNumeral: {summary['satbRomanNumeral']}")
    outputPath = modelHdf5.replace(".model_checkpoint", ".results")
    outputPath = outputPath.replace(".hdf5", "")
    Path(outputPath).mkdir(parents=True, exist_ok=True)
    df.to_csv(f"{outputPath}/results.csv")
    with open(f"{outputPath}/summary.txt", "w") as fd:
        for task, score in summary.items():
            fd.write(f"{task}: {score}\n")
    return str(outputPath), summary


class CurriculumIterator(utils.Sequence):
    def __init__(self, x, y, batchsize, increaseperepoch=0.02):
        self.batchsize = batchsize
        self.realratio = 0.0
        self.increaseperepoch = increaseperepoch
        self.xreal = []
        self.xsynth = []
        for xi in x:
            _, seqlen, features = xi.shape
            xi = xi.reshape(2, -1, seqlen, features)
            self.xreal.append(xi[0])
            self.xsynth.append(xi[1])
        self.len = len(self.xreal[0])
        self.yreal = []
        self.ysynth = []
        for yi in y:
            _, seqlen, features = yi.shape
            yi = yi.reshape(2, -1, seqlen, features)
            self.yreal.append(yi[0])
            self.ysynth.append(yi[1])
        self.set_curriculum()

    def set_curriculum(self):
        realratio = min(self.realratio, 1.0)
        lensynth = int(self.len * (1.0 - realratio))
        lenreal = int(self.len * realratio)
        idxsynth = np.random.choice(self.len, lensynth, replace=False)
        idxreal = np.random.choice(self.len, lenreal, replace=False)
        x = [np.zeros(xi.shape) for xi in self.xreal]
        y = [np.zeros(yi.shape) for yi in self.yreal]
        for idx, inp in enumerate(self.xsynth):
            x[idx][:lensynth] = np.take(inp, idxsynth, axis=0)
        for idx, inp in enumerate(self.xreal):
            x[idx][lensynth : lensynth + lenreal] = np.take(inp, idxreal, axis=0)
        for idx, out in enumerate(self.ysynth):
            y[idx][:lensynth] = np.take(out, idxsynth, axis=0)
        for idx, out in enumerate(self.yreal):
            y[idx][lensynth : lensynth + lenreal] = np.take(out, idxreal, axis=0)
        self.x = x
        self.y = y
        return

    def __len__(self):
        return math.ceil(self.len / self.batchsize)

    def __getitem__(self, idx):
        batch_x = []
        batch_y = []
        for xi in self.x:
            batch_x.append(
                xi[idx * self.batchsize : (idx + 1) * self.batchsize]
            )
        for yi in self.y:
            batch_y.append(
                yi[idx * self.batchsize : (idx + 1) * self.batchsize]
            )
        return batch_x, batch_y

    def on_epoch_end(self):
        self.realratio += self.increaseperepoch
        print(f"Curriculum learning: {self.realratio*100.0}% real examples")
        self.set_curriculum()


def train(
    X_train,
    y_train,
    X_test,
    y_test,
    modelName="AugmentedNet",
    checkpointPath=".model_checkpoint/",
    lrBoundaries=[40],
    lrValues=[0.01, 0.0001],
    epochs=100,
    batchsize=16,
):
    # printTrainingExample(X_train, y_train)
    model = models.available_models[modelName](X_train, y_train)

    stepsPerEpoch = X_train[0].array.shape[0] // batchsize
    lrBoundaries = [x * stepsPerEpoch for x in lrBoundaries]
    lr_schedule = optimizers.schedules.PiecewiseConstantDecay(
        boundaries=lrBoundaries, values=lrValues
    )
    model.compile(
        optimizer=optimizers.Adam(learning_rate=lr_schedule),
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics="accuracy",
    )

    print(model.summary())
    # Unpacking the numpy arrays inside the input and output representations
    x = [xi.array for xi in X_train]
    y = [yi.array for yi in y_train]
    x = x if len(x) > 1 else x[0]
    y = y if len(y) > 1 else y[0]
    xv = [xi.array for xi in X_test]
    yv = [yi.array for yi in y_test]
    xv = xv if len(xv) > 1 else xv[0]
    yv = yv if len(yv) > 1 else yv[0]

    modelNameSuffix = (
        "{epoch:02d}"
        + "-{val_monitored_loss:.3f}"
        + "-{val_monitored_accuracy:.4f}"
        + ".hdf5"
    )

    # Maybe this will force gc on the python lists?
    X_train = y_train = X_test = y_test = []

    curriculum = CurriculumIterator(x, y, batchsize, increaseperepoch=0.01)

    # for inputs, targets in curriculum.iterator():
    #     print(inputs, targets)
    # print("something")

    gc.collect()
    model.fit(
        curriculum,
        epochs=epochs,
        # shuffle=True,
        batch_size=None,
        validation_data=(xv, yv),
        callbacks=[
            ModdedModelCheckpoint(
                checkpointPath + modelNameSuffix,
                monitor="val_y_monitored_loss",
                mode="auto",
            ),
        ],
    )

    bestModel = findBestModel(checkpointPath=checkpointPath)
    return bestModel


def run_experiment(
    experiment_name,
    run_name,
    generateData,
    syntheticDataStrategy,
    model,
    lr_boundaries,
    lr_values,
    nogpu,
    epochs,
    batchsize,
    **kwargs,
):
    if nogpu:
        disableGPU()
    else:
        # Ideally, this shouldn't be necessary; but this is not an ideal world
        tensorflowGPUHack()
    mlflow.tensorflow.autolog()
    mlflow.set_experiment(experiment_name)
    mlflow.start_run(run_name=run_name)
    for k, v in kwargs.items():
        mlflow.log_param(f"custom_{k}", v)
    timestamp = datetime.datetime.now().strftime("%y%m%dT%H%M%S")
    checkpoint = f".model_checkpoint/{experiment_name}/{run_name}-{timestamp}/"
    npzNoExt, _ = os.path.splitext(kwargs["npzOutput"])
    if generateData or not os.path.isfile(f"{npzNoExt}.npz"):
        kwargs["synthetic"] = False
        generateDataset(**kwargs)
        # log_artifacts(DATASETDIR, artifact_path="dataset")
    if syntheticDataStrategy:
        if generateData or not os.path.isfile(f"{npzNoExt}-synth.npz"):
            kwargs["synthetic"] = True
            generateDataset(**kwargs)
            # log_artifacts(SYNTHDATASETDIR, artifact_path="dataset-synth")
    (X_train, y_train), (X_test, y_test) = loadData(
        npzPath=npzNoExt,
        syntheticDataStrategy=syntheticDataStrategy,
        modelName=model,
    )
    bestmodel = train(
        X_train,
        y_train,
        X_test,
        y_test,
        modelName=model,
        checkpointPath=checkpoint,
        lrBoundaries=lr_boundaries,
        lrValues=lr_values,
        epochs=epochs,
        batchsize=batchsize,
    )
    modelpath = os.path.join(checkpoint, bestmodel)
    results, summary = evaluate(modelpath, X_test, y_test)
    mlflow.log_artifacts(results, artifact_path="results")
    # Helps organizing them in the mlflow interface
    summary = {f"results_{k}": v for k, v in summary.items()}
    mlflow.log_metrics(summary)
    print(f"The trained model is available in: {modelpath}")


if __name__ == "__main__":
    parser = cli.train()
    args = parser.parse_args()
    kwargs = vars(args)
    run_experiment(**kwargs)
