import pygame as pg
from typing import Dict, List, Optional
from api.GameObject import GameObject
from api.UI.GameUI import GameUI
from api.engine.GameCamera import GameCamera
from api.environment.Background import Background
from api.environment.Parallax import ParallaxBackground
from api.utils import GlobalVariables


class Scene(pg.Surface):
    def __init__(self, size: tuple[int, int]):
        super().__init__(size)
        self.size = pg.Vector2(size)
        self.layers: Dict[str, List[GameObject]] = {}
        self.layer_order: List[str] = []
        self.layer_surfaces: Dict[str, pg.Surface] = {}
        self.game_objects: List[GameObject] = []
        self.camera : GameCamera = GameCamera((0, 0))
        self.background: Optional[Background | ParallaxBackground] = None
        self.UI = GameUI(size)
        size = pg.Vector2(size)
        self.default_surface = pg.Surface(size, pg.SRCALPHA).convert_alpha()

    def __ensure_layer(self, layer_name: str):
        if layer_name not in self.layers:
            self.layers[layer_name] = []
            surf = pg.Surface(self.size, pg.SRCALPHA).convert_alpha()
            self.layer_surfaces[layer_name] = surf
            if layer_name == "default":
                self.layer_order.insert(0, layer_name)
            else:
                self.layer_order.append(layer_name)

    def add_surface(self, surface: pg.Surface, layer: str = "default"):
        self.__ensure_layer(layer)
        self.layer_surfaces[layer].blit(surface, (0, 0))

    def add(self, game_object: GameObject, layer: str = "default"):
        self.__ensure_layer(layer)
        if game_object.id not in [obj.id for obj in self.layers[layer]]:
            self.layers[layer].append(game_object)
            self.game_objects.append(game_object)

    def remove(self, game_object: GameObject, layer: str = "default"):
        if layer in self.layers and game_object in self.layers[layer]:
            self.layers[layer].remove(game_object)
            self.game_objects.remove(game_object)

    def set_layer(self,  index: int, layer: str):
        self.__ensure_layer(layer)
        if layer in self.layer_order:
            self.layer_order.remove(layer)
        self.layer_order.insert(max(0, min(index, len(self.layer_order))), layer)

    def set_background(self, p_bg: Background | ParallaxBackground):
        self.background = p_bg

    def draw(self, screen: pg.Surface):
        self.fill((0, 0, 0))
        GlobalVariables.set_variable("game_objects", self.game_objects)

        #TODO: when pausing the game, stop the FPS completely (no more events)
        self.camera.update()

        if self.background:
            if isinstance(self.background, Background):
                self.set_layer(0, "_background")
                self.layer_surfaces["_background"].blit(self.background.draw(), (0, 0))
            elif isinstance(self.background, ParallaxBackground):
                self.set_layer(0, "_background")
                self.background.draw(self, self.camera.position, layer="background")

        if self.UI:
            self.set_layer(len(self.layer_order), "_UI")
            self.layer_surfaces["_UI"].fill((0, 0, 0, 0))
            self.UI.update()
            self.UI.draw(self.layer_surfaces["_UI"])


        for name in self.layer_order:
            if "_" in name:
                layer_surf = self.layer_surfaces[name]
                if "#" in name:
                    self.blit(layer_surf, pg.Vector2(0, 0) - self.camera.position)
                else:
                    self.blit(layer_surf, pg.Vector2(0, 0))
            elif "#" not in name:
                layer_surf = self.layer_surfaces[name]
                layer_surf.fill((0, 0, 0, 0))
                for obj in self.layers[name]:
                    obj.draw(layer_surf)
                self.blit(layer_surf, (0, 0))
            else:
                for obj in self.layers[name]:
                    relative_pos = obj.pos - self.camera.position
                    if -self.size.x - obj.size.x < relative_pos.x < self.size.x + obj.size.x:
                        obj.draw(self, offset=self.camera.position)


        self.blit(self.default_surface, (0, 0))
        screen.blit(self, (0, 0))

    def clear(self):
        for layer in self.layers:
            self.layers[layer].clear()



