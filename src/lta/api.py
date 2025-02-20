"""Main API for lta project."""

from collections import namedtuple
import os

from lta.files import prepare_temp_directory, create_checksums
from lta.network import (
    fetch_corpus_metadata,
    fetch_interview_ids,
    fetch_session_metadata,
    fetch_archiving_batches,
)
from lta.cmdi_processes import copy_corpus_cmdi, process_session_cmdi_dir


# Archive element types : [summary: str, owner: str, done: bool, id: int]
Archive = namedtuple("Archive", ["domain", "name", "batch", "media_dir", "id"])
Archive.__new__.__defaults__ = ("http://localhost:3000", "cdoh", 1, None, None)


def process_archive(
    archive, temp_dir, media_dir, fetch_only, skip_fetch, output_dir, dry_run=True
):
    """The whole archive process."""

    if not isinstance(archive, Archive):
        raise TypeError("archive must be Archive object")
    if not isinstance(temp_dir, str):
        raise TypeError("temp_dir must be string")

    if not skip_fetch:
        fetch_cmdi_metadata(archive, temp_dir)

    if fetch_only:
        return

    if not os.path.exists(media_dir):
        raise FileNotFoundError(
            f"Configuration error: media dir {media_dir} does not exist"
        )

    if not os.path.isdir(media_dir):
        raise NotADirectoryError(
            f"Configuration error: media dir {media_dir} is not a directory"
        )

    copy_corpus_cmdi(temp_dir, output_dir, dry_run)

    process_session_cmdi_dir(temp_dir, output_dir, media_dir, dry_run)

    # Create checksums?


def fetch_cmdi_metadata(archive, temp_dir):
    """Fetch corpus cmdi, get interview ids and get session cmdis."""
    prepare_temp_directory(temp_dir)

    fetch_corpus_metadata(archive.name, archive.domain, archive.batch, temp_dir)
    print("Fetched corpus cmdi...")

    interview_ids = fetch_interview_ids(archive.domain, archive.batch)
    print(
        f"{archive.name} batch {archive.batch:03} has {len(interview_ids)} interview ids..."
    )

    for id in interview_ids:
        fetch_session_metadata(archive.domain, archive.batch, id, temp_dir)
        print(f"Fetched {id} session cmdi...")


def list_batches(domain):
    """Get a list of the archiving batches for the given domain."""
    return fetch_archiving_batches(domain)


def create_file_checksums(dir, algorithm):
    """Recursively create checksums in directory with the specified algorithm."""
    create_checksums(dir, algorithm)


if __name__ == "__main__":
    create_file_checksums("test_video.mp4", "sha256")
