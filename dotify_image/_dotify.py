from datetime import datetime
from math import sqrt
from random import random
from typing import Final, Dict

from PIL import Image, ImageDraw

from _dotify_cli import *
from _dotify_coloring import DotifyColoring
from _dotify_pattern import DotifyPattern
from _dotify_texture import DotifyTexture
from _rgb_color import RGB, RGBColor


class Dotify:

    def __init__(
        self: 'Dotify',
        input_image: Image.Image,
        background_color: RGBColor,
        dot_size: int,
        pattern: DotifyPattern,
        coloring: DotifyColoring,
        texture: DotifyTexture,
        up_scaling: int,
    ) -> None:
        start_time: Final[datetime] = output_start_time()

        self._input_image: Final[Image.Image] = input_image.convert(mode=RGB)
        self._background_color: Final[RGBColor] = background_color
        self._dot_size: Final[int] = dot_size
        self._pattern: Final[DotifyPattern] = pattern
        self._coloring: Final[DotifyColoring] = coloring
        self._texture: Final[DotifyTexture] = texture
        self._up_scaling: Final[int] = up_scaling

        self._output_image: Final[Image.Image] = self._get_initial_output_image()
        self._draw: Final[ImageDraw] = ImageDraw.Draw(im=self._output_image, mode=RGB)
        self._draw_pattern()

        output_end_time(start_time)

    @staticmethod
    def image(input_image: Image.Image) -> Image.Image:
        background_color: Final[RGBColor] = get_background_color()
        dot_size: Final[int] = get_dot_size(input_image.size)
        pattern: Final[DotifyPattern] = get_pattern()
        coloring: Final[DotifyColoring] = get_coloring()
        texture: Final[DotifyTexture] = get_texture()
        up_scaling: Final[int] = get_up_scaling()

        return Dotify(input_image, background_color, dot_size, pattern, coloring, texture, up_scaling)\
            ._output_image

    def _get_initial_output_image(self: 'Dotify') -> Image.Image:
        return Image.new(
            mode=RGB,
            size=(
                self._input_image.width * self._up_scaling,
                self._input_image.height * self._up_scaling,
            ),
            color=self._background_color,
        )

    def _draw_pattern(self: 'Dotify') -> None:
        match self._pattern:
            case DotifyPattern.RECTILINEAR:
                return self._draw_rectilinear_grid()
            case DotifyPattern.HEXAGONAL:
                return self._draw_hexagonal_grid()

    def _draw_rectilinear_grid(self: 'Dotify') -> None:
        for x_min in range(0, self._input_image.width, self._dot_size):
            for y_min in range(0, self._input_image.height, self._dot_size):
                self._draw_region(x_min, y_min)

    def _draw_hexagonal_grid(self: 'Dotify') -> None:
        line_height: Final[int] = round(self._dot_size * sqrt(3))
        for x_min in range(0, self._input_image.width, self._dot_size):
            for y_min in range(0, self._input_image.height, line_height):
                self._draw_region(x_min, y_min)
        for x_min in range(self._dot_size // 2, self._input_image.width, self._dot_size):
            for y_min in range(-(line_height // 2), self._input_image.height, line_height):
                self._draw_region(x_min, y_min)

    def _draw_region(self: 'Dotify', x_min: int, y_min: int) -> None:
        color_frequencies: Final[Dict[RGBColor, int]] = self._get_color_frequencies(x_min, y_min)
        if len(color_frequencies) > 0:
            color: Final[RGBColor] = self._get_color(color_frequencies)

            min_dot_width: Final[float] = self._get_min_dot_width(color_frequencies, color)
            max_dot_width: Final[float] = self._get_max_dot_width()
            dot_width: Final[float] = min(min_dot_width, max_dot_width)

            x_mid: Final[float] = self._get_x_mid(x_min)
            y_mid: Final[float] = self._get_y_mid(y_min)

            self._draw.ellipse(
                xy=(x_mid - dot_width, y_mid - dot_width, x_mid + dot_width, y_mid + dot_width),
                fill=color,
                outline=color,
            )

    def _get_color_frequencies(self: 'Dotify', x_min: int, y_min: int) -> Dict[RGBColor, int]:
        color_frequencies: Final[Dict[RGBColor, int]] = {}

        for x in range(x_min, self._get_x_max(x_min)):
            for y in range(y_min, self._get_y_max(y_min)):
                rgb_color: RGBColor = self._input_image.getpixel((x, y))
                if rgb_color != self._background_color:
                    if rgb_color not in color_frequencies:
                        color_frequencies[RGBColor.of(rgb_color)] = 0
                    color_frequencies[rgb_color] += 1

        return color_frequencies

    def _get_color(self: 'Dotify', color_frequencies: Dict[RGBColor, int]) -> RGBColor:
        match self._coloring:
            case DotifyColoring.MEAN:
                return self._get_mean_color(color_frequencies)
            case DotifyColoring.MODE:
                return self._get_mode_color(color_frequencies)

    def _get_mean_color(self: 'Dotify', color_frequencies: Dict[RGBColor, int]) -> RGBColor:
        mean_freq: Final[int] = sum(color_frequencies.values())

        red: Final[int] = self._background_color.red + round(sum([
            (color.red - self._background_color.red) * freq for color, freq in color_frequencies.items()
        ]) / mean_freq)
        green: Final[int] = self._background_color.green + round(sum([
            (color.green - self._background_color.green) * freq for color, freq in color_frequencies.items()
        ]) / mean_freq)
        blue: Final[int] = self._background_color.blue + round(sum([
            (color.blue - self._background_color.blue) * freq for color, freq in color_frequencies.items()
        ]) / mean_freq)

        return RGBColor(red, green, blue)

    @staticmethod
    def _get_mode_color(color_frequencies: Dict[RGBColor, int]) -> RGBColor:
        return max(color_frequencies, key=color_frequencies.get)

    def _get_frequency(self: 'Dotify', color_frequencies: Dict[RGBColor, int], color: RGBColor) -> int:
        match self._coloring:
            case DotifyColoring.MEAN:
                return self._get_mean_frequency(color_frequencies)
            case DotifyColoring.MODE:
                return self._get_mode_frequency(color_frequencies, color)

    @staticmethod
    def _get_mean_frequency(color_frequencies: Dict[RGBColor, int]) -> int:
        return sum(color_frequencies.values())

    @staticmethod
    def _get_mode_frequency(color_frequencies: Dict[RGBColor, int], color: RGBColor) -> int:
        return color_frequencies[color]

    def _get_min_dot_width(self: 'Dotify', color_frequencies: Dict[RGBColor, int], color: RGBColor) -> float:
        frequency: Final[int] = self._get_frequency(color_frequencies, color)
        return frequency / self._dot_size / 2 * self._up_scaling

    def _get_max_dot_width(self: 'Dotify') -> float:
        max_dot_width: Final[float] = self._dot_size / 2 * self._up_scaling
        capped_max_dot_width: Final[float] = max_dot_width - max(max_dot_width / 2.5, 2)
        match self._texture:
            case DotifyTexture.SMOOTH:
                return capped_max_dot_width
            case DotifyTexture.ROUGH:
                return capped_max_dot_width * ((4 + random()) / 5)

    def _get_x_max(self: 'Dotify', x_min: int) -> int:
        return min(x_min + self._dot_size, self._input_image.width)

    def _get_y_max(self: 'Dotify', y_min: int) -> int:
        return min(y_min + self._dot_size, self._input_image.height)

    def _get_x_mid(self: 'Dotify', x_min: int) -> float:
        return (x_min + self._get_x_max(x_min)) / 2 * self._up_scaling

    def _get_y_mid(self: 'Dotify', y_min: int) -> float:
        return (y_min + self._get_y_max(y_min)) / 2 * self._up_scaling
