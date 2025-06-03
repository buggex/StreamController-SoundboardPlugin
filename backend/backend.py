from streamcontroller_plugin_tools import BackendBase

from com_buggex_sc_soundboard.backend import PlayerInterface, PlayerPygame, PlayerVLC
from com_buggex_sc_soundboard.helpers import Consts
from com_buggex_sc_soundboard.helpers.Consts import Players

from loguru import logger as log

class SoundboardBackend(BackendBase):
    player : PlayerInterface

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device = ""
        self.player = None

    def set_player(self, playerType):
        match playerType:
            case Players.Pygame:
                self.player = PlayerPygame()
            case Players.libVLC:
                self.player = PlayerVLC()
            case _:
                log.error(f"Unknown playerType {playerType}")

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

backend = SoundboardBackend()