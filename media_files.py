import os
import re

def filter_media_files(filename):
    pair = os.path.splitext(filename)
    ext = pair[1].lower()
    return ext in ['.m2ts', '.mp4', '.avi']

def filter_transcript_files(filename):
    pair = os.path.splitext(filename)
    ext = pair[1].lower()
    return ext in ['.ods', '.pdf']

def check_directory_integrity(path):
    files = list(os.listdir(path))
    files.remove('.DS_Store')

    first_file = files[0]
    m = re.search('_(\d{2})_', first_file)
    first_match = m.group(1)

    num_parts = int(first_match)

    media_files = list(filter(filter_media_files, list(files)))
    transcript_files = list(filter(filter_transcript_files, list(files)))

    media_files.sort()
    transcript_files.sort()

    if (len(files) != num_parts * 2):
        raise ValueError('Wrong number of files.')

    if (len(media_files) != num_parts):
        raise ValueError('Wrong number of media files.')

    if (len(transcript_files) != num_parts):
        raise ValueError('Wrong number of transcript files.')
