from enum import Enum

ID = "com_buggex_sc_soundboard"

SETTING_DEVICE = "selected_device"
SETTING_BACKEND = "selected_backend"

SETTING_SOUND_PATH      = "sound_path"
SETTING_SOUND_VOLUME    = "sound_volume"

class Players(Enum):
    Pygame = 1
    libVLC = 2
