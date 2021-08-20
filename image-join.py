"""
Name: Image Join
Written By: Nathaniel Holden
Date: 5/30/2019
Dependencies: numpy, Pillow

Inputs: a list of images
Outputs: a jpg of the images stacked horizontally or vertically
Notes: may not currently account for image directory. 
"""

from typing import Final, Optional

from numpy import hstack, sum, vstack
from PIL import Image


def get_image_input() -> Optional[str]:
    file_name: Final[str] = input('Image Name or (Stop): ')

    if file_name.lower() == 'stop':
        return None

    if file_name.endswith('.jpg'):
        return file_name

    return file_name + '.jpg'


def get_images_input() -> list[Image]:
    file_names: Final[list[str]] = []

    file_name: Optional[str] = get_image_input()
    while file_name is not None:
        file_names.append(file_name)
        file_name = get_image_input()

    return [Image.open(i) for i in file_names]


def get_min_image_size(images: list[Image]) -> tuple[int, int]:
    return sorted([(sum(i.size), i.size) for i in images])[0][1]


def resize_images(images: list[Image]) -> list[Image]:
    min_size: Final[tuple[int, int]] = get_min_image_size(images)

    return [image.resize(min_size) for image in images]


def stack_images(images: list[Image]) -> Image:
    orientation: str = input('(h)orizontal or (v)ertical image stack? ').lower()

    if orientation == 'h':  # horizontal stacking
        return Image.fromarray(hstack(images))

    if orientation == 'v':  # vertical stacking
        return Image.fromarray(vstack(images))


def save_image(image: Image) -> None:
    output_file_name: str = input('New Image Name: ')
    image.save(output_file_name + '.jpg')


# This is a tool to join multiple images in an horizontal or vertical stack
# Just input the image names when requested, choose a direction, and
# choose an output name
# you don't need to add the .jpg to the input or output file names
def join_images() -> None:
    input_images: Final[list[Image]] = get_images_input()
    resized_images: Final[list[Image]] = resize_images(input_images)
    stacked_image: Final[Image] = stack_images(resized_images)
    save_image(stacked_image)


if __name__ == '__main__':
    while True:
        join_images()
