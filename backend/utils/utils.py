
import os
import random
from dotenv import load_dotenv

load_dotenv('.env.dev')
IS_CLOUD_STORE = bool(int(os.getenv('DEBUG_MODE', '0')))


STORAGES_PATH = ''
DEFAULT_THUMBNAIL_POST_PATH = f'{STORAGES_PATH}/mediafiles/default_thumnails'
DEFAULT_AVATAR_PATH = f'{STORAGES_PATH}/mediafiles/default_avatars'

CLOUD_AVATAR_LIST = ["/images/default_avatars/001-cat.png",
                     "/images/default_avatars/002-puma.png",
                     "/images/default_avatars/003-rabbit.png",
                     "/images/default_avatars/004-goat.png",
                     "/images/default_avatars/005-lion.png",
                     "/images/default_avatars/006-gorilla.png",
                     "/images/default_avatars/007-pig.png",
                     "/images/default_avatars/008-antelope.png",
                     "/images/default_avatars/009-buffalo.png",
                     "/images/default_avatars/010-hippo.png",
                     "/images/default_avatars/011-kangaroo.png",
                     "/images/default_avatars/012-leopard.png",
                     "/images/default_avatars/013-frog.png",
                     "/images/default_avatars/014-beaver.png",
                     "/images/default_avatars/015-racoon.png",
                     "/images/default_avatars/016-fox.png",
                     "/images/default_avatars/017-black-panther.png",
                     "/images/default_avatars/018-wolf.png",
                     "/images/default_avatars/019-zebra.png",
                     "/images/default_avatars/020-mandrill.png",
                     "/images/default_avatars/021-mouse.png",
                     "/images/default_avatars/022-bug.png",
                     "/images/default_avatars/023-tiger.png",
                     "/images/default_avatars/024-unicorn.png",
                     "/images/default_avatars/025-horse.png",
                     "/images/default_avatars/026-bulldog.png",
                     "/images/default_avatars/027-bat.png",
                     "/images/default_avatars/028-camel.png",
                     "/images/default_avatars/029-cat-1.png",
                     "/images/default_avatars/030-cow.png",
                     "/images/default_avatars/031-husky.png",
                     "/images/default_avatars/032-giraffe.png",
                     "/images/default_avatars/033-german-shepherd.png",
                     "/images/default_avatars/034-koala.png",
                     "/images/default_avatars/035-bear.png",
                     "/images/default_avatars/036-elephant.png"]

CLOUD_THUMBNAIL_LIST = ["/images/default_thumnails/thumbnail-01.jpg",
                        "/images/default_thumnails/thumbnail-02.jpg",
                        "/images/default_thumnails/thumbnail-03.jpg",
                        "/images/default_thumnails/thumbnail-04.jpg"]


def short_text(text, word_limit=15):
    words = text.split()
    shortened = " ".join(words[:word_limit])
    return shortened


def get_random_thumbnail():
    if IS_CLOUD_STORE:
        random_file_path = random.choice(CLOUD_THUMBNAIL_LIST)
    else:
        folder_path = DEFAULT_THUMBNAIL_POST_PATH
        files = [f for f in os.listdir(folder_path) if os.path.isfile(
            os.path.join(folder_path, f))]
        if not files:
            return None
        random_file = random.choice(files)
        random_file_path = f'/default_thumbnails/{random_file}'
    return random_file_path


def get_random_avatar():
    if IS_CLOUD_STORE:
        random_file_path = random.choice(CLOUD_AVATAR_LIST)
    else:
        folder_path = DEFAULT_AVATAR_PATH
        files = [f for f in os.listdir(folder_path) if os.path.isfile(
            os.path.join(folder_path, f))]
        if not files:
            return None
        random_file = random.choice(files)
        random_file_path = f'/default_avatars/{random_file}'
    return random_file_path
