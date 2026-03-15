"""
API's Time class, for tracking time in the physics engine: clock FPS, delta time, and total time.
"""

import time
import pygame as pg


class Time:
    """
    Manages time-related functionalities for the game, including tracking delta time, total time, and FPS locking.
    """
    clock: pg.time.Clock
    lockedFPS: bool
    maxFps: int
    _deltaTime: float

    #NOTE: deltaTime = frameScale for clarity reason and harmonization with Unity's Time class
    deltaTime: float
    totalTime: float
    frameScale: float
    maxDeltaTime: float

    def __init__(self, maxFps:int):
        """
        Initialize the Time class with a maximum FPS limit.

        NOTE: All clock properties are still accessessible through Time.clock

        :param maxFps: Maximum frames per second to lock the game loop to.
        """

        #NOTE: All clock properties are still accessessible through Time.clock
        self.timeScale = 1
        self.clock = pg.time.Clock()
        #Let escape the True power of computers!!
        #Without limit, the Game Engine is more precise but more hazardous
        self.lockedFPS = True 
        self.maxFps = maxFps
        #_deltaTime is the real delta time (calculated with the clock). deltaTime is the scaled delta time
        self._deltaTime = 1 / max(1, maxFps)
        self.totalTime = 0
        #Prevent physics jumps when the loop is frozen for whatever reason. Activated only after 1/20 = 50ms
        self.maxDeltaTime = 1 / 20
        #1.0 ~= one frame at target FPS. => Harmonizes physics calculations across different frame rates. (0.5 = half a frame, 2 =two frames)
        self.frameScale = self._deltaTime * max(1, self.maxFps)
        self.deltaTime = self.frameScale
        self.chronos : dict[str, float] = {}

    def get_ticks(self) -> int:
        """
        Get the number of milliseconds since the Time class was initialized.

        :return: Milliseconds since initialization.
        """
        return int(self.totalTime * 1000)

    def start_chrono(self, name: str):
        """
        Start a named chronometer for measuring elapsed time.

        :param name: Identifier for the chronometer.
        """
        if name not in self.chronos:
            self.chronos[name] = self.totalTime

    def get_chrono(self, name: str) -> float:
        """
        Get the elapsed time in seconds for a named chronometer.

        :param name: Identifier for the chronometer.
        :return: Elapsed time in seconds, or -1 if the chronometer does not exist.
        """
        if name in self.chronos:
            return self.totalTime - self.chronos[name]
        return -1

    def stop_chrono(self, name: str):
        """
        Stop a named chronometer and return the elapsed time in seconds.

        :param name: Identifier for the chronometer.
        :return: Elapsed time in seconds, or -1 if the chronometer does not exist.
        """
        if name in self.chronos:
            elapsed = self.totalTime - self.chronos[name]
            del self.chronos[name]
            return elapsed
        return -1

    def update(self):
        """Update the Time instance by calculating delta time and total time.

        :param time_instance: The Time instance to update.
        """
        self.totalTime += self._deltaTime
        if self.lockedFPS:
            raw_delta = self.clock.tick(self.maxFps) / 1000 #1000 for making 1s
        else:
            raw_delta = self.clock.tick() / 1000 #1000 for making 1s

        self._deltaTime = min(raw_delta, self.maxDeltaTime)
        self.frameScale = self._deltaTime * max(1, self.maxFps) * self.timeScale

        #NOTE: deltaTime = frameScale for clarity reason and harmonization with Unity's Time class
        self.deltaTime = self.frameScale