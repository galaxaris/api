import pygame as pg
from api.utils import GlobalVariables


class AudioManager:
    sfx: dict[str, pg.mixer.Sound]
    music: dict[str, str] #Music is stored directly as path.
    sfx_volume: float
    music_volume: float

    def __init__(self, sfx_volume=0.8, music_volume=1, channels=16):
        pg.mixer.init()
        pg.mixer.set_num_channels(channels)

        self.sfx = {}
        self.music = {}

        self.sfx_volume = sfx_volume
        self.music_volume = music_volume

        pg.mixer.music.set_volume(self.music_volume)
        
        GlobalVariables.set_variable("audio_manager", self)

    #### LOADING ####

    def load_sfx(self, name: str, path: str):
        sound = pg.mixer.Sound(path)
        sound.set_volume(self.sfx_volume)
        self.sfx[name] = sound

    def load_music(self, name: str, path: str):
        self.music[name] = path

    #### PLAYING/STOPPING ####
    #(loops: 0 = play once, -1 = loop indefinitely)

    def play_sfx(self, name: str, loops=0):
        if name in self.sfx:
            if self.sfx[name].get_num_channels() == 0: #Allows to avoid sound spamming
                self.sfx[name].play(loops=loops)

    def stop_sfx(self, name: str):
        if name in self.sfx:
            self.sfx[name].stop()

    def play_music(self, name: str, loops=-1): #Default: on loop
        if name in self.music:
            pg.mixer.music.load(self.music[name])
            pg.mixer.music.play(loops)

    def stop_music(self):
        pg.mixer.music.stop()

    def pause_music(self):
        pg.mixer.music.pause()

    def resume_music(self):
        pg.mixer.music.unpause()

    def stop_all_sfx(self):
        pg.mixer.stop()


    #### VOLUME ####

    def set_sfx_volume(self, volume):
        self.sfx_volume = volume
        for sound in self.sfx.values():
            sound.set_volume(volume)

    def set_music_volume(self, volume):
        self.music_volume = volume
        pg.mixer.music.set_volume(volume)
