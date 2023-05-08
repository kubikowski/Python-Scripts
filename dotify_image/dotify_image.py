"""
Name: Dotify Image
Author: Nathaniel Holden
Version: 0.0.5
Date: 2023-4-28
Dependencies: Pillow

Inputs:
  * an image path
  * [optional] a background color
  * [optional] a dot size
  * [optional] a dot color calculation method
  * [optional] a dot placement pattern
  * [optional] an up-scaling ratio
  * [optional] an output file path (.png if unspecified)
Outputs:
  * a dotified version of the input image
"""

from typing import Final

from PIL import Image

from _dotify import Dotify
from _dotify_cli import get_input_image_path, get_output_image_path


def dotify_image() -> None:
    input_image_path: Final[str] = get_input_image_path()
    input_image: Final[Image.Image] = Image.open(input_image_path)

    output_image: Final[Image.Image] = Dotify.image(input_image)
    output_image_path: Final[str] = get_output_image_path()

    output_image.save(output_image_path)


if __name__ == '__main__':
    while True:
        try:
            dotify_image()
        except KeyboardInterrupt:
            break
