from enum import Enum
from typing import Final


class DotifyMethod(Enum):
    MEAN = 'mean'
    MODE = 'mode'

    @staticmethod
    def from_input() -> 'DotifyMethod':
        pattern: Final[str] = input('(mean) or (mode): ').strip()
        return DotifyMethod.from_string(pattern)

    @staticmethod
    def from_string(method: str) -> 'DotifyMethod':
        match method.lower():
            case 'mean':
                return DotifyMethod.MEAN
            case 'mode':
                return DotifyMethod.MODE
            case _:
                return DotifyMethod.MEAN
