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

# Import gtk modules
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

class Soundboard(PluginBase):
    def __init__(self):
        super().__init__()
        
        self.lm = self.locale_manager

        # Launch backend
        backend_path = Path(__file__).parent / "backend" / "backend.py"
        venv_path = Path(__file__).parent / ".venv"

        self.launch_backend(
            backend_path=backend_path, open_in_terminal=False, venv_path=venv_path
        )
        self.wait_for_backend(tries=5)

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
        self.register(
            plugin_name = self.lm.get("plugin.name"),
            github_repo = "https://github.com/buggex/sc_soundboard",
            plugin_version = "1.0.0",
            app_version = "1.5.0-beta"
        )

    def get_settings_area(self):
        self.device_model = Gtk.StringList().new(get_devices(DeviceFilter.SINK))
        self.device_dropdown = Adw.ComboRow(model=self.device_model, title=self.lm.get("setting.device"))

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
