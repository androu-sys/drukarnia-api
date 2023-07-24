# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Get requirements
with open(path.join(HERE, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

# This call to setup() does all the work
setup(
    name="drukarnia-api",
    version="1.1.1",
    description="wrapper for the Drukarnia API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/androu-sys/drukarnia-api",
    author="Andrii Herts",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["drukarnia_api", "drukarnia_api.network", "drukarnia_api.shortcuts", "drukarnia_api.objects"],
    include_package_data=True,
    install_requires=requirements
)
