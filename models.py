import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from output_representations import (
    available_representations as availableOutputs,
)


def AugmentedNet(inputs, outputs, blocks=6):
    """Definition of the AugmentedNet architecture."""
    x = []  # (raw) inputs of the network
    xprime = []  # inputs after initial convolutional blocks
    for i in inputs:
        sequenceLength = i.array.shape[1]
        inputFeatures = i.array.shape[2]
        name = i.name.replace("training_", "")
        xi = layers.Input(shape=(sequenceLength, inputFeatures), name=name)
        x.append(xi)
        for i in range(blocks):
            filters = 2 ** (blocks - 1 - i)
            kernel = 2 ** i
            h = layers.Conv1D(filters, kernel, padding="same")(xi)
            h = layers.BatchNormalization()(h)
            h = layers.Activation("relu")(h)
            xi = layers.Concatenate()([xi, h])
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
    y = []
    for output in outputs:
        outputFeatures = output.outputFeatures
        out = layers.Dense(outputFeatures, name=output.shortname)(h)
        y.append(out)
    model = keras.Model(inputs=x, outputs=y)
    return model


def Micchi2020(inputs, outputs):
    """The model by Micchi et al. (2020)."""

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


def ModifiedMicchi2020(inputs, outputs):
    """A modified version of the model by Micchi et al. (2020)."""

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

    # (raw) inputs of the network
    x = []
    # inputs after batchnorm, a dense layer to induce sparsity, etc.
    xprime = []
    for i in inputs:
        sequenceLength = i.array.shape[1]
        inputFeatures = i.array.shape[2]
        xi = layers.Input(shape=(sequenceLength, inputFeatures), name=i.name)
        x.append(xi)
        # xi = DenseNetLayer(xi, b=2, f=8, n=1)
        xii = layers.BatchNormalization()(xi)
        xii = layers.Conv1D(32, 1, padding="same")(xii)
        xii = layers.Activation("relu")(xii)
        xii = layers.BatchNormalization()(xii)
        xii = layers.Conv1D(8, 8, padding="same")(xii)
        xii = layers.Activation("relu")(xii)
        xii = layers.BatchNormalization()(xii)
        xi = layers.Concatenate()([xi, xii])
        xii = layers.BatchNormalization()(xi)
        xii = layers.Conv1D(32, 1, padding="same")(xii)
        xii = layers.Activation("relu")(xii)
        xii = layers.BatchNormalization()(xii)
        xii = layers.Conv1D(8, 8, padding="same")(xii)
        xii = layers.Activation("relu")(xii)
        xii = layers.BatchNormalization()(xii)
        xi = layers.Concatenate()([xi, xii])
        xprime.append(xi)
    if len(x) > 1:
        inputs = layers.Concatenate()([xi for xi in xprime])
    else:
        inputs = xprime[0]

    h = DenseNetLayer(inputs, b=1, f=8, n=1)
    # h = PoolingLayer(h, 32, 2, n=1)
    # h = DenseNetLayer(h, 2, 5, n=2)
    # h = PoolingLayer(h, 48, 2, n=1)

    h = layers.Bidirectional(layers.GRU(30, return_sequences=True))(h)
    h = layers.BatchNormalization()(h)
    h = layers.Bidirectional(layers.GRU(30, return_sequences=True))(h)
    h = layers.BatchNormalization()(h)

    # I don't think we need the TimeDistributed
    # https://stackoverflow.com/questions/47305618
    # https://github.com/keras-team/keras/issues/11547
    # h = layers.TimeDistributed(layers.Dense(64, activation="tanh"))(h)

    h = layers.Concatenate()([inputs, h])
    h = layers.BatchNormalization()(h)

    y = []
    for output in outputs:
        outputFeatures = output.outputFeatures
        out = layers.Dense(outputFeatures, name=output.shortname)(h)
        y.append(out)

    model = keras.Model(inputs=x, outputs=y)
    return model


available_models = {
    "AugmentedNet": AugmentedNet,
    "Micchi2020": Micchi2020,
    "ModifiedMicchi2020": ModifiedMicchi2020,
}
