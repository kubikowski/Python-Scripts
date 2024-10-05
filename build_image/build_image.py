from pathlib import Path
from typing import Final

from matplotlib import pyplot as plt
from matplotlib import image as mpimg
from matplotlib import style
from numpy import array
from PIL import Image

from util.path import get_output_image_path
from util.pixel_color import PixelColor
from util.rgb_color import RGBA, RGBColor


plt.style.use('Solarize_Light2')
plt.title('Sprinter Van')
plt.xlabel('van length (inches)')
plt.ylabel('van width (inches)')


def build_image() -> None:
    image_path: Final[Path] = get_output_image_path()
    image_width: Final[int] = _input_width()
    image_height: Final[int] = _input_height()

    image: Final[Image.Image] = Image.new(mode=RGBA, size=(image_width, image_height), color=(0, 0, 0, 0))
    _draw_box(image)

    plt.imshow(image)
    plt.show()


def _input_width() -> int:
    width: Final[str] = input('Please input an image width:\n  → ').strip()
    return int(width) if width != '' else 100


def _input_height() -> int:
    height: Final[str] = input('Please input an image height:\n  → ').strip()
    return int(height) if height != '' else 100


def _draw_box(image: Image.Image) -> None:
    x_init: Final[int] = int(input('Please enter an initial x coordinate:\n  → ').strip())
    y_init: Final[int] = int(input('Please enter an initial y coordinate:\n  → ').strip())
    x_final: Final[int] = int(input('Please enter an final x coordinate:\n  → ').strip())
    y_final: Final[int] = int(input('Please enter an final y coordinate:\n  → ').strip())
    color: Final[RGBColor] = PixelColor.input_color().color

    for x in range(x_init, x_final):
        for y in range(y_init, y_final):
            image.putpixel((x, y), color)


if __name__ == '__main__':
    build_image()
