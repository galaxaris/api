from dataclasses import dataclass

from api.Texture import Texture


@dataclass()
class Background:
    texture: Texture
    repeat_x: bool
    repeat_y: bool
    scroll_speed_x: float
    scroll_speed_y: float
    def get_offset(self, time: float) -> tuple[float, float]:
        offset_x = (self.scroll_speed_x * time) % self.texture.width if self.repeat_x else 0
        offset_y = (self.scroll_speed_y * time) % self.texture.height if self.repeat_y else 0
        return offset_x, offset_y

    def set_texture(self, new_texture: Texture):
        self.texture = new_texture
    def set_repeat(self, repeat_x: bool, repeat_y: bool):
        self.repeat_x = repeat_x
        self.repeat_y = repeat_y
    def set_scroll_speed(self, scroll_speed_x: float, scroll_speed_y: float):
        self.scroll_speed_x = scroll_speed_x
        self.scroll_speed_y = scroll_speed_y

class ParallaxBackground(Background):
    layers: list[tuple[Texture, float, float]]  # List of (texture, scroll_speed_x, scroll_speed_y)

    def get_layer_offsets(self, time: float) -> list[tuple[float, float]]:
        offsets = []
        for texture, speed_x, speed_y in self.layers:
            offset_x = (speed_x * time) % texture.width if self.repeat_x else 0
            offset_y = (speed_y * time) % texture.height if self.repeat_y else 0
            offsets.append((offset_x, offset_y))
        return offsets
    def add_layer(self, texture: Texture, scroll_speed_x: float, scroll_speed_y: float):
        self.layers.append((texture, scroll_speed_x, scroll_speed_y))
    def remove_layer(self, index: int):
        if 0 <= index < len(self.layers):
            self.layers.pop(index)
    def set_layer_scroll_speed(self, index: int, scroll_speed_x: float, scroll_speed_y: float):
        if 0 <= index < len(self.layers):
            texture, _, _ = self.layers[index]
            self.layers[index] = (texture, scroll_speed_x, scroll_speed_y)
    def set_layers(self, layers: list[tuple[Texture, float, float]]):
        self.layers = layers
    def clear_layers(self):
        self.layers.clear()
    def __post_init__(self):
        if not hasattr(self, 'layers'):
            self.layers = []
    def __init__(self, texture: Texture, repeat_x: bool, repeat_y: bool,
                 scroll_speed_x: float, scroll_speed_y: float,
                 layers: list[tuple[Texture, float, float]] = None):
        super().__init__(texture, repeat_x, repeat_y, scroll_speed_x, scroll_speed_y)
        self.layers = layers if layers is not None else []
