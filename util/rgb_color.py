from collections import namedtuple
from typing import Final, Tuple

__all__: Final[list[str]] = [
    'RGB',
    'RGBA',
    'RGBColor',
    'RGBAColor',
]


RGB: Final[str] = 'RGB'
RGBA: Final[str] = 'RGBA'

__RGBColor__ = namedtuple('RGBColor', ('red', 'green', 'blue'))
__RGBAColor__ = namedtuple('RGBAColor', __RGBColor__._fields + ('alpha',))


class RGBColor(__RGBColor__):

    @staticmethod
    def of(color: Tuple[int, int, int] | Tuple[int, int, int, int] | 'RGBColor') -> 'RGBColor':
        if len(color) == 4:
            return RGBAColor(color[0], color[1], color[2], color[3])
        else:
            return RGBColor(color[0], color[1], color[2])

    def to_string(self: 'RGBColor') -> str:
        return 'rgb({}, {}, {})'.format(self.red, self.green, self.blue)

    def to_hex_string(self: 'RGBColor') -> str:
        return '#{:02x}{:02x}{:02x}'.format(self.red, self.green, self.blue)


class RGBAColor(__RGBAColor__, RGBColor):

    @staticmethod
    def of(color: Tuple[int, int, int] | Tuple[int, int, int, int] | 'RGBColor') -> 'RGBAColor':
        alpha: Final[int] = color[3] if len(color) == 4 else 255
        return RGBAColor(color[0], color[1], color[2], alpha)

    def to_string(self: 'RGBAColor') -> str:
        return 'rgba({}, {}, {}, {})'.format(self.red, self.green, self.blue, self.alpha)

    def to_hex_string(self: 'RGBAColor') -> str:
        return '#{:02x}{:02x}{:02x}{:02x}'.format(self.red, self.green, self.blue, self.alpha)
