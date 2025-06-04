from com_buggex_sc_soundboard.backend.player_interface import PlayerInterface

import vlc
import time

from loguru import logger as log

PLAY_WAIT_TIME_SECONDS = 0.05
MAX_PLAY_WAIT_TRIES = int(1 / PLAY_WAIT_TIME_SECONDS)

class PlayerVLC(PlayerInterface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device = ""
        self.instance = vlc.Instance()
        self.player = None

    def __del__(self):
        self.stop_sound()

    def set_device(self, device):
        log.debug(f"new device: {device}")
        self.stop_sound()
        self.device = device

    def play_sound(self, path_to_sound, volume):
        log.debug(f"Play file: {path_to_sound} at {volume}")
        # Stop old
        self.stop_sound()

        # Start new
        media = self.instance.media_new("file://" + path_to_sound)
        self.player = media.player_new_from_media()
        self.player.audio_output_device_set(None, self.find_device(self.player, self.device))
        r = self.player.play()
        if r == 0:
            # We need for playback to begin before we can set volume
            # TODO: Need to find a better solution
            tries = 0
            while self.player.is_playing() == 0 and tries < MAX_PLAY_WAIT_TRIES:
                time.sleep(PLAY_WAIT_TIME_SECONDS)
                tries += 1
            self.player.audio_set_volume(int(volume))
        else:
            log.error(f"Failed to play. File: {path_to_sound}")

    def stop_sound(self):
        if self.player:
            self.player.release()

    def find_device(self, player, device_name):
        devices = player.audio_output_device_enum()
        if devices:
            device = devices
            while device:
                device = device.contents
                if device_name in str(device.description):
                    return device.device
                device = device.next
        return None
