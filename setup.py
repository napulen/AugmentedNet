#!/usr/bin/env python

from distutils.core import setup
from pathlib import Path

from setuptools import find_packages


def read_version() -> str:
    """
    This script reads the information inside AugmentedNet/__init__.py without
     importing the package, which is not allowed inside the setup.py file
    """
    version = None

    with open(Path(__file__).parent / "AugmentedNet" / "__init__.py", "r") as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith("__version__"):
            version = line.split('"')[1]
    if version is None:
        raise RuntimeError(
            "Can't read package version from file AugmentedNet/__init__.py"
        )
    return version


setup(
    name="AugmentedNet",
    version=read_version(),
    description="A Roman Numeral Analysis Network with Synthetic Training Examples and Additional Tonal Tasks",
    author="Néstor Nápoles López",
    author_email="",
    url="https://github.com/napulen/AugmentedNet/",
    python_requires=">=3.7",
    install_requires=[
        "music21>=6.7,<7",
        "numpy>=1.19,<2",
        "pandas>=1.4,<2",
        "tensorflow>=2.5,<3",
        "mlflow>=1.23<2",
    ],
    packages=find_packages(),
)
