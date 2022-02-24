import os
import json
import requests
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-f', '--file', help='original cmdi xml metadata file',
    type=ascii)
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')

args = parser.parse_args()
