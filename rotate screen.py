import rotatescreen
import keyboard
import os
from infi.systray import SysTrayIcon
states = {"primarystate": 0, "secondarystate": 270}
primarystate = 0
secondarystate = 270


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
    match value:
        case 0:
            Icon = "landscape.ico"
        case 90:
            Icon = "portrait.ico"
        case 180:
            Icon = "landscapeF.ico"
        case 270:
            Icon = "portraitF.ico"
    systray.update(icon=Icon)


def say_hello(systray):
    rotatesecondary(True)
    return


def setrotationparams(state):
    states["primarystate"] = state[0]
    states["secondarystate"] = state[1]


menu_options = (
    ("reset rotation", None, say_hello),
    ("set rotation 0-270", None, lambda systray:  setrotationparams([0, 270])),
    ("set rotation 0-90", None, lambda systray:  setrotationparams([0, 90])),
    ("set rotation 0-180", None, lambda systray:  setrotationparams([0, 180])),
    ("set rotation 90-270", None,
     lambda systray:  setrotationparams([90, 270])),
    ("set secondary as primary", None, lambda systray: setrotationparams([states["secondarystate"], states["primarystate"]])),)


def on_quit_callback(systray):
    os._exit(1)


systray = SysTrayIcon("icon.ico", "Screen rotation",
                      menu_options, on_quit=on_quit_callback)
settrayIconTo(rotatescreen.get_secondary_displays()[0].current_orientation)
systray.start()


screen = rotatescreen.get_secondary_displays()[0]
# rotatescreen.get_secondary_displays()[0].rotate_to(90)


keyboard.add_hotkey("ctrl+alt+j", rotatesecondary)

keyboard.wait()
