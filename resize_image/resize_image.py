"""
Name: Resize Image
Author: Nathaniel Holden
Version: 0.0.1
Date: 2024-4-12
Dependencies: Pillow

Inputs:
  · an input image path
  · an output file path (.png if unspecified)
Outputs:
  · a resized output image
"""
from pathlib import Path
from typing import Final

from PIL import Image

from util.path import get_input_image_path, get_output_image_path
from util.rgb_color import RGBA, RGBAColor


def resize_image() -> None:
    input_image: Final[Image.Image] = _input_image()

    output_width: Final[int] = _input_width(input_image.width)
    output_height: Final[int] = _input_height(input_image.height)
    output_image: Final[Image.Image] = Image.new(mode=RGBA, size=(output_width, output_height), color=(0, 0, 0, 0))

    initial_height: Final[int] = _get_initial_height(input_image)
    for width in range(min(input_image.width, output_width)):
        for height in range(initial_height, min(input_image.height, output_height)):
            pixel = RGBAColor.of(input_image.getpixel(xy=(width, height)))
            output_image.putpixel(xy=(width, height - initial_height), value=pixel)

    _save_image(output_image)


def _input_image() -> Image.Image:
    file_path: Final[Path] = get_input_image_path()
    return Image.open(file_path)


def _save_image(image: Image.Image) -> None:
    file_path: Final[Path] = get_output_image_path()
    image.save(file_path)


def _input_width(current_width: int) -> int:
    width: Final[str] = input(
        'Would you like to change the image width?\n' +
        '  The current image width is {} px.\n'.format(current_width) +
        '  → ').strip()

    return int(width) if width != '' else current_width


def _input_height(current_height: int) -> int:
    height: Final[str] = input(
        'Would you like to change the image height?\n' +
        '  The current image height is {} px.\n'.format(current_height) +
        '  → ').strip()

    return int(height) if height != '' else current_height


def _get_initial_height(input_image: Image.Image) -> int:
    height: int = 0
    for width in range(input_image.width):
        for height in range(input_image.height):
            if RGBAColor.of(input_image.getpixel(xy=(width, height))).alpha != 0:
                break
    return height


if __name__ == '__main__':
    resize_image()
