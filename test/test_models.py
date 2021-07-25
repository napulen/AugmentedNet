"""Tests for AugmentedNet.models."""

import os
import unittest

import numpy as np

from AugmentedNet import models
from AugmentedNet.train import InputOutput

# Force no-gpu mode in this test
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


class TestModels(unittest.TestCase):
    def test_augmented_net(self):
        inputs = [
            InputOutput(f"input{i}", np.zeros((1, 640, 19))) for i in range(2)
        ]
        outputs = [
            InputOutput(f"output{i}", np.zeros((1, 640, 30))) for i in range(6)
        ]
        for o in outputs:
            o.shortname = o.name
            o.outputFeatures = 30
        model = models.AugmentedNet(inputs, outputs, blocks=6)
        self.assertEqual(model.count_params(), 77002)
