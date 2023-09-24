import random
import appscript
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_img_extension(file_path):
    file_path = file_path.lower()
    if file_path.endswith('.jpg') or file_path.endswith('.jpeg') or file_path.endswith('.png'):
        return True
    return False


def get_random_file(folder_path):
    files = [f for f in os.listdir(folder_path) if check_img_extension(f)]
    if not files:
        return None
    return os.path.join(folder_path, random.choice(files))


horizontal_folder_path = os.path.abspath("../horizontal_images/")
vertical_folder_path = os.path.abspath("../vertical_images/")

se = appscript.app('System Events')
desktops = se.desktops.display_name.get()
monitor = None
for d in desktops:
    img_path = None
    desk = se.desktops[appscript.its.display_name == d]
    curr_img_path = desk.picture.get()[0]

    if d == 'S27E590':
        folder = horizontal_folder_path
        monitor = 'horizontal'
    elif d == 'Kg251Q':
        folder = vertical_folder_path
        monitor = 'vertical'
    while True:
        img_path = get_random_file(folder)
        if img_path != curr_img_path:
            break
    print(f'Setting {monitor} monitor wallpaper to {img_path}')
    desk.picture.set(appscript.mactypes.File(img_path))
