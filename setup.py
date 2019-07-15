import io
import os
import re
from setuptools import setup, find_packages


def read(*names, **kwargs):
    with io.open(
            os.path.join(os.path.dirname(__file__), *names),
            encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")


VERSION = find_version('tqdmlogger', '__init__.py')


requirements = [
    'tqdm >= 4.26.0',
]


setup(
    name='tqdm-logger',
    version=VERSION,
    author='Leo Mao',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=requirements,
)
