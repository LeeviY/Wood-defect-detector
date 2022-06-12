import os
import numpy as np
import tensorflow as tf
from pathlib import Path

model_path = os.path.dirname(os.path.realpath(__file__))
new_model = tf.keras.models.load_model(model_path + '\\saved_model\\my_model\\')

# Check its architecture
new_model.summary()

img = tf.keras.utils.load_img(
    Path.cwd().joinpath("wood_photo\knot_with_crack\\100000073_1.bmp"), target_size=(128, 350)
)

img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0) # Create a batch

predictions = new_model.predict(img_array)
score = tf.nn.softmax(predictions[0])

class_names = ['Crack', 'Dead_Knot', 'Knot_missing', 'Live_Knot', 'Marrow', 'Quartzity', 'knot_with_crack', 'resin']

print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(score)], 100 * np.max(score))
)