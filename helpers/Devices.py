import pygame
import pygame._sdl2.audio as sdl2_audio

def GetAudioDevices():
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    return sdl2_audio.get_audio_device_names(False)
