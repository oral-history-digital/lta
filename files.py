from pathlib import Path

def filename_to_ext(name):
    return Path(name).suffix
