"""
Name: Image Join
Written By: Nathaniel Holden
Date: 5/30/2019
Dependencies: numpy, Pillow

Inputs:
  · a list of image paths
  · a stacking orientation
  · an output file path (.png if unspecified)
Outputs:
    a combination of the images, stacked horizontally or vertically
"""

from typing import Final, Optional

from PIL import Image

from image_format import ImageFormat
from orientation import Orientation


def stack_images() -> None:
    input_images: Final[list[Image]] = _input_images()
    orientation: Final[Orientation] = Orientation.from_input()

    resized_images: Final[list[Image]] = orientation.resize_images(input_images)
    stacked_image: Final[Image] = orientation.stack_images(resized_images)

    _save_image(stacked_image)


def _input_images() -> list[Image]:
    file_paths: Final[list[str]] = []

    file_path: Optional[str] = _input_image_path()
    while file_path is not None:
        file_paths.append(file_path)
        file_path = _input_image_path()

    return [Image.open(i) for i in file_paths]


def _input_image_path() -> Optional[str]:
    file_path: Final[str] = input('image path or (stop): ')

    if file_path.lower() == 'stop':
        return None
    elif ImageFormat.from_file_path(file_path) is None:
        raise ValueError('unsupported file format in path: "{}"'.format(file_path))
    else:
        return file_path


def _save_image(image: Image) -> None:
    file_path: Final[str] = input('new image path: ')
    formatted_path: Final[str] = ImageFormat.add_format_to_path(file_path)

    image.save(formatted_path)


if __name__ == '__main__':
    while True:
        stack_images()
