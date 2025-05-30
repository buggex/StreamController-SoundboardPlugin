# Import StreamController modules
from src.backend.PluginManager.EventAssigner import EventAssigner
from src.backend.DeckManagement.InputIdentifier import Input
from src.backend.PluginManager.InputBases import ActionCore

# Helpers
from com_buggex_sc_soundboard.helpers import Consts

# Import python modules
import os

# Import gtk modules - used for the config rows
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib

from loguru import logger as log

class PlayAction(ActionCore):

    sound_path      : str = ""
    sound_volume    : int = 100

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_event_assigner(EventAssigner(
            id="play",
            ui_label="Play",
            default_events=[Input.Key.Events.DOWN],
            callback=lambda data : self.on_key_down()
        ))

    def get_config_rows(self) -> list:
        self.ui_sound_path = PathRow(self)

        self.ui_volume = Adw.SpinRow.new_with_range(min=0, max=100, step=1)
        self.ui_volume.set_title("Volume")
        self.ui_volume.set_value(100)
        self.ui_volume.connect("notify::value", self.on_sound_volume_changed)

        self.load_config_values()

        return [self.ui_sound_path, self.ui_volume]
    
    def on_sound_path_changed(self, path):
        self.sound_path = path
        settings = self.get_settings()
        settings[Consts.SETTING_SOUND_PATH] = self.sound_path
        self.set_settings(settings)

    def on_sound_volume_changed(self, control, param):
        self.sound_volume = self.ui_volume.get_value()
        settings = self.get_settings()
        settings[Consts.SETTING_SOUND_VOLUME] = self.sound_volume
        self.set_settings(settings)

    def load_config_values(self):
        settings = self.get_settings()
        
        path = settings.get(Consts.SETTING_SOUND_PATH)
        if path is not None:
            self.ui_sound_path.label.set_label(path)
            self.sound_path = path

        volume = settings.get(Consts.SETTING_SOUND_VOLUME)
        if volume is not None:
            self.ui_volume.set_value(volume)
            self.sound_volume = volume
        
    def on_ready(self) -> None:
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "info.png")
        self.set_media(media_path=icon_path, size=0.75)

    def on_key_down(self):
        self.plugin_base.backend.play_sound(self.sound_path, self.sound_volume)

class PathRow(Adw.PreferencesRow):
    def __init__(self, action : PlayAction):
        super().__init__(title="Path:")
        self.action = action

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self.set_child(self.main_box)

        self.label = Gtk.Label(hexpand=True, label="Path to sound file...", xalign=0, margin_start=12)
        self.label.set_ellipsize(1)
        self.label.set_size_request(height=50, width=-1)
        self.main_box.append(self.label)

        self.config_button = Gtk.Button(label="Browse")
        self.main_box.append(self.config_button)
        self.config_button.connect("clicked", self.on_config)

        self.dialog = Gtk.FileDialog.new()
        self.dialog.set_title("Choose a sound file")
    
    def on_config(self, button):
        self.dialog.open(callback=lambda source_object, res: self.on_path_choosen(res))

    def on_path_choosen(self, result):
        try:
            file = self.dialog.open_finish(result)
            path = file.get_path()
            self.label.set_label(path)
            self.action.on_sound_path_changed(path)
        except GLib.Error as e:
            log.warning(f"Failed to open. Error: {e}")

