from enum import Enum


class DotifyMethod(Enum):
    MEAN = 'mean'
    MODE = 'mode'

    @staticmethod
    def from_string(method: str) -> 'DotifyMethod':
        match method.lower():
            case 'mean':
                return DotifyMethod.MEAN
            case 'mode':
                return DotifyMethod.MODE
            case _:
                return DotifyMethod.MEAN
