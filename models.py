import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from common import SEQUENCELENGTH


def simpleGRU(inputFeatures, outputClasses):
    inputs = layers.Input(shape=(SEQUENCELENGTH, inputFeatures))
    x = layers.Dense(32)(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(32)(x)
    x = layers.BatchNormalization()(x)
    x = layers.Bidirectional(layers.GRU(30, return_sequences=True))(x)
    x = layers.BatchNormalization()(x)
    x = layers.Bidirectional(layers.GRU(30, return_sequences=True))(x)
    x = layers.BatchNormalization()(x)
    outputs = layers.Dense(outputClasses)(x)
    model = keras.Model(inputs=[inputs], outputs=[outputs])
    return model
    # return keras.Sequential(
    #     [
    #         keras.Input(shape=(SEQUENCELENGTH, inputFeatures)),
    #         layers.Dense(32),
    #         layers.BatchNormalization(),
    #         layers.Dense(32),
    #         layers.BatchNormalization(),
    #         layers.Bidirectional(layers.GRU(30, return_sequences=True)),
    #         layers.BatchNormalization(),
    #         layers.Bidirectional(layers.GRU(30, return_sequences=True)),
    #         layers.BatchNormalization(),
    #         layers.Dense(outputClasses),
    #     ]
    # )


def micchi2020(inputFeatures, outputClasses):
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
            y = layers.MaxPooling1D(s, s, padding="same", data_format="channels_last")(
                y
            )
        return y

    # def MultiTaskLayer(x, derive_root, input_type):
    #     classes_key = 30 if input_type.startswith('spelling') else 24  # Major keys: 0-11, Minor keys: 12-23
    #     classes_degree = 21  # 7 degrees * 3: regular, diminished, augmented
    #     classes_root = 35 if input_type.startswith('spelling') else 12  # the twelve notes without enharmonic duplicates
    #     classes_quality = 12  # ['M', 'm', 'd', 'a', 'M7', 'm7', 'D7', 'd7', 'h7', 'Gr+6', 'It+6', 'Fr+6']
    #     classes_inversion = 4  # root position, 1st, 2nd, and 3rd inversion (the last only for seventh chords)

    #     o_key = TimeDistributed(Dense(classes_key, activation='softmax'), name='key')(x)
    #     z = Concatenate()([x, o_key])
    #     o_dg1 = TimeDistributed(Dense(classes_degree, activation='softmax'), name='degree_1')(z)
    #     o_dg2 = TimeDistributed(Dense(classes_degree, activation='softmax'), name='degree_2')(z)
    #     o_qlt = TimeDistributed(Dense(classes_quality, activation='softmax'), name='quality')(x)
    #     o_inv = TimeDistributed(Dense(classes_inversion, activation='softmax'), name='inversion')(x)
    #     if derive_root and input_type.startswith('pitch'):
    #         o_roo = Lambda(find_root_pitch, name='root')([o_key, o_dg1, o_dg2])
    #     else:
    #         o_roo = TimeDistributed(Dense(classes_root, activation='softmax'), name='root')(x)
    #     return [o_key, o_dg1, o_dg2, o_qlt, o_inv, o_roo]

    def MultiTaskLayer(x, input_type, output_classes):
        o_single = layers.TimeDistributed(
            layers.Dense(output_classes),
        )(x)
        return [o_single]

    notes = layers.Input(shape=(SEQUENCELENGTH, inputFeatures))
    # mask = layers.Input(shape=(None, 1))

    x = DenseNetLayer(notes, b=4, f=8, n=1)
    x = PoolingLayer(x, 32, 2, n=1)
    x = DenseNetLayer(x, 4, 5, n=2)
    x = PoolingLayer(x, 48, 2, n=1)

    # Super-ugly hack otherwise tensorflow can't save the model, see https://stackoverflow.com/a/55229794/5048010
    # x = layers.Lambda(lambda t: __import__('tensorflow').multiply(*t), name='apply_mask')((x, mask))
    # x = layers.Masking()(x)  # is this useless?

    x = layers.Bidirectional(layers.GRU(64, return_sequences=True, dropout=0.3))(x)

    # I don't think we need the TimeDistributed
    # https://stackoverflow.com/questions/47305618
    # https://github.com/keras-team/keras/issues/11547
    x = layers.TimeDistributed(layers.Dense(64, activation="tanh"))(x)
    y = MultiTaskLayer(x, "spelling", outputClasses)

    # x = layers.Dense(outputClasses)(y)

    model = keras.Model(inputs=[notes], outputs=y)
    return model
