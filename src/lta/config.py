"""Handle configuration files for lta CLI."""

from collections import namedtuple
from configparser import ConfigParser
import os


class NoConfig(Exception):
    """No config found."""


ApplicationConfig = namedtuple(
    "ApplicationConfig", ["domain", "media_path", "temp_path"]
)


def get_config(archive_name):
    """Return ApplicationConfig object after reading config file."""
    parser = ConfigParser()
    config_file = os.path.expanduser("~/.lta.config")
    if not os.path.exists(config_file):
        media_path = "~/lta_media/"
        temp_path = "/tmp/lta_tmp"
    else:
        parser.read(config_file)
        try:
            domain = parser.get(archive_name, "Domain")
            media_path = parser.get(archive_name, "MediaPath")
            temp_path = parser.get(archive_name, "TempPath")
        except Exception:
            raise NoConfig(
                f"Configuration error: no config for archive {archive_name} found. Configured archives are: {', '.join(parser.sections())}"
            )

    media_path = os.path.expanduser(media_path)
    temp_path = os.path.expanduser(temp_path)

    if not os.path.exists(temp_path):
        raise FileNotFoundError(
            f"Configuration error: temp dir {temp_path} does not exist"
        )

    if not os.path.isdir(temp_path):
        raise NotADirectoryError(
            f"Configuration error: file {temp_path} is not a directory"
        )

    return ApplicationConfig(domain, media_path, temp_path)


def list_config():
    """Return list of config sections after reading config file."""
    parser = ConfigParser()
    config_file = os.path.expanduser("~/.lta.config")
    parser.read(config_file)
    return parser.sections()
