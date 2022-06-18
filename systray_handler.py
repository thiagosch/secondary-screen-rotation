
from infi.systray import SysTrayIcon
import rotatescreen

import os
import sys

states = {}
isOpen = {"status": False}
systray = {}


def settrayIconTo(value, systray):
    if(value == 0):
        Icon = resource_path("images/landscape.ico")
    elif value == 90:
        Icon = resource_path("images/portrait.ico")
    elif value == 180:
        Icon = resource_path("images/landscapeF.ico")
    elif value == 270:
        Icon = resource_path("images/portraitF.ico")
    systray.update(icon=Icon)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def on_quit_callback(systray):
    os._exit(1)


def initialize_systray(settingsWindow):
    def show_settings_window():
        if(isOpen["status"]):
            settingsWindow.GUI().root.focus_force()
            return
        isOpen["status"] = True
        isOpen["status"] = settingsWindow.GUI().run()
    menu_options = (
        ("Settings", None, lambda systray: show_settings_window()), 
    )
    systray = SysTrayIcon("icon.ico", "Screen rotation",
                          menu_options, on_quit=on_quit_callback)

    settrayIconTo(rotatescreen.get_secondary_displays()
                  [0].current_orientation, systray)
    systray.start()
    return systray
