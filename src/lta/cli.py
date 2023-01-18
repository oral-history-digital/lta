"""Command Line Interface (CLI) for lta project."""

from __future__ import print_function
import sys
import click
from contextlib import contextmanager

from lta.api import Archive, fetch_metadata
from lta.config import get_config, list_config

class LtaException(Exception):
    """An lta error has occurred."""


# The main entry point for lta.
@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(version='0.1.0')
def lta_cli():
    """OHD long term archiving tool"""


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


@lta_cli.command(help="list configured archives")
def list():
    """List configured archives."""
    try:
        sections = list_config()
        print(*sections)
    except Exception:
        sys.exit(f'No configuration file found.')


@contextmanager
def _lta_db():
    #config = lta.config.get_config()
    #tasks.start_tasks_db(config.db_path, config.db_type)
    yield
    #tasks.stop_tasks_db()


if __name__ == '__main__':
    lta_cli()
