
import os
import glob
import shutil
from PIL import Image, ImageOps
from pathlib import Path, WindowsPath

def crop_object(box: tuple, image: Image) -> Image:
    crp_image = image.crop(box)
    return crp_image

def check_box(box: tuple) -> bool:
    x_dif = box[2] - box[0]
    y_dif = box[3] - box[1]

    threshold = 15

    if x_dif <= threshold:
        return False
    if y_dif <= threshold:
        return False
    return True

def map_label(label: str) -> str:
    if label in knot_labels:
        return "knot"
    if label in crack_labels:
        return "crack"
    if label in spot_lables:
        return "spot"
    if label in perfect_labels:
        return "perfect"

    print("label not found", label)

def cut_perfect(image: Image) -> list:
    images = []

    size = 300
    x_offset = (image_width % size) / 2
    y_offset = (image_height % size) / 2

    for i in range(0, int(image_width / size)):
        for j in range(0, int(image_height / size)):
            x = x_offset + i * size
            y = y_offset + j * size
            box_dim = (x, y, x + size, y + size)
            crp_image = crop_object(box_dim, image)
            images.append(crp_image)

    return images


dirname = os.path.dirname(__file__)
label_directory = os.path.join(dirname, "Bounding_Boxes", "Bounding_Boxes")

knot_labels = ["Live_Knot", "Dead_Knot", "Knot_missing", "knot_with_crack"]
crack_labels = ["Crack"]
spot_lables = ["resin", "Marrow", "Blue_stain"]
perfect_labels = ["Quartzity", "overgrown"]

path = Path.cwd().joinpath("Bounding_Boxes")

print(path)

# copy images to class directory
src_dir = Path.cwd().joinpath("Images")
dst_dir = Path.cwd().joinpath("wood_photo")

image_width = 1400
image_height = 512

count = 0
for filename in path.glob('*'):
    with open(filename) as label_file:
        lines = label_file.readlines()

        # get id of picture from file name
        id = filename.as_posix().split('/')[-1].split('_')[0]
        print(id)
        # check if matching image file exists
        if not src_dir.joinpath(id + ".bmp").exists():
            continue
        
        # open source image
        input_image = Image.open(src_dir.joinpath(id + ".bmp"))
        #label = "perfect" # set as flawless as default
        is_perfect = True
        line_count = 0
        for line in lines:
            label, left, top, right, down = line.split('\t')

            # merge labels
            label = map_label(label)
            #print(src_dir.joinpath(id + ".bmp"))
            if label == "perfect":
                continue
            else:
                is_perfect = False

            # create bounding box area
            box_dim = (int(float(left) * image_width), int(float(top) * image_height), 
            int(float(right) * image_width), int(float(down) * image_height))

            # check if box size is legal
            if check_box(box_dim):
                crp_image = crop_object(box_dim, input_image)
                resized_image = crp_image.resize((300, 300))
                resized_image.save(dst_dir.joinpath(label, (id + "_" + str(line_count) + ".bmp")))
            else:
                print(id, "invalid area")
            line_count += 1
        
        # if image  had no defects
        if is_perfect:
            perfect_parts = cut_perfect(input_image)
            for img in perfect_parts:
                img.save(dst_dir.joinpath(label, (id + "_" + str(line_count) + ".bmp")))
                line_count += 1

    count += 1
    if count % 1000 == 0:
        print(count)

