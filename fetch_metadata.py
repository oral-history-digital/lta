import os
import json
import requests
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

def create_output_directory():
    if not os.path.exists(f'./{dir_name}'):
        os.mkdir(f'./{dir_name}')


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


def fetch_interview_metadata(id):
    url = f'{host}/de/interviews/{id}/cmdi_metadata.xml?batch={batch_number}'
    r = requests.get(url, allow_redirects=True)
    f = open(f'./{dir_name}/{id}.xml', 'wb')
    f.write(r.content)
    f.close()
    print(f'{dir_name}/{id}.xml fetched…')


create_output_directory()
fetch_archive_metadata()

ids = read_ids()
for id in ids:
    fetch_interview_metadata(id)
