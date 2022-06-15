
import os
import glob
from pydoc import classname
from turtle import width
from PIL import Image, ImageOps
from pathlib import Path, WindowsPath
from numpy import full, pad

IMAGE_WIDTH = 1400  # width of output image
IMAGE_HEIGHT = 512  # height of input image
PADDING_X = 75      # left and right border of input image to be ignored
PADDING_Y = 0       # top and bottom border of input image to be ignored
IMAGE_SIZE = 256    # size of output images

# Takes tuple of bounding box with (left, top, right, down)
# returns True if box is legal
def check_box(box: tuple) -> bool:
    x_dif = box[2] - box[0]
    y_dif = box[3] - box[1]

    # minimum size of bbox dimension
    threshold = 10

    # check for shape and size of bbox
    if x_dif * y_dif >= threshold * threshold:
        if x_dif >= threshold and y_dif >= threshold:
            return True

    return False

# maps labels down to common terms
# takes and returns a string
def map_label(label: str) -> str:
    if label in ["Live_Knot", "Dead_Knot", "Knot_missing", "knot_with_crack"]:
        return "knot"
    if label in ["Quartzity", "overgrown"]:
        return "perfect"
    if label == "Crack":
        return "crack"
    if label == "resin":
        return "spot"
    if label == "Marrow":
        return "marrow"
    if label == "Blue_Stain":
        return "stain"

    print("label not found", label)

# cuts image in to sections and returns a list of images
def cut_perfect(image: Image, width: int, height: int) -> list:
    images = []

    x_offset = (width % IMAGE_SIZE) / 2
    y_offset = (height % IMAGE_SIZE) / 2

    for i in range(0, int(width / IMAGE_SIZE)):
        for j in range(0, int(height / IMAGE_SIZE)):
            x = x_offset + i * IMAGE_SIZE
            y = y_offset + j * IMAGE_SIZE
            box_dim = (x, y, x + IMAGE_SIZE, y + IMAGE_SIZE)
            crp_image = image.crop(box_dim)
            images.append(crp_image)

    return images

def calculate_bbox(box: tuple, img_width: int, img_height: int, pad_x: int, pad_y: int, size: int) -> tuple:
    r = size / 2
    # bbox radiae
    box_x_r = (box[2] - box[0]) / 2
    box_y_r = (box[3] - box[1]) / 2
    # calculate expanded bbox dimensions
    left = box[0] - (r - box_x_r)
    top = box[1] - (r - box_y_r)
    right = box[2] + (r - box_x_r)
    down = box[3] + (r - box_y_r)

    # move bbox in x-axis
    if left <= pad_x:
        movement = abs(left) + pad_x
        left += movement
        right += movement
    elif right >= img_width - pad_x:
        movement = abs(right - img_width) + pad_x
        left -= movement
        right -= movement

    # move bbox in y-axis
    if top <= pad_y:
        movement = abs(top) + pad_y
        top += movement
        down += movement
    elif down >= img_height - pad_y:
        movement = abs(down - img_height) + pad_y
        top -= movement
        down -= movement

    return (left, top, right, down)

# working directory
dirname = os.path.dirname(__file__)

# directory for bouding box files
bbox_dir = Path(os.path.dirname(os.path.realpath(__file__))).joinpath("Bounding_Boxes")

print(bbox_dir)

# copy images to class directory
src_dir = Path.cwd().joinpath("Images")
dst_dir = Path.cwd().joinpath("wood_photo")

# create class subfolders if they don't exist
classes = ["crack", "knot", "perfect", "spot", "stain", "marrow"]
for class_name in classes:
    path = dst_dir.joinpath(class_name)
    if not os.path.exists(path):
        os.mkdir(path)

count = 0
# loop through label files
for filename in bbox_dir.glob('*'):
    with open(filename) as label_file:
        lines = label_file.readlines()

        # get id of picture from file name
        id = filename.as_posix().split('/')[-1].split('_')[0]
        # check if matching image file exists
        if not src_dir.joinpath(id + ".bmp").exists():
            continue

        # open source image
        input_image = Image.open(src_dir.joinpath(id + ".bmp"))
        label = "perfect" # set as flawless as default
        is_perfect = True
        line_count = 0
        for line in lines:
            label, left, top, right, down = line.split('\t')

            # merge labels
            label = map_label(label)
            #print(src_dir.joinpath(id + ".bmp"))

            if label == "perfect":
                continue
            
            is_perfect = False

            # create bounding box area
            try:
                box_dim = (int(float(left) * IMAGE_WIDTH), int(float(top) * IMAGE_HEIGHT), 
                int(float(right) * IMAGE_WIDTH), int(float(down) * IMAGE_HEIGHT))
            except:
                print(id, "Not valid")
                left = left.replace(',', '.')
                top = top.replace(',', '.')
                right = right.replace(',', '.')
                down = down.replace(',', '.')

                box_dim = (int(float(left) * IMAGE_WIDTH), int(float(top) * IMAGE_HEIGHT), 
                int(float(right) * IMAGE_WIDTH), int(float(down) * IMAGE_HEIGHT))

            #exit()

            # check if box size is legal
            if check_box(box_dim):
                new_box = calculate_bbox(box_dim, IMAGE_WIDTH, IMAGE_HEIGHT, PADDING_X, PADDING_Y, IMAGE_SIZE)
                # crop image to bbox and save
                crp_image = input_image.crop(new_box)
                crp_image.save(dst_dir.joinpath(label, "{}_{}.png".format(id, line_count)))
                img.close()
            else:
                print(id, "invalid area")
            line_count += 1
        
        # if image had no defects
        if is_perfect:
            perfect_parts = cut_perfect(input_image, IMAGE_WIDTH, IMAGE_HEIGHT)
            for img in perfect_parts:
                img.save(dst_dir.joinpath(label, (id + "_" + str(line_count) + ".png")))
                img.close()
                line_count += 1

    count += 1
    if count % 1000 == 0:
        print(count)

