# Import StreamController modules
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase

# Import python modules
import os

# Import gtk modules - used for the config rows
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

class SimpleAction(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_config_rows(self) -> list:
        self.sound_path = PathRow(self)

        self.sound_title = Adw.EntryRow.new()
        self.sound_title.set_title("Title")
        self.sound_title.connect("changed", self.on_sound_title_changed)

        self.load_config_values()

        return [self.sound_path, self.sound_title]
    
    def on_sound_path_changed(self, sound_path):
        settings = self.get_settings()
        settings["sound_path"] = sound_path
        self.set_settings(settings)

    def on_sound_title_changed(self, sound_title):
        settings = self.get_settings()
        settings["sound_title"] = sound_title.get_text()
        self.set_settings(settings)

    def load_config_values(self):
        settings = self.get_settings()
        
        path = settings.get("sound_path")
        if path is not None:
            self.sound_path.label.set_label(path)

        title = settings.get("sound_title")
        if title is not None:
            self.sound_title.set_text(title)
        
    def on_ready(self) -> None:
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "info.png")
        self.set_media(media_path=icon_path, size=0.75)
        
    def on_key_down(self) -> None:
        print("Key down")
    
    def on_key_up(self) -> None:
        print("Key up")

def on_path_choosen(dialog, result, pathrow):
    file = dialog.open_finish(result)
    path = file.get_path()
    pathrow.label.set_label(path)
    pathrow.action.on_sound_path_changed(path)

class PathRow(Adw.PreferencesRow):
    def __init__(self, simpleAction : SimpleAction):
        super().__init__(title="Path:")
        self.action = simpleAction

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, hexpand=True)
        self.set_child(self.main_box)

        self.label = Gtk.Label(hexpand=True, label="Path to sound file...", xalign=0, margin_start=12)
        self.main_box.append(self.label)

        self.config_button = Gtk.Button(label="Browse")
        self.main_box.append(self.config_button)
        self.config_button.connect("clicked", self.on_config)

        self.dialog = Gtk.FileDialog.new()
        self.dialog.set_title("Choose sound file")
    
    def on_config(self, button):
        self.dialog.open(callback=on_path_choosen,user_data=self)

