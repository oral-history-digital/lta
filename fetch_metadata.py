import os
import json
import requests
import subprocess
from argparse import ArgumentParser

dir_name = 'cmdis'

parser = ArgumentParser()
parser.add_argument('-l', '--local', action='store_true',
    help='use local server', default=False)
parser.add_argument('-b', '--batch', help='archiving batch number',
    type=int, default=1)
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')

args = parser.parse_args()

is_local = args.local
batch_number = args.batch

if (is_local):
    host = 'http://www.example.com:3000'
else:
    host = 'https://deutsches-gedaechtnis.fernuni-hagen.de'

print(f'Fetching data from host {host}')

def create_output_directory(name):
    if not os.path.exists(f'./{name}'):
        os.mkdir(f'./{name}')


def read_ids():
    f = open('./interview-ids.json')
    data = json.load(f)
    f.close()
    return data


def fetch_archive_metadata():
    url = f'{host}/de/project/cmdi_metadata.xml?batch={batch_number}'
    r = requests.get(url, allow_redirects=True)
    f = open(f'./{dir_name}/ohd_adg_{batch_number:03}.xml', 'wb')
    f.write(r.content)
    f.close()
    print(f'{dir_name}/ohd_adg_{batch_number:03}.xml fetched…')

    # Check integrity.
    cp = subprocess.run([
        'xmllint',
        '--schema',
        'media-corpus-profile.xsd',
        f'./{dir_name}/ohd_adg_{batch_number:03}.xml',
        '--noout'
    ], capture_output=True)

    if cp.returncode == 0:
        print(f'{dir_name}/ohd_adg_{batch_number:03}.xml validated…')


def fetch_interview_metadata(id):
    url = f'{host}/de/interviews/{id}/cmdi_metadata.xml?batch={batch_number}'
    r = requests.get(url, allow_redirects=True)

    # Create interview cmdi in separate directory.
    if not os.path.exists(f'./{dir_name}/{id}'):
        os.mkdir(f'./{dir_name}/{id}')

    f = open(f'./{dir_name}/{id}/{id}.xml', 'wb')
    f.write(r.content)
    f.close()

    print(f'{dir_name}/{id}/{id}.xml fetched…')

    # Check integrity.
    cp = subprocess.run([
        'xmllint',
        '--schema',
        'media-session-profile.xsd',
        f'{dir_name}/{id}/{id}.xml',
        '--noout'
    ], capture_output=True)

    if cp.returncode == 0:
        print(f'{dir_name}/{id}/{id}.xml validated…')


create_output_directory(dir_name)
fetch_archive_metadata()

ids = read_ids()
for id in ids:
    fetch_interview_metadata(id)
