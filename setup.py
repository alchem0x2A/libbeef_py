from glob import glob
from pathlib import Path

from setuptools import find_packages, setup

setup(
    name="libbeef-py",
    version="0.0.1",
    description="Simple python interface to BEEF-vdW ensemble calculations",
    url="https://github.com/alchem0x2A/libbeef_py",
    packages=find_packages(),
    include_package_data=False,
    package_data={},
    install_requires=["numpy"],
)
