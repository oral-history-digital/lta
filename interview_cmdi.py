import xml.etree.ElementTree as ET
from files import filename_to_ext
import os

ns = '{http://www.clarin.eu/cmd/}'


def get_mimetype(filename):
    extension = filename_to_ext(filename).lower()

    match extension:
        case '.mp4':
            return 'video/mp4'
        case '.m2ts':
            return 'video/mpeg'
        case '.avi':
            return 'video/msvideo'
        case '.pdf':
            return 'application/pdf'
        case '.ods':
            return 'application/vnd.oasis.opendocument.spreadsheet'
        case '.csv':
            return 'text/plain'


def get_media_type(filename):
    extension = filename_to_ext(filename).lower()

    match extension:
        case '.mp4' | '.m2ts' | '.avi':
            return 'video'



def resource_id(index, prefix):
    index_str = str(index)
    return f"{prefix}_{index_str.rjust(10, '0')}"


def write_resource_xml(node, interview_id, filename, index, resource_prefix):
    file_id = resource_id(index + 1, resource_prefix)
    path = filename # os.path.join(interview_id, filename)
    mimetype = get_mimetype(filename)

    resource_proxy = ET.SubElement(node, 'ResourceProxy', { 'id': file_id })
    resource_type = ET.SubElement(resource_proxy, 'ResourceType',
        { 'mimetype': mimetype })
    resource_type.text = 'Resource'
    resource_ref = ET.SubElement(resource_proxy, 'ResourceRef')
    resource_ref.text = path


def change_resource_proxy_list(root_elem, interview_id, media_files,
    transcript_files):
    resources = root_elem.find(f'{ns}Resources')
    resource_proxy_list = resources.find(f'{ns}ResourceProxyList')
    resource_proxy_list.clear()

    for idx, media_file in enumerate(media_files):
        write_resource_xml(resource_proxy_list, interview_id, media_file,
            idx, 'r')

    for idx, transcript_file in enumerate(transcript_files):
        write_resource_xml(resource_proxy_list, interview_id, transcript_file,
            idx, 'm')


def get_media_session(root_elem):
    components = root_elem.find(f'{ns}Components')
    media_session_profile = components.find(f'{ns}media-session-profile')
    media_session = media_session_profile.find(f'{ns}media-session')
    return media_session


def remove_media_annotation_bundles(node):
    bundles = node.findall(f'{ns}media-annotation-bundle')
    for bundle in bundles:
        node.remove(bundle)


def change_media_session_bundle(root_elem, num_bundles, media_type, transcript_files):
    media_session = get_media_session(root_elem)
    remove_media_annotation_bundles(media_session)

    actors = get_actors(root_elem)
    actors_str = ' '.join(actors)

    # Create one media annotation bundle for each part.
    for index in range(1, num_bundles + 1):
        bundle = ET.SubElement(media_session, 'media-annotation-bundle')

        media_file_id = resource_id(index, 'r')
        media_file = ET.SubElement(bundle, 'media-file',
            { 'ref': media_file_id, 'actor-ref': actors_str })
        media_type_elem = ET.SubElement(media_file, 'Type')
        media_type_elem.text = media_type

        transcript_file_id = resource_id(index, 'm')
        transcript_mimetype = get_mimetype(
            transcript_files[index - 1])
        written_resource = ET.SubElement(bundle, 'WrittenResource',
            { 'ref': transcript_file_id, 'actor-ref': actors_str })
        annotation_type_outer = ET.SubElement(written_resource,
            'AnnotationType')
        annotation_type_inner = ET.SubElement(annotation_type_outer,
            'AnnotationType')
        annotation_type_inner.text = 'Orthography'
        annotation_format_outer = ET.SubElement(written_resource,
            'AnnotationFormat')
        annotation_format_inner = ET.SubElement(annotation_format_outer,
            'AnnotationFormat')
        annotation_format_inner.text = transcript_mimetype


def change_written_resources(root_elem):
    media_session = get_media_session(root_elem)
    written_resources = media_session.findall(f'{ns}WrittenResource')
    for written_resource in written_resources:
        media_session.remove(written_resource)


def get_actors(root_elem):
    media_session = get_media_session(root_elem)
    media_session_actors = media_session.find(f'{ns}media-session-actors')
    actors = []
    for media_session_actor in media_session_actors:
        actors.append(media_session_actor.attrib['id'])
    return actors
