from ntpath import join
import keyboard
from rotate_screen import rotate_secondary


def addHotkeys(ShortcutArray, states, flushHotkeys=False, directInput=False):
    shortcut = ""
    if directInput:
        shortcut = ShortcutArray
    
    else:
        for key in ShortcutArray:
            if key:
                if shortcut:
                    shortcut += "+" + key
                else:
                    shortcut += key
 
    def execute(states):
        rotate_secondary(states)
    if(flushHotkeys):
        keyboard.unhook_all_hotkeys()
    keyboard.add_hotkey(shortcut, lambda: execute(states))
