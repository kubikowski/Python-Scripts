"""
Name: Dotify Image
Author: Nathaniel Holden
Version: 0.0.2
Date: 2023-4-28
Dependencies: Pillow

Inputs:
  * an image path
  * [optional] a background color
  * [optional] a dot size
  * [optional] a dot color calculation method
  * [optional] an up-scaling ratio
  * [optional] a dot placement pattern
  * an output file path (.png if unspecified)
Outputs:
  * a dotified version of the input image
"""

from os import path
from typing import Final

from PIL import Image

from dotify._dotify import Dotify
from stack_images._image_format import ImageFormat


def dotify_image() -> None:
    input_image: Final[Image.Image] = _input_image()
    output_image: Final[Image] = Dotify.image(input_image)

    _save_image(output_image)


def _input_image() -> Image.Image:
    file_path: Final[str] = _input_image_path()

    return Image.open(file_path)


def _input_image_path() -> str:
    file_path: Final[str] = input('image path or (stop): ')

    if file_path.lower() == 'stop':
        raise KeyboardInterrupt()
    elif ImageFormat.from_file_path(file_path) is None:
        raise ValueError('unsupported file format in path: "{}"'.format(file_path))
    else:
        return path.expanduser(file_path)


def _save_image(image: Image.Image) -> None:
    file_path: Final[str] = input('new image path: ')
    formatted_path: Final[str] = ImageFormat.add_format_to_path(file_path)

    image.save(formatted_path)


if __name__ == '__main__':
    while True:
        try:
            dotify_image()
        except KeyboardInterrupt:
            break
