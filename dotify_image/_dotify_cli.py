from datetime import datetime
from os import path
from typing import List, Final, Tuple

from PIL import ImageColor

from _dotify_coloring import DotifyColoring
from _dotify_pattern import DotifyPattern
from _dotify_texture import DotifyTexture
from _rgb_color import RGBColor
from util.image_format import ImageFormat

__all__: Final[List[str]] = [
    'get_input_image_path',
    'get_background_color',
    'get_dot_size',
    'get_pattern',
    'get_coloring',
    'get_texture',
    'get_up_scaling',
    'get_output_image_path',
    'output_start_time',
    'output_end_time',
]


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
        '  → ').strip().strip("px")


def get_pattern() -> DotifyPattern:
    pattern: Final[str] = input_pattern()
    return DotifyPattern.from_string(pattern)


def input_pattern() -> str:
    return input(
        'Would you like to specify a dot placement pattern?\n' +
        '  (r)ectalinear or (h)exagonal:\n' +
        '  → ').strip()


def get_coloring() -> DotifyColoring:
    coloring: Final[str] = input_coloring()
    return DotifyColoring.from_string(coloring)


def input_coloring() -> str:
    return input(
        'Would you like to specify a coloring method?\n' +
        '  (mean) or (mode) color:\n' +
        '  → ').strip()


def get_texture() -> DotifyTexture:
    texture: Final[str] = input_texture()
    return DotifyTexture.from_string(texture)


def input_texture() -> str:
    return input(
        'Would you like to specify a dot texture?\n' +
        '  (s)mooth, (r)ough, (c)oarse, or (g)lossy:\n' +
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


def output_start_time() -> datetime:
    start_time: Final[datetime] = datetime.now()
    print('Generating dotified image...')
    return start_time


def output_end_time(start_time: datetime) -> None:
    end_time: Final[datetime] = datetime.now()
    elapsed_time: Final[datetime] = datetime.utcfromtimestamp((end_time - start_time).total_seconds())
    print('Completed in {} seconds.'.format(elapsed_time.strftime('%S.%f')[:-3]))
