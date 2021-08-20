"""
Name: Image Join
Written By: Nathaniel Holden
Date: 5/30/2019
Dependencies: numpy, Pillow

Inputs:
 · a list of image paths
 · a stacking orientation
 · an output file path (.png if unspecified)
Outputs: a combination of the images, stacked horizontally or vertically
"""

from enum import Enum
from typing import Final, Optional

from numpy import hstack, vstack
from PIL import Image


class ImageFormat(Enum):
    JPG = 'jpeg'
    PNG = 'png'

    @staticmethod
    def from_file_path(file_path: str) -> Optional['ImageFormat']:
        sanitized_path: Final[str] = file_path.lower()

        if sanitized_path.endswith('.jpg') or sanitized_path.endswith('.jpeg'):
            return ImageFormat.JPG
        if sanitized_path.endswith('.png'):
            return ImageFormat.PNG

        return None

    @staticmethod
    def format_path(file_path: str) -> str:
        image_format: ImageFormat = ImageFormat.from_file_path(file_path)

        if image_format is not None:
            return file_path
        else:
            return file_path + '.png'


class Orientation(Enum):
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'

    @staticmethod
    def from_string(orientation: str) -> 'Orientation':
        if orientation == 'h':
            return Orientation.HORIZONTAL
        if orientation == 'v':
            return Orientation.VERTICAL

    def resize_images(self: 'Orientation', images: list[Image]) -> list[Image]:
        min_size: Final[int] = self._get_min_image_size(images)
        return [self._resize_image(image, min_size) for image in images]

    def _get_min_image_size(self: 'Orientation', images: list[Image]) -> int:
        if self == Orientation.HORIZONTAL:
            return min([i.size[1] for i in images])
        if self == Orientation.VERTICAL:
            return min([i.size[0] for i in images])

    def _resize_image(self: 'Orientation', image: Image, min_size: int) -> Image:
        if self == Orientation.HORIZONTAL:
            scale_factor: Final[float] = float(image.size[0] / image.size[1])
            return image.resize([int(min_size * scale_factor), min_size])
        if self == Orientation.VERTICAL:
            scale_factor: Final[float] = float(image.size[1] / image.size[0])
            return image.resize([min_size, int(min_size * scale_factor)])

    def stack_images(self: 'Orientation', images: list[Image]) -> Image:
        if self == Orientation.HORIZONTAL:
            return Image.fromarray(hstack(images))
        if self == Orientation.VERTICAL:
            return Image.fromarray(vstack(images))


def get_input_image_path() -> Optional[str]:
    file_path: Final[str] = input('image path or (stop): ')

    if file_path.lower() == 'stop':
        return None
    elif ImageFormat.from_file_path(file_path) is None:
        raise ValueError('unsupported file format in path: "{}"'.format(file_path))
    else:
        return file_path


def get_input_images() -> list[Image]:
    file_paths: Final[list[str]] = []

    file_path: Optional[str] = get_input_image_path()
    while file_path is not None:
        file_paths.append(file_path)
        file_path = get_input_image_path()

    return [Image.open(i) for i in file_paths]


def get_orientation() -> Orientation:
    orientation: Final[str] = input('(h)orizontal or (v)ertical image stack: ')
    return Orientation.from_string(orientation[0].lower())


def save_image(image: Image) -> None:
    file_path: Final[str] = input('new image path: ')
    formatted_path: Final[str] = ImageFormat.format_path(file_path)

    image.save(formatted_path)


def join_images() -> None:
    input_images: Final[list[Image]] = get_input_images()
    orientation: Final[Orientation] = get_orientation()

    resized_images: Final[list[Image]] = orientation.resize_images(input_images)
    stacked_image: Final[Image] = orientation.stack_images(resized_images)

    save_image(stacked_image)


if __name__ == '__main__':
    while True:
        join_images()
