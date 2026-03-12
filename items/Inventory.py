from api.UI.GameUI import UIElement, GameUI
import pygame as pg


class Inventory(UIElement):
    def __init__(self, pos: tuple[int,int]|pg.Vector2 = (0,0), size: tuple[int,int]|pg.Vector2 = (0,0)):
        super().__init__(pos, size)
        self.items = []
        self.UI = GameUI(size)
