"""
Name: Rename Images
Author: Nathaniel Holden
Version: 0.0.3
Date: 2024-4-09

Inputs:
  · A working directory.
  · Whether to recursively include subdirectories.
  · Validations for each potential image to rename.
"""
from os import listdir, path, rename
from pathlib import Path
from time import ctime, strftime, strptime
from typing import Final

from util.image_format import ImageFormat


def rename_images() -> None:
    working_dir: Final[Path] = input_working_dir()
    recursive: Final[bool] = include_sub_dirs(working_dir)
    rename_images_in_dir(working_dir, working_dir, recursive)


def input_working_dir() -> Path:
    working_dir: Final[str] = input(
        'Enter a directory path:\n' +
        '  → ').strip()

    return Path(path.expandvars(path.expanduser(working_dir)))


def include_sub_dirs(working_dir: Path) -> bool:
    return len(get_sub_dirs(working_dir)) > 0 and input_include_sub_dirs(working_dir)


def input_include_sub_dirs(working_dir: Path) -> bool:
    print('\nThis directory also contains the following subdirectories:')

    for sub_dir in get_sub_dirs(working_dir):
        print_sub_dir(working_dir, sub_dir)

    return input(
        '\nWould you like to rename images in these subdirectories as well? Y/[N]' +
        '\n  → ').strip().lower().startswith('y')


def print_sub_dir(working_dir: Path, active_dir: Path) -> None:
    relative_path: Final[str] = path.relpath(active_dir, working_dir)
    print('  → {}'.format(relative_path))

    for sub_dir in get_sub_dirs(active_dir):
        print_sub_dir(working_dir, sub_dir)


def rename_images_in_dir(working_dir: Path, active_dir: Path, recursive: bool) -> None:
    print_active_dir(working_dir, active_dir)

    for file_path in get_files(active_dir):
        print_file_metadata(file_path)

        if ImageFormat.from_file_path(file_path) is not None:
            verify_rename_image(file_path)

    if recursive:
        for sub_dir in get_sub_dirs(active_dir):
            rename_images_in_dir(working_dir, sub_dir, recursive)


def print_active_dir(working_dir: Path, active_dir: Path) -> None:
    relative_path: Final[str] = path.relpath(active_dir, working_dir)
    display_path: Final[str] = str(working_dir) if working_dir == active_dir else relative_path
    print(
        '\n# - {} #'.format('Directory: '.ljust(73, '-')) +
        '\n# {} #'.format(str(display_path).ljust(75, ' ')) +
        '\n# {} #'.format(''.ljust(75, '-')))


def get_sub_dirs(working_dir: Path) -> list[Path]:
    handles: Final[list[Path]] = [working_dir / handle for handle in listdir(working_dir)]
    return [handle for handle in handles if path.isdir(handle)]


def get_files(working_dir: Path) -> list[Path]:
    handles: Final[list[Path]] = [working_dir / handle for handle in listdir(working_dir)]
    return [handle for handle in handles if path.isfile(handle)]


def print_file_metadata(file_path: Path) -> None:
    file_name: Final[str] = path.split(file_path)[-1]
    print(
        '\nFile Name: "{}"'.format(file_name) +
        '\n  → Contents Modified: {}'.format(timestamp(path.getmtime(file_path))) +
        '\n  → Metadata Modified: {}'.format(timestamp(path.getctime(file_path))) +
        '\n  → Accessed:          {}'.format(timestamp(path.getatime(file_path))))


def verify_rename_image(file_path: Path) -> None:
    if has_timestamp_file_name(file_path):
        print_has_timestamp_file_name()
        return

    if input_should_rename_image(file_path):
        new_file_path: Final[Path] = get_new_file_path(file_path)
        rename(file_path, new_file_path)
        print_file_renamed(file_path, new_file_path)


def has_timestamp_file_name(file_path: Path) -> bool:
    file_name: Final[str] = path.splitext(path.split(file_path)[-1])[0]
    new_file_name: Final[str] = path.splitext(get_new_file_name(file_path))[0]
    return file_name == new_file_name


def print_has_timestamp_file_name() -> None:
    print('  → Already uses a timestamp as its file name.')


def input_should_rename_image(file_path: Path) -> bool:
    image_format: Final[ImageFormat] = ImageFormat.from_file_path(file_path)
    new_file_name: Final[str] = get_new_file_name(file_path)
    return input(
        '  → Recognized as {}\n'.format(image_format) +
        '  → Would you like to rename this file as "{}"? Y/[N]\n'.format(new_file_name) +
        '  → ').strip().lower().startswith('y')


def print_file_renamed(file_path: Path, new_file_path: Path) -> None:
    file_name: Final[str] = path.split(file_path)[-1]
    new_file_name: Final[str] = path.split(new_file_path)[-1]
    print(
        '\nFile Renamed Successfully:' +
        '\n  → Old File Name: "{}"'.format(file_name) +
        '\n  → New File Name: "{}"'.format(new_file_name))


def get_new_file_path(file_path: Path) -> Path:
    working_dir = path.split(file_path)[0]
    new_file_name: Final[str] = get_new_file_name(file_path)
    return Path(working_dir) / new_file_name


def get_new_file_name(file_path: Path) -> str:
    image_format: Final[ImageFormat] = ImageFormat.from_file_path(file_path)
    return image_format.format_path(timestamp(path.getmtime(file_path)))


def timestamp(epoch_millis: float) -> str:
    return strftime('%Y-%m-%d %H:%M:%S', strptime(ctime(epoch_millis)))


if __name__ == '__main__':
    rename_images()
