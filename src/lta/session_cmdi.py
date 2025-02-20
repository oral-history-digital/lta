import xml.etree.ElementTree as ET

from lta.mediatypes import mimetype_from_filename

ns = "{http://www.clarin.eu/cmd/}"


def resource_id(index, prefix):
    return f"{prefix}_{str(index).rjust(10, '0')}"


def write_resource_xml(node, interview_id, filename, index, resource_prefix):
    file_id = resource_id(index + 1, resource_prefix)
    path = filename
    mimetype = mimetype_from_filename(filename)

    resource_proxy = ET.SubElement(node, "ResourceProxy", {"id": file_id})
    resource_type = ET.SubElement(
        resource_proxy, "ResourceType", {"mimetype": mimetype}
    )
    resource_type.text = "Resource"
    resource_ref = ET.SubElement(resource_proxy, "ResourceRef")
    resource_ref.text = path


def change_resource_proxy_list(root_elem, interview_id, media_files, transcript_files):
    resources = root_elem.find(f"{ns}Resources")
    resource_proxy_list = resources.find(f"{ns}ResourceProxyList")

    for idx, media_file in enumerate(media_files):
        write_resource_xml(resource_proxy_list, interview_id, media_file, idx, "r")

    for idx, transcript_file in enumerate(transcript_files):
        write_resource_xml(resource_proxy_list, interview_id, transcript_file, idx, "m")


def get_media_session(root_elem):
    components = root_elem.find(f"{ns}Components")
    media_session_profile = components.find(f"{ns}media-session-profile")
    media_session = media_session_profile.find(f"{ns}media-session")
    return media_session


def change_media_session_bundle(root_elem, num_bundles, media_type, transcript_files):
    media_session = get_media_session(root_elem)

    actors = get_actors(root_elem)
    actors_str = " ".join(actors)

    # Create one media annotation bundle for each part.
    for index in range(1, num_bundles + 1):
        bundle = ET.SubElement(media_session, "media-annotation-bundle")

        media_file_id = resource_id(index, "r")
        media_file = ET.SubElement(
            bundle, "media-file", {"ref": media_file_id, "actor-ref": actors_str}
        )
        media_type_elem = ET.SubElement(media_file, "Type")
        media_type_elem.text = media_type

        transcript_file_id = resource_id(index, "m")
        transcript_mimetype = mimetype_from_filename(transcript_files[index - 1])
        written_resource = ET.SubElement(
            bundle,
            "WrittenResource",
            {"ref": transcript_file_id, "actor-ref": actors_str},
        )
        annotation_type_outer = ET.SubElement(written_resource, "AnnotationType")
        annotation_type_inner = ET.SubElement(annotation_type_outer, "AnnotationType")
        annotation_type_inner.text = "Orthography"
        annotation_format_outer = ET.SubElement(written_resource, "AnnotationFormat")
        annotation_format_inner = ET.SubElement(
            annotation_format_outer, "AnnotationFormat"
        )
        annotation_format_inner.text = transcript_mimetype


def get_actors(root_elem):
    media_session = get_media_session(root_elem)
    media_session_actors = media_session.find(f"{ns}media-session-actors")
    actors = []
    for media_session_actor in media_session_actors:
        actors.append(media_session_actor.attrib["id"])
    return actors
