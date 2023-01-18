import os
import subprocess

def create_output_directory(path):
    combined_path = os.path.join('.', path)
    if not os.path.exists(combined_path):
        os.mkdir(combined_path)


def validate_xml(path, schema):
    schema_path = os.path.join(os.path.dirname(__file__), schema)

    cp = subprocess.run([
        'xmllint',
        '--schema',
        schema_path,
        path,
        '--noout'
    ], capture_output=True)

    if cp.returncode == 0:
        return 0
    else:
        return cp.stderr.decode('utf8')
