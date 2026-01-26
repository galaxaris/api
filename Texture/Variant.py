from dataclasses import dataclass

from api.Texture import Texture

@dataclass()
class Variant:
    HOVER: Texture
    PRESSED: Texture
    IN_COLLISION: Texture
    DESTROYED: Texture
    DISABLED: Texture
