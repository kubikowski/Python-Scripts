from enum import Enum
from typing import Final


class DotifyPattern(Enum):
    RECTILINEAR = 'rectilinear'
    HEXAGONAL = 'hexagonal'

    @staticmethod
    def from_input() -> 'DotifyPattern':
        pattern: Final[str] = input('(r)ectalinear or (h)exagonal: ')
        return DotifyPattern.from_string(pattern)

    @staticmethod
    def from_string(pattern: str) -> 'DotifyPattern':
        match pattern[0].lower():
            case 'r':
                return DotifyPattern.RECTILINEAR
            case 'h':
                return DotifyPattern.HEXAGONAL
            case _:
                raise ValueError('Invalid DotifyPattern: {}'.format(pattern))
