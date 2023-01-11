import os
import json
import shutil
import subprocess
import requests
import pathlib
import tempfile
from argparse import ArgumentParser


def process_dir(input_dir, output_dir, media_dir):
    files = os.listdir(input_dir)

    for file in files:
        filepath = os.path.join(input_dir, file)

        if os.path.isfile(filepath):
            # Copy archive cmdi file.
            shutil.copy(filepath, output_dir)
        else:
            # Process interview cmdi file.
            interview_cmdi_input = os.path.join(input_dir, file, f'{file}.xml')
            interview_output_dir = os.path.join(output_dir, file)
            interview_cmdi_output = os.path.join(output_dir, file, f'{file}.xml')
            interview_media_dir = os.path.join(media_dir, file)

            if not os.path.exists(interview_output_dir):
                os.mkdir(interview_output_dir)

            cp = subprocess.run([
                'python',
                'process_interview_cmdi.py',
                '--inputfile',
                interview_cmdi_input,
                '--outputfile',
                interview_cmdi_output,
                '--mediadir',
                interview_media_dir
            ], check=True)



parser = ArgumentParser(
    prog = 'lta',
    description = 'OHD long term archiving tool',
    epilog = 'Good luck'
)
parser.add_argument('-i', '--inputdir', required=True, type=pathlib.Path,
    help='path of input directory')
parser.add_argument('-o', '--outputdir', required=True, type=pathlib.Path,
    help='path of output directory')
parser.add_argument('-m', '--mediadir', required=True, type=pathlib.Path,
    help='directory of media files')
parser.add_argument('-v', '--version', action='version',
    version='%(prog)s 0.1')

args = parser.parse_args()

input_dir = args.inputdir
output_dir = args.outputdir
media_dir = args.mediadir


process_dir(input_dir, output_dir, media_dir)
