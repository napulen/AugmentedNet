"""Various utilities used throughout the other modules."""

import os

import numpy as np
import tensorflow as tf


def tensorflowGPUHack():
    # https://github.com/tensorflow/tensorflow/issues/37942
    gpu_devices = tf.config.experimental.list_physical_devices("GPU")
    for device in gpu_devices:
        tf.config.experimental.set_memory_growth(device, True)


def disableGPU():
    # Disabling the GPU
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def padToSequenceLength(arr, sequenceLength, value=0):
    frames, features = arr.shape
    featuresPerSequence = sequenceLength * features
    featuresInExample = frames * features
    padding = featuresPerSequence - (featuresInExample % featuresPerSequence)
    paddingTimesteps = int(padding / features)
    arr = np.pad(arr, ((0, paddingTimesteps), (0, 0)), constant_values=value)
    arr = arr.reshape(-1, sequenceLength, features)
    return arr
