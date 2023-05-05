from enum import Enum


class DotifyPattern(Enum):
    RECTILINEAR = 'rectilinear'
    HEXAGONAL = 'hexagonal'

    @staticmethod
    def from_string(pattern: str) -> 'DotifyPattern':
        match pattern[0].lower() if pattern else '':
            case 'r':
                return DotifyPattern.RECTILINEAR
            case 'h':
                return DotifyPattern.HEXAGONAL
            case _:
                return DotifyPattern.RECTILINEAR
