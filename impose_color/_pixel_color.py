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
