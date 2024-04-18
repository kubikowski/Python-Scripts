from os import path
from pathlib import Path
from typing import Final

from util.image_format import ImageFormat

__all__: Final[list[str]] = [
    'normalize_path',
    'get_input_image_path',
    'get_output_image_path',
]


def normalize_path(file_path: Path | str) -> Path:
    """Normalizes a file path, with tilde and variable expansion."""
    return Path(path.expandvars(path.expanduser(file_path)))


def get_input_image_path() -> Path:
    file_path: Final[str] = input_input_image_path()
    norm_path: Final[Path] = normalize_path(file_path)

    if file_path == '' or file_path.lower() == 'cancel':
        raise KeyboardInterrupt()
    if not path.exists(norm_path):
        raise ValueError('No file exists at the given path: "{}"'.format(file_path))
    if path.isdir(norm_path):
        raise ValueError('The given path is a directory: "{}"'.format(file_path))
    if ImageFormat.from_file_path(file_path) is None:
        raise ValueError('Unsupported image file format: "{}"'.format(file_path))

    return norm_path


def get_output_image_path() -> Path:
    file_path: Final[str] = input_output_image_path()
    valid_path: Final[str] = ImageFormat.PNG.format_path(file_path) if file_path else 'output.png'
    norm_path: Final[Path] = normalize_path(valid_path)

    if path.isdir(norm_path):
        raise ValueError('The given path is a directory: "{}"'.format(valid_path))
    if path.exists(norm_path) and not input_overwrite_file_path(valid_path):
        raise ValueError('Another file already exists at the given path: "{}"'.format(valid_path))

    return norm_path


def input_input_image_path() -> str:
    return input(
        'Please enter an image path or (cancel)\n' +
        '  → ').strip()


def input_output_image_path() -> str:
    return input(
        'Please enter an output image path:\n' +
        '  → ').strip()


def input_overwrite_file_path(file_path: str) -> bool:
    return input(
        'Another file already exists at the given path: "{}"\n'.format(file_path) +
        '  Would you like to overwrite it? [y/N]\n'
        '  → ').strip().lower().startswith('y')
