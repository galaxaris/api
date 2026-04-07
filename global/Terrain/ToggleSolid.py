import pygame as pg
from api.environment.Solid import Solid


class ToggleSolid(Solid):
    def __init__(self, pos, size):
        super().__init__(pos,size)

    def set_state(self, state):
        if(state):
            self.add_tag("solid")
        else:
            self.remove_tag("solid")

    def get_state(self):
        return "solid" in self.tags


    #TODO: Subscribe to event

    def toggle(self):
        self.set_state(not self.get_state())

