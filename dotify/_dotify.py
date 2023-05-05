from math import sqrt
from typing import Final, Tuple

from PIL import Image, ImageColor, ImageDraw

from dotify._dotify_pattern import DotifyPattern
from dotify._dotify_method import DotifyMethod

RGB: Final[str] = 'RGB'


class Dotify:

    def __init__(
            self: 'Dotify',
            input_image: Image.Image,
            background_color: Tuple[int, int, int],
            dot_size: int,
            method: DotifyMethod,
            up_scaling: int,
    ) -> None:
        self._input_image: Final[Image.Image] = input_image.convert(RGB)
        self._background_color: Final[Tuple[int, int, int]] = background_color
        self._dot_size: Final[int] = dot_size
        self._method: Final[DotifyMethod] = method
        self._up_scaling: Final[int] = up_scaling

        self._output_image: Final[Image.Image] = self._get_initial_output_image()
        self._draw = ImageDraw.Draw(self._output_image)

    @staticmethod
    def image(input_image: Image.Image) -> Image.Image:
        background_color: Final[Tuple[int, int, int]] = Dotify._input_background_color()
        dot_size: Final[int] = Dotify._input_dot_size(input_image)
        method: Final[DotifyMethod] = DotifyMethod.from_input()
        up_scaling: Final[int] = Dotify._input_up_scaling()
        dotify: Final[Dotify] = Dotify(input_image, background_color, dot_size, method, up_scaling)

        match DotifyPattern.from_input():
            case DotifyPattern.RECTILINEAR:
                return dotify._draw_rectilinear_grid()
            case DotifyPattern.HEXAGONAL:
                return dotify._draw_hexagonal_grid()

    @staticmethod
    def _input_dot_size(input_image: Image.Image) -> int:
        recommended_dot_size: Final[int] = min(input_image.size) // 100
        print('The original image size is {} px.'.format(input_image.size))
        print('We recommend a dot size of {} px.'.format(recommended_dot_size))
        input_dot_size: Final[str] = input('Dot Size (px): ').strip()
        return int(input_dot_size) if input_dot_size else recommended_dot_size

    @staticmethod
    def _input_background_color() -> Tuple[int, int, int]:
        print('Would you like to specify a background color?')
        print('If you do not, the default is black.')
        input_color: Final[str] = input('Background Color: ').strip()
        valid_color: Final[str] = input_color if input_color else 'black'
        return ImageColor.getrgb(valid_color)

    @staticmethod
    def _input_up_scaling() -> int:
        print('Would you like to up-scale the output image?')
        print('If so, enter an up-scaling multiplier.')
        input_up_scale: Final[str] = input('Output up-scale: ').strip()
        return int(input_up_scale) if input_up_scale else 1

    def _get_initial_output_image(self: 'Dotify') -> Image.Image:
        size: Final[Tuple[int, int]] = (
            self._input_image.width * self._up_scaling,
            self._input_image.height * self._up_scaling,
        )

        return Image.new(RGB, size, self._background_color)

    def _draw_rectilinear_grid(self: 'Dotify') -> Image.Image:
        for x_min in range(0, self._input_image.width, self._dot_size):
            for y_min in range(0, self._input_image.height, self._dot_size):
                self._draw_region(x_min, y_min)

        return self._output_image

    def _draw_hexagonal_grid(self: 'Dotify') -> Image.Image:
        line_height: Final[int] = round(self._dot_size * sqrt(3))

        for x_min in range(0, self._input_image.width, self._dot_size):
            for y_min in range(0, self._input_image.height, line_height):
                self._draw_region(x_min, y_min)

        for x_min in range(self._dot_size // 2, self._input_image.width, self._dot_size):
            for y_min in range(-(line_height // 2), self._input_image.height, line_height):
                self._draw_region(x_min, y_min)

        return self._output_image

    def _draw_region(self: 'Dotify', x_min: int, y_min: int) -> None:
        color_frequencies: Final[dict] = self._get_color_frequencies(x_min, y_min)

        if len(color_frequencies) > 0:
            color: Final[Tuple[int, int, int]] = self._get_color(color_frequencies)
            frequency: Final[int] = self._get_frequency(color_frequencies, color)

            min_dot_width: Final[float] = (frequency / self._dot_size / 2 * self._up_scaling)
            max_dot_width: Final[float] = (self._dot_size / 2 * self._up_scaling)
            capped_max_dot_width: Final[float] = max_dot_width - max(max_dot_width / 2.5, 2)
            dot_width: Final[float] = min(min_dot_width, capped_max_dot_width)

            x_mid: Final[float] = self._get_x_mid(x_min)
            y_mid: Final[float] = self._get_y_mid(y_min)

            self._draw.ellipse(
                xy=(
                    x_mid - dot_width,
                    y_mid - dot_width,
                    x_mid + dot_width,
                    y_mid + dot_width,
                ),
                fill=color,
                outline=color,
            )

    def _get_color_frequencies(self: 'Dotify', x_min: int, y_min: int) -> dict:
        color_frequencies: Final[dict] = {}

        for x in range(x_min, self._get_x_max(x_min)):
            for y in range(y_min, self._get_y_max(y_min)):
                rgb_color: Tuple[int, int, int] = self._input_image.getpixel((x, y))

                if rgb_color != self._background_color:
                    if rgb_color not in color_frequencies:
                        color_frequencies[rgb_color] = 0
                    color_frequencies[rgb_color] += 1

        return color_frequencies

    def _get_color(self: 'Dotify', color_frequencies: dict) -> Tuple[int, int, int]:
        match self._method:
            case DotifyMethod.MEAN:
                return self._get_mean_color(color_frequencies)
            case DotifyMethod.MODE:
                return self._get_mode_color(color_frequencies)

    def _get_mean_color(self: 'Dotify', color_frequencies: dict) -> Tuple[int, int, int]:
        mean_freq: Final[int] = sum(color_frequencies.values())

        red: Final[int] = self._background_color[0] + round(sum([
            (color[0] - self._background_color[0]) * freq for color, freq in color_frequencies.items()
        ]) / mean_freq)
        green: Final[int] = self._background_color[1] + round(sum([
            (color[1] - self._background_color[1]) * freq for color, freq in color_frequencies.items()
        ]) / mean_freq)
        blue: Final[int] = self._background_color[2] + round(sum([
            (color[2] - self._background_color[2]) * freq for color, freq in color_frequencies.items()
        ]) / mean_freq)

        return red, green, blue

    def _get_mode_color(self: 'Dotify', color_frequencies: dict) -> Tuple[int, int, int]:
        return max(color_frequencies, key=color_frequencies.get)

    def _get_frequency(self: 'Dotify', color_frequencies: dict, color: Tuple[int, int, int]) -> int:
        match self._method:
            case DotifyMethod.MEAN:
                return self._get_mean_frequency(color_frequencies)
            case DotifyMethod.MODE:
                return self._get_mode_frequency(color_frequencies, color)

    def _get_mean_frequency(self: 'Dotify', color_frequencies: dict) -> int:
        return sum(color_frequencies.values())

    def _get_mode_frequency(self: 'Dotify', color_frequencies: dict, color: Tuple[int, int, int]) -> int:
        return color_frequencies[color]

    def _get_x_max(self: 'Dotify', x_min: int) -> int:
        return min(x_min + self._dot_size, self._input_image.width)

    def _get_y_max(self: 'Dotify', y_min: int) -> int:
        return min(y_min + self._dot_size, self._input_image.height)

    def _get_x_mid(self: 'Dotify', x_min: int) -> float:
        return (x_min + self._get_x_max(x_min)) / 2 * self._up_scaling

    def _get_y_mid(self: 'Dotify', y_min: int) -> float:
        return (y_min + self._get_y_max(y_min)) / 2 * self._up_scaling
