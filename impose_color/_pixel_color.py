from typing import Final

from PIL import ImageColor


class PixelColor(object):
    def __init__(self, color: str) -> None:
        super(PixelColor, self).__init__()
        self.color: Final[tuple[int, int, int, int]] = ImageColor.getrgb(color)
        self.r: Final[int] = self.color[0]
        self.g: Final[int] = self.color[1]
        self.b: Final[int] = self.color[2]
        self.a: Final[int] = self.color[3] if len(self.color) == 4 else 255

    @staticmethod
    def input_background_color() -> 'PixelColor':
        background_color: Final[str] = input(
            'Please enter a background color:\n' +
            '  · any web named color, eg: white\n' +
            '  · any hex color, eg: #FFF or #FFFFFF\n' +
            '  · any rbg color, eg: rgb(255,255,255)\n' +
            '  -> ')
        return PixelColor(background_color)

    @staticmethod
    def input_foreground_color() -> 'PixelColor':
        foreground_color: Final[str] = input(
            'Please enter a foreground color with an alpha value:\n' +
            '  · any hexa color, eg: #0007 or #0000007F\n' +
            '  · any rgba color, eg rgba(0,0,0,127)\n' +
            '  -> ')
        return PixelColor(foreground_color)

    def get_imposed_color(self, imposed: 'PixelColor') -> 'PixelColor':
        r: Final[int] = self._calculate_target_hue(self.r, imposed.r, imposed.a)
        g: Final[int] = self._calculate_target_hue(self.g, imposed.g, imposed.a)
        b: Final[int] = self._calculate_target_hue(self.b, imposed.b, imposed.a)

        return PixelColor('rgb({},{},{})'.format(r, g, b))

    @staticmethod
    def _calculate_target_hue(background_hue: int, foreground_hue: int, a: int) -> int:
        alpha: Final[float] = float(a / 255)
        return int(((1 - alpha) * background_hue) + (alpha * foreground_hue))

    def to_string(self) -> str:
        if len(self.color) == 4:
            return 'rgba{}'.format(self.color)
        else:
            return 'rgb{}'.format(self.color)
