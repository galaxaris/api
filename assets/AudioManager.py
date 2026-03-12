import pygame as pg
from io import BytesIO
import wave
from api.utils.Console import *


class AudioManager:
    """
    AudioManager class. Handles the loading, playing, and stopping of sound effects and music in the game.
    """
    sfx: dict[str, pg.mixer.Sound]
    music: dict[str, str | None] # Music is stored directly as path.
    sfx_volume: float
    music_volume: float

    def __init__(self, sfx_volume:float|int = 0.8, music_volume:float|int = 1, channels:float|int = 16):
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
        self.is_muted = False
        self.current_music_name = None

        pg.mixer.music.set_volume(self.music_volume)


    def _create_silent_sound(self, duration_ms: int = 50000) -> pg.mixer.Sound:
        """
        Complicated function to avoid errors...

        Creates a tiny valid WAV in memory so fallback SFX always match mixer settings.

        :param duration_ms: Duration of the silent sound in milliseconds
        :return: A silent pygame Sound
        """
        init = pg.mixer.get_init()
        if init is None:
            raise RuntimeError("Mixer is not initialized")

        sample_rate, audio_format, channels = init
        sample_width = abs(audio_format) // 8
        frame_count = max(1, int(sample_rate * duration_ms / 1000))

        # Signed formats use 0 as silence. Unsigned formats use midpoint.
        if audio_format > 0:
            neutral = 1 << (abs(audio_format) - 1)
            sample = neutral.to_bytes(sample_width, byteorder="little", signed=False)
        else:
            sample = (0).to_bytes(sample_width, byteorder="little", signed=True)

        frame = sample * channels
        raw_frames = frame * frame_count

        wav_buffer = BytesIO()
        with wave.open(wav_buffer, "wb") as wav_file:
            wav_file.setnchannels(channels)
            wav_file.setsampwidth(sample_width)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(raw_frames)

        wav_buffer.seek(0)
        return pg.mixer.Sound(file=wav_buffer)

    #### LOADING ####

    def load_sfx(self, name: str, path: str):
        """
        Loads a sound effect from the specified path and assigns it a name for later use.

        :param name: Name to assign to the sound effect
        :param path: Path to the sound effect file
        """
        #Checks if the file exists and is a valid audio file before trying to load it
        error = False
        extensions = [".wav", ".ogg", ".mp3"]
        try:
            file = open(path, "rb")
            file.close()
            if not any(path.endswith(ext) for ext in extensions):
                print_error(f"File '{path}' does not have a common audio extension. Supported extensions are: {', '.join(extensions)}.")
                error = True
        except FileNotFoundError:
            print_error(f"Sound effect file '{path}' not found.")
            error = True
        except Exception as e:
            print_error(f"Error loading sound effect from {path}: {e}")
            error = True

        if not error:
            sound = pg.mixer.Sound(path)
            sound.set_volume(self.sfx_volume)
            self.sfx[name] = sound
        else:
            # Use a tiny silent fallback to keep SFX calls safe.
            silent_sound = self._create_silent_sound()
            silent_sound.set_volume(0)
            name = f"missing_sfx_{name}"
            self.sfx[name] = silent_sound

    def load_music(self, name: str, path: str):
        """
        Loads a music track from the specified path and assigns it a name for later use.

        :param name: Name to assign to the music track
        :param path: Path to the music file
        """
        #Checks if the file exists and is a valid audio file before trying to load it
        error = False
        extensions = [".wav", ".ogg", ".mp3"]
        try:
            file = open(path, "rb")
            file.close()
            if not any(path.endswith(ext) for ext in extensions):
                print_error(f"File '{path}' does not have a common audio extension. Supported extensions are: {', '.join(extensions)}.")
                error = True
        except FileNotFoundError:
            print_error(f"Music file '{path}' not found.")
            error = True
        except Exception as e:
            print_error(f"Error loading music from {path}: {e}")
            error = True

        if not error:
            self.music[name] = path
        else:
            # Use a tiny silent fallback to keep music calls safe.
            self.music[name] = None

    #### PLAYING/STOPPING ####
    #(loops: 0 = play once, -1 = loop indefinitely)

    def play_sfx(self, name: str, loops=0, allow_overlap=True):
        """
        Plays the specified sound effect.

        :param name: Name of the sound effect to play
        :param loops: Number of times to loop the sound effect (0 = play once, -1 = loop indefinitely)
        :param allow_overlap: When `False`, allows to avoid sound spamming
        """
        if name in self.sfx:
            if allow_overlap or self.sfx[name].get_num_channels() == 0:
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
            if self.music[name] is not None:
                pg.mixer.music.load(self.music[name])
                pg.mixer.music.play(loops)
                self.current_music_name = name
            else:
                self.current_music_name = f"missing_music_{name}"
                self.pause_music()


    def stop_music(self):
        """
        Stops the currently playing music track.
        """
        pg.mixer.music.stop()
        self.current_music_name = None


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
        return self.current_music_name
    
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
    
    def toggle_audio(self):
        """
        Toggles between mute and unmute states for both music and sound effects.
        """
        if self.music_volume > 0 or self.sfx_volume > 0:
            self.set_music_volume(0)
            self.set_sfx_volume(0)
            self.is_muted = True
        else:
            self.set_music_volume(1)
            self.set_sfx_volume(1)
            self.is_muted = False