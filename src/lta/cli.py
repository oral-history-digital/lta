"""Command Line Interface (CLI) for lta project."""

from __future__ import print_function
import sys
import click

from lta.api import Archive, process_archive, list_batches
from lta.config import get_config, list_config
from lta import __version__
from datetime import datetime

class LtaException(Exception):
    """An lta error has occurred."""


# The main entry point for lta.
@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(version=__version__)
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


@lta_cli.command(help="show archiving batches for an archive")
@click.argument('archive')
def batches(archive):
    """List archiving batches for an archive."""
    app_config = get_config(archive)
    batches = list_batches(app_config.domain)

    for batch in batches:
        batch_number = batch['number']
        batch_name = f'ohd_{archive}_{batch_number:03}'
        interview_count = len(batch['interview_ids'])
        created_at = datetime.fromisoformat(batch['created_at'])
        created_at_str = created_at.strftime('%Y/%m/%d')
        title = f'Batch {batch_number} ({batch_name}) was created on {created_at_str} and has {interview_count} interviews:'
        click.secho(title, bold=True)

        interviews = ', '.join(batch['interview_ids'])
        click.secho(interviews)


@lta_cli.command(help="check media files")
@click.argument('archive')
@click.argument('batch', default=1)
def check(archive, batch):
    """Check media files."""
    click.secho(archive)
    click.secho(batch)

    # TODO:
    # Check metadata against files:
    # Check if media folders are missing.
    # Check if there are media folders that are not in the metadata.
    # Check if the number of tapes of an interview corresponds to the number of media files.
    # Check media files alone:
    # Check if every media file has a transcript file.
    # Check for unknown file formats.
    # Check for files with 0 bytes.


@lta_cli.command(help="fetch and process archive metadata")
@click.argument('archive')
@click.option('-b', '--batch', default=1, show_default=True, help='batch number')
@click.option('-f', '--fetch-only', is_flag=True, help='just fetch metadata files to temp dir')
@click.option('-s', '--skip-fetch', is_flag=True, help='do not fetch metadata, use temp dir instead')
@click.option('-o', '--output-dir', required=False, type=click.Path(exists=True, file_okay=False,
    dir_okay=True, writable=True, resolve_path=True),
    help='use output directory other than media directory')
@click.option('-d', '--dry-run', is_flag=True, help='do not create any files')
@click.option('-c', '--checksums', is_flag=True, help='create checksums')
@click.option('-t', '--type', type=click.Choice(['MD5', 'SHA1', 'SHA256'], case_sensitive=False),
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
