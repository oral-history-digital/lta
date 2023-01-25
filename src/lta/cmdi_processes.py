import os
import subprocess
import shutil
import xml.etree.ElementTree as ET
from media_files import check_directory_integrity

import lta.session_cmdi as cmdi
from lta.files import create_directory_if_not_exists


ET.register_namespace('', 'http://www.clarin.eu/cmd/')


def process_session_cmdi(input_file, output_file, media_dir):
    """Check media files and enricht original session cmdi with media data."""

    print(f'Processing file {input_file}...')
    # Directory scanning.

    base_path = media_dir
    stem = input_file.stem
    interview_id = stem
    dir_path = base_path # os.path.join(base_path, stem)
    files = os.listdir(dir_path)

    def filter_media_files(filename):
        pair = os.path.splitext(filename)
        ext = pair[1].lower()
        return ext in ['.m2ts', '.mp4', '.avi']

    def filter_transcript_files(filename):
        pair = os.path.splitext(filename)
        ext = pair[1].lower()
        return ext in ['.ods', '.pdf', '.csv']


    media_files = list(filter(filter_media_files, list(files)))
    transcript_files = list(filter(filter_transcript_files, list(files)))

    media_files.sort()
    transcript_files.sort()

    # Get media_type from first media file.
    first_media_file = media_files[0]
    print(first_media_file)
    media_type = cmdi.get_media_type(first_media_file)


    if (len(media_files) != len(transcript_files)):
        raise ValueError(f'{input_file}: Number of media files does not match number of transcript files.')

    check_directory_integrity(dir_path)

    num_parts = len(media_files)


    # Parse and change xml.

    tree = ET.parse(input_file)
    root = tree.getroot()

    cmdi.change_resource_proxy_list(root, interview_id, media_files, transcript_files)
    cmdi.change_media_session_bundle(root, num_parts, media_type, transcript_files)
    cmdi.change_written_resources(root)

    actors = cmdi.get_actors(root)

    # Write to tempfile
    output_str = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    #tree.write(output_file, encoding='utf-8', xml_declaration=True)

    # Subprocess pretty
    cp1 = subprocess.run(['xmllint', '--format', '-'],
        input=output_str, capture_output=True)

    if cp1.returncode == 0:
        print('Prettified…')

    prettified_output = cp1.stdout

    # Check integrity.
    cp2 = subprocess.run(['xmllint', '--schema', 'media-session-profile.xsd',
        '--noout', '-'],
        input=prettified_output, capture_output=True)

    if cp2.returncode == 0:
        print('Validated…')
    else:
        print('Not validated', cp2.stderr)

    # Save it.
    with open(output_file, 'wb') as binary_file:
        binary_file.write(prettified_output)
        print('Saved…')


def copy_corpus_cmdi(input_dir, output_dir):
    """Find the corpus cmdi file in input_dir and copy it to output_dir."""

    files = os.listdir(input_dir)

    for file in files:
        filepath = os.path.join(input_dir, file)

        if os.path.isfile(filepath):  # corpus cmdi file
            shutil.copy(filepath, output_dir)


def process_session_cmdi_dir(input_dir, output_dir, media_dir):
    """Find each session cmdi and call process function on it."""

    files = os.listdir(input_dir)

    for file in files:
        filepath = os.path.join(input_dir, file)

        if os.path.isdir(filepath):  # directory with session cmdi.
            input_session_cmdi = os.path.join(input_dir, file, f'{file}.xml')
            interview_output_dir = os.path.join(output_dir, file)
            output_session_cmdi = os.path.join(output_dir, file, f'{file}.xml')
            interview_media_dir = os.path.join(media_dir, file)

            create_directory_if_not_exists(interview_output_dir)

            process_session_cmdi(input_session_cmdi, output_session_cmdi, interview_media_dir)
