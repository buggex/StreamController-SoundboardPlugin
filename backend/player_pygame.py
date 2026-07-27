from player_interface import PlayerInterface

import pygame
import pygame._sdl2.audio as sdl2_audio

from loguru import logger as log

class PlayerPygame(PlayerInterface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device = ""

    def __del__(self):
        try:
            log.error("Finalizing Pygame player")
            pygame.mixer.quit()
        except Exception as e:
            log.error(f"Failed to quit mixer: {e}")

    def set_device(self, device):
        if device == "":
            return
        
        self.device = device

        try:
            pygame.mixer.quit()
            pygame.mixer.init(devicename=self.device)
        except Exception as e:
            log.error(f"Failed to initialize mixer with device '{self.device}': {e}")

    def play_sound(self, path_to_sound, volume):
        try:
            log.debug(f"Play file: {path_to_sound} at {volume}")
            pygame.mixer.music.load(path_to_sound)
            pygame.mixer.music.set_volume(volume/100.0)
            pygame.mixer.music.play()
        except Exception as e:
            log.error(f"Failed to play sound: {e}")

    def stop_sound(self):
        try:
            pygame.mixer.music.stop()
        except Exception as e:
            log.error(f"Failed to stop sound: {e}")

    def get_audio_devices(self):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            devices = sdl2_audio.get_audio_device_names(False)
            pygame.mixer.quit()
            return devices
        except Exception as e:
            log.error(f"Failed to get audio devices: {e}")
            return []
