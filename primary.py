from email.policy import default
from genericpath import exists
from tkinter import *
from tkinter import ttk
import settings_handler as Sh
from rotate_screen import  rotate_secondary
from systray_handler import initialize_systray
import settings_window as Sw
import keyboard
defaultSave = {"primarystate": 0,
               "secondarystate": 270, "rotationid": 1, "shortcut": ["ctrl", "alt", "j"],"shortcut_type":"primary"}
from shortcut_handler import addHotkeys

states = {}

def first_launch():

    root = Tk()
    root.title("Rotate screen config file warning")
    frame_text_warning = Frame()
    frame_buttons = Frame()

    warningL1 = ttk.Label(master=frame_text_warning,
                          text="This program will generate a configuration file on")
    warningL2 = ttk.Label(master=frame_text_warning,
                          text=Sh.fullpath)
    warningL1.pack()
    warningL2.pack()

    def deny_file_save(event):
        root.destroy()

    button = Button(master=frame_buttons, text="Confirm",
                    width=8,
                    height=1,)
    button.bind("<Button-1>", (lambda event, root=root: run_program(root)))
    button.pack(side=LEFT, padx=4)
    button2 = Button(master=frame_buttons, text="Cancel",
                     width=8,
                     height=1,)
    button2.bind("<Button-1>", deny_file_save)
    button2.pack(side=RIGHT, padx=4)

    frame_text_warning.pack(padx=6, pady=4)
    frame_buttons.pack(padx=6, pady=4)
    root.minsize(350, 50)

    root.mainloop()





def run_tray_app(statesFromFile):
    states["primarystate"] = statesFromFile["primarystate"]
    states["secondarystate"] = statesFromFile["secondarystate"]
    states["rotationid"] = statesFromFile["rotationid"]
    states["shortcut"] = statesFromFile["shortcut"]
    # set_rotation_params(states)
    addHotkeys(states["shortcut"],states)
    
    initialize_systray(Sw)



def run_program(root=False):
    # if root is set, that menas that the warning window it's needed to be closed
    # the window needed to be closed means that the program needs to save the default file because it's the first run
    if(root):
        Sh.confirm_file_save(defaultSave, root)
        root.destroy()
    
    run_tray_app(Sh.get_settings())



if(not exists(Sh.fullpath)):
    first_launch()
else:
    run_program()
    keyboard.wait()
    

states = {}