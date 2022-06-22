import os

import numpy as np
import pandas as pd
from tensorflow import keras
import tensorflow as tf

from AugmentedNet.train import loadData, _loadNpz, InputOutput
from AugmentedNet.output_representations import (
    available_representations as availableOutputs,
)
from AugmentedNet.utils import tensorflowGPUHack


OUTPUTS = [
    "LocalKey38",
    "ChordQuality15",
    "Inversion4",
    "ChordRoot35",
    "PrimaryDegree22",
    "SecondaryDegree22",
    "Degree",
    "RomanNumeral",
]


def evaluate(modelHdf5, X_test, y_true):
    model = keras.models.load_model(modelHdf5)
    X = [xi.array for xi in X_test]
    X = X if len(X) > 1 else X[0]
    y_preds = model.predict(X)
    dfdict = {}
    features = []
    for y, ypred in zip(y_true, y_preds):
        name = y.name.replace("validation_y_", "")
        # print(name)
        features.append(name)
        dfdict["true_" + name] = []
        dfdict["pred_" + name] = []
        for true, preds in zip(y.array, ypred):
            decodedTrue = availableOutputs[name].decode(true)
            dfdict["true_" + name].extend(decodedTrue)
            predsCategorical = np.argmax(preds, axis=1).reshape(-1, 1)
            decodedPreds = availableOutputs[name].decode(predsCategorical)
            dfdict["pred_" + name].extend(decodedPreds)
    df = pd.DataFrame(dfdict)
    for feature in features:
        df[feature] = df["true_" + feature] == df["pred_" + feature]
        # print(f"{feature}: {df[feature].mean().round(3)}")
    # Some custom features
    df["Degree"] = df.PrimaryDegree22 & df.SecondaryDegree22
    df["RomanNumeral"] = (
        df.LocalKey38
        & df.ChordQuality15
        & df.ChordRoot35
        & df.Inversion4
        & df.Degree
    )
    # print(f"Degree: {df.Degree.mean().round(3)}")
    # print(f"RomanNumeral: {df.RomanNumeral.mean().round(3)}")
    # df.to_csv("results.csv")

    return [df[f].mean().round(3) for f in OUTPUTS]


evaluations = {
    "6t": {
        "models": [
            "experiments/.model_checkpoint/testset/abc6t-210725T100707"
        ],
        "datasets": ["experiments/abc6t", "wirwtc6t"],
    }
}


if __name__ == "__main__":
    # Disabling the GPU
    # os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    tf.get_logger().setLevel("ERROR")
    tensorflowGPUHack()
    for evaluation, d in evaluations.items():
        models = d["models"]
        datasets = d["datasets"]
        for model in models:
            for dataset in datasets:
                print(evaluation, model, dataset)
                strategy = None
                if "synth" in evaluation:
                    strategy = "concatenate"

                (_, _), (X_test, y_test) = loadData(
                    npzPath=dataset,
                    syntheticDataStrategy=strategy,
                    modelName="AugmentedNet",
                )

                checkpoints = os.listdir(model)
                bestAcc = 0.0
                for checkpoint in sorted(
                    checkpoints, key=lambda x: int(x.split("-")[0])
                ):
                    modelCheckpoint = os.path.join(model, checkpoint)
                    outputs = evaluate(modelCheckpoint, X_test, y_test)
                    k, q, i, r, primd, secd, deg, rn = outputs
                    acc = np.mean([k, q, i, r, primd, secd]).round(3)
                    print(checkpoint, [k, deg, q, i, rn], acc, end="")
                    if acc > bestAcc:
                        print("\t\tbest so far!")
                        bestAcc = acc
                        bestModel = modelCheckpoint
                        bestOutputs = outputs
                    else:
                        print()
                print(bestModel, bestAcc, bestOutputs)
