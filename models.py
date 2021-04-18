from tensorflow import keras
from tensorflow.keras import layers
from common import SEQUENCELENGTH

def simpleGRU(inputFeatures, outputClasses):
    return keras.Sequential(
        [
            keras.Input(shape=(SEQUENCELENGTH, inputFeatures)),
            layers.Dense(32, activation="relu"),
            layers.BatchNormalization(),
            layers.Dense(32, activation="relu"),
            layers.BatchNormalization(),
            layers.Bidirectional(layers.GRU(30, return_sequences=True)),
            layers.BatchNormalization(),
            layers.Bidirectional(layers.GRU(30, return_sequences=True)),
            layers.BatchNormalization(),
            layers.Dense(outputClasses),
        ]
    )
