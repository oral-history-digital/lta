"""Top-level package for lta."""

from importlib.metadata import version

__version__ = version("lta")

from .api import *  # noqa
from .cli import lta_cli  # noqa
