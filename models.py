import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from output_representations import (
    available_representations as availableOutputs,
)


def simpleGRU(inputs, outputs):
    # (raw) inputs of the network
    x = []
    # inputs after batchnorm, a dense layer to induce sparsity, etc.
    xprime = []
    for i in inputs:
        sequenceLength = i.array.shape[1]
        inputFeatures = i.array.shape[2]
        name = i.name.replace("training_", "")
        xi = layers.Input(shape=(sequenceLength, inputFeatures), name=name)
        x.append(xi)
        xi = layers.Dense(32)(xi)
        xi = layers.BatchNormalization()(xi)
        xi = layers.Activation("relu")(xi)
        xprime.append(xi)
    if len(x) > 1:
        inputs = layers.Concatenate()([xi for xi in xprime])
    else:
        inputs = xprime[0]
    h = layers.Dense(64)(inputs)
    h = layers.BatchNormalization()(h)
    h = layers.Activation("relu")(h)
    h = layers.Dense(32)(h)
    h = layers.BatchNormalization()(h)
    h = layers.Activation("relu")(h)
    h = layers.Bidirectional(layers.GRU(30, return_sequences=True))(h)
    h = layers.BatchNormalization()(h)
    h = layers.Bidirectional(layers.GRU(30, return_sequences=True))(h)
    h = layers.BatchNormalization()(h)
    h = layers.Bidirectional(layers.GRU(30, return_sequences=True))(h)
    h = layers.BatchNormalization()(h)
    y = []
    for output in outputs:
        outputFeatures = output.outputFeatures
        out = layers.Dense(outputFeatures, name=output.shortname)(h)
        y.append(out)
    model = keras.Model(inputs=x, outputs=y)
    return model


def micchi2020(inputs, outputs):
    def DenseNetLayer(x, b, f, n=1):
        with tf.name_scope(f"denseNet_{n}"):
            for _ in range(b):
                y = layers.BatchNormalization()(x)
                y = layers.Conv1D(
                    filters=4 * f,
                    kernel_size=1,
                    padding="same",
                    data_format="channels_last",
                )(y)
                y = layers.Activation("relu")(y)
                y = layers.BatchNormalization()(y)
                y = layers.Conv1D(
                    filters=f,
                    kernel_size=8,
                    padding="same",
                    data_format="channels_last",
                )(y)
                y = layers.Activation("relu")(y)
                x = layers.Concatenate()([x, y])
        return x

    def PoolingLayer(x, k, s, n=1):
        with tf.name_scope(f"poolingLayer_{n}"):
            y = layers.BatchNormalization()(x)
            y = layers.Conv1D(
                filters=k,
                kernel_size=1,
                padding="same",
                data_format="channels_last",
            )(y)
            y = layers.Activation("relu")(y)
            y = layers.BatchNormalization()(y)
            y = layers.MaxPooling1D(
                s, s, padding="same", data_format="channels_last"
            )(y)
        return y

    def MultiTaskLayer(h, outputs):
        y = []
        for output in outputs:
            outputFeatures = output.outputFeatures
            out = layers.Dense(outputFeatures, name=output.shortname)(h)
            y.append(out)
        return y

    _, sequenceLength, inputFeatures = inputs[0].array.shape
    notes = layers.Input(shape=(sequenceLength, inputFeatures))

    x = DenseNetLayer(notes, b=4, f=8, n=1)
    x = PoolingLayer(x, 32, 2, n=1)
    x = DenseNetLayer(x, 4, 5, n=2)
    x = PoolingLayer(x, 48, 2, n=1)

    x = layers.Bidirectional(
        layers.GRU(64, return_sequences=True, dropout=0.3)
    )(x)

    # I don't think we need the TimeDistributed
    # however, leaving as is
    # https://stackoverflow.com/questions/47305618
    # https://github.com/keras-team/keras/issues/11547
    x = layers.TimeDistributed(layers.Dense(64, activation="tanh"))(x)
    y = MultiTaskLayer(x, outputs)

    model = keras.Model(inputs=[notes], outputs=y)
    return model


def modifiedMicchi2020(inputs, outputs):
    def DenseNetLayer(x, b, f, n=1):
        with tf.name_scope(f"denseNet_{n}"):
            for _ in range(b):
                y = layers.BatchNormalization()(x)
                y = layers.Conv1D(
                    filters=4 * f,
                    kernel_size=1,
                    padding="same",
                    data_format="channels_last",
                )(y)
                y = layers.Activation("relu")(y)
                y = layers.BatchNormalization()(y)
                y = layers.Conv1D(
                    filters=f,
                    kernel_size=8,
                    padding="same",
                    data_format="channels_last",
                )(y)
                y = layers.Activation("relu")(y)
                x = layers.Concatenate()([x, y])
        return x

    def PoolingLayer(x, k, s, n=1):
        with tf.name_scope(f"poolingLayer_{n}"):
            y = layers.BatchNormalization()(x)
            y = layers.Conv1D(
                filters=k,
                kernel_size=1,
                padding="same",
                data_format="channels_last",
            )(y)
            y = layers.Activation("relu")(y)
            y = layers.BatchNormalization()(y)
            y = layers.MaxPooling1D(
                s, s, padding="same", data_format="channels_last"
            )(y)
        return y

    # (raw) inputs of the network
    x = []
    # inputs after batchnorm, a dense layer to induce sparsity, etc.
    xprime = []
    for i in inputs:
        sequenceLength = i.array.shape[1]
        inputFeatures = i.array.shape[2]
        xi = layers.Input(shape=(sequenceLength, inputFeatures), name=i.name)
        x.append(xi)
        # xi = layers.Dense(32)(xi)
        # xi = layers.BatchNormalization()(xi)
        # xi = layers.Activation("relu")(xi)
        xprime.append(xi)
    if len(x) > 1:
        inputs = layers.Concatenate()([xi for xi in xprime])
    else:
        inputs = xprime[0]

    h = DenseNetLayer(inputs, b=4, f=8, n=1)
    h = PoolingLayer(h, 32, 2, n=1)
    h = DenseNetLayer(h, 4, 5, n=2)
    h = PoolingLayer(h, 48, 2, n=1)

    h = layers.Bidirectional(
        layers.GRU(64, return_sequences=True, dropout=0.3)
    )(h)

    # I don't think we need the TimeDistributed
    # https://stackoverflow.com/questions/47305618
    # https://github.com/keras-team/keras/issues/11547
    h = layers.TimeDistributed(layers.Dense(64, activation="tanh"))(h)

    y = []
    for output in outputs:
        outputFeatures = output.array.shape[2]
        out = layers.Dense(outputFeatures, name=output.name)(h)
        y.append(out)

    model = keras.Model(inputs=x, outputs=y)
    return model


available_models = {
    "simpleGRU": simpleGRU,
    "micchi2020": micchi2020,
    "modifiedMicchi2020": modifiedMicchi2020,
}