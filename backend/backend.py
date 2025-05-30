from streamcontroller_plugin_tools import BackendBase
from pathlib import Path

import pygame

class SoundboardBackend(BackendBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_device(self, device):
        pygame.mixer.quit()
        pygame.mixer.init(devicename=device)

    def play_sound(self, path_to_sound, volume=100.0):
        pygame.mixer.music.load(path_to_sound)
        pygame.mixer.music.set_volume(volume/100.0)
        pygame.mixer.music.play()

    def stop_sound(self):
        pygame.mixer.music.stop()

backend = SoundboardBackend()