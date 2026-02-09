import pygame as pg
from typing import Dict, List, Optional
from api.GameObject import GameObject
from api.environment.Background import Background


class Scene(pg.Surface):
    def __init__(self, width: int, height: int):
        super().__init__((width, height))
        self.width = width
        self.height = height
        self.background: Optional[Background] = None
        self.layers: Dict[str, List[GameObject]] = {}
        self.layer_order: List[str] = []
        self.layer_surfaces: Dict[str, pg.Surface] = {}
        self.default_surface = pg.Surface((width, height), pg.SRCALPHA).convert_alpha()

    def __ensure_layer(self, layer_name: str):
        if layer_name not in self.layers:
            self.layers[layer_name] = []
            surf = pg.Surface((self.width, self.height), pg.SRCALPHA).convert_alpha()
            self.layer_surfaces[layer_name] = surf
            if layer_name == "default":
                self.layer_order.insert(0, layer_name)
            else:
                self.layer_order.append(layer_name)

    def add(self, game_object: GameObject, layer: str = "default"):
        self.__ensure_layer(layer)
        if game_object.id not in [obj.id for obj in self.layers[layer]]:
            self.layers[layer].append(game_object)

    def remove(self, game_object: GameObject, layer: str = "default"):
        if layer in self.layers and game_object in self.layers[layer]:
            self.layers[layer].remove(game_object)

    def set_layer(self,  index: int, layer: str):
        self.__ensure_layer(layer)
        if layer in self.layer_order:
            self.layer_order.remove(layer)
        self.layer_order.insert(max(0, min(index, len(self.layer_order))), layer)

    def draw(self, screen: pg.Surface):
        self.fill((0, 0, 0))

        if self.background:
            self.background.draw(self)



        for name in self.layer_order:
            layer_surf = self.layer_surfaces[name]
            layer_surf.fill((0, 0, 0, 0))

            for obj in self.layers[name]:
                obj.draw(layer_surf)

            self.blit(layer_surf, (0, 0))

        self.blit(self.default_surface, (0, 0))
        screen.blit(self, (0, 0))

        #Reset surface layers to avoid drawing artifacts



    def clear(self):
        for layer in self.layers:
            self.layers[layer].clear()