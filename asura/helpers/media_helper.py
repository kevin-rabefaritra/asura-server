import base64
from django.core.files.base import ContentFile
import re

def base64_to_file_content(input: str, filename: str) -> ContentFile:
    """
    Converts a base64 image to a ContentFile
    Only accepts png / jpeg files

    @param base64 the base64 representation of the image
    @param filename the filename of the ContentFile WITHOUT extension
    The extension will be based on the input str
    """
    if not is_base64_valid(input):
        raise ValueError('Input base64 is not supported. input=%s' % input)
    
    _search = re.search(r'data:([a-z\/]+);base64,(.+)', input)
    format, rawdata = _search.groups()
    _, extension = format.split('/') # split "png" from "image/png"
    output_filename = '%s.%s' % (filename, extension)
    return ContentFile(base64.b64decode(rawdata), output_filename)


def is_base64_valid(input: str) -> bool:
    """
    Returns a boolean whether a base64 image is valid or not
    """
    _search = re.search(r'data:([a-z\/]+);base64,(.+)', input)

    # Check if the base64 input representation is correct
    if not _search:
        return False
    
    # Check if the image format is supported
    format, _ = _search.groups()
    if format not in ['image/png', 'image/jpeg']:
        return False
    
    return True
