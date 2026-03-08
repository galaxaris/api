"""Scene composition and layered rendering."""

import pygame as pg
from typing import Dict, List, Optional
from api.GameObject import GameObject
from api.UI.GameUI import GameUI
from api.engine.GameCamera import GameCamera
from api.environment.Background import Background
from api.environment.Parallax import ParallaxBackground
from api.utils import GlobalVariables


class Scene(pg.Surface):
    """
    Scene class, based on pygame.Surface. Represents a game scene, containing game objects, layers, a camera, and a background.

    The Scene is responsible for managing the rendering of game objects, handling the camera's position and movement, and drawing the background.
    """
    def __init__(self, size: tuple[int, int]):
        """
        Initializes the Scene with a given size.

        :param size: Size of the scene (width, height)
        """
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
        """
        **Private method**

        Ensures that a layer with the given name exists. If it doesn't, it creates it.

        :param layer_name: Name of the layer to ensures existence of
        """
        if layer_name not in self.layers:
            self.layers[layer_name] = []
            surf = pg.Surface(self.size, pg.SRCALPHA).convert_alpha()
            self.layer_surfaces[layer_name] = surf
            if layer_name == "default":
                self.layer_order.insert(0, layer_name)
            else:
                self.layer_order.append(layer_name)

    def add_surface(self, surface: pg.Surface, layer: str = "default"):
        """
        Adds a surface to the specified layer. If the layer doesn't exist, it will be created.
        
        :param surface: The surface to be added
        :param layer: The name of the layer to which the surface should be added (default is "default")
        """

        self.__ensure_layer(layer)
        self.layer_surfaces[layer].blit(surface, (0, 0))

    def add(self, game_object: GameObject, layer: str = "default"):
        """
        Adds a game object to the specified layer. If the layer doesn't exist, it will be created.
        """
        self.__ensure_layer(layer)
        if game_object.id not in [obj.id for obj in self.layers[layer]]:
            self.layers[layer].append(game_object)
            self.game_objects.append(game_object)

    def remove(self, game_object: GameObject, layer: str = "default"):
        """
        Removes a game object from the specified layer.
        """
        if layer in self.layers and game_object in self.layers[layer]:
            self.layers[layer].remove(game_object)
            self.game_objects.remove(game_object)

    def set_layer(self,  index: int, layer: str):
        """
        **z-index** equivalent

        Sets the rendering order of the specified layer by moving it to the given index in the layer order list.

        :param index: The new index for the layer in the rendering order (0 is the bottom layer)
        :param layer: The name of the layer to be reordered
        """
        self.__ensure_layer(layer)
        if layer in self.layer_order:
            self.layer_order.remove(layer)
        self.layer_order.insert(max(0, min(index, len(self.layer_order))), layer)

    def set_background(self, p_bg: Background | ParallaxBackground):
        """
        Sets an amazing (or not) background: static or parallax, the universe is yours!
        """
        self.background = p_bg

    def draw(self, screen: pg.Surface):
        """
        Draws the scene. Handles correct rendering of different layers

        :param screen: The surface on which the scene should be drawn (usually the main display surface)
        """
        self.fill((0, 0, 0))
        GlobalVariables.set_variable("game_objects", self.game_objects)
        GlobalVariables.set_variable("default_surface", self.default_surface)

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
        """
        Clears all layers and the default surface. Useful for resetting the scene before redrawing.
        """
        for layer in self.layers:
            self.layers[layer].clear()



