import os
import json
import requests
import pathlib
from argparse import ArgumentParser
import xml.etree.ElementTree as ET
import interview_cmdi as cmdi

ET.register_namespace('', 'http://www.clarin.eu/cmd/')

parser = ArgumentParser()
parser.add_argument('file', type=pathlib.Path,
    help='original cmdi xml metadata file')
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')

args = parser.parse_args()



tree = ET.parse(args.file)
root = tree.getroot()

for child in root:
    print(child.tag)


cmdi.change_resource_proxy_list(root)
cmdi.change_media_session_bundle(root)
cmdi.change_written_resources(root)

actors = cmdi.get_actors(root)

print(actors, ' '.join(actors))

tree.write('output.xml', encoding='utf-8', xml_declaration=True)

# ods => application/vnd.oasis.opendocument.spreadsheet
