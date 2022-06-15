
import os
from PIL import Image, ImageOps
from pathlib import Path

folders = ["Images5", "Images6", "Images7"]
dst_dir = Path('\\'.join([os.path.dirname(os.path.realpath(__file__)), "Images"]))

print(dst_dir)

for folder_name in folders:
    src_dir = Path('\\'.join([os.path.dirname(os.path.realpath(__file__)), folder_name]))
    print("Source:", src_dir)
    for image_path in src_dir.glob('*'):
        filename = image_path.as_posix().split('/')[-1]

        #print("File:", filename)

        image = Image.open(image_path)
        scaled_image = image.resize((int(1400), int(512)), Image.BICUBIC)
        gray_image = ImageOps.grayscale(scaled_image)
        gray_image.save(dst_dir.joinpath(filename))
    print(folder_name, "done")

