from dataclasses import dataclass

from api.Utils.AssetPath import AssetPath


@dataclass()
class Music:
    title: str
    duration: int  # duration in seconds
    loop: bool
    audio_path: AssetPath