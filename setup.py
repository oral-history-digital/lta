"""Minimal setup file for lta project."""

from setuptools import setup, find_packages

setup(
    name='lta',
    version='0.1.0',
    license='GNU GPLv3',
    description='OHD long term archiving tool',

    author='Marc Altmann',
    author_email='marc.altmann@cedis.fu-berlin.de',
    url='',

    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    install_requires=['click==8.1.3', 'tinydb==3.15.1', 'six'],

    entry_points={
        'console_scripts': [
            'lta = lta.cli:lta_cli',
        ]
    },
)
