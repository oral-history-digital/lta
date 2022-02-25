ns = '{http://www.clarin.eu/cmd/}'


def change_resource_proxy_list(root_elem):
    resources = root_elem.find(f'{ns}Resources')
    resource_proxy_list = resources.find(f'{ns}ResourceProxyList')
    resource_proxy_list.clear()


def get_media_session(root_elem):
    components = root_elem.find(f'{ns}Components')
    media_session_profile = components.find(f'{ns}media-session-profile')
    media_session = media_session_profile.find(f'{ns}media-session')
    return media_session


def change_media_session_bundle(root_elem):
    media_session = get_media_session(root_elem)
    media_annotation_bundle = media_session.find(f'{ns}media-annotation-bundle')
    media_annotation_bundle.clear()


def change_written_resources(root_elem):
    media_session = get_media_session(root_elem)
    written_resource = media_session.find(f'{ns}WrittenResource')
    media_session.remove(written_resource)


def get_actors(root_elem):
    media_session = get_media_session(root_elem)
    media_session_actors = media_session.find(f'{ns}media-session-actors')
    actors = []
    for media_session_actor in media_session_actors:
        actors.append(media_session_actor.attrib['id'])
    return actors
