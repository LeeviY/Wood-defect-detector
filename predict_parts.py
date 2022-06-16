import tkinter as tk
import os
from PIL import Image, ImageTk
from pathlib import Path
from random import randint

IMAGE_SIZE = 256
PADDING = 20

def cut_perfect(root:tk.Canvas, image: Image, width: int, height: int) -> list:
    images = []

    size = 256
    x_offset = (width % size) / 2
    y_offset = (height % size) / 2

    divider = int(size / 4)

    x_iter = int(width / divider) - 4
    y_iter = int(height / divider) - 3

    for i in range(0, x_iter):
        for j in range(0, y_iter):
            x = x_offset + i * divider
            y = y_offset + j * divider
            box_dim = (x, y, x + size, y + size)
            
            draw_rectangle(root, (x, y))
            crp_image = image.crop(box_dim)
            images.append(crp_image)

    return images

def draw_rectangle(root:tk.Canvas, coord: tuple, size_x=IMAGE_SIZE, size_y=IMAGE_SIZE):
    x, y = coord
    #color = "#"+("%06x"%randint(0,16777215))
    root.create_rectangle(x, y, x + size_x, y + size_y, outline="red", width=2)

dir_path = os.path.dirname(os.path.realpath(__file__))
img_id = "101100008"
img_dir = Path(dir_path).joinpath("Images", img_id + ".bmp")

window = tk.Tk()

# open image
img = Image.open(img_dir)
img_x, img_y = img.size

# set image as canvas background
img_tk = ImageTk.PhotoImage(img)
canvas = tk.Canvas(window, width=img_x + PADDING , height=img_y + PADDING)
canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
#canvas.create_image(img_x / 2, img_y / 2, image=img_tk)
canvas.pack(padx=PADDING, pady=PADDING)

count = 0
for cut in cut_perfect(canvas, img, img_x, img_y):
    cut.save("{}\Validation\{}.png".format(dir_path, count))
    count += 1




window.title("Prediction")
window.mainloop()