import pygame as pg
from api.GameObject import GameObject
from api.environment.Background import Background


class Scene(pg.Surface):
    background: Background | None
    layers: dict[str, pg.Surface]
    layer_order: list[str]

    def __init__(self, width: int, height: int):
        super().__init__((width, height))
        self.layers = {}
        self.layer_order = []
        self.background = None

    def __add_layer(self, layer_name: str):
        if layer_name not in self.layers:
            surf = pg.Surface(self.get_size(), pg.SRCALPHA)
            self.layers[layer_name] = surf
            if layer_name not in self.layer_order:
                if layer_name == "default":
                    self.layer_order.insert(0, layer_name)
                else:
                    self.layer_order.append(layer_name)

    def add(self, game_object: GameObject, layer: str = "default"):
        self.__add_layer(layer)
        game_object.draw(self.layers[layer])

    def set_layer(self, order: int, layer: str):
        self.__add_layer(layer)
        if layer in self.layer_order:
            self.layer_order.remove(layer)
        self.layer_order.insert(order, layer)

    def clear_layer(self, layer: str):
        if layer in self.layers:
            self.layers[layer].fill((0, 0, 0, 0))  # Remplit de transparent

    def clear(self):
        self.layers = {}
        self.layer_order = []

    def draw(self, screen: pg.Surface):
        self.fill((0, 0, 0))

        if self.background:
            self.background.draw()

        for layer_name in self.layer_order:
            if layer_name in self.layers:
                self.blit(self.layers[layer_name], (0, 0))

        screen.blit(self, (0, 0))

    def remove_layer(self, layer: str):
        if layer in self.layers:
            del self.layers[layer]
        if layer in self.layer_order:
            self.layer_order.remove(layer)