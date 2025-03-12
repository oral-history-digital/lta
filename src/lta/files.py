import os
import hashlib
from shutil import rmtree


def create_directory_if_not_exists(path, dry_run=False):
    """Check if directory exists and create it otherwise."""
    if os.path.exists(path):
        return

    if dry_run:
        print(f"[DRYRUN] Creating directory {path}")
    else:
        os.mkdir(path)


def prepare_temp_directory(path):
    """Remove directory if it exists and create a new empty one."""
    if os.path.exists(path):
        rmtree(path)

    os.mkdir(path)


def file_checksum(file, hash_method):
    """Return checksum of a file with the specified algorithm."""

    hash = hash_method()

    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)

    digest = hash.hexdigest()
    return digest


def write_checksum(file, checksum, dry_run=True):
    if dry_run:
        print(f"[DRYRUN] Writing checksum file {file}")
    else:
        with open(file, "w") as f:
            f.write(checksum + "\n")


def create_checksums(
    dir, algorithm, ext_blacklist=["", ".md5", ".sha1", ".sha256"], dry_run=True
):
    """Recursively create checksums in directory with the specified algorithm."""

    if algorithm == "MD5":
        hash_method = hashlib.md5
    elif algorithm == "SHA1":
        hash_method = hashlib.sha1
    elif algorithm == "SHA256":
        hash_method = hashlib.sha256
    else:
        raise TypeError("algorithm must be one of MD5, SHA1, SHA256")

    if not os.path.exists(dir):
        raise FileNotFoundError("dir not found")

    if not os.path.isdir(dir):
        raise NotADirectoryError("dir is not a directory")

    # TODO: Make it recursive
    hash_extension = f".{algorithm.lower()}"
    files = os.listdir(dir)

    for file in files:
        filepath = os.path.join(dir, file)
        is_file = os.path.isfile(filepath)
        ext = os.path.splitext(filepath)[1]
        is_blacklisted = ext in ext_blacklist

        if is_file and not is_blacklisted:
            checksum = file_checksum(filepath, hash_method)
            write_checksum(filepath + hash_extension, checksum, dry_run)
