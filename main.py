import sys
import os
from pathlib import Path
from typing import Dict, Any

# Add plugin to sys.paths
ABSOLUTE_PLUGIN_PATH = str(Path(__file__).parent.parent.absolute())
sys.path.insert(0, ABSOLUTE_PLUGIN_PATH)

# Import StreamController modules
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder

# Import actions
from com_buggex_soundboard.actions.playaction.playaction import PlayAction
from com_buggex_soundboard.actions.stopaction.stopaction import StopAction

# Helpers
from com_buggex_soundboard.helpers import Consts

# Import gtk modules
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

from loguru import logger as log

class Soundboard(PluginBase):
    def __init__(self):
        super().__init__()
        
        self.lm = self.locale_manager

        # Start backend
        self.launch_backend(
            os.path.join(self.PATH, "backend", "backend.py"),
            os.path.join(self.PATH, "backend", ".venv"),
            open_in_terminal=False,
        )
        self.wait_for_backend(tries=5)

        # Setup backend
        settings = self.get_settings()

        selected_device = settings.get(Consts.SETTING_DEVICE)
        if selected_device is not None:
            self.backend.set_device(selected_device)
        else:
            # Assume this is first time, set the first device found
            devices = self.backend.get_audio_devices()
            if len(devices) > 0:
                settings[Consts.SETTING_DEVICE] = devices[0]
                self.set_settings(settings)
                self.backend.set_device(devices)
            else:
                log.error("Failed to find a sound device!")

        selected_player = settings.get(Consts.SETTING_PLAYER)
        if selected_player is not None:
            self.backend.set_player(selected_player)
        else:
            # Assume this is first time, set the default player
            default_player = list(Consts.PLAYER_NAMES.keys())[0]
            settings[Consts.SETTING_PLAYER] = default_player
            self.set_settings(settings)
            self.backend.set_player(default_player)

        ## Register actions
        self.play_action_holder = ActionHolder(
            plugin_base = self,
            action_base = PlayAction,
            action_id = Consts.ID + "::PlayAction",
            action_name = self.lm.get("actions.play.title"),
        )
        self.add_action_holder(self.play_action_holder)

        self.stop_action_holder = ActionHolder(
            plugin_base = self,
            action_base = StopAction,
            action_id = Consts.ID + "::StopAction",
            action_name = self.lm.get("actions.stop.title"),
        )
        self.add_action_holder(self.stop_action_holder)

        # Register plugin
        self.register()

    def get_settings_area(self):
        settings = self.get_settings()

        # Device
        self.device_model = Gtk.StringList().new(self.backend.get_audio_devices())
        self.device_dropdown = Adw.ComboRow(model=self.device_model, title=self.lm.get("setting.device"))
        
        selected_device = settings.get(Consts.SETTING_DEVICE)
        if selected_device is not None:
            index = self.device_model.find(selected_device)
            if index < self.device_model.get_n_items():
                self.device_dropdown.set_selected(index)

        self.device_dropdown.connect("notify::selected", self.on_device_dropdown_changed)

        # Player
        player_model = Gtk.StringList().new(list(Consts.PLAYER_NAMES.keys()))
        self.player_dropdown = Adw.ComboRow(model=player_model, title=self.lm.get("setting.player") + "*")

        selected_player = settings.get(Consts.SETTING_PLAYER)
        if selected_player is not None:
            index = player_model.find(selected_player)
            self.player_dropdown.set_selected(index)

        self.player_dropdown.connect("notify::selected", self.on_player_dropdown_changed)

        self.loading_label = Gtk.Label(label="*" + self.lm.get("setting.player.note"))
        
        group = Adw.PreferencesGroup()
        group.add(self.device_dropdown)
        group.add(self.player_dropdown)
        group.add(self.loading_label)
        return group
    
    def on_device_dropdown_changed(self, combo, data):
        selected_device = combo.get_selected_item().get_string()

        settings = self.get_settings()
        settings[Consts.SETTING_DEVICE] = selected_device
        self.set_settings(settings)

        if selected_device is not None:
            self.backend.set_device(selected_device)

    def on_player_dropdown_changed(self, combo, data):
        selected_player = combo.get_selected_item().get_string()

        settings = self.get_settings()
        settings[Consts.SETTING_PLAYER] = selected_player
        self.set_settings(settings)

        if selected_player is not None:
            self.backend.set_player(selected_player)
