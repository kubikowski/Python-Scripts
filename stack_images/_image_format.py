from enum import Enum
from os import path
from typing import Final, Optional


class ImageFormat(Enum):
    JPG = 'jpeg'
    PNG = 'png'

    @staticmethod
    def from_file_path(file_path: str) -> Optional['ImageFormat']:
        sanitized_path: Final[str] = file_path.lower()
        file_extension: Final[str] = path.splitext(sanitized_path)[-1].strip('.')

        match file_extension:
            case 'jpg' | 'jpeg':
                return ImageFormat.JPG
            case 'png':
                return ImageFormat.PNG
            case _:
                return None

    @staticmethod
    def add_format_to_path(file_path: str) -> str:
        image_format: Final[ImageFormat] = ImageFormat.from_file_path(file_path)

        if image_format is not None:
            return file_path
        else:
            return file_path + '.png'
