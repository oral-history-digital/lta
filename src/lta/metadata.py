import os
import json
import requests
from files import create_output_directory, validate_xml


def fetch_ids():
    url = f'{host}/de/project/archiving_batches/{batch_number}.json'
    response = requests.get(url, allow_redirects=True)
    data = response.json()
    return data


def fetch_archive_metadata(domain, archive_name, batch_number, dir_name):
    url = f'{domain}/de/project/cmdi_metadata.xml?batch={batch_number}'
    r = requests.get(url, allow_redirects=True)
    path = os.path.join('.', dir_name, f'ohd_{archive_name}_{batch_number:03}.xml')
    f = open(path, 'wb')
    f.write(r.content)
    f.close()
    print(f'{path} fetched…')

    result = validate_xml(path, 'media-corpus-profile.xsd')
    if result == 0:
        print(f'{path} validated…')
    else:
        print(result)


def fetch_interview_metadata(id):
    url = f'{host}/de/interviews/{id}/cmdi_metadata.xml?batch={batch_number}'
    r = requests.get(url, allow_redirects=True)

    # Create interview cmdi in separate directory.
    if not os.path.exists(f'./{dir_name}/{id}'):
        os.mkdir(f'./{dir_name}/{id}')

    f = open(f'./{dir_name}/{id}/{id}.xml', 'wb')
    f.write(r.content)
    f.close()

    path = f'{dir_name}/{id}/{id}.xml'

    print(f'{path} fetched…')

    result = validate_xml(path, 'media-session-profile.xsd')
    if result == 0:
        print(f'{path} validated…')
    else:
        print(result)


def fetch(domain, archive_name, batch, target_dir):
    create_output_directory(target_dir)
    fetch_archive_metadata(domain, archive_name, batch, target_dir)

    #ids = fetch_ids()
    #for id in ids:
    #    fetch_interview_metadata(id)
