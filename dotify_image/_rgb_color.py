from typing import Final, NamedTuple, Tuple

RGB: Final[str] = 'RGB'


class RGBColor(NamedTuple):
    red: int
    green: int
    blue: int

    @staticmethod
    def of(color: Tuple[int, int, int]) -> 'RGBColor':
        return RGBColor(color[0], color[1], color[2])
