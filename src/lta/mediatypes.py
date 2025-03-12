from pathlib import Path
import os


def mimetype_from_filename(filename):
    """
    Returns a standard mimetype according to the filename's extension.
    """
    extension = Path(filename).suffix.lower()

    extension_to_mimetype = {
        ".mp4": "video/mp4",
        ".m2ts": "video/mpeg",
        ".avi": "video/x-msvideo",
        ".pdf": "application/pdf",
        ".ods": "application/vnd.oasis.opendocument.spreadsheet",
        ".csv": "text/plain",
        ".vtt": "text/vtt",
    }

    if extension in extension_to_mimetype:
        return extension_to_mimetype[extension]
    else:
        raise TypeError(f"cannot determine mimetype for {filename}")


def is_media_file(filename):
    """Returns True is filename is a media file according to its extension."""
    pair = os.path.splitext(filename)
    ext = pair[1].lower()
    return ext in [".m2ts", ".mp4", ".avi"]


def is_transcript_file(filename):
    """Returns True if filename is a transcript file according to its extension."""
    pair = os.path.splitext(filename)
    ext = pair[1].lower()
    return ext in [".ods", ".pdf", ".csv", ".vtt"]


# TODO: Probably not used any longer.
def mediatype_from_filename(filename):
    """Returns 'video' or 'audio' according to the media filename's extension."""
    extension = Path(filename).suffix.lower()

    # TODO: Finish audio part, if possible to determinate from extension alone.
    video_extensions = [".mp4", ".m2ts", ".avi"]
    audio_extensions = []

    if extension in video_extensions:
        return "video"
    elif extension in audio_extensions:
        return "audio"
    else:
        raise TypeError(f"cannot determine media file type for {filename}")
