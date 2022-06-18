
import os
import json
appdat_path = os.getenv('APPDATA')
savepath = "rotate-screen"
savefile = "config-rotate-screen.json"
fullpath = os.path.join(appdat_path, savepath, savefile)

def get_settings():
    settingsFile = open(os.path.join(appdat_path, savepath, savefile), "r")
    return json.loads(settingsFile.read())



def confirm_file_save(saveData, root=False):
    if(not os.path.exists(os.path.join(appdat_path, savepath))):
        os.mkdir(os.path.join(appdat_path, savepath))
        with open(os.path.join(appdat_path, savepath, savefile), "w") as settingsFile:
            settingsFile.write(json.dumps(saveData))
    else:
        with open(os.path.join(appdat_path, savepath, savefile), "w") as settingsFile:
            settingsFile.write(json.dumps(saveData))
    


