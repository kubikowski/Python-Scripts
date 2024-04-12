from enum import Enum
from random import random


class DotifyTexture(Enum):
    SMOOTH = 'SMOOTH'
    ROUGH = 'ROUGH'
    COARSE = 'COARSE'
    GLOSSY = 'GLOSSY'
    HOLY = 'HOLY'

    @staticmethod
    def from_string(texture: str) -> 'DotifyTexture':
        match texture[0].lower() if texture else '':
            case 's':
                return DotifyTexture.SMOOTH
            case 'r':
                return DotifyTexture.ROUGH
            case 'c':
                return DotifyTexture.COARSE
            case 'g':
                return DotifyTexture.GLOSSY
            case 'h':
                return DotifyTexture.HOLY
            case _:
                return DotifyTexture.SMOOTH

    def get_min_dot_width(self: 'DotifyTexture', min_dot_width: float) -> float:
        match self:
            case DotifyTexture.HOLY:
                return min_dot_width if random() >= 0.5 else 0
            case _:
                return min_dot_width

    def get_max_dot_width(self: 'DotifyTexture', max_dot_width: float) -> float:
        match self:
            case DotifyTexture.SMOOTH:
                return max_dot_width
            case DotifyTexture.ROUGH | DotifyTexture.HOLY:
                return max_dot_width * ((3 + random()) / 4)
            case DotifyTexture.COARSE:
                return max_dot_width * ((2 + random()) / 3)
            case DotifyTexture.GLOSSY:
                return max_dot_width * ((1 + random()) / 2)
