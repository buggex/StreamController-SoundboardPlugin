import sys
from pathlib import Path
from typing import Dict, Any

ABSOLUTE_PLUGIN_PATH = str(Path(__file__).parent.parent.absolute())
sys.path.insert(0, ABSOLUTE_PLUGIN_PATH)

# Import StreamController modules
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder

# Import actions
from .actions.PlayAction.PlayAction import PlayAction
from .actions.StopAction.StopAction import StopAction

# Helpers
from .helpers.PulseHelpers import get_devices, DeviceFilter
from .helpers import Consts

# Backend
from .backend.backend import SoundboardBackend

# Import gtk modules
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

class Soundbard(PluginBase):
    def __init__(self):
        super().__init__()

        # Launch backend
        self.backend = SoundboardBackend()

        # Setup backend
        settings = self.get_settings()
        selected_device = settings.get(Consts.SETTING_DEVICE)
        if selected_device is not None:
            self.backend.set_device(selected_device)

        ## Register actions
        self.play_action_holder = ActionHolder(
            plugin_base = self,
            action_base = PlayAction,
            action_id = Consts.ID + "::PlayAction",
            action_name = "Play sound",
        )
        self.add_action_holder(self.play_action_holder)

        self.stop_action_holder = ActionHolder(
            plugin_base = self,
            action_base = StopAction,
            action_id = Consts.ID + "::StopAction",
            action_name = "Stop sound",
        )
        self.add_action_holder(self.stop_action_holder)

        # Register plugin
        self.register(
            plugin_name = "Soundboard",
            github_repo = "https://github.com/buggex/sc_soundboard",
            plugin_version = "1.0.0",
            app_version = "1.5.0-beta"
        )

    def get_settings_area(self):
        self.device_model = Gtk.StringList().new(get_devices(DeviceFilter.SINK))
        self.device_dropdown = Adw.ComboRow(model=self.device_model, title="Playback device:")

        settings = self.get_settings()
        selected_device = settings.get(Consts.SETTING_DEVICE)

        if selected_device is not None:
            index = self.device_model.find(selected_device)
            if index < self.device_model.get_n_items():
                self.device_dropdown.set_selected(index)

        self.device_dropdown.connect("notify::selected", self.on_device_dropdown_changed)
        
        group = Adw.PreferencesGroup()
        group.add(self.device_dropdown)
        return group
    
    def on_device_dropdown_changed(self, combo, data):
        selected_device = combo.get_selected_item().get_string()

        settings = self.get_settings()
        settings[Consts.SETTING_DEVICE] = selected_device
        self.set_settings(settings)

        if selected_device is not None:
            self.backend.set_device(selected_device)
