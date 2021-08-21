from enum import Enum
from typing import Final

from PIL import Image
from numpy import hstack, vstack


class Orientation(Enum):
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'

    @staticmethod
    def from_input() -> 'Orientation':
        orientation: Final[str] = input('(h)orizontal or (v)ertical: ')
        return Orientation.from_string(orientation[0].lower())

    @staticmethod
    def from_string(orientation: str) -> 'Orientation':
        if orientation == 'h':
            return Orientation.HORIZONTAL
        if orientation == 'v':
            return Orientation.VERTICAL

    def resize_images(self: 'Orientation', images: list[Image]) -> list[Image]:
        min_size: Final[int] = self._get_min_image_size(images)
        return [self._resize_image(image, min_size) for image in images]

    def _get_min_image_size(self: 'Orientation', images: list[Image]) -> int:
        if self == Orientation.HORIZONTAL:
            return min([i.size[1] for i in images])
        if self == Orientation.VERTICAL:
            return min([i.size[0] for i in images])

    def _resize_image(self: 'Orientation', image: Image, min_size: int) -> Image:
        if self == Orientation.HORIZONTAL:
            scale_factor: Final[float] = float(image.size[0] / image.size[1])
            return image.resize([int(min_size * scale_factor), min_size])

        if self == Orientation.VERTICAL:
            scale_factor: Final[float] = float(image.size[1] / image.size[0])
            return image.resize([min_size, int(min_size * scale_factor)])

    def stack_images(self: 'Orientation', images: list[Image]) -> Image:
        if self == Orientation.HORIZONTAL:
            return Image.fromarray(hstack(images))
        if self == Orientation.VERTICAL:
            return Image.fromarray(vstack(images))
