from rembg import remove
from PIL import Image
from typing import Union
import cv2
import numpy as np
from .uploaded_files import parse_uploaded_file


def remove_background(img: Union[bytes, Image, str]) -> Image:
    if type(img) == Image:
        output = remove(img)
        return output
    if type(img) == bytes:
        input_img = Image.fromarray(np.uint8(cv2.cvtColor(parse_uploaded_file(img), cv2.COLOR_RGB2BGR)))
        output = remove(input_img)
        return output
    if type(img) == str:
        with open(img, 'rb') as i:
            input_img = i.read()
            output = remove(input_img)
            return output


def change_background(img:Union[bytes, Image, str], back_img: Union[bytes, Image, str]) -> Image:
    back_removed_img = remove_background(img)
    if type(back_img) == bytes:
        back = Image.fromarray(np.uint8(cv2.cvtColor(parse_uploaded_file(back_img), cv2.COLOR_RGB2BGR)))
    if type(back_img) == Image:
        back = img
    if type(back_img) == str:
        with open(img, 'rb') as i:
            back = i.read()
    back.paste(back_removed_img, (0, 0), mask=back_removed_img)
    return back




