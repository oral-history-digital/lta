import os
import json
import requests
import pathlib
from argparse import ArgumentParser
import xml.etree.ElementTree as ET
import interview_cmdi as cmdi
from media_files import check_directory_integrity

ET.register_namespace('', 'http://www.clarin.eu/cmd/')



def process_file(file, media_type):
    print(f'Processing file {file}...')
    # Directory scanning.

    base_path = '/mnt/trove.storage.fu-berlin.de/ohd-av/bas_packages/adg'
    stem = file.stem
    interview_id = stem
    dir_path = os.path.join(base_path, stem)
    files = os.listdir(dir_path)

    def filter_media_files(filename):
        pair = os.path.splitext(filename)
        ext = pair[1].lower()
        return ext in ['.m2ts', '.mp4', '.avi']

    def filter_transcript_files(filename):
        pair = os.path.splitext(filename)
        ext = pair[1].lower()
        return ext in ['.ods', '.pdf']


    media_files = list(filter(filter_media_files, list(files)))
    transcript_files = list(filter(filter_transcript_files, list(files)))

    media_files.sort()
    transcript_files.sort()

    if (len(media_files) != len(transcript_files)):
        raise ValueError(f'{file}: Number of media files does not match number of transcript files.')

    check_directory_integrity(dir_path)

    num_parts = len(media_files)


    # Parse and change xml.

    tree = ET.parse(file)
    root = tree.getroot()

    cmdi.change_resource_proxy_list(root, interview_id, media_files, transcript_files)
    cmdi.change_media_session_bundle(root, num_parts, media_type, transcript_files)
    cmdi.change_written_resources(root)

    actors = cmdi.get_actors(root)

    output_filename = os.path.join('output', file)

    tree.write(output_filename, encoding='utf-8', xml_declaration=True)







parser = ArgumentParser()
parser.add_argument('files', type=pathlib.Path, nargs='+',
    help='original cmdi xml metadata files')
parser.add_argument('-t', '--mediatype', choices=['video', 'audio'],
    default='video', help='type of media files')
parser.add_argument('-v', '--version', action='version',
    version='%(prog)s 0.1')

args = parser.parse_args()

filenames = list(args.files)
media_type = args.mediatype

for filename in filenames:
    process_file(filename, media_type)
