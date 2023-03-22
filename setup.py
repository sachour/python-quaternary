import setuptools
from distutils.core import setup

version = "0.1.0"

with open('README.txt') as file:
    long_description = file.read()

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Topic :: Scientific/Engineering :: Visualization"
]

setup(
    name="python-quaternary",
    version=version,
    packages=['quaternary'],
    install_requires=["matplotlib>=2"],
    author="Sofiane H. Achour and contributors",
    author_email="sachour@utexas.edu",
    classifiers=classifiers,
    description="Make quaternary plots in python with matplotlib",
    long_description=long_description,
    keywords="matplotlib quaternary plotting",
    license="MIT",
    url="https://github.com/sachour/python-quaternary",
    download_url="https://github.com/sachour/python-quaternary/tarball/{}".format(version),
)