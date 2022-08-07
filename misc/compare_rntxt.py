import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from AugmentedNet.annotation_parser import parseAnnotation
from AugmentedNet.feature_representation import COMMON_ROMAN_NUMERALS


def compare_annotation_df(a, b):
    pcset_accuracy = sum(a.a_pcset == b.a_pcset) / len(a.index)
    key_accuracy = sum(a.a_tonicizedKey == b.a_tonicizedKey) / len(a.index)
    inversion_accuracy = sum(a.a_inversion == b.a_inversion) / len(a.index)
    roman_numeral = sum(a.a_romanNumeral == b.a_romanNumeral) / len(a.index)
    return roman_numeral, pcset_accuracy, inversion_accuracy, key_accuracy


def compute_confusion_matrix(a, b):
    roman_numeral_classes = len(COMMON_ROMAN_NUMERALS)
    matrix = np.zeros((roman_numeral_classes, roman_numeral_classes))
    for gt, pred in zip(a.a_romanNumeral, b.a_romanNumeral):
        gtidx = COMMON_ROMAN_NUMERALS.index(gt)
        predidx = COMMON_ROMAN_NUMERALS.index(pred)
        matrix[gtidx, predidx] += 1
    return matrix


if __name__ == "__main__":
    root = "phd_thesis_predictions"
    groundtruth = "predictions_groundtruth"
    models = [m for m in os.listdir(root) if m != groundtruth and "rntxt" in m]
    gtdir = os.path.join(root, groundtruth)
    dfdict = {
        "file": [],
        "model": [],
        "rn_acc": [],
        "pcset_acc": [],
        "inversion_acc": [],
        "key_acc": [],
        "confusion_matrix": [],
    }
    i = 0
    for f in sorted(os.listdir(gtdir)):
        # if "bps-07" not in f:
        #     continue
        print(f)
        path = os.path.join(root, groundtruth, f)
        a = parseAnnotation(path)
        for model in models:
            mpath = os.path.join(root, model, f)
            if not os.path.exists(mpath):
                continue
            print(f"\t{mpath}", end=" ")
            try:
                b = parseAnnotation(mpath)
            except:
                print("\tFAILED")
                continue
            b = b.reindex_like(a, method="ffill")
            b = b.fillna(method="bfill")
            diff = compare_annotation_df(a, b)
            confm = compute_confusion_matrix(a, b)
            plt.imshow(confm, cmap="Blues")
            plt.savefig(f"plots/{f}_{model}.png")
            print(diff)
            rn, pcset, inversion, key = diff
            dfdict["file"].append(f)
            dfdict["model"].append(model.split("_")[1])
            dfdict["rn_acc"].append(rn)
            dfdict["pcset_acc"].append(pcset)
            dfdict["inversion_acc"].append(inversion)
            dfdict["key_acc"].append(key)
            dfdict["confusion_matrix"].append(confm.tolist())
    df = pd.DataFrame(dfdict)
    df.to_csv("evaluation.csv")
    print(df)
    for model in df.model.unique():
        dfmodel = df[df.model == model]
        rn = dfmodel.rn_acc.mean().round(3)
        pcset = dfmodel.pcset_acc.mean().round(3)
        inv = dfmodel.inversion_acc.mean().round(3)
        key_acc = dfmodel.key_acc.mean().round(3)
        print(model, rn, pcset, inv, key_acc)
