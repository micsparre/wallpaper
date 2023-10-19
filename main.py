import random
import appscript
import os
import logging
import pytz
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

BASE_LOG_PATH = os.environ.get('LOG_DIR', 'logs/')
LOG_FILENAME = 'wallpaper.log'
LOG_PATH = os.path.join(BASE_LOG_PATH, datetime.now(
    pytz.timezone('US/Pacific')).strftime('%Y-%m-%d_%H-%M-%S'), LOG_FILENAME)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(LOG_PATH)
logger.addHandler(file_handler)


def check_img_extension(file_path):
    file_path = file_path.lower()
    if file_path.endswith('.jpg') or file_path.endswith('.jpeg') or file_path.endswith('.png'):
        return True
    logger.warning(f'File {file_path} is not a valid image file')
    return False


def get_random_file(folder_path):
    files = [f for f in os.listdir(folder_path) if check_img_extension(f)]
    if not files:
        logger.warning(f'No valid images in {folder_path}')
        return None
    return os.path.join(folder_path, random.choice(files))


if __name__ == '__main__':
    logger.info(
        f"Starting execution at {datetime.now(pytz.timezone('US/Pacific')).strftime('%Y-%m-%d %H:%M:%S')}")

    horizontal_folder_path = os.path.abspath("horizontal_images")
    vertical_folder_path = os.path.abspath("vertical_images")

    se = appscript.app('System Events')
    desktops = se.desktops.display_name.get()
    logger.info(f'Found desktops: {desktops}')

    monitor = None
    for d in desktops:
        logger.info(f'Processing desktop {d}')
        img_path = None
        desk = se.desktops[appscript.its.display_name == d]
        print(f"desktop size: {desk.size}")
        curr_img_path = desk.picture.get()[0]

        if d.lower() == 'color lcd':
            folder = horizontal_folder_path
            monitor = 'horizontal'
        elif d.lower() == 'kg251q':
            folder = vertical_folder_path
            monitor = 'vertical'
        else:
            logger.error(f'Unknown monitor {d}, exiting')
            exit()

        while True:
            img_path = get_random_file(folder)
            if img_path != curr_img_path:
                break
        logger.info(f'Found image {img_path} for {monitor} monitor')
        desk.picture.set(appscript.mactypes.File(img_path))

    logger.info(
        f'Finished execution at {datetime.now(pytz.timezone("US/Pacific")).strftime("%Y-%m-%d %H:%M:%S")}')
