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


@lta_cli.command(help="fetch and process archive metadata")
@click.argument('archive')
@click.option('-b', '--batch', default=1, help='batch number')
@click.option('--fetch-only', is_flag=True, help='just fetch metadata files to temp dir')
@click.option('--dry-run', is_flag=True, help='do not create any files')
@click.option('--checksums/--no-checksums', default=False, help='create checksums')
@click.option('--type', type=click.Choice(['MD5', 'SHA1', 'SHA256'], case_sensitive=False),
    default='SHA256', show_default=True, help='hash type for checksum generation')
def archive(archive, batch, fetch_only, dry_run, checksums, type):
    """Fetch and process archive metadata."""
    try:
        app_config = get_config(archive)
    except Exception as inst:
        sys.exit(inst.args[0])
        #sys.exit(f'No configuration for {archive} archive found. Try "list" command.')

    fetch_metadata(Archive(app_config.domain, archive, int(batch)),
        app_config.temp_path)



if __name__ == '__main__':
    lta_cli()
