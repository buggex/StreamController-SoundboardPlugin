from streamcontroller_plugin_tools import BackendBase

from player_interface import PlayerInterface
from player_pygame import PlayerPygame
from player_vlc import PlayerVLC

from loguru import logger as log

import pygame
import pygame._sdl2.audio as sdl2_audio

# To get access to plugin files
import sys
from pathlib import Path
ABSOLUTE_PLUGIN_PATH = str(Path(__file__).parent.parent.absolute())
sys.path.insert(0, ABSOLUTE_PLUGIN_PATH)

from helpers import Consts
from helpers.Consts import Players

class SoundboardBackend(BackendBase):
    player : PlayerInterface

    def __init__(self):
        super().__init__()
        self.device = ""
        self.player = None

    def set_player(self, playerType):
        player = Consts.PLAYER_NAMES[playerType]
        log.debug(f"new player: {playerType}")
        match player:
            case Players.Pygame:
                self.player = PlayerPygame()
            case Players.libVLC:
                self.player = PlayerVLC()
            case _:
                log.error(f"Unknown playerType {playerType} {player}")

        if self.player is not None:
            self.player.set_device(self.device)

    def set_device(self, device):
        self.device = device
        if self.player is not None:
            self.player.set_device(device)

    def play_sound(self, path_to_sound, volume):
        if self.player is not None:
            self.player.play_sound(path_to_sound, volume)

    def stop_sound(self):
        if self.player is not None:
            self.player.stop_sound()

    def get_audio_devices(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        return sdl2_audio.get_audio_device_names(False)

backend = SoundboardBackend()
