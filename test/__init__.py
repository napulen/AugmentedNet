import os
import json


class AuxiliaryFiles(object):
    """Reads any relevant auxiliary files of a unit test."""

    def __init__(self, modulepath):
        testpath = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(testpath, "auxiliary_files", modulepath)
        if not os.path.exists(path):
            # Nothing to load here
            return
        files = os.listdir(path)
        for file in files:
            base, ext = file.rsplit(".")
            filepath = os.path.join(path, file)
            # Where a json file is found, assume a python dict is expected
            if ext == "json":
                jsoncontent = json.load(open(filepath))
                setattr(self, base, jsoncontent)
            else:
                setattr(self, base, filepath)
