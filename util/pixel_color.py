from typing import Final

from PIL import ImageColor

from util.rgb_color import RGBColor, RGBAColor


class PixelColor(object):
    def __init__(self: 'PixelColor', color: RGBColor) -> None:
        self.color: Final[RGBColor] = color
        self.red: Final[int] = color.red
        self.green: Final[int] = color.green
        self.blue: Final[int] = color.blue
        self.alpha: Final[int] = color.alpha if isinstance(color, RGBAColor) else 255

    @staticmethod
    def of(color: str) -> 'PixelColor':
        return PixelColor(RGBColor.of(ImageColor.getrgb(color)))

    @staticmethod
    def input_color() -> 'PixelColor':
        background_color: Final[str] = input(
            'Please enter a color:\n' +
            '  · any web named color, eg: white\n' +
            '  · any hex[a] color, eg: #FFF or #0000007F\n' +
            '  · any rbg[a] color, eg: rgb(255,255,255) or rgba(0,0,0,127)\n' +
            '  → ')
        return PixelColor.of(background_color)

    @staticmethod
    def input_background_color() -> 'PixelColor':
        background_color: Final[str] = input(
            'Please enter a background color:\n' +
            '  · any web named color, eg: white\n' +
            '  · any hex color, eg: #FFF or #FFFFFF\n' +
            '  · any rbg color, eg: rgb(255,255,255)\n' +
            '  → ')
        return PixelColor.of(background_color)

    @staticmethod
    def input_foreground_color() -> 'PixelColor':
        foreground_color: Final[str] = input(
            'Please enter a foreground color with an alpha value:\n' +
            '  · any hexa color, eg: #0007 or #0000007F\n' +
            '  · any rgba color, eg rgba(0,0,0,127)\n' +
            '  → ')
        return PixelColor.of(foreground_color)

    @staticmethod
    def input_gradient_steps() -> int:
        return int(input(
            'Please enter a number of gradient steps\n' +
            'between the background and foreground colors:\n' +
            '  → '))

    def get_imposed_gradient(self: 'PixelColor', imposed: 'PixelColor', gradient_steps: int) -> list['PixelColor']:
        gradient_alphas: Final[list[int]] = [round(255 * step / (gradient_steps + 1)) for step in range(1, gradient_steps + 1)]
        imposed_alphas: Final[list['PixelColor']] = [imposed.get_imposed_alpha(alpha) for alpha in gradient_alphas]
        return [self.get_imposed_color(imposed_alpha) for imposed_alpha in imposed_alphas]

    def get_imposed_alpha(self: 'PixelColor', alpha: int) -> 'PixelColor':
        return PixelColor(RGBAColor.of((self.red, self.green, self.blue, alpha)))

    def get_imposed_color(self: 'PixelColor', imposed: 'PixelColor') -> 'PixelColor':
        red: Final[int] = self._calculate_target_hue(self.red, imposed.red, imposed.alpha)
        green: Final[int] = self._calculate_target_hue(self.green, imposed.green, imposed.alpha)
        blue: Final[int] = self._calculate_target_hue(self.blue, imposed.blue, imposed.alpha)

        return PixelColor(RGBColor.of((red, green, blue)))

    @staticmethod
    def _calculate_target_hue(background_hue: int, foreground_hue: int, a: int) -> int:
        alpha: Final[float] = float(a / 255)
        return int(((1 - alpha) * background_hue) + (alpha * foreground_hue))

    def to_string(self: 'PixelColor') -> str:
        return self.color.to_string()

    def to_hex_string(self: 'PixelColor') -> str:
        return self.color.to_hex_string()
