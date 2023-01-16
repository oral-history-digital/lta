"""Main API for lta project."""

from collections import namedtuple
from fetch_metadata import fetch

# Archive element types : [summary: str, owner: str, done: bool, id: int]
Archive = namedtuple('Archive', ['domain', 'batch', 'media_dir', 'id'])
Archive.__new__.__defaults__ = ('http://localhost:3000', 1, None, None)

def download_metadata(archive, target_dir):  # type: (Archive, string) -> None
    """Download metadata to target directory."""
    if not isinstance(archive, Archive):
        raise TypeError('archive must be Archive object')
    if not isinstance(target_dir, str):
        raise TypeError('target_dir must be string')

    fetch(archive.domain, archive.batch, target_dir)
