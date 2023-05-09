from enum import Enum


class DotifyTexture(Enum):
    SMOOTH = 'SMOOTH'
    ROUGH = 'ROUGH'
    COARSE = 'COARSE'
    GLOSSY = 'GLOSSY'

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
            case _:
                return DotifyTexture.SMOOTH
