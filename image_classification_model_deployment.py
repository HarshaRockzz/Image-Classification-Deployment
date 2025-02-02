# -*- coding: utf-8 -*-
"""Image Classification Model Deployment.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VUGtoFQs14RsbgB7GxHg2uNqgmMGOWSi
"""

# Commented out IPython magic to ensure Python compatibility.
import os
import zipfile
import pathlib

!pip install split-folders
import splitfolders as sf

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import Xception
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Dense

from google.colab import files

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# %matplotlib inline

# Kaggle username and key
os.environ['KAGGLE_USERNAME'] = 'harsharockerzzz'
os.environ['KAGGLE_KEY']      = 'c1cefea4cc184cb0d30547be43e5f107'

# Download dataset from Kaggle
!kaggle datasets download -d duttadebadri/image-classification

# Unzip the downloaded zip file
localZip = '/content/image-classification.zip'
zipRef = zipfile.ZipFile(localZip, 'r')
zipRef.extractall('image-classification')
zipRef.close()

# List directory
baseDir = 'image-classification/images/images'
os.listdir(baseDir)

# Rename directory
os.rename(baseDir + '/art and culture',       baseDir + '/art')
os.rename(baseDir + '/architecure',           baseDir + '/archi')
os.rename(baseDir + '/food and d rinks',      baseDir + '/fnb')
os.rename(baseDir + '/travel and  adventure', baseDir + '/travel')

# List renamed directory
os.listdir(baseDir)

# Split directory
sf.ratio(
    baseDir,
    output = os.path.join('image-classification/image'),
    seed   = None,
    ratio  = (0.8, 0.2)
)

# Train and val dir for each archi, art, fnb, travel
imageDir = 'image-classification/image'

trainDirArchi  = os.path.join(imageDir, 'train/archi')
trainDirArt    = os.path.join(imageDir, 'train/art')
trainDirFnb    = os.path.join(imageDir, 'train/fnb')
trainDirTravel = os.path.join(imageDir, 'train/travel')

valDirArchi    = os.path.join(imageDir, 'val/archi')
valDirArt      = os.path.join(imageDir, 'val/art')
valDirFnb      = os.path.join(imageDir, 'val/fnb')
valDirTravel   = os.path.join(imageDir, 'val/travel')

# Count train and val image
trainSet = (
      len(os.listdir(trainDirArchi))
    + len(os.listdir(trainDirArt))
    + len(os.listdir(trainDirFnb))
    + len(os.listdir(trainDirTravel))
)

valSet = (
      len(os.listdir(valDirArchi))
    + len(os.listdir(valDirArt))
    + len(os.listdir(valDirFnb))
    + len(os.listdir(valDirTravel))
)

print(f'Train Set      : {trainSet}')
print(f'Validation Set : {valSet}')

# List directory of train and validation image
trainDir = os.path.join(imageDir, 'train')
valDir   = os.path.join(imageDir, 'val')

print(os.listdir(trainDir))
print(os.listdir(valDir))

# Image Augmentation for duplicating image
trainDatagen = ImageDataGenerator(
    rescale            = 1./255,
    rotation_range     = 30,
    # width_shift_range  = 0.2,
    # height_shift_range = 0.2,
    shear_range        = 0.2,
    zoom_range         = 0.2,
    horizontal_flip    = True,
    # vertical_flip      = True,
    fill_mode          = 'nearest',
    # validation_split   = 0.2
)

valDatagen = ImageDataGenerator(
    rescale         = 1./255
)

# Preperation the training and validation data with .flow_from_directory()
trainGen = trainDatagen.flow_from_directory(
    trainDir,
    target_size = (200, 200),
    batch_size  = 50,
    shuffle     = True,
    color_mode  = 'rgb',
    class_mode  = 'categorical',
    # save_format = 'jpeg'
)

valGen = valDatagen.flow_from_directory(
    valDir,
    target_size = (200, 200),
    batch_size  = 50,
    shuffle     = True,
    color_mode  = 'rgb',
    class_mode  = 'categorical',
    # save_format = 'jpeg'
)

baseModel = Xception(weights="imagenet", include_top=False, input_shape=(200, 200, 3))

baseModel.trainable = False

baseModel.summary()
print(f'Base Model Layer : {len(baseModel.layers)}')

model = Sequential([
    baseModel,
    GlobalAveragePooling2D(),
    Dense(4, activation='softmax')
])

model.summary()

# Model architecture
# pre_trained_model = ResNet152V2(
#     weights      = 'imagenet',
#     include_top  = False,
#     input_tensor = Input(shape=(150, 150, 3))
# )

# for layer in pre_trained_model.layers:
#     layer.trainable = False

# model_output = pre_trained_model.output

# m = Flatten(name='flatten')(model_output)
# m = Dropout(0.5)(m)
# m = Dense(128, activation='relu')(m)
# m = Dense(4,   activation='softmax')(m)

