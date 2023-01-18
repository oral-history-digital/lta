import os
import subprocess
import xmlschema

def create_output_directory(path):
    combined_path = os.path.join('.', path)
    if not os.path.exists(combined_path):
        os.mkdir(combined_path)


def validate_xml(path, schema):
    schema_path = os.path.join(os.path.dirname(__file__), schema)
    schema = xmlschema.XMLSchema(schema_path)

    if schema.is_valid(path):
        return 0
    else:
        return 1
