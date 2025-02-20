import os
import xmlschema


def validate_xml(file_path, schema):
    schema_path = os.path.join(os.path.dirname(__file__), schema)
    schema = xmlschema.XMLSchema(schema_path)
    schema.validate(file_path)


def validate_corpus_cmdi(file_path):
    validate_xml(file_path, "media-corpus-profile.xsd")


def validate_session_cmdi(file_path):
    validate_xml(file_path, "media-session-profile.xsd")
