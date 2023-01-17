import os
import subprocess

def create_output_directory(path):
    combined_path = os.path.join('.', path)
    if not os.path.exists(combined_path):
        os.mkdir(combined_path)


def validate_xml(path, schema):
    cp = subprocess.run([
        'xmllint',
        '--schema',
        f'../../{schema}',
        path,
        '--noout'
    ], capture_output=True)

    if cp.returncode == 0:
        return 0
    else:
        return cp.stderr.decode('utf8')
