from os.path import join, dirname

from setuptools import setup, find_packages


def read(filename):
    with open(join(dirname(__file__), filename)) as fileobj:
        return fileobj.read()


def get_version(package):
    return [
        line for line in read('{}/version.py'.format(package)).splitlines()
        if line.startswith('__version__ = ')][0].split("'")[1]


PROJECT_NAME = 'python-tplink-smarthome'
VERSION = get_version('tplink_smarthome')


setup(
    name=PROJECT_NAME,
    version=VERSION,
    description='A package to communicate with TP-Link smart devices.',
    long_description=read('README.rst'),
    long_description_content_type='text/x-rst',
    author='Jeffrey Muller',
    author_email='jeffrey.muller92@gmail.com',
    url='https://github.com/j-muller/python-tplink-smarthome',
    packages=find_packages(exclude=['tests']),
    install_requires=[
    ],
    classifiers=[
        'Programming Language :: Python :: 3.5',
    ],
)
