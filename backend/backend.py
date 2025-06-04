from com_buggex_sc_soundboard.backend.player_interface import PlayerInterface
from com_buggex_sc_soundboard.backend.player_pygame import PlayerPygame
from com_buggex_sc_soundboard.backend.player_vlc import PlayerVLC

from com_buggex_sc_soundboard.helpers import Consts
from com_buggex_sc_soundboard.helpers.Consts import Players

from loguru import logger as log

class SoundboardBackend():
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
