import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tkinter as tk

import tensorflow as tf
import keras
from keras.preprocessing import image

from PIL import Image
from pathlib import Path

def cut_perfect(image: Image, width: int, height: int) -> list:
    images = []

    size = 256
    x_offset = (width % size) / 2
    y_offset = (height % size) / 2

    for i in range(0, int(width / size)):
        for j in range(0, int(height / size)):
            x = x_offset + i * size
            y = y_offset + j * size
            box_dim = (x, y, x + size, y + size)
            crp_image = image.crop(box_dim)
            images.append(crp_image)

    return images

dir_path = os.path.dirname(os.path.realpath(__file__))
new_model = tf.keras.models.load_model(dir_path + '\\saved_model\\my_model\\')

# Check its architecture
new_model.summary()

#img_id = "100100046"
img_id = "101100008"
img_dir = Path(dir_path).joinpath("Images", img_id + ".bmp")

# splice input image into validation set
source_image = Image.open(img_dir)
count = 0
for img in cut_perfect(source_image, 1400, 512):
    img.save("{}\Validation\{}.png".format(dir_path, str(count)))
    count += 1

BATCH_SIZE = 9
IMG_HEIGHT = 256
IMG_WIDTH = 256

dir_path = dir_path + "\Validation"

# load all images into a list
images = []
for img in os.listdir(dir_path):
    img = os.path.join(dir_path, img)
    img = keras.utils.load_img(img)
    img = keras.utils.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    images.append(img)

# stack up images list to pass for prediction
images = np.vstack(images)

class_names = ["Crack", "Knot", "Marrow", "Perfect", "Spot"]

# make predictions
predictions = new_model.predict(images, batch_size=BATCH_SIZE)

# analyze predictions
plt.figure(figsize=(10, 10))
plt.suptitle("Image " + img_id)
for i in range(9):
    score = tf.nn.softmax(predictions[i])

    ax = plt.subplot(3, 3, i + 1)
    img = mpimg.imread("{}\{}.png".format(dir_path, i))

    plt.imshow(img)
    plt.title("{} {:.2f}%".format(class_names[np.argmax(score)], 100 * np.max(score)))
    plt.axis("off")

plt.show()
