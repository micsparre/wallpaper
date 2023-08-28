import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import appscript
import random

def get_random_file(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if not files:
        return None
    return os.path.join(folder_path, random.choice(files))

horizontal_folder_path = os.path.abspath("../horizontal_images/")
vertical_folder_path = os.path.abspath("../vertical_images/")

se = appscript.app('System Events')
desktops = se.desktops.display_name.get()
for d in desktops:
    img_path = None
    desk = se.desktops[appscript.its.display_name == d]
    curr_img_path = desk.picture.get()
    
    if d == 'S27E590':
        folder = horizontal_folder_path
    elif d == 'Kg251Q':
        folder = vertical_folder_path
    
    while True:
            img_path = get_random_file(folder)
            if img_path != curr_img_path:
                break
    
    desk.picture.set(appscript.mactypes.File(img_path))
