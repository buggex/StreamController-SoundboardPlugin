from abc import ABC, abstractmethod

# creating interface
class PlayerInterface(ABC):

    @abstractmethod
    def set_device(self, device):
       pass

    @abstractmethod
    def play_sound(self, path_to_sound, volume):
        pass

    @abstractmethod
    def stop_sound(self):
        pass