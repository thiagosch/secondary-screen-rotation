import queue
import threading
import keyboard
from tkinter import *
from settings_handler import confirm_file_save, get_settings
from shortcut_handler import addHotkeys
import customtkinter
import os
import sys
class GUI:
    WIDTH = 780
    HEIGHT = 420

    def __init__(self):
        self.status = True
        self.lettersArray = "numlock a b c d e f g h i j k l m n o p q r s t u v w x y z".upper().split(" ")
        self.root = customtkinter.CTk()
        self.root.title("Rotate screen configuration")
        icon = self.resource_path("images/landscape.ico")
        self.root.iconbitmap(icon)
        # self.root.minsize(480, 360)
        self.root.geometry(f"{GUI.WIDTH}x{GUI.HEIGHT}")
        self.root.eval('tk::PlaceWindow . center')
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

    def run(self):

        self.setSettings()
        self.stc_settings_title()
        self.stc_shortcut_sett()
        self.stc_rotation_togglers()
        self.stc_save_settings()
        self.root.mainloop()
        return self.status

    def resource_path(self,relative_path):
        
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    def savesettings(self, event):
        confirm_file_save(self.settings)

    def setSettings(self):
        settings_file = get_settings()
        self.settings = settings_file
        self.shortcut = settings_file["shortcut"]

    def stc_settings_title(self):
        frame = customtkinter.CTkFrame(master=self.root)
        customtkinter.CTkLabel(master=frame, text="Rotate Screen Settings",
                               ).pack(pady=5)
        frame.pack(pady=10)

    def stc_shortcut_sett(self):

        advanced_settings = False
        newframe = customtkinter.CTkFrame(master=self.root, corner_radius=10)
        manual_frame = self.stc_manual_shortcut(newframe)
        primary_frame = self.stc_primary_shortcut(newframe)

        to_manual_input = customtkinter.CTkButton(master=newframe, text="Advanced settings", width=120,
                                                  height=32,
                                                  command=lambda: enable_manual_input())

        def enable_manual_input():
            nonlocal advanced_settings, to_manual_input
            advanced_settings = not advanced_settings
            to_manual_input.pack_forget()
            if(advanced_settings):
                to_manual_input.configure(text="Basic settings")
                primary_frame.pack_forget()
                
                manual_frame.pack(pady=5)
            else:
                to_manual_input.configure(text="Advanced settings")
                manual_frame.pack_forget()
                primary_frame.pack(pady=5)
            to_manual_input.pack(pady=10)
        
        primary_frame.pack(pady=5)
        to_manual_input.pack(pady=10)
        newframe.pack(padx=20, pady=20,fill=X)

    def stc_primary_shortcut(self, newframe):
        shortcut_frame = customtkinter.CTkFrame(master=newframe)
        if(self.settings["shortcut_type"] == "primary"):
            selectedOptions = {"option1": customtkinter.StringVar(self.root, self.shortcut[0]), "option2": customtkinter.StringVar(
                self.root, self.shortcut[1]), "option3": customtkinter.StringVar(self.root, self.shortcut[2])}
        else:
            selectedOptions = {"option1": customtkinter.StringVar(self.root, "ctrl"), "option2": customtkinter.StringVar(
                self.root, "alt"), "option3": customtkinter.StringVar(self.root, "j")}

        def save_structurator(selectedOptions):
            command = [selectedOptions["option1"].get(
            ), selectedOptions["option2"].get(), selectedOptions["option3"].get()]
            self.saveShortcut(command, "primary")

        optionsLabel = customtkinter.CTkLabel(
            master=shortcut_frame, text="shortcut",  width=20)
        cBox1 = customtkinter.CTkComboBox(master=shortcut_frame, variable=selectedOptions["option1"], values=["", "ctrl", "alt", "windows"],
                                          command=lambda selection: save_structurator(selectedOptions))

        cBox2 = customtkinter.CTkComboBox(master=shortcut_frame, variable=selectedOptions["option2"], values=["", "ctrl", "alt", "windows"],
                                          command=lambda selection: save_structurator(selectedOptions))
        cBox3 = customtkinter.CTkComboBox(master=shortcut_frame, variable=selectedOptions["option3"], values=self.lettersArray,
                                          command=lambda selection: save_structurator(selectedOptions))

        optionsLabel.grid(row=1, column=0, pady=20)
        cBox1.grid(row=1, column=1)
        cBox2.grid(row=1, column=2, padx=3)
        cBox3.grid(row=1, column=3, padx=3)
        return shortcut_frame

    def stc_manual_shortcut(self, newframe):
        shortcut_frame = customtkinter.CTkFrame(master=newframe)

        def threading_shortcut_reader():
            self.queue = queue.Queue()
            to_manual_input.configure(state=DISABLED)
            ThreadedTask(self.queue, optionsLabel=optionsLabel).start()
            self.root.after(100, process_queue)

        def process_queue():
            try:

                input = self.queue.get_nowait()
                to_manual_input.configure(state=NORMAL)
                optionsLabel["text"] = input["label"]
                self.saveShortcut(input["shortcut"], "manual")

            except queue.Empty:
                self.root.after(100, process_queue)

        to_manual_input = customtkinter.CTkButton(master=shortcut_frame, text="Start recording shortcut",
                                                  command=lambda: threading_shortcut_reader())

        optionsLabel = customtkinter.CTkLabel(
            master=shortcut_frame, text="Select shortcut manually")
        to_manual_input.grid(row=0, column=0, pady=10)
        optionsLabel.grid(row=0, column=1, pady=10,)

        return shortcut_frame

    def stc_rotation_togglers(self):
        rotation_variable = IntVar(self.root, self.settings["rotationid"])
        togglers = [("Set rotation 0-270", 1,
                     {"primarystate": 0, "secondarystate": 270}),
                    ("Set rotation 0-90", 2,
                     {"primarystate": 0, "secondarystate": 90}),
                    ("Set rotation 0-180", 3,
                     {"primarystate": 0, "secondarystate": 180}),
                    ("Set rotation 90-270", 4,
                     {"primarystate": 90, "secondarystate": 270})]

        newframe2 = customtkinter.CTkFrame(master=self.root)
        customtkinter.CTkLabel(
            master=newframe2, text="Rotation",  width=20).grid(row=2, column=0)
        for togglerText, togglerValues, values in togglers:

            customtkinter.CTkRadioButton(master=newframe2,
                                         text=togglerText,
                                         variable=rotation_variable,
                                         width=20,
                                         padx=20,
                                         # command=togglerValues,
                                         value=togglerValues,
                                         command=lambda: self.save_rotation_selection(
                                             togglers, rotation_variable)
                                         ).grid(row=2, column=togglerValues, pady=10)
        newframe2.pack(padx=20, pady=20, ipadx=20)

    def stc_save_settings(self):

        frame_buttons = customtkinter.CTkFrame(master=self.root)
        button = customtkinter.CTkButton(frame_buttons, text="Save settings",
                                         width=120,
                                         height=32,
                                         command=lambda: self.save_settings())

        button.pack()
        frame_buttons.pack(padx=20, pady=20)

    def saveShortcut(self, command, tyep_of_save):
        self.settings["shortcut"] = command
        self.shortcut = command

        self.settings["shortcut_type"] = tyep_of_save
        return

    def save_settings(self, directInput=False):
        if(not directInput):
            shortcut = self.settings["shortcut"]
        else:
            shortcut = directInput
        confirm_file_save(self.settings)
        addHotkeys(shortcut, self.settings, True, directInput)
        return

    def save_rotation_selection(self, togglers, rotation_variable):
        newRotationSettings = togglers[rotation_variable.get()-1]
        self.settings["primarystate"] = newRotationSettings[2]["primarystate"]
        self.settings["secondarystate"] = newRotationSettings[2]["secondarystate"]
        self.settings["rotationid"] = newRotationSettings[1]

    def on_closing(self):
        self.status = False
        self.root.destroy()

    def to_the_top(self):
        self.root.withdraw()


class ThreadedTask(threading.Thread):
    def __init__(self, queue, optionsLabel=False):
        self.optionsLabel = optionsLabel
        super().__init__()
        self.queue = queue

    def run(self):
        self.optionsLabel["text"] = "'ESC' to confirm shortcut"
        input = keyboard.record()
        shortcut = []
        label = ""
        for key in input:
            if(key.event_type == "down"):
                if(key.name in shortcut):
                    continue
                shortcut.append(key.name)
                label += key.name+"+"
            else:
                label = label[:-1]
                break
        self.queue.put({"label": label, "shortcut": shortcut})
