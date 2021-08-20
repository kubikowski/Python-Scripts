"""
Name: Image Join
Written By: Nathaniel Holden
Date: 5/30/2019
Dependencies: numpy, Pillow

Inputs: a list of images
Outputs: a jpg of the images stacked horizontally or vertically
Notes: may not currently account for image directory. 
"""

from enum import Enum
from typing import Final, Optional

from numpy import hstack, vstack
from PIL import Image


class Orientation(Enum):
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'

    @staticmethod
    def from_string(orientation: str) -> 'Orientation':
        if orientation == 'h':
            return Orientation.HORIZONTAL
        if orientation == 'v':
            return Orientation.VERTICAL

    def get_min_image_size(self: 'Orientation', images: list[Image]) -> int:
        if self == Orientation.HORIZONTAL:
            return min([i.size[1] for i in images])
        if self == Orientation.VERTICAL:
            return min([i.size[0] for i in images])

    def resize_image(self: 'Orientation', image: Image, min_size: int) -> Image:
        if self == Orientation.HORIZONTAL:
            scale_factor: Final[float] = float(image.size[0] / image.size[1])
            return image.resize([int(min_size * scale_factor), min_size])
        if self == Orientation.VERTICAL:
            scale_factor: Final[float] = float(image.size[1] / image.size[0])
            return image.resize([min_size, int(min_size * scale_factor)])

    def resize_images(self: 'Orientation', images: list[Image]) -> list[Image]:
        min_size: Final[int] = self.get_min_image_size(images)
        return [self.resize_image(image, min_size) for image in images]

    def stack_images(self: 'Orientation', images: list[Image]) -> Image:
        if self == Orientation.HORIZONTAL:
            return Image.fromarray(hstack(images))
        if self == Orientation.VERTICAL:
            return Image.fromarray(vstack(images))


def get_image_input() -> Optional[str]:
    file_name: Final[str] = input('Image Name or (Stop): ')

    if file_name.lower() == 'stop':
        return None
    elif file_name.endswith('.jpg'):
        return file_name
    else:
        return file_name + '.jpg'


def get_images_input() -> list[Image]:
    file_names: Final[list[str]] = []

    file_name: Optional[str] = get_image_input()
    while file_name is not None:
        file_names.append(file_name)
        file_name = get_image_input()

    return [Image.open(i) for i in file_names]


def get_orientation() -> Orientation:
    orientation: Final[str] = input('(h)orizontal or (v)ertical image stack: ')
    return Orientation.from_string(orientation[0].lower())


def save_image(image: Image) -> None:
    output_file_name: Final[str] = input('New Image Name: ')
    image.save(output_file_name + '.jpg')


# This is a tool to join multiple images in an horizontal or vertical stack
# Just input the image names when requested, choose a direction, and
# choose an output name
# you don't need to add the .jpg to the input or output file names
def join_images() -> None:
    input_images: Final[list[Image]] = get_images_input()
    orientation: Final[Orientation] = get_orientation()

    resized_images: Final[list[Image]] = orientation.resize_images(input_images)
    stacked_image: Final[Image] = orientation.stack_images(resized_images)

    save_image(stacked_image)


if __name__ == '__main__':
    while True:
        join_images()
