from enum import Enum


class DotifyColoring(Enum):
    MEAN = 'mean'
    MODE = 'mode'

    @staticmethod
    def from_string(coloring: str) -> 'DotifyColoring':
        match coloring.lower():
            case 'mean':
                return DotifyColoring.MEAN
            case 'mode':
                return DotifyColoring.MODE
            case _:
                return DotifyColoring.MEAN