# model = Sequential(pre_trained_model.input, m)

# from tensorflow.keras.applications import EfficientNetB3
# from tensorflow.keras.layers import BatchNormalization

# model = Sequential([
#     EfficientNetB3(weights="imagenet", include_top=False, pooling='max', input_shape=(200, 200, 3), input_tensor=Input(shape=(200, 200, 3))),
#     BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001),
#     Dropout(0.25),
#     Flatten(),
#     Dense(256, activation='relu'),
#     Dense(128, activation='relu'),
#     Dense(4,   activation='softmax')
#     # Conv2D(64,  (3, 3), activation='relu', input_shape=(200, 200, 3)),
#     # MaxPooling2D(2, 2),
#     # Dropout(0.25),
#     # Conv2D(64,  (3, 3), activation='relu'),
#     # MaxPooling2D(2, 2),
#     # Conv2D(128,  (3, 3), activation='relu'),
#     # MaxPooling2D(2, 2),
#     # Conv2D(256,  (3, 3), activation='relu'),
#     # MaxPooling2D(2, 2),
#     # Conv2D(512,  (3, 3), activation='relu'),
#     # MaxPooling2D(2, 2),
#     # Dropout(0.25),
#     # Flatten(),
#     # Dense(512, activation='relu'),
#     # Dense(4,   activation='softmax')
# ])

# model.summary()

model.compile(
    optimizer = 'adam',
    # optimizer = tf.optimizers.Adam(lr=1e-4),
    # optimizer = tf.keras.optimizers.SGD(lr=1e-4, momentum=0.9),
    loss      = 'categorical_crossentropy',
    metrics   = ['accuracy']
)

# Stop training callback
class stopCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if (logs.get('accuracy') > 0.92 and logs.get('val_accuracy') > 0.92):
            print('\nAccuracy and Validation Accuracy reach > 92%')
            # self.model.stop_training = True

stopTraining = stopCallback()

# ReduceLROnPlateau callback
reduceLROP   = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', patience=3)

"""---

**Cannot connect to GPU backend**


You cannot currently connect to a GPU due to usage limits in Colab. [Learn more](https://research.google.com/colaboratory/faq.html#usage-limits)

If you are interested in priority access to GPUs and higher usage limits, you may want to check out [Colab Pro](https://colab.research.google.com/signup?utm_source=dialog&utm_medium=link&utm_campaign=gpu_assignment_failure).

---
"""

# Model training with .fit()
epoch = 10

history = model.fit(
    trainGen,
    # steps_per_epoch  = 32,
    epochs           = epoch,
    validation_data  = valGen,
    # validation_steps = 5,
    verbose          = 2,
    callbacks        = [stopTraining, ]
)

# Visualize accuracy and loss plot
accuracy     = history.history['accuracy']
val_accuracy = history.history['val_accuracy']

loss         = history.history['loss']
val_loss     = history.history['val_loss']

plt.figure(figsize = (12, 4))

plt.subplot(1, 2, 1)
plt.plot(range(epoch), accuracy,     label='Training Accuracy')
plt.plot(range(epoch), val_accuracy, label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(loc='lower right')

plt.subplot(1, 2, 2)
plt.plot(range(epoch), loss,     label='Training Loss')
plt.plot(range(epoch), val_loss, label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(loc='upper right')

plt.show()

print(trainGen.class_indices)

uploaded = files.upload()

# Predicting images
for up in uploaded.keys():
    path = up
    img  = image.load_img(path, target_size = (200, 200))

    imgplot = plt.imshow(img)
    x       = image.img_to_array(img)
    x       = np.expand_dims(x, axis = 0)

    images  = np.vstack([x])
    classes = model.predict(images, batch_size = 10)
    print(up)

    # if classes[0][0] == 1:
    #     print('Architecture')
    # elif classes[0][1] == 1:
    #     print('Food and Drinks')
    # elif classes[0][2] == 1:
    #     print('Art and Culture')
    # elif classes[0][3] == 1:
    #     print('Travel and Adventure')
    # else:
    #     print('Unclassified')

    if classes == 0:
        print('Architecture')
    elif classes == 1:
        print('Art and Culture')
    elif classes == 2:
        print('Food and Drinks')
    elif classes == 3:
        print('Travel and Adventure')
    else:
        print('Unclassified')

# Save model to SavedModel format
exportDir = 'saved_model/'
tf.saved_model.save(model, exportDir)

# Convert model to TF-Lite format
converter    = tf.lite.TFLiteConverter.from_saved_model(exportDir)
tflite_model = converter.convert()

# tflite_model_file = pathlib.Path('vegs.tflite')
# tflite_model_file.write_bytes(tflite_model)

# Save the model
with open('model.tflite', 'wb') as t:
    t.write(tflite_model)