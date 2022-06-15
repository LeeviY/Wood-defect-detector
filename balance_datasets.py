import numpy as np
import os
from PIL import Image, ImageOps
from pathlib import Path, WindowsPath
from random import random, choice, randint

def flip_image(image: Image) -> Image:
    rand = random()

    if rand < 0.75:
        image = ImageOps.flip(image)
    if rand > 0.25:
        image = ImageOps.mirror(image)

    return image

def rotate_image(image: Image) -> Image:
    rand = random()

    #image = image.rotate(360 * rand, Image.NEAREST, expand = 1)
    image = image.rotate(90 * randint(0, 3), Image.NEAREST, expand = 1)

    return image

image_path = Path(os.path.dirname(os.path.realpath(__file__))).joinpath("wood_photo")

class_sizes = []

for dir in image_path.glob('*'):
    class_sizes.append(len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))]))

max_size = max(class_sizes)
print(max_size)

for dir in image_path.glob('*'):
    size = len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))])
    print("Balancing {}/ with {} items to size {}".format(str(dir).split('\\')[-1], size, max_size))
    for i in range(0, max_size - size):
        # choose random image to be augmented
        img_dir = choice(os.listdir(dir))
        try:
            img = Image.open(dir.joinpath(img_dir))
        except:
            i -= 1
            print("Failed to open", img_dir)
            continue
        new_image = img
        rand = random()
        # choose augemnt randomly
        if rand < 0.75:
            new_image = flip_image(new_image)
        if rand > 0.25:
            new_image = rotate_image(new_image)

        random_id = randint(100000, 999999)
        start, end = img_dir.split('_')
        new_image.save(dir.joinpath(start + '_' + str(random_id) + ".png"))

    print("Balancing {}/ done".format(str(dir).split('\\')[-1]))
        



