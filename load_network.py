import os
import numpy as np
import tensorflow as tf
from pathlib import Path

model_path = os.path.dirname(os.path.realpath(__file__))
new_model = tf.keras.models.load_model(model_path + '\\saved_model\\my_model\\')

# Check its architecture
new_model.summary()

img = tf.keras.utils.load_img(
    Path.cwd().joinpath("wood_photo\crack\\99300074_0.bmp"), target_size=(300, 300, 3)
)

img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0) # Create a batch

predictions = new_model.predict(img_array)
score = tf.nn.softmax(predictions[0])

class_names = ['crack', 'knot', 'spot']

print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(score)], 100 * np.max(score))
)