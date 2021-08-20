from enum import Enum
from typing import Final, Optional


class ImageFormat(Enum):
    JPG = 'jpeg'
    PNG = 'png'

    @staticmethod
    def from_file_path(file_path: str) -> Optional['ImageFormat']:
        sanitized_path: Final[str] = file_path.lower()

        if sanitized_path.endswith('.jpg') or sanitized_path.endswith('.jpeg'):
            return ImageFormat.JPG
        if sanitized_path.endswith('.png'):
            return ImageFormat.PNG
        return None

    @staticmethod
    def add_format_to_path(file_path: str) -> str:
        image_format: ImageFormat = ImageFormat.from_file_path(file_path)

        if image_format is not None:
            return file_path
        else:
            return file_path + '.png'
