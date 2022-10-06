try:
    from rembg import remove
except ImportError:
    print('Please install rembg to use this utility...')

from PIL import Image
from typing import Union
try:
    import cv2
except ImportError:
    print('Please install opencv-python to use this utility...')
import numpy as np
from .uploaded_files import parse_uploaded_file


def remove_background(img):
    if type(img) == bytes:
        input_img = Image.fromarray(np.uint8(cv2.cvtColor(parse_uploaded_file(img), cv2.COLOR_RGB2BGR)))
        output = remove(input_img)
        return output
    if type(img) == str:
        with open(img, 'rb') as i:
            input_img = i.read()
            output = remove(input_img)
            return output
    output = remove(img)
    return output


def change_background(img, back_img, return_as_np_array=True):
    back_removed_img = remove_background(img)
    back = back_img
    if type(back_img) == bytes:
        back = Image.fromarray(np.uint8(cv2.cvtColor(parse_uploaded_file(back_img), cv2.COLOR_RGB2BGR)))
    if type(back_img) == str:
        with open(img, 'rb') as i:
            back = i.read()
    back.paste(back_removed_img, (0, 0), mask=back_removed_img)
    return cv2.cvtColor(np.asarray(back), cv2.COLOR_RGB2BGR)




