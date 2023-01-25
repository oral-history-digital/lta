import os
import requests

from lta.files import validate_xml, create_directory_if_not_exists


def fetch_corpus_metadata(archive_name, archive_domain, batch_number, dir_name):
    """Fetches the corpus CMDI metadata file of the given archive and batch."""

    url = f'{archive_domain}/de/project/cmdi_metadata.xml?batch={batch_number}'
    response = requests.get(url, allow_redirects=True)

    file_path = os.path.join(dir_name, f'ohd_{archive_name}_{batch_number:03}.xml')
    with open(file_path, 'wb') as f:
        f.write(response.content)

    result = validate_xml(file_path, 'media-corpus-profile.xsd')
    if result == 0:
        return True
    else:
        raise ValueError(f'{file_path} is not valid a valid corpus cmdi file')


def fetch_interview_ids(domain, batch_number):
    """Fetches interview ids of the given domain and batch"""

    url = f'{domain}/de/project/archiving_batches/{batch_number}.json'
    response = requests.get(url, allow_redirects=True)
    data = response.json()
    return data


def fetch_session_metadata(domain, batch_number, interview_id, dir_name):
    """Fetches the session CMDI metadata file for the given interview_id."""

    url = f'{domain}/de/interviews/{interview_id}/cmdi_metadata.xml?batch={batch_number}'
    response = requests.get(url, allow_redirects=True)

    dir_path = os.path.join(dir_name, interview_id)
    create_directory_if_not_exists(dir_path)

    file_path = os.path.join(dir_path, f'{interview_id}.xml')

    with open(file_path, 'wb') as f:
        f.write(response.content)

    result = validate_xml(file_path, 'media-session-profile.xsd')
    if result == 0:
        return True
    else:
        raise ValueError(f'{file_path} is not valid a valid session cmdi file')
