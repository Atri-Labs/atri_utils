from io import BufferedReader, TextIOWrapper
from typing import BinaryIO
import numpy as np
import cv2
import os
from typing import Union


def parse_uploaded_file(file: Union[bytes, BinaryIO, BufferedReader, str, TextIOWrapper]):
    """
    This functions returns a numpy.ndarray(3D-Array) from the image uploaded
    if file passed is None it returns None
    if file type is str (currently expects the file_name is passed)


    """
    if type(file) is None:
        return None

    if type(file) == bytes:
        p = np.frombuffer(file, np.uint8)
        return cv2.imdecode(p, cv2.IMREAD_COLOR)

    # this refers to file_name
    if type(file) == str:
        return cv2.imread(os.path.dirname(os.path.realpath(__file__)) + '/' + file)

    if type(file) == BufferedReader:
        p = np.frombuffer(file.read(), np.uint8)
        return cv2.imdecode(p, cv2.IMREAD_COLOR)






