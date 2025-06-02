from streamcontroller_plugin_tools import BackendBase

import vlc

class SoundboardBackend(BackendBase):
    device      : str = ""
    instance    : vlc.Instance = None
    player      : vlc.MediaPlayer = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = vlc.Instance()

    def set_device(self, device):
        self.device = device

    def play_sound(self, path_to_sound, volume=100):
        # Stop old
        self.stop_sound()

        # Start new
        media = self.instance.media_new("file://" + path_to_sound)
        self.player = media.player_new_from_media()
        self.player.audio_output_device_set(None, self.find_device(self.player, self.device))
        self.player.audio_set_volume(int(volume)) # TODO why does volume not work
        self.player.play()

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

backend = SoundboardBackend()