from enum import Enum
from math import pi
from typing import Final, Optional

from util.rgb_color import RGBColor


class DotifyColoring(Enum):
    CONSTANT = 'constant'
    MEAN = 'mean'
    MODE = 'mode'

    @staticmethod
    def from_string(coloring: str) -> 'DotifyColoring':
        match coloring.lower():
            case 'constant':
                return DotifyColoring.CONSTANT
            case 'mode':
                return DotifyColoring.MODE
            case 'mean' | _:
                return DotifyColoring.MEAN

    # region get_color
    def get_color(self: 'DotifyColoring', color_frequencies: dict[RGBColor, int],
                  background_color: RGBColor, foreground_color: RGBColor) -> RGBColor:
        match self:
            case DotifyColoring.CONSTANT:
                return foreground_color
            case DotifyColoring.MEAN:
                return self._get_mean_color(color_frequencies, background_color)
            case DotifyColoring.MODE:
                return self._get_mode_color(color_frequencies)

    @staticmethod
    def _get_mean_color(color_frequencies: dict[RGBColor, int], background_color: RGBColor) -> RGBColor:
        red: Final[int] = DotifyColoring._get_mean_component_color(0, color_frequencies, background_color)
        green: Final[int] = DotifyColoring._get_mean_component_color(1, color_frequencies, background_color)
        blue: Final[int] = DotifyColoring._get_mean_component_color(2, color_frequencies, background_color)

        return RGBColor(red, green, blue)

    @staticmethod
    def _get_mean_component_color(component: int, color_frequencies: dict[RGBColor, int], background_color: RGBColor) -> int:
        mean_freq: Final[int] = sum(color_frequencies.values())

        return background_color[component] + round(sum([
            (color[component] - background_color[component]) * freq
            for color, freq in color_frequencies.items()
        ]) / mean_freq)

    @staticmethod
    def _get_mode_color(color_frequencies: dict[RGBColor, int]) -> RGBColor:
        return max(color_frequencies, key=color_frequencies.get)
    # endregion get_color

    # region get_frequency
    def get_frequency(self: 'DotifyColoring', color_frequencies: dict[RGBColor, int],
                      background_color: RGBColor, foreground_color: RGBColor) -> int:
        match self:
            case DotifyColoring.CONSTANT:
                return self._get_constant_frequency(color_frequencies, background_color, foreground_color)
            case DotifyColoring.MEAN:
                return self._get_mean_frequency(color_frequencies)
            case DotifyColoring.MODE:
                return self._get_mode_frequency(color_frequencies, foreground_color)

    @staticmethod
    def _get_constant_frequency(color_frequencies: dict[RGBColor, int],
                                background_color: RGBColor, foreground_color: RGBColor) -> int:
        mean_freq: Final[int] = sum(color_frequencies.values())
        if mean_freq == 0:
            return 0

        red_bias: Final[Optional[float]] = DotifyColoring._get_component_bias(0, color_frequencies, background_color, foreground_color)
        green_bias: Final[Optional[float]] = DotifyColoring._get_component_bias(1, color_frequencies, background_color, foreground_color)
        blue_bias: Final[Optional[float]] = DotifyColoring._get_component_bias(2, color_frequencies, background_color, foreground_color)

        biases: Final[list[float]] = [bias for bias in [red_bias, green_bias, blue_bias] if bias is not None]
        return round(((sum(biases) / len(biases)) * (4 / pi)) * mean_freq) if (len(biases) > 0) else 0

    @staticmethod
    def _get_component_bias(component: int, color_frequencies: dict[RGBColor, int],
                            background_color: RGBColor, foreground_color: RGBColor) -> Optional[float]:
        mean_freq: Final[int] = sum(color_frequencies.values())
        component_min: Final[int] = min(foreground_color[component], background_color[component])
        component_range: Final[int] = abs(foreground_color[component] - background_color[component])

        if component_range > 0:
            return sum([
                min(max(((color[component] - component_min) / component_range), 0), 1) * freq
                for color, freq in color_frequencies.items()
            ]) / mean_freq

    @staticmethod
    def _get_mean_frequency(color_frequencies: dict[RGBColor, int]) -> int:
        return sum(color_frequencies.values())

    @staticmethod
    def _get_mode_frequency(color_frequencies: dict[RGBColor, int], foreground_color: RGBColor) -> int:
        return color_frequencies[foreground_color]
    # endregion get_frequency

    # region dot_width
    def cap_max_dot_width(self: 'DotifyColoring', max_dot_width: float) -> float:
        match self:
            case DotifyColoring.CONSTANT:
                return max_dot_width * (4 / pi)
            case _:
                return max_dot_width - max(max_dot_width / 2.5, 2)
    # endregion dot_width
