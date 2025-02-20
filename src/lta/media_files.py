import os
import re

def get_file_extension(filename):
    pair = os.path.splitext(filename)
    ext = pair[1].lower()
    return ext

def filter_media_files(filename):
    ext = get_file_extension(filename)
    return ext in ['.m2ts', '.mp4', '.avi']

def filter_transcript_files(filename):
    ext = get_file_extension(filename)
    return ext in ['.ods', '.pdf', '.csv']

def filter_blacklisted_files(filename):
    ext = get_file_extension(filename)
    return ext not in ['.DS_Store', '.sha256', '.xml']

def check_directory_integrity(path):
    files = list(os.listdir(path))
    files_after_blacklist = list(filter(filter_blacklisted_files, files))

    first_file = files_after_blacklist[0]
    m = re.search(r'_(\d{2})_', first_file)
    first_match = m.group(1)

    num_parts = int(first_match)

    media_files = list(filter(filter_media_files, files_after_blacklist))
    transcript_files = list(filter(filter_transcript_files, files_after_blacklist))
    media_files.sort()
    transcript_files.sort()

    if (len(files_after_blacklist) != num_parts * 2):
        raise ValueError('Wrong number of files.')

    if (len(media_files) != num_parts):
        raise ValueError('Wrong number of media files.')

    if (len(transcript_files) != num_parts):
        raise ValueError('Wrong number of transcript files.')
