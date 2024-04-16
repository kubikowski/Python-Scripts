"""
Name: Stack Images
Author: Nathaniel Holden
Version: 0.2.3
Date: 30/05/2019
Dependencies: numpy, Pillow

Inputs:
  · a list of image paths
  · a stacking orientation
  · an output file path (.png if unspecified)
Outputs:
  · a combination of the images, stacked horizontally or vertically
"""
from pathlib import Path
from typing import Final, Optional

from PIL import Image

from _orientation import Orientation
from util.path import get_input_image_path, get_output_image_path


def stack_images() -> None:
    input_images: Final[list[Image.Image]] = _input_images()
    orientation: Final[Orientation] = Orientation.from_input()

    resized_images: Final[list[Image.Image]] = orientation.resize_images(input_images)
    stacked_image: Final[Image.Image] = orientation.stack_images(resized_images)

    _save_image(stacked_image)


def _input_images() -> list[Image.Image]:
    file_paths: Final[list[Path]] = []

    file_path: Optional[Path] = get_input_image_path()
    while file_path is not None:
        file_paths.append(file_path)
        file_path = get_input_image_path()

    return [Image.open(i) for i in file_paths]


def _save_image(image: Image) -> None:
    file_path: Final[Path] = get_output_image_path()
    image.save(file_path)


if __name__ == '__main__':
    while True:
        stack_images()
