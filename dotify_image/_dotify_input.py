from os import path
from typing import Tuple, Final

from PIL import ImageColor

from _dotify_method import DotifyMethod
from _dotify_pattern import DotifyPattern
from _rgb_color import RGBColor
from stack_images._image_format import ImageFormat


def get_input_image_path() -> str:
    file_path: Final[str] = input_input_image_path()
    if file_path == '' or file_path.lower() == 'stop':
        raise KeyboardInterrupt()
    elif ImageFormat.from_file_path(file_path) is None:
        raise ValueError('unsupported file format in path: "{}"'.format(file_path))
    else:
        return path.expanduser(file_path)


def input_input_image_path() -> str:
    return input(
        '\nPlease enter an image path or (stop)\n' +
        '  → ').strip()


def get_background_color() -> RGBColor:
    input_color: Final[str] = input_background_color()
    valid_color: Final[str] = input_color if input_color else 'black'
    return RGBColor.of(ImageColor.getrgb(valid_color))


def input_background_color() -> str:
    return input(
        'Would you like to specify a background color?\n' +
        '  If you do not, the default is black.\n' +
        '  → ').strip()


def get_dot_size(image_size: Tuple[int, int]) -> int:
    recommended_dot_size: Final[int] = max(min(image_size) // 100, 5)
    dot_size: Final[str] = input_dot_size(image_size, recommended_dot_size)
    return int(dot_size) if dot_size else recommended_dot_size


def input_dot_size(image_size: Tuple[int, int], recommended_dot_size: int) -> str:
    return input(
        'Would you like to specify a dot size?\n' +
        '  The original image size is {} px.\n'.format(image_size) +
        '  We recommend a dot size of {} px.\n'.format(recommended_dot_size) +
        '  → ').strip()


def get_method() -> DotifyMethod:
    method: Final[str] = input_method()
    return DotifyMethod.from_string(method)


def input_method() -> str:
    return input(
        'Would you like to specify a dot calculation method?\n' +
        '  (mean) or (mode):\n' +
        '  → ').strip()


def get_pattern() -> DotifyPattern:
    pattern: Final[str] = input_pattern()
    return DotifyPattern.from_string(pattern)


def input_pattern() -> str:
    return input(
        'Would you like to specify a dot placement pattern?\n' +
        '  (r)ectalinear or (h)exagonal:\n' +
        '  → ').strip()


def get_up_scaling() -> int:
    up_scaling: Final[str] = input_up_scaling()
    return int(up_scaling) if up_scaling else 1


def input_up_scaling() -> str:
    return input(
        'Would you like to up-scale the output image?\n' +
        '  If so, enter an up-scaling multiplier.\n' +
        '  → ').strip()


def get_output_image_path() -> str:
    file_path: Final[str] = input_output_image_path()
    valid_path: Final[str] = file_path if file_path else 'output.png'
    return ImageFormat.add_format_to_path(valid_path)


def input_output_image_path() -> str:
    return input(
        'Please enter an output image path:\n' +
        '  → ').strip()
