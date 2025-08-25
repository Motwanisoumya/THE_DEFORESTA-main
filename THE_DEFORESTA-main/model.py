import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Rescaling, RandomFlip, RandomRotation, RandomZoom, Dropout 
from tensorflow.keras.utils import image_dataset_from_directory  
import pathlib


data_dir = pathlib.Path('C:\\Users\\mitta\\OneDrive\\Desktop\\Hackathon\\Dataset')
img_width = 350
img_height = 350
batch_size = 32
num_classes = 2

train_ds = image_dataset_from_directory(
    data_dir,
    validation_split=0.25,
    subset='training',
    seed=123,
    image_size=(img_width, img_height),
    batch_size=batch_size
)

val_ds = image_dataset_from_directory(
    data_dir,
    validation_split=0.25,
    subset='validation',
    seed=123,
    image_size=(img_width, img_height),
    batch_size=batch_size
)


AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)


data_augmentation = Sequential(
  [
    RandomFlip("horizontal", input_shape=(img_width, img_height,3)),
    RandomRotation(0.1),
    RandomZoom(0.1),
  ]
)


model = Sequential([
    data_augmentation,
    Rescaling(1./250, offset=-1, input_shape=(img_width, img_height, 3)),
    Conv2D(32, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Conv2D(64, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Conv2D(128, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Dropout(0.1),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(num_classes)
])

model.compile(
  optimizer='adam',
  loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
  metrics=['accuracy'])

model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=50
)

model.save('Deforest.keras')

# test_loss, test_acc = model.evaluate(test_images, test_labels)

# predictions = model.predict(my_images)