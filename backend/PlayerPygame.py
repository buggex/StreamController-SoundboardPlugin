from com_buggex_sc_soundboard.backend import PlayerInterface

import pygame

from loguru import logger as log

class PlayerPygame(PlayerInterface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device = ""

    def __del__(self):
        print("PlayerPygame Del")

    def set_device(self, device):
        self.device = device

    def play_sound(self, path_to_sound, volume):
        pygame.mixer.quit()
        pygame.mixer.init(devicename=self.device)
    
        pygame.mixer.music.load(path_to_sound)
        pygame.mixer.music.set_volume(volume/100.0)
        pygame.mixer.music.play()

    def stop_sound(self):
        pygame.mixer.music.stop()