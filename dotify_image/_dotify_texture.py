from enum import Enum


class DotifyTexture(Enum):
    SMOOTH = 'SMOOTH'
    ROUGH = 'ROUGH'

    @staticmethod
    def from_string(sizing: str) -> 'DotifyTexture':
        match  sizing[0].lower() if sizing else '':
            case 's':
                return DotifyTexture.SMOOTH
            case 'r':
                return DotifyTexture.ROUGH
            case _:
                return DotifyTexture.SMOOTH
