from enum import Enum
from os import path
from pathlib import Path
from typing import Final, Optional


class ImageFormat(Enum):
    JPEG = 'jpeg'
    PNG = 'png'
    TIFF = 'tiff'
    WEBP = 'webp'

    @staticmethod
    def from_file_path(file_path: Path | str) -> Optional['ImageFormat']:
        file_extension: Final[str] = path.splitext(file_path)[-1].strip('.').lower()

        match file_extension:
            case 'jpg' | 'jpeg':
                return ImageFormat.JPEG
            case 'png':
                return ImageFormat.PNG
            case 'tif' | 'tiff':
                return ImageFormat.TIFF
            case 'webp':
                return ImageFormat.WEBP
            case _:
                return None

    def format_path(self: 'ImageFormat', file_path: Path | str) -> str:
        current_format: Final[ImageFormat] = ImageFormat.from_file_path(file_path)

        if current_format is None:
            return '{}.{}'.format(file_path, self.value)
        else:
            return file_path
