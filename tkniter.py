from genericpath import exists
from ntpath import join
from tkinter import *
from tkinter import ttk
import os
import json
appdat_path = os.getenv('APPDATA')
savepath = "rotate-screen"
savefile = "config-rotate-screen.json"


print(appdat_path)


def run_program(root=False):
    if(root):
        print("destroy")
        root.destroy()
    else:
        print("run")
    
defaultSave = {"primarystate": 0, "secondarystate": 270}

def confirm_file_save(event,root):
    if(not os.path.exists(os.path.join(appdat_path, savepath))):
        os.mkdir(os.path.join(appdat_path, savepath))
        print(os.path.join(appdat_path, savepath, savefile))
        with open(os.path.join(appdat_path, savepath, savefile), "w") as f:
            f.write(json.dumps(defaultSave))
    else:
        with open(os.path.join(appdat_path, savepath, savefile), "w") as f:
            f.write(json.dumps(defaultSave))
    run_program(root)


def first_launch():

    root = Tk()
    root.title("Rotate screen config file warning")
    frame_text_warning = Frame()
    frame_buttons = Frame()

    warningL1 = ttk.Label(master=frame_text_warning,
                          text="This program will generate a configuration file on")
    warningL2 = ttk.Label(master=frame_text_warning,
                          text=os.path.join(appdat_path, savepath, savefile))
    warningL1.pack()
    warningL2.pack()
    

    def deny_file_save(event):
        root.destroy()

    button = Button(master=frame_buttons, text="Confirm",
                    width=8,
                    height=1,)
    button.bind("<Button-1>",(lambda event, root=root: confirm_file_save(event,root)))
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


if(not exists(os.path.join(appdat_path, savepath, savefile))):
    first_launch()
else:
    run_program()
