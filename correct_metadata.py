import os
import json
import requests
import pathlib
from argparse import ArgumentParser
import xml.etree.ElementTree as ET
import interview_cmdi as cmdi
from media_files import check_directory_integrity


ET.register_namespace('', 'http://www.clarin.eu/cmd/')

parser = ArgumentParser()
parser.add_argument('file', type=pathlib.Path,
    help='original cmdi xml metadata file')
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')

args = parser.parse_args()


# Directory scanning.

file = args.file
base_path = '/mnt/trove.storage.fu-berlin.de/ohd-av/bas_packages/adg'
stem = file.stem
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
    raise ValueError('Number of media files does not match number of transcript files.')

print(media_files)
print(transcript_files)


check_directory_integrity(dir_path)




# Parse and change xml.

tree = ET.parse(file)
root = tree.getroot()

cmdi.change_resource_proxy_list(root)
cmdi.change_media_session_bundle(root)
cmdi.change_written_resources(root)

actors = cmdi.get_actors(root)

print(actors, ' '.join(actors))

tree.write('output.xml', encoding='utf-8', xml_declaration=True)

# ods => application/vnd.oasis.opendocument.spreadsheet
