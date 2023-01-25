"""Command Line Interface (CLI) for lta project."""

from __future__ import print_function
import sys
import click

from lta.api import Archive, process_archive
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
@click.option('--skip-fetch', is_flag=True, help='do not fetch metadata, use temp dir instead')
@click.option('--output-dir', required=False, type=str, help='use output directory other than media directory')
@click.option('--dry-run', is_flag=True, help='do not create any files')
@click.option('--checksums/--no-checksums', default=False, help='create checksums')
@click.option('--type', type=click.Choice(['MD5', 'SHA1', 'SHA256'], case_sensitive=False),
    default='SHA256', show_default=True, help='hash type for checksum generation')
def archive(archive, batch, fetch_only, skip_fetch, output_dir, dry_run, checksums, type):
    """Fetch and process archive metadata."""
    try:
        app_config = get_config(archive)

    except Exception as inst:
        sys.exit(inst.args[0])

    arch = Archive(app_config.domain, archive, int(batch))
    actual_output_dir = output_dir or app_config.media_path

    process_archive(arch, app_config.temp_path, app_config.media_path, fetch_only,
        skip_fetch, actual_output_dir, dry_run)



if __name__ == '__main__':
    lta_cli()
