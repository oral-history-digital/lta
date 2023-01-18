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
    include_package_data=True,

    install_requires=['click==8.1.3', 'requests==2.28.2', 'xmlschema==2.1.1'],

    entry_points={
        'console_scripts': [
            'lta = lta.cli:lta_cli',
        ]
    }
)
