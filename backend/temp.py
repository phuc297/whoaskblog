import os
import random


def get_random_filename():
    folder_path='./static/defaultthumnail'
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if not files:
        return None
    random_file = random.choice(files)
    print(random_file)
    return random_file

get_random_filename()