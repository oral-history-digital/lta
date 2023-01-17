"""Main API for lta project."""

from collections import namedtuple
from lta.metadata import fetch

# Archive element types : [summary: str, owner: str, done: bool, id: int]
Archive = namedtuple('Archive', ['domain', 'name', 'batch', 'media_dir', 'id'])
Archive.__new__.__defaults__ = ('http://localhost:3000', 'cdoh', 1, None, None)

def fetch_metadata(archive, target_dir):  # type: (Archive, string) -> None
    """Download metadata to target directory."""
    if not isinstance(archive, Archive):
        raise TypeError('archive must be Archive object')
    if not isinstance(target_dir, str):
        raise TypeError('target_dir must be string')

    fetch(archive.domain, archive.name, archive.batch, target_dir)
