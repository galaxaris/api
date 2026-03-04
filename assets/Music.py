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
        self.sound = pg.mixer.music.load(path)

    def play(self, loops: int = 0):
        pg.mixer.music.play(loops=loops)

    def stop(self):
        pg.mixer.music.stop()

    def set_volume(self, volume: float):
        pg.mixer.music.set_volume(volume)

    def get_volume(self) -> float:
        return pg.mixer.music.get_volume()