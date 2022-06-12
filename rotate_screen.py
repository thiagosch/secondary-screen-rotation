import rotatescreen
import keyboard
import os
import sys
from infi.systray import SysTrayIcon


states = {"primarystate": 0, "secondarystate": 270}
primarystate = 0
secondarystate = 270


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def rotatesecondary(resetvalue=False):
    if(rotatescreen.get_secondary_displays()[0].current_orientation == states["primarystate"]):
        rotation = states["secondarystate"]
    else:
        rotation = states["primarystate"]
    if resetvalue:
        rotation = states["primarystate"]
    settrayIconTo(rotation)
    return screen.rotate_to(rotation)


def settrayIconTo(value):
    if(value == 0):
        Icon = resource_path("images/landscape.ico")
    elif value == 90:
        Icon = resource_path("images/portrait.ico")
    elif value == 180:
        Icon = resource_path("images/landscapeF.ico")
    elif value == 270:
        Icon = resource_path("images/portraitF.ico")
    systray.update(icon=Icon)


def setrotationparams(state):
    states["primarystate"] = state[0]
    states["secondarystate"] = state[1]


def set_shortcut():
    return


menu_options = (
    ("Reset rotation", None, lambda systray: rotatesecondary(True)),
    ("Set shortcut", None, lambda systray: set_shortcut),
    ("Set rotation 0-270", None, lambda systray:  setrotationparams([0, 270])),
    ("Set rotation 0-90", None, lambda systray:  setrotationparams([0, 90])),
    ("Set rotation 0-180", None, lambda systray:  setrotationparams([0, 180])),
    ("Set rotation 90-270", None,
     lambda systray:  setrotationparams([90, 270])),
    ("Set secondary as primary", None, lambda systray: setrotationparams([states["secondarystate"], states["primarystate"]])),)


def on_quit_callback(systray):
    os._exit(1)


systray = SysTrayIcon("icon.ico", "Screen rotation",
                      menu_options, on_quit=on_quit_callback)
settrayIconTo(rotatescreen.get_secondary_displays()[0].current_orientation)

screen = rotatescreen.get_secondary_displays()[0]


def run_tray_app():
    systray.start()
    keyboard.add_hotkey("ctrl+alt+j", rotatesecondary)
    keyboard.wait()


run_tray_app()
