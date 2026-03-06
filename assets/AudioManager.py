import pygame as pg
from api.utils import GlobalVariables


class AudioManager:
    """
    AudioManager class. Handles the loading, playing, and stopping of sound effects and music in the game.
    """
    sfx: dict[str, pg.mixer.Sound]
    music: dict[str, str] #Music is stored directly as path.
    sfx_volume: float
    music_volume: float

    def __init__(self, sfx_volume=0.8, music_volume=1, channels=16):
        """
        Initializes the AudioManager with the given volume levels and number of channels.

        :param sfx_volume: Volume level for sound effects (0.0 to 1.0)
        :param music_volume: Volume level for music (0.0 to 1.0)
        :param channels: Number of audio channels to initialize. More channels allow more simultaneous sounds, but use more resources.
        """
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
        """
        Loads a sound effect from the specified path and assigns it a name for later use.

        :param name: Name to assign to the sound effect
        :param path: Path to the sound effect file
        """
        sound = pg.mixer.Sound(path)
        sound.set_volume(self.sfx_volume)
        self.sfx[name] = sound

    def load_music(self, name: str, path: str):
        """
        Loads a music track from the specified path and assigns it a name for later use.

        :param name: Name to assign to the music track
        :param path: Path to the music file
        """
        self.music[name] = path

    #### PLAYING/STOPPING ####
    #(loops: 0 = play once, -1 = loop indefinitely)

    def play_sfx(self, name: str, loops=0):
        """
        Plays the specified sound effect.

        :param name: Name of the sound effect to play
        :param loops: Number of times to loop the sound effect (0 = play once, -1 = loop indefinitely)
        """
        if name in self.sfx:
            if self.sfx[name].get_num_channels() == 0: #Allows to avoid sound spamming
                self.sfx[name].play(loops=loops)

    def stop_sfx(self, name: str):
        """
        Stops the specified sound effect if it is currently playing.

        :param name: Name of the sound effect to stop
        """
        if name in self.sfx:
            self.sfx[name].stop()

    def play_music(self, name: str, loops=-1):
        """
        Plays the specified music track (loops indefinitely by default).

        :param name: Name of the music track to play
        :param loops: Number of times to loop the music track (0 = play once, -1 = loop indefinitely)
        """
        if name in self.music:
            pg.mixer.music.load(self.music[name])
            pg.mixer.music.play(loops)

    def stop_music(self):
        """
        Stops the currently playing music track.
        """
        pg.mixer.music.stop()

    def pause_music(self):
        """
        Pauses the currently playing music track.
        """
        pg.mixer.music.pause()

    def resume_music(self):
        """
        Resumes the currently paused music track.
        """ 
        pg.mixer.music.unpause()

    def stop_all_sfx(self):
        """
        Stops all currently playing sound effects.

        **Use with caution!**
        """
        pg.mixer.stop()


    #### VOLUME ####

    def set_sfx_volume(self, volume):
        """
        Sets the volume for all sound effects.

        :param volume: Volume level to set for sound effects (0.0 to 1.0)
        """
        self.sfx_volume = volume
        for sound in self.sfx.values():
            sound.set_volume(volume)

    def set_music_volume(self, volume):
        """
        Sets the volume for all music tracks.
        
        :param volume: Volume level to set for music tracks (0.0 to 1.0)
        """
        self.music_volume = volume
        pg.mixer.music.set_volume(volume)


    ### UTILS ###
    def is_music_playing(self):
        """
        Checks if any music track is currently playing.

        :return: `True` if music is playing, `False` otherwise
        """
        return pg.mixer.music.get_busy()
    
    def is_sfx_playing(self, name: str):
        """
        Checks if the specified sound effect is currently playing.

        :param name: Name of the sound effect to check
        :return: `True` if the sound effect is playing, `False` otherwise
        """
        if name in self.sfx:
            return self.sfx[name].get_num_channels() > 0
        return False
    
    def current_music(self):
        """
        Returns the name of the currently playing music track, or `None` if no music is playing.

        :return: Name of the currently playing music track, or `None` if no music is playing
        """
        for name, path in self.music.items():
            if pg.mixer.music.get_busy() and pg.mixer.music.get_pos() >= 0:
                return name
        return None
    
    def current_sfx(self):
        """
        Returns a list of names of currently playing sound effects.

        :return: List of names of currently playing sound effects
        """
        playing_sfx = []
        for name, sound in self.sfx.items():
            if sound.get_num_channels() > 0:
                playing_sfx.append(name)
        return playing_sfx