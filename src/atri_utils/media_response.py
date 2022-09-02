from typing import Union
from starlette.datastructures import UploadFile
from io import BufferedReader, TextIOWrapper
from typing import BinaryIO
import mimetypes
import base64
from pathlib import PosixPath, WindowsPath

ACCEPTED_FILETYPES = Union[BinaryIO, BufferedReader, TextIOWrapper, str, UploadFile, bytes, PosixPath, WindowsPath]

def get_mime_type(mime_type: Union[str, None], filename: Union[str, None], file: ACCEPTED_FILETYPES) -> str:
    # guard - Do not auto-detect mime-type if already provided
    if mime_type != None and type(mime_type) == str:
        return mime_type
    
    if type(file) == UploadFile:
        return file.content_type

    if type(file) == PosixPath:
        return mimetypes.guess_type(str(file))[0]

    if type(file) == str:
        return mimetypes.guess_type(file)[0]

    # guard
    if filename == None:
        return None

    return mimetypes.guess_type(filename)[0]

def extract_from_buffer_reader(file: BufferedReader, encoding: str) -> str:
    """
    Converts BufferReader to  base64 string
    """
    bytes_data = file.read()
    return base64.b64encode(bytes_data).decode(encoding)

def extract_from_uploadfile(file: UploadFile, encoding: str) -> str:
    """
    Converts fastapi.UploadFile to  base64 string
    """
    bytes_data = file.file.read()
    if bytes_data == b'':
        print("WARNING: Have you already called read on the UploadFile object")
    return base64.b64encode(bytes_data).decode(encoding)

def extract_from_bianryio(file: BinaryIO, encoding: str) -> str:
    """
    Converts python's BinaryIO to  base64 string
    """
    bytes_data = file.read()
    return base64.b64encode(bytes_data).decode(encoding)

def extract_from_textiowrapper(file: TextIOWrapper, encoding: str) -> str:
    """
    Converts python's TextIOWrapper to  base64 string
    """
    bytes_data = bytes(file.read(), encoding)
    return base64.b64encode(bytes_data).decode(encoding)

def extract_from_filename(filename: str, encoding: str) -> str:
    with open(filename, "rb") as f:
        return extract_from_buffer_reader(f, encoding)

def extract_from_bytes(file: bytes, encoding: str) -> str:
    return base64.b64encode(file).decode(encoding)

def extract_from_path(file: Union[PosixPath, WindowsPath], encoding: str) -> str:
    return extract_from_filename(str(file), encoding)

def create_media_response(
    file: ACCEPTED_FILETYPES,
    mime_type: Union[str, None] = None,
    filename: Union[str, None] = None,
    encoding: str = "utf-8"
    ):
    """
    If mime_type is provided, filename parameter will be ignored.
    If filename is provided and mime_type isn't, filename will be used to predict the mime-type.
    In case of UploadFile, UploadFile.content_type will be used as mime-type.
    If a str is passed as file, then it will be considered as a file path.

    It returns None, if mime-type cannot be guessed/found.
    It returns None, if the type of file is unsupported.
    """
    detected_mime_type = get_mime_type(mime_type, filename, file)

    if detected_mime_type == None:
        return None
    
    data = ""

    if type(file) == BufferedReader:
        data = extract_from_buffer_reader(file, encoding)

    elif type(file) == UploadFile:
        data = extract_from_uploadfile(file, encoding)

    elif type(file) == BinaryIO:
        data = extract_from_bianryio(file, encoding)

    elif type(file) == TextIOWrapper:
        data = extract_from_textiowrapper(file, encoding)
    
    elif type(file) == str:
        data = extract_from_filename(file, encoding)
    
    elif type(file) == bytes:
        data = extract_from_bytes(file, encoding)

    elif type(file) == PosixPath or type(file) == WindowsPath:
        data = extract_from_path(file, encoding)

    else:
        return None

    src = "data:" + detected_mime_type + ";base64, " + data
    
    return src
    
