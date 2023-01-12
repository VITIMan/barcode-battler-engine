# -*- encoding: utf-8 -*-
import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='barcode-battler-engine',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
    ],
    python_requires=">=3.9",
    license='GPL3',
    description='Set of tools to simulate Barcode Battler II functionality.',
    scripts=[
        'barcodebattler-reader'
    ],
    long_description=README,
    url='https://github.com/VITIMan/barcode-battler-engine.git',  # noqa
    author='Victoriano Navarro, VITIMan',
    author_email='bimbiribase@protonmail.com',
    classifiers=[
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Games/Entertainment :: Role-Playing'
    ],
)
