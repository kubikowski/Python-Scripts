"""
Name: Impose Color
Author: Nathaniel Holden
Version: 0.1.3
Date: 18/03/2020
Dependencies: Pillow

Inputs:
  · an opaque (RGB) background color
  · a semi-transparent (RGBA) foreground color
Outputs:
  · an opaque (rgb) imposed color
"""

from typing import Final, List

from _pixel_color import PixelColor


def impose_color() -> None:
    background_color: Final[PixelColor] = PixelColor.input_background_color()
    foreground_color: Final[PixelColor] = PixelColor.input_foreground_color()
    imposed_color: Final[PixelColor] = background_color.get_imposed_color(foreground_color)

    print(
        'background color: {}\n'.format(background_color.to_string()) +
        'foreground color: {}\n'.format(foreground_color.to_string()) +
        'imposed color:    {}\n'.format(imposed_color.to_string())
    )


def impose_color_gradient() -> None:
    background_color: Final[PixelColor] = PixelColor.input_background_color()
    foreground_color: Final[PixelColor] = PixelColor.input_foreground_color()
    gradient_steps: Final[int] = PixelColor.input_gradient_steps()
    imposed_gradient: Final[List[PixelColor]] = background_color.get_imposed_gradient(foreground_color, gradient_steps)

    print(
        'background color: {}\n'.format(background_color.to_string()) +
        'foreground color: {}\n'.format(foreground_color.to_string()) +
        'gradient colors:'
    )
    print('\n'.join([
        '{} {}'.format('{}.'.format(index + 1).ljust(3), color.to_string())
        for index, color in enumerate(imposed_gradient)
    ]))


if __name__ == '__main__':
    while True:
        impose_color()
