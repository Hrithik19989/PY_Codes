import tensorflow as tf
from keras.applications import MobileNetV2
from keras.preprocessing import image
from keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
import numpy as np


# Load the MobileNetV2 model
model = MobileNetV2(weights='imagenet')

# Load an image for testing
img_path = "D:\Python\PY Codes\simba-8618301_1280.jpg"  # Path to your test image
img = image.load_img(img_path, target_size=(224, 224))

# Preprocess the image
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

# Make predictions
preds = model.predict(x)
print('Predicted:', decode_predictions(preds, top=3)[0])