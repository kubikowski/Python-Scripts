from typing import Final, NamedTuple, Tuple

RGB: Final[str] = 'RGB'
RGBA: Final[str] = 'RGBA'


class RGBColor(NamedTuple):
    red: int
    green: int
    blue: int

    @staticmethod
    def of(color: Tuple[int, int, int] | 'RGBColor') -> 'RGBColor':
        return RGBColor(color[0], color[1], color[2])

    def to_string(self: 'RGBColor') -> str:
        return 'rgb({}, {}, {})'.format(self.red, self.green, self.blue)


class RGBAColor(NamedTuple):
    red: int
    green: int
    blue: int
    alpha: int

    @staticmethod
    def of(color: Tuple[int, int, int] | Tuple[int, int, int, int] | 'RGBColor' | 'RGBAColor') -> 'RGBAColor':
        alpha: Final[int] = color[3] if len(color) == 4 else 255
        return RGBAColor(color[0], color[1], color[2], alpha)

    def to_string(self: 'RGBAColor') -> str:
        return 'rgba({}, {}, {}, {})'.format(self.red, self.green, self.blue, self.alpha)
