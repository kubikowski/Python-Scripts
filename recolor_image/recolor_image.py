"""
Name: Recolor Images
Author: Nathaniel Holden
Version: 0.0.1
Date: 2024-4-16
Dependencies: Pillow

Inputs:
  · an input image path
  · a color to replace in the original image
  · a replacement color for the output image
  · an output file path (.png if unspecified)
Outputs:
  · an image with a color replaced
"""
from pathlib import Path
from typing import Final

from PIL import Image, ImageColor

from util.path import get_input_image_path, get_output_image_path
from util.rgb_color import RGBA, RGBAColor


def recolor_image() -> None:
    input_image: Final[Image.Image] = _input_image()
    output_image: Final[Image.Image] = Image.new(mode=RGBA, size=input_image.size, color=(0, 0, 0, 0))
    original_color: Final[RGBAColor] = _get_original_color()
    replacement_color: Final[RGBAColor] = _get_replacement_color()

    for width in range(input_image.width):
        for height in range(input_image.height):
            pixel: RGBAColor = RGBAColor.of(input_image.getpixel(xy=(width, height)))

            if (pixel.red == original_color.red
                    and pixel.green == original_color.green
                    and pixel.blue == original_color.blue
                    and pixel.alpha == original_color.alpha):
                output_image.putpixel(xy=(width, height), value=replacement_color)
            else:
                output_image.putpixel(xy=(width, height), value=pixel)

    _save_image(output_image)


def _input_image() -> Image.Image:
    file_path: Final[Path] = get_input_image_path()
    return Image.open(file_path)


def _save_image(image: Image.Image) -> None:
    file_path: Final[Path] = get_output_image_path()
    image.save(file_path)


def _get_original_color() -> RGBAColor:
    input_color: Final[str] = _input_original_color()
    valid_color: Final[str] = input_color if input_color else 'black'
    return RGBAColor.of(ImageColor.getrgb(valid_color))


def _get_replacement_color() -> RGBAColor:
    input_color: Final[str] = _input_replacement_color()
    valid_color: Final[str] = input_color if input_color else 'black'
    return RGBAColor.of(ImageColor.getrgb(valid_color))


def _input_original_color() -> str:
    return input(
        'Would you like to specify a color to replace?\n' +
        '  If you do not, the default is black.\n' +
        '  → ').strip()


def _input_replacement_color() -> str:
    return input(
        'Would you like to specify a replacement color?\n' +
        '  If you do not, the default is black.\n' +
        '  → ').strip()


if __name__ == '__main__':
    recolor_image()
