import os
import xml.etree.ElementTree as ET
from shutil import copyfile
from lxml import etree
from pathlib import Path

from lta.mediatypes import is_media_file, is_transcript_file, mediatype_from_filename
from lta.media_files import check_directory_integrity
from lta.xml_validation import validate_session_cmdi
from lta.session_cmdi import change_resource_proxy_list, change_media_session_bundle
from lta.files import create_directory_if_not_exists


ET.register_namespace('', 'http://www.clarin.eu/cmd/')


def pretty_print_lxml(input):
    temp = etree.fromstring(input)
    pretty = etree.tostring(temp, pretty_print=True)
    return pretty


def process_session_cmdi(input_file, output_file, media_dir, dry_run):
    """Check media files and enricht original session cmdi with media data."""

    # Directory scanning.
    base_path = media_dir
    stem = Path(input_file).stem
    interview_id = stem
    dir_path = base_path
    files = os.listdir(dir_path)

    media_files = list(filter(is_media_file, list(files)))
    media_files.sort()

    transcript_files = list(filter(is_transcript_file, list(files)))
    transcript_files.sort()

    # Get media_type from first media file.
    first_media_file = media_files[0]
    media_type = mediatype_from_filename(first_media_file)

    if (len(media_files) != len(transcript_files)):
        raise ValueError(f'{input_file}: Number of media files does not match number of transcript files.')

    check_directory_integrity(dir_path)

    num_parts = len(media_files)


    # Parse and change xml.

    tree = ET.parse(input_file)
    root = tree.getroot()

    change_resource_proxy_list(root, interview_id, media_files, transcript_files)
    change_media_session_bundle(root, num_parts, media_type, transcript_files)


    # Write to tempfile
    output = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    prettified_output = pretty_print_lxml(output)


    # Save it.
    if dry_run:
        print(f'[DRYRUN] Saved session cmdi file to {output_file}')
    else:
        with open(output_file, 'wb') as f:
            f.write(prettified_output)

        validate_session_cmdi(output_file)
        print(f'Saved session cmdi file to {output_file}')


def copy_corpus_cmdi(input_dir, output_dir, dry_run = False):
    """Find the corpus cmdi file in input_dir and copy it to output_dir."""

    files = os.listdir(input_dir)

    for file in files:
        source_path = os.path.join(input_dir, file)

        if os.path.isfile(source_path):  # Corpus cmdi should be the only file in the directory.
            target_path = os.path.join(output_dir, file)
            copyfile(source_path, target_path)
            print(f'{"[DRYRUN] " if dry_run else ""}Created file {target_path}')


def process_session_cmdi_dir(input_dir, output_dir, media_dir, dry_run = False):
    """Find each session cmdi and call process function on it."""

    files = os.listdir(input_dir)

    for file in files:
        filepath = os.path.join(input_dir, file)

        if os.path.isdir(filepath):  # directory with session cmdi.
            input_session_cmdi = os.path.join(input_dir, file, f'{file}.xml')
            interview_output_dir = os.path.join(output_dir, file)
            output_session_cmdi = os.path.join(interview_output_dir, f'{file}.xml')
            interview_media_dir = os.path.join(media_dir, file)

            if dry_run:
                print(f'[DRYRUN] Creating directory {interview_output_dir}')
            else:
                create_directory_if_not_exists(interview_output_dir)

            process_session_cmdi(input_session_cmdi, output_session_cmdi, interview_media_dir,
                dry_run)
