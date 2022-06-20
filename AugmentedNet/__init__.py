"""A Roman numeral analysis network with synthetic data and additional tasks."""

from os.path import dirname, basename, isfile, join
import glob

__author__ = "Néstor Nápoles López"
__version__ = "1.7.1"
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [
    basename(f)[:-3]
    for f in modules
    if isfile(f) and not f.endswith("__init__.py")
]
