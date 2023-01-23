"""Main API for lta project."""

from collections import namedtuple
import hashlib

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


def create_checksums(dir, algorithm):
    """Recursively create checksums in directory with the specified algorithm."""

    # TODO: In the end two functions: for single file and for directory.

    if algorithm == 'MD5':
        hash_method = hashlib.md5
    elif algorithm == 'SHA1':
        hash_method = hashlib.sha1
    elif algorithm == 'SHA256':
        hash_method = hashlib.sha256
    else:
        raise TypeError('algorithm must be one of MD5, SHA1, SHA256')

    hash = hash_method()

    with open(dir, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)

    digest = hash.hexdigest()
    return digest


if __name__ == '__main__':
    create_checksums('test_video.mp4', 'sha256')
