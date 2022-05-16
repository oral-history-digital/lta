import os
import json
import requests
from argparse import ArgumentParser

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

def makedir():
    if not os.path.exists('./cmdis'):
        os.mkdir('./cmdis')


def read_ids():
    f = open('./new-interview-ids.json')
    data = json.load(f)
    f.close()
    return data


def fetch_collection_metadata():
    url = f'{host}/de/project/cmdi_metadata.xml?batch={batch_number}'
    r = requests.get(url, allow_redirects=True)
    f = open(f'./cmdis/ohd_adg_{batch_number:03}.xml', 'wb')
    f.write(r.content)
    f.close()
    print("Collection metadata fetched…")


def fetch_interview_metadata(id):
    url = f'{host}/de/interviews/{id}/cmdi_metadata.xml?batch={batch_number}'
    r = requests.get(url, allow_redirects=True)
    f = open(f'./cmdis/{id}.xml', 'wb')
    f.write(r.content)
    f.close()
    print(f'{id} fetched…')

ids = read_ids()
makedir()

fetch_collection_metadata()

for id in ids:
    fetch_interview_metadata(id)
