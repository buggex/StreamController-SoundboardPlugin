from enum import Enum

ID = "com_buggex_sc_soundboard"

SETTING_DEVICE = "selected_device"
SETTING_PLAYER = "selected_player"

SETTING_SOUND_PATH      = "sound_path"
SETTING_SOUND_VOLUME    = "sound_volume"

class Players(Enum):
    Pygame = 0
    libVLC = 1


PLAYER_NAMES = {
  "Pygame": Players.Pygame,
  "libVLC": Players.libVLC
}