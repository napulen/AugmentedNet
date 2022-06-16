from hashlib import sha256
import io
import unittest

import pandas as pd

from AugmentedNet.common import ANNOTATIONSCOREDUPLES, DATASPLITS
from AugmentedNet.joint_parser import parseAnnotationAndScore

from test import AuxiliaryFiles

aux = AuxiliaryFiles("dataset_tsv_generator")


def _annotationScoreHashes():
    for nickname, (annotation, score) in ANNOTATIONSCOREDUPLES.items():
        with open(annotation, "rb") as afd:
            annotationStr = afd.read()
        with open(score, "rb") as sfd:
            scoreStr = sfd.read()
        annotationSha256 = sha256(annotationStr).hexdigest()
        scoreSha256 = sha256(scoreStr).hexdigest()
        annotationSha256GT, scoreSha256GT = aux.hashes.get(nickname, ("", ""))
        yield (
            nickname,
            annotationSha256GT,
            scoreSha256GT,
            annotationSha256,
            scoreSha256,
        )


class TestDatasetTsvGenerator(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_dataset_and_splits_length(self):
        """ This one checks there are no duplicate entries. """
        train, val, test = DATASPLITS.values()
        allAnnotations = list(ANNOTATIONSCOREDUPLES.keys())
        allSplits = train + val + test
        self.assertEqual(len(allAnnotations), len(allSplits))

    def test_dataset_and_splits_equal(self):
        """ This one checks there are no missing/distinct entries."""
        train, val, test = DATASPLITS.values()
        allAnnotations = list(ANNOTATIONSCOREDUPLES.keys())
        allSplits = train + val + test
        self.assertEqual(set(allAnnotations), set(allSplits))

    def test_dataset_nicknames(self):
        """Checks that the identifiers ('nicknames') haven't changed. """
        nicknamesGT = tuple(sorted(aux.hashes.keys()))
        nicknames = tuple(sorted(ANNOTATIONSCOREDUPLES.keys()))
        self.assertTupleEqual(nicknamesGT, nicknames)

    def test_dataset_checksums(self):
        """Checks that the annotation,score contents haven't changed. """
        for hashes in _annotationScoreHashes():
            nickname, aGT, sGT, a, s = hashes
            with self.subTest(nickname=nickname):
                self.assertEqual(aGT, a, msg="The annotation hash changed.")
                self.assertEqual(sGT, s, msg="The score hash changed.")

    def test_quality_metrics(self):
        """For files that changed, compare the metrics."""
        for hashes in _annotationScoreHashes():
            nickname, aGT, sGT, a, s = hashes
            annotation, score = ANNOTATIONSCOREDUPLES[nickname]
            with self.subTest(nickname=nickname):
                if aGT == a and sGT == s:
                    # Assume the test will pass
                    continue
                dfGT = pd.read_csv(aux.dataset_gt, sep="\t")
                misalignmentGT = dfGT[dfGT.file == nickname].misalignmentMean
                qualityGT = dfGT[dfGT.file == nickname].qualityMean
                bassGT = dfGT[dfGT.file == nickname].incongruentBassMean
                df = parseAnnotationAndScore(
                    annotation, score, fixedOffset=0.25
                )
                misalignment = df.measureMisalignment.mean()
                quality = df.qualitySquaredSum.mean()
                bass = df.incongruentBass.mean()
                self.assertLessEqual(
                    float(misalignment),
                    float(misalignmentGT),
                )
                self.assertLessEqual(float(quality), float(qualityGT))
                self.assertLessEqual(float(bass), float(bassGT))
