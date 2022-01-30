import os


class AuxiliaryFiles(object):
    def __init__(self, modulepath):
        testpath = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(testpath, "auxiliary_files", modulepath)
        files = os.listdir(path)
        for file in files:
            base, ext = file.rsplit(".")
            filepath = os.path.join(path, file)
            setattr(self, base, filepath)