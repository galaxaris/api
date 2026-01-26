from dataclasses import dataclass

from api.Texture import Texture
from api.Utils.Tag import Tag


@dataclass()
class Animation:
    frames: list[Texture]
    frame_duration: float  # Duration of each frame in seconds
    trigger: Tag # Whether the animation is triggered
    loop: bool = True  # Whether the animation should loop
    def get_frame(self, time: float) -> Texture:
        total_duration = len(self.frames) * self.frame_duration
        if not self.loop and time >= total_duration:
            return self.frames[-1]
        time = time % total_duration
        frame_index = int(time / self.frame_duration)
        return self.frames[frame_index]
