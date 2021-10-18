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
        return Orientation.from_string(orientation)

    @staticmethod
    def from_string(orientation: str) -> 'Orientation':
        match orientation[0].lower():
            case 'h':
                return Orientation.HORIZONTAL
            case 'v':
                return Orientation.VERTICAL
            case _:
                raise ValueError('Invalid Orientation: {}'.format(orientation))

    def resize_images(self: 'Orientation', images: list[Image]) -> list[Image]:
        min_size: Final[int] = self._get_min_image_size(images)
        return [self._resize_image(image, min_size) for image in images]

    def _get_min_image_size(self: 'Orientation', images: list[Image]) -> int:
        match self:
            case Orientation.HORIZONTAL:
                return min([i.size[1] for i in images])
            case Orientation.VERTICAL:
                return min([i.size[0] for i in images])

    def _resize_image(self: 'Orientation', image: Image, min_size: int) -> Image:
        match self:
            case Orientation.HORIZONTAL:
                scale_factor: Final[float] = float(image.size[0] / image.size[1])
                return image.resize([int(min_size * scale_factor), min_size])
            case Orientation.VERTICAL:
                scale_factor: Final[float] = float(image.size[1] / image.size[0])
                return image.resize([min_size, int(min_size * scale_factor)])

    def stack_images(self: 'Orientation', images: list[Image]) -> Image:
        match self:
            case Orientation.HORIZONTAL:
                return Image.fromarray(hstack(images))
            case Orientation.VERTICAL:
                return Image.fromarray(vstack(images))
