from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
from keras.datasets import cifar10
import tensorflow as tf
from keras import backend as K
import cv2
from keras import utils
import numpy as np
import matplotlib
import scipy.misc
import PIL
from PIL import Image
import os
import time
import keras
import scipy.misc
step = 1.2
(x_train, y_train), (x_test, y_test) = cifar10.load_data()
layer_name = 'block5_conv3'
filter_index = 0  # can be any integer from 0 to 511, as there are 512 filters in that layer

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.hdf5")
print("Loaded model from disk")

# this is the placeholder for the input images
input_img = loaded_model.input

def normalize(x):
    # utility function to normalize a tensor by its L2 norm
    return x / (K.sqrt(K.mean(K.square(x))) + 1e-5)


img_width = 32
img_height = 32
loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
layer_dict = dict([(layer.name, layer) for layer in loaded_model.layers])

print(layer_dict)
loss = K.mean(loaded_model.output[:, 1])
grads = K.gradients(loss, input_img)[0]
grads /= (K.sqrt(K.mean(K.square(grads))) + 1e-5)
iterate = K.function([input_img], [loss, grads])
#input_img_data = np.random.random((1, 3, img_width, img_height)) * 20 + 128.
if K.image_data_format() == 'channels_first':
    input_img_data = np.random.random((1, 3, img_width, img_height))
#    input_img_data = (input_img_data - 0.5) * 20 + 128
    print ("channels first")
else:
    input_img_data = np.random.random((1, img_width, img_height, 3))
    input_img_data = (input_img_data - 0.5) * 20 + 128

for i in range(400):
    loss_value, grads_value = iterate([input_img_data])
    input_img_data += grads_value * step
    print ("iterations:", i)

def deprocess_image(x):
    # normalize tensor: center on 0., ensure std is 0.1
    x -= x.mean()
    x /= (x.std() + 1e-5)
    x *= 0.1

    # clip to [0, 1]
    x += 0.5
    x = np.clip(x, 0, 1)

    # convert to RGB array
    x *= 255
    x = x.transpose((1, 2, 0))
    x = np.clip(x, 0, 255).astype('uint8')
    return x

img = input_img_data[0]
#img = deprocess_image(img)
data = np.asarray(img, dtype="uint8").reshape(1, 32, 32, 3)

scipy.misc.imsave('test3.png', img)

