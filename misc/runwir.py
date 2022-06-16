import os
from pprint import pprint
import shutil

from AugmentedNet.inference import predict
from AugmentedNet.utils import tensorflowGPUHack
from tensorflow import keras


if __name__ == "__main__":
    wirpath = "When-in-Rome-master/Corpus"
    tensorflowGPUHack()
    model = keras.models.load_model("AugmentedNet.hdf5")
    success = []
    fail = []
    for root, _, files in os.walk(wirpath):
        for f in files:
            if f == "score.mxl":
                filepath = os.path.join(root, f)
                print(filepath)
                rn1 = f.replace(".mxl", "_annotated.xml")
                rn1path = os.path.join(root, rn1)
                rn2 = "analysis_automatic.txt"
                rn2path = os.path.join(root, rn2)
                if os.path.exists(rn2path):
                    success.append(rn2path)
                    continue
                try:
                    predict(model, filepath)
                except:
                    print("FAILED!")
                    fail.append(rn2path)
                    continue
                shutil.move(rn1path, rn2path)
                success.append(rn2path)
    pprint(success)
    pprint(fail)
