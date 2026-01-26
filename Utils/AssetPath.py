from dataclasses import dataclass
from enum import Enum

class AssetProvider(Enum):
    GLOBAL = 1
    BUNDLED = 2

@dataclass
class AssetPath:
    file_path: str
    provided_by: AssetProvider