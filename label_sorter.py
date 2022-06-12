
import os
import glob
import shutil
from PIL import Image, ImageOps
from pathlib import Path, WindowsPath

def copy_bmp_to(src: WindowsPath, dst: WindowsPath, id_list: list):
    print(src, dst)
    for filename in id_list:
        if (src.joinpath(filename + ".bmp").exists()):
            #shutil.copy(src.joinpath(filename + ".bmp"), dst.joinpath(filename + ".bmp"))
            image = Image.open(src.joinpath(filename + ".bmp"))
            new_image = image.resize((int(350), int(128)), Image.Resampling.BICUBIC)
            gray_image = ImageOps.grayscale(new_image)
            gray_image.save(dst.joinpath(filename + ".bmp"))
            image.close()
            new_image.close()

dirname = os.path.dirname(__file__)
label_directory = os.path.join(dirname, "Bounding_Boxes", "Bounding_Boxes")

knot_labels = ["Live_Knot", "Deat_Knot", "Knot_missing", "knot_with_crack"]
crack_labels = ["Crack"]
dark_lables = ["resin", "Marrow", "Blue_stain"]
perfect_labels = ["Quartzity", "overgrown"]

knots = []
cracks = []
darks = []
perfects = []

last = "a"
path = Path.cwd().joinpath("Bounding_Boxes")

print(path)

count = 0
for filename in path.glob('*'):
    #if filename.endswith(".txt"):
    if filename.match("*/" + last):
        break

    with open(filename) as label_file:
        lines = label_file.readlines()
        # no label
        id = filename.as_posix().split('/')[-1].split('_')[0]
        if len(lines) == 0:
            perfects.append(id)
        # single label
        if len(lines) == 1:
            # get label from line
            label = lines[0].split('\t')[0]
            if label in knot_labels:
                knots.append(id)
            elif label in crack_labels:
                cracks.append(id)
            elif label in dark_lables:
                darks.append(id)
            elif label in perfect_labels:
                perfects.append(id)
    count += 1
    if count % 1000 == 0:
        print(count)

print("knots:{}, cracks:{}, darks:{}, perfects:{}".format(len(knots), len(cracks), len(darks), len(perfects)))

# copy images to class directory
src_dir = Path.cwd().joinpath("Images2")
dst_dir = Path.cwd().joinpath("wood_photo")

copy_bmp_to(src_dir, dst_dir.joinpath("knot"), knots)
copy_bmp_to(src_dir, dst_dir.joinpath("crack"), cracks)
copy_bmp_to(src_dir, dst_dir.joinpath("dark"), darks)
copy_bmp_to(src_dir, dst_dir.joinpath("perfect"), perfects)

