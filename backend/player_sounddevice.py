from player_interface import PlayerInterface

import sounddevice
import soundfile

from loguru import logger as log

class PlayerSoundDevice(PlayerInterface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device = ""

    def __del__(self):
        sounddevice.stop()

    def set_device(self, device):
        if device == "":
            return
        
        self.device = device

    def play_sound(self, path_to_sound, volume):
        log.debug(f"Play file: {path_to_sound} at {volume}")
        try:
            data, fs = soundfile.read(path_to_sound)
            sounddevice.play(data, device=self.device)
        except Exception as e:
            log.error(f"Failed to play sound: {e}")

    def stop_sound(self):
        sounddevice.stop()

    def get_audio_devices(self):
        devices = []
        try:
            for device in sounddevice.query_devices():
                if device['max_output_channels'] > 0:
                    devices.append(device['name'])
        except Exception as e:
            log.error(f"Failed to get audio devices: {e}")
        return devices
