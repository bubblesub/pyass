import os
import sys
from pathlib import Path

from setuptools import find_packages, setup

libs = ["libass.dll"]
data_libs = []

if set(["bdist_wheel", "--plat-name", "win_amd64"]) <= set(sys.argv) or (
    os.name == "nt" and all([os.path.exists(f) for f in libs])
):
    data_libs = [("Scripts", libs)]

setup(
    author="Luni-4",
    author_email="luni-4@hotmail.it",
    name="ass",
    version="0.0.1",
    description="Bindings for Libass",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/bubblesub/pyass",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
    ],
    data_files=data_libs,
    python_requires=">=3.2",
    packages=find_packages(),
    package_dir={"ass": "ass"},
    package_data={"ass": ["data/*", "../COPYING", "../COPYING.LESSER"]},
)
