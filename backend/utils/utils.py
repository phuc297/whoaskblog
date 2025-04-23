
import os
import random

DEFAULT_THUMBNAIL_POST_PATH = './mediafiles/default_thumnails'
DEFAULT_AVATAR_PATH = './mediafiles/default_avatars'


def short_text(text, word_limit=15):
    words = text.split()
    shortened = " ".join(words[:word_limit])
    return shortened


def get_random_thumbnail():
    folder_path = DEFAULT_THUMBNAIL_POST_PATH
    files = [f for f in os.listdir(folder_path) if os.path.isfile(
        os.path.join(folder_path, f))]
    if not files:
        return None
    random_file = random.choice(files)
    random_file_path = f'/default_thumnails/{random_file}'
    return random_file_path


def get_random_avatar():
    folder_path = DEFAULT_AVATAR_PATH
    files = [f for f in os.listdir(folder_path) if os.path.isfile(
        os.path.join(folder_path, f))]
    if not files:
        return None
    random_file = random.choice(files)
    random_file_path = f'/default_avatars/{random_file}'
    return random_file_path
