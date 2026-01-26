from dataclasses import dataclass
from enum import Enum

class TextureProvider(Enum):
    GLOBAL = 1
    BUNDLED = 2

@dataclass()
class Texture:
    file_path: str
    provided_by: TextureProvider
    opacity: int
    def load(self):
        # Placeholder for texture loading logic
        pass

    def unload(self):
        # Placeholder for texture unloading logic
        pass

