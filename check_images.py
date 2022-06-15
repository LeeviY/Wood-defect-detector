import os
from PIL import Image
from pathlib import Path

image_path = Path(os.path.dirname(os.path.realpath(__file__))).joinpath("wood_photo")

for dir in image_path.glob('*'):
    for image in dir.glob('*'):
        try:
            img = Image.open(image)
            img.close()
        except:
            print(image.as_posix, "removed")
            os.remove(image)