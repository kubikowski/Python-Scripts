"""
Name: Impose Color
Author: Nathaniel Holden
Version: 0.1.6
Date: 18/03/2020
Dependencies: Pillow

Inputs:
  · an opaque (RGB) background color
  · a semi-transparent (RGBA) foreground color
Outputs:
  · an opaque (rgb) imposed color
"""
from typing import Final, List

from util.pixel_color import PixelColor


def impose_color() -> None:
    background_color: Final[PixelColor] = PixelColor.input_opaque_color(context='background')
    foreground_color: Final[PixelColor] = PixelColor.input_transparent_color(context='foreground')
    imposed_color: Final[PixelColor] = background_color.get_imposed_color(foreground_color)

    print(
        'background color: {}\n'.format(background_color.to_string()) +
        'foreground color: {}\n'.format(foreground_color.to_string()) +
        'imposed color:    {}\n'.format(imposed_color.to_string())
    )


def impose_color_gradient() -> None:
    primary_color: Final[PixelColor] = PixelColor.input_opaque_color('primary')
    secondary_color: Final[PixelColor] = PixelColor.input_opaque_color('secondary')
    gradient_steps: Final[int] = PixelColor.input_gradient_steps()
    imposed_gradient: Final[List[PixelColor]] = primary_color.get_imposed_gradient(secondary_color, gradient_steps)

    print(
        'primary color:   {}\n'.format(primary_color.to_string()) +
        'secondary color: {}\n'.format(secondary_color.to_string()) +
        'gradient colors:'
    )

    gradient_steps_length: Final[int] = len(str(gradient_steps))
    print('\n'.join([
        '{} {}'.format('{}.'.format(index + 1).ljust(gradient_steps_length + 1), color.to_string())
        for index, color in enumerate(imposed_gradient)
    ]))


if __name__ == '__main__':
    while True:
        impose_color()
