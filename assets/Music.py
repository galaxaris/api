import pygame as pg

class Music:
    """
    Class for handling music. 
    
    NOTE: Different from Sfx, because only one music can be played at a time, on a reserved channel.

    This allows to handle music easier, without worrying about channels or overlapping sounds 
    ==> if a new music is played, the previous one will automatically stop.

    If wanted, a music can still be played as a Sfx.
    """
    def __init__(self, path: str):
        self.path = path
        self.music = pg.mixer.music.load(path)
        pg.mixer.music.stop() #Ensure music is stopped on initialization, to avoid any potential issues with music playing before intended

    def play(self, loops: int = -1, fade_ms: int = 0):
        self.music = pg.mixer.music.load(self.path)
        pg.mixer.music.play(loops=loops, fade_ms=fade_ms) #(loops: 0 = play once, -1 = loop indefinitely)

    def stop(self):
        pg.mixer.music.stop()

    def set_volume(self, volume: float):
        self.music.set_volume(volume)

    def get_volume(self) -> float:
        return self.music.get_volume()