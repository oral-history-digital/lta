"""Command Line Interface (CLI) for lta project."""

from __future__ import print_function
import click
#import lta.config
from contextlib import contextmanager
#from lta.api import Task


# The main entry point for lta.
@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(version='0.1.0')
def lta_cli():
    """Run the lta application."""


@lta_cli.command(help="download metadata")
@click.argument('domain')
@click.argument('batch')
def download(domain, batch):
    """Download metadata."""
    print(domain, batch)

    with _lta_db():
        print('to be implemented')
        #lta.add(Task(summary, owner))


@contextmanager
def _lta_db():
    #config = lta.config.get_config()
    #tasks.start_tasks_db(config.db_path, config.db_type)
    yield
    #tasks.stop_tasks_db()


if __name__ == '__main__':
    lta_cli()
