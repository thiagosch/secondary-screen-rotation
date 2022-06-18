
import rotatescreen
from settings_handler import confirm_file_save
from systray_handler import settrayIconTo,systray


screen = rotatescreen.get_secondary_displays()[0]
def rotate_secondary(states,resetvalue=False):
    
    if(rotatescreen.get_secondary_displays()[0].current_orientation == states["primarystate"]):
        rotation = states["secondarystate"]
    else:
        rotation = states["primarystate"]
    if resetvalue:
        rotation = states["primarystate"]
    settrayIconTo(rotation,systray)
    screen.rotate_to(rotation)
    return rotation



