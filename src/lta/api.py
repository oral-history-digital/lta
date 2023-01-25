"""Main API for lta project."""

from collections import namedtuple

import lta.files
from lta.network import fetch_corpus_metadata, fetch_interview_ids, fetch_session_metadata

# Archive element types : [summary: str, owner: str, done: bool, id: int]
Archive = namedtuple('Archive', ['domain', 'name', 'batch', 'media_dir', 'id'])
Archive.__new__.__defaults__ = ('http://localhost:3000', 'cdoh', 1, None, None)


def process_archive(archive, temp_dir, dry_run = True):
    """The whole archive process."""

    if not isinstance(archive, Archive):
        raise TypeError('archive must be Archive object')
    if not isinstance(temp_dir, str):
        raise TypeError('temp_dir must be string')


    lta.files.create_directory_if_not_exists(temp_dir)

    fetch_cmdi_metadata(archive, temp_dir)

    # 2. Do some checks on the media files.
    # 3. Process metadata
    # 4. Write metadata files to media directory or custom directory.
    # 5. Create checksums.


def fetch_cmdi_metadata(archive, temp_dir):
    """Fetch corpus cmdi, get interview ids and get session cmdis."""
    fetch_corpus_metadata(archive.name, archive.domain, archive.batch, temp_dir)
    print(f'Fetched corpus cmdi...')

    interview_ids = fetch_interview_ids(archive.domain, archive.batch)
    print(f'{archive.name} batch {archive.batch:03} has {len(interview_ids)} interview ids...')

    for id in interview_ids:
        fetch_session_metadata(archive.domain, archive.batch, id, temp_dir)
        print(f'Fetched {id} session cmdi...')



def create_checksums(dir, algorithm):
    """Recursively create checksums in directory with the specified algorithm."""

    lta.files.create_checksums(dir, algorithm)


if __name__ == '__main__':
    create_checksums('test_video.mp4', 'sha256')
