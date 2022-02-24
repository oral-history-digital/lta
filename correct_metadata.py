import os
import json
import requests
import pathlib
from argparse import ArgumentParser
import xml.etree.ElementTree as ET

ET.register_namespace('', 'http://www.clarin.eu/cmd/')

parser = ArgumentParser()
parser.add_argument('-f', '--file', type=pathlib.Path, required=True,
    help='original cmdi xml metadata file')
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')

args = parser.parse_args()

tree = ET.parse(args.file)
root = tree.getroot()

for child in root:
    print(child.tag)

# Change ResourceProxyList
resources = root.find('{http://www.clarin.eu/cmd/}Resources')
resource_proxy_list = resources.find('{http://www.clarin.eu/cmd/}ResourceProxyList')
resource_proxy_list.clear()

# Fix lower part

components = root.find('{http://www.clarin.eu/cmd/}Components')
media_session_profile = components.find('{http://www.clarin.eu/cmd/}media-session-profile')
media_session = media_session_profile.find('{http://www.clarin.eu/cmd/}media-session')
media_annotation_bundle = media_session.find('{http://www.clarin.eu/cmd/}media-annotation-bundle')
media_annotation_bundle.clear()

written_resource = media_session.find('{http://www.clarin.eu/cmd/}WrittenResource')
media_session.remove(written_resource)

# find out actors
media_session_actors = media_session.find('{http://www.clarin.eu/cmd/}media-session-actors')
actors = []
for media_session_actor in media_session_actors:
    actors.append(media_session_actor.attrib['id'])

print(actors, ' '.join(actors))

# Change media-annotation-bundle
# Change WrittenResource parts





tree.write('output.xml', encoding='utf-8', xml_declaration=True)

# ods => application/vnd.oasis.opendocument.spreadsheet
