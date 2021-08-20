"""
Name: Color Imposer
Written By: Nathaniel Holden
Date: 3/18/2020
Dependencies: Pillow

Inputs: a background color and
        a semi-transparent foreground color,
Outputs: an opaque (rgb) version of the imposed color.
"""

from typing import Final

from PIL import ImageColor


class PixelColor(object):
    def __init__(self, color: str):
        super(PixelColor, self).__init__()
        self.color: Final[tuple[int, int, int, int]] = ImageColor.getrgb(color)
        self.r: Final[int] = self.color[0]
        self.g: Final[int] = self.color[1]
        self.b: Final[int] = self.color[2]
        self.a: Final[int] = self.color[3] if len(self.color) == 4 else 255

    def get_imposed_color(self, imposed: 'PixelColor') -> 'PixelColor':
        r: Final[int] = self.calculate_target_hue(self.r, imposed.r, imposed.a)
        g: Final[int] = self.calculate_target_hue(self.g, imposed.g, imposed.a)
        b: Final[int] = self.calculate_target_hue(self.b, imposed.b, imposed.a)
        return PixelColor('rgb({},{},{})'.format(r, g, b))

    @staticmethod
    def calculate_target_hue(bg_hue: int, fg_hue: int, a: int) -> int:
        alpha: Final[float] = float(a / 255)
        return int(((1 - alpha) * bg_hue) + (alpha * fg_hue))

    def to_string(self) -> str:
        if len(self.color) == 4:
            return 'rgba{}'.format(self.color)
        else:
            return 'rgb{}'.format(self.color)


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
