# Import StreamController modules
from src.backend.PluginManager.EventAssigner import EventAssigner
from src.backend.DeckManagement.InputIdentifier import Input
from src.backend.PluginManager.InputBases import ActionCore

# Import python modules
import os

class StopAction(ActionCore):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_event_assigner(EventAssigner(
            id="stop",
            ui_label=self.plugin_base.lm.get("actions.stop.label"),
            default_event=Input.Key.Events.DOWN,
            callback=lambda data : self.on_key_down()
        ))
    
    def on_ready(self) -> None:
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "stop.png")
        self.set_media(media_path=icon_path, size=0.75)

    def on_key_down(self):
        self.plugin_base.backend.stop_sound()        


