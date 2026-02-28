from api.GameObject import GameObject
import pygame as pg

class Trigger(GameObject):
    _EDITOR = "placeable"
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], 
                 target_tag: str, actions: list[callable], once: bool = False):
        super().__init__(pos, size)
        
        self.add_tag("trigger")
        self.target_tag = target_tag
        self.actions = actions
        self.once = once

    def add_action(self, action):
        if not hasattr(self, "actions"):
            self.actions = []
        self.actions.append(action)

    def update(self, others):
        super().update(others)
        for obj in others:
            if self.target_tag in obj.tags:
                for action in self.actions:
                    action(obj)
                if self.once:
                    self.remove_tag("trigger")