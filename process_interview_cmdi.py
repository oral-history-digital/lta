import os
import json
import subprocess
import requests
import pathlib
import tempfile
from argparse import ArgumentParser
import xml.etree.ElementTree as ET
from media_files import check_directory_integrity
import interview_cmdi as cmdi

ET.register_namespace('', 'http://www.clarin.eu/cmd/')


def process_file(input_file, output_file, media_dir):
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








parser = ArgumentParser()
parser.add_argument('-i', '--inputfile', required=True, type=pathlib.Path,
    help='original cmdi xml metadata file')
# TODO: Use STDOUT instead or optionally.
parser.add_argument('-o', '--outputfile', required=True, type=pathlib.Path,
    help='path of output file')
parser.add_argument('-m', '--mediadir', required=True, type=pathlib.Path,
    help='directory of media files')
parser.add_argument('-v', '--version', action='version',
    version='%(prog)s 0.1')

args = parser.parse_args()

input_file = args.inputfile
output_file = args.outputfile
media_dir = args.mediadir

print(input_file, output_file, media_dir)

process_file(input_file, output_file, media_dir)
