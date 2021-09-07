# -*- coding: utf-8 -*-

"""
    Fit a CNN on the pngs files in png_v4 ---------> (with image_dataset_from_directory)
    for one machine e.g. 'valve' (list_datasets[0])
    from: https://keras.io/examples/vision/image_classification_from_scratch/
"""

from utils import list_datasets, rootFolder
import datetime
import sys
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


# Part 1 - Building the CNN
image_size = (333, 216)
batch_size = 32
data_augmentation = keras.Sequential(
    [
        # layers.experimental.preprocessing.RandomFlip("horizontal"),
        # layers.experimental.preprocessing.RandomRotation(0.1),
    ]
)

# Initialising the CNN v4: make model
def make_model(input_shape, num_classes):
    inputs = keras.Input(shape=input_shape)
    # Image augmentation block
    x = data_augmentation(inputs)
    
    # Entry block
    x = layers.experimental.preprocessing.Rescaling(1.0 / 255)(x)
    x = layers.Conv2D(32, 3, strides=2, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    x = layers.Conv2D(64, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    previous_block_activation = x  # Set aside residual

    for size in [128, 256]: #, 512, 728]:
        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.MaxPooling2D(3, strides=2, padding="same")(x)

        # Project residual
        residual = layers.Conv2D(size, 1, strides=2, padding="same")(
            previous_block_activation
        )
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x  # Set aside next residual

    x = layers.SeparableConv2D(1024, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    x = layers.GlobalAveragePooling2D()(x)
    if num_classes == 2:
        activation = "sigmoid"
        units = 1
    else:
        activation = "softmax"
        units = num_classes

    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(units, activation=activation)(x)
    return keras.Model(inputs, outputs)

model = make_model(input_shape=image_size + (3,), num_classes=2)
epochs = 8 # 50

model.compile(
    optimizer=keras.optimizers.Adam(1e-3),
    loss="binary_crossentropy",
    metrics=["accuracy"],
)

# Part 2 - Fitting the CNN to the images
for folder_machine in list_datasets: 
    use_folder = rootFolder + 'data/' + folder_machine + '/png_v4'
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        use_folder,
        validation_split=0.2,
        subset="training",
        seed=1337,
        image_size=image_size,
        batch_size=batch_size,
    )
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        use_folder,
        validation_split=0.2,
        subset="validation",
        seed=1337,
        image_size=image_size,
        batch_size=batch_size,
    )
    model.fit(
        train_ds, epochs=epochs, validation_data=val_ds,
    )

    # save the model to disk  ----------------------- ' + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '_
    filename_classifier = rootFolder + '4_dc_classifiers/' + folder_machine + '_cnn.h5'
    model.save(filename_classifier)

    print(folder_machine, ': model saved: ', filename_classifier)
    

# Visualize the data 9 first images
# import matplotlib.pyplot as plt

# plt.figure(figsize=(10, 10))
# for images, labels in train_ds.take(1):
#     for i in range(9):
#         ax = plt.subplot(3, 3, i + 1)
#         plt.imshow(images[i].numpy().astype("uint8"))
#         plt.title(int(labels[i]))
#         plt.axis("off")

  
# /Users/david/opt/anaconda3/lib/python3.8/site-packages/tensorflow/python/keras/utils/generic_utils.py:494: CustomMaskWarning: Custom mask layers require a config and must override get_config. When loading, the custom mask layer must be passed to the custom_objects argument.
#   warnings.warn('Custom mask layers require a config and must override '
# model saved: /Users/david/DEVS_LOCAL/dev-ia-son/partage-ia-son/dc_classifiers/2021-08-20-23-07-58_valve_cnn.h5





