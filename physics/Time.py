"""
API's Time class, for tracking time in the physics engine: clock FPS, delta time, and total time.
"""

import time
import pygame as pg


class Time:
    clock: pg.time.Clock
    lockedFPS: bool
    maxFps: int
    deltaTime: float
    totalTime: float

    def __init__(self, maxFps):
        self.clock = pg.time.Clock()
        #To be removed when using deltaTime: not useful anymore. Let escape the True power of computers!!
        #Without limit, the Game Engine is more precise
        self.lockedFPS = True 
        self.maxFps = maxFps
        self.deltaTime = 0
        self.totalTime = 0

    def get_ticks():
        ...

    def timeSinceLevelLoad():
        ...

    


    def update(self):
        self.totalTime += self.deltaTime
        if self.lockedFPS:              
            self.deltaTime = self.clock.tick(self.maxFps) / 1000 #1000 for making 1s
        else:                            
            self.deltaTime = self.clock.tick() / 1000 #1000 for making 1s
