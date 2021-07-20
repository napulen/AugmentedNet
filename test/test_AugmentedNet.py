"""General checks of the AugmentedNet package itself."""

from pathlib import Path
import unittest

import AugmentedNet


class TestAugmentedNet(unittest.TestCase):
    def test_unittest_pairs(self):
        """Every module in AugmentedNet should have an associated unittest."""
        modules = AugmentedNet.__all__
        cwd = Path(__file__).parent
        testFiles = [f.name for f in cwd.iterdir() if f.name.endswith(".py")]
        for module in modules:
            testFile = f"test_{module}.py"
            with self.subTest(module=module, testFile=testFile):
                self.assertIn(testFile, testFiles)
