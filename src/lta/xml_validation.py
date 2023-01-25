import os
import xmlschema


def validate_xml(file_path, schema):
    schema_path = os.path.join(os.path.dirname(__file__), schema)
    schema = xmlschema.XMLSchema(schema_path)
    return schema.is_valid(file_path)


def is_valid_corpus_cmdi(file_path):
    return validate_xml(file_path, 'media-corpus-profile.xsd')


def is_valid_session_cmdi(file_path):
    return validate_xml(file_path, 'media-session-profile.xsd')
