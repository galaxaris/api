from dataclasses import dataclass
from api.Utils.AssetPath import AssetPath


@dataclass()
class Texture:
    path: AssetPath
    opacity: int
    def load(self):
        # Placeholder for texture loading logic
        pass

    def unload(self):
        # Placeholder for texture unloading logic
        pass

