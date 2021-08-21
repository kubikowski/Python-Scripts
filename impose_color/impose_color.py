"""
Name: Impose Color
Author: Nathaniel Holden
Version: 0.1.1
Date: 18/03/2020
Dependencies: Pillow

Inputs:
  · an opaque (RGB) background color
  · a semi-transparent (RGBA) foreground color
Outputs:
  · an opaque (rgb) imposed color
"""

from typing import Final

from _pixel_color import PixelColor


def impose_color():
    background_input: Final[str] = str(input(
        'Please enter a background color:\n' +
        ' · any standard color name, Ex: white\n' +
        ' · a custom color, EX: #FFF or rgb(255,255,255)\n-> '))
    background_color: Final[PixelColor] = PixelColor(background_input)

    foreground_input: Final[str] = str(input(
        'Please enter a custom foreground color with an alpha value:\n' +
        ' · #FFF7 or #FFFFFF7F or rgba(255,255,255,127)\n-> '))
    foreground_color: Final[PixelColor] = PixelColor(foreground_input)

    imposed_color: Final[PixelColor] = background_color.get_imposed_color(foreground_color)

    print(
        'background color: {}\n'.format(background_color.to_string()) +
        'foreground color: {}\n'.format(foreground_color.to_string()) +
        'imposed color:    {}\n'.format(imposed_color.to_string()))


if __name__ == '__main__':
    while True:
        impose_color()
