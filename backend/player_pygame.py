from com_buggex_sc_soundboard.backend.player_interface import PlayerInterface

import pygame

from loguru import logger as log

class PlayerPygame(PlayerInterface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device = ""

    def __del__(self):
        pygame.mixer.quit()

    def set_device(self, device):
        log.debug(f"new device: {device}")
        pygame.mixer.quit()
        self.device = device

    def play_sound(self, path_to_sound, volume):
        log.debug(f"Play file: {path_to_sound} at {volume}")
        pygame.mixer.quit()
        pygame.mixer.init(devicename=self.device)
    
        pygame.mixer.music.load(path_to_sound)
        pygame.mixer.music.set_volume(volume/100.0)
        pygame.mixer.music.play()

    def stop_sound(self):
        pygame.mixer.music.stop()