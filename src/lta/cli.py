"""Command Line Interface (CLI) for lta project."""

from __future__ import print_function
import sys
import click
from contextlib import contextmanager

from lta.api import Archive, fetch_metadata, create_checksums
from lta.config import get_config, list_config

class LtaException(Exception):
    """An lta error has occurred."""


# The main entry point for lta.
@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(version='0.1.0')
def lta_cli():
    """OHD long term archiving tool"""


@lta_cli.command(help="list configured archives")
def list():
    """List configured archives."""
    try:
        sections = list_config()
        print(*sections)
    except Exception:
        sys.exit(f'No configuration file found.')


@lta_cli.command(help="fetch metadata from archive")
@click.argument('name')
@click.option('-b', '--batch', default=1, help='batch number')
def fetch(name, batch):
    """Fetch metadata."""
    try:
        app_config = get_config(name)
    except Exception:
        sys.exit(f'No configuration for {name} archive found. Try "list" command.')

    fetch_metadata(Archive(app_config.domain, name, int(batch)),
        app_config.temp_path)


@lta_cli.command(help="process metadata")
def process():
    """Process metadata."""


@lta_cli.command(help="copy metadata to server")
def copy():
    """Copy metadata."""



@lta_cli.command(help="do all steps of the process at once")
def all():
    """Do all steps of the process at once."""


@lta_cli.command(help="create checksums")
@click.option('-a', '--algorithm', type=click.Choice(['MD5', 'SHA1', 'SHA256'], case_sensitive=False),
    default='SHA256', show_default=True, help='algorithm for checksum generation')
def checksums(algorithm):
    """Create checksums in media directory."""
    print(algorithm)

    path = '/path/to/files'

    create_checksums(path, algorithm)



if __name__ == '__main__':
    lta_cli()
