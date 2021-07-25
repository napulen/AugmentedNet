"""Tests for AugmentedNet.cli."""

import unittest

from AugmentedNet import cli


class TestCli(unittest.TestCase):
    def test_base_argument_names(self):
        argsGT = set(cli.DefaultArguments._base.keys())
        args = set(vars(cli._base().parse_args([])))
        self.assertEqual(args, argsGT)

    def test_tsv_argument_names(self):
        argsGT = set(cli.DefaultArguments._tsv.keys())
        args = set(vars(cli.tsv().parse_args([])))
        parentArgs = set(vars(cli._base().parse_args([])))
        self.assertEqual(args - parentArgs, argsGT)

    def test_npz_argument_names(self):
        argsGT = set(cli.DefaultArguments._npz.keys())
        args = set(vars(cli.npz().parse_args([])))
        parentArgs = set(vars(cli._base().parse_args([])))
        self.assertEqual(args - parentArgs, argsGT)

    def test_train_argument_names(self):
        argsGT = set(cli.DefaultArguments._train.keys())
        args = set(vars(cli.train().parse_args(["debug", "cli"])))
        parentArgs = set(vars(cli.npz().parse_args([])))
        positional = {"experiment_name", "run_name"}
        self.assertEqual(args - parentArgs - positional, argsGT)


# TODO: Validate structure of a default json file
