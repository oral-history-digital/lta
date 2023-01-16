"""Handle configuration files for lta CLI."""

from collections import namedtuple
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

import os

class NoConfig(Exception):
    """No config found."""

ApplicationConfig = namedtuple('ApplicationConfig',
    ['domain', 'media_path', 'temp_path'])

def get_config(archive_name):
    """Return ApplicationConfig object after reading config file."""
    parser = ConfigParser()
    config_file = os.path.expanduser('~/.lta.config')
    if not os.path.exists(config_file):
        media_path = '~/lta_media/'
        temp_path = '/tmp/lta_tmp'
    else:
        parser.read(config_file)
        try:
            domain = parser.get(archive_name, 'Domain')
            media_path = parser.get(archive_name, 'MediaPath')
            temp_path = parser.get(archive_name, 'TempPath')
        except Exception:
            raise NoConfig(archive_name)

    media_path = os.path.expanduser(media_path)
    temp_path = os.path.expanduser(temp_path)
    return ApplicationConfig(domain, media_path, temp_path)
