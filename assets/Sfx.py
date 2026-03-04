import pygame as pg

class Sfx:
    """
    Class for handling SFX. 
    
    NOTE: Different from Music, because only one music can be played at a time, on a reserved channel.

    Pygame automatically handles channels for SFX, so multiple SFX can be played at the same time without worrying about it.
    """
    def __init__(self, path: str):
        self.path = path
        self.sound = pg.mixer.Sound(path)

    def play(self, loops: int = 0):
        self.sound.play(loops=loops)

    def stop(self):
        self.sound.stop()

    def set_volume(self, volume: float):
        self.sound.set_volume(volume)

    def get_volume(self) -> float:
        return self.sound.get_volume()