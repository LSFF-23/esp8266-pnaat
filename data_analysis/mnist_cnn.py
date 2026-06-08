import collections, random
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from matplotlib import pyplot
import numpy as np

# 1. Preparing the dataset

# Downloading the mnist dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Splitting the training dataset into training and validation in a balanced way (75% train, 25% validation)
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, stratify=y_train, test_size=0.25, random_state=42)

# Checking the number of images in each dataset
print('Number of training images:', x_train.shape[0])
print('Number of validation images:', x_val.shape[0])
print('Number of test images:', x_test.shape[0])

# Counting the number of images per digit
counterTrain = collections.Counter(y_train)
counterVal = collections.Counter(y_val)
counterTest = collections.Counter(y_test)

# Plotting the number of images for each digit in a grouped bar chart
x_axis = np.arange(10)  # Creating indices for the 10 digits (0 to 9)
width = 0.25

fig, ax = pyplot.subplots(figsize=(10, 5))
rects1 = ax.bar(x_axis - width, [counterTrain[i] for i in range(10)], width, label='Train')
rects2 = ax.bar(x_axis, [counterVal[i] for i in range(10)], width, label='Validation')
rects3 = ax.bar(x_axis + width, [counterTest[i] for i in range(10)], width, label='Test')

ax.set_title('Images per digit')
ax.set_ylabel('Number of images')
ax.set_xlabel('Digit')
ax.set_xticks(x_axis)
ax.set_xticklabels(range(10))
ax.legend()
pyplot.show()

# 2. Formatting Data for Keras

# Input images need to be in a 4‑dimensional array (Batch_Size, Height, Width, Channels)
x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_val = x_val.reshape(x_val.shape[0], 28, 28, 1)
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)

input_shape = (28, 28, 1)

# Converting pixel values to float32
x_train = x_train.astype('float32')
x_val = x_val.astype('float32')
x_test = x_test.astype('float32')

# Normalizing pixel values (values between 0 and 1)
x_train /= 255
x_val /= 255
x_test /= 255

# 3. Building the CNN Architecture

model = Sequential()

# Convolution operation with 3x3 filter followed by ReLU
model.add(Conv2D(28, kernel_size=(3,3), input_shape=input_shape, activation='relu'))

# Max Pooling operation 2x2
model.add(MaxPooling2D(pool_size=(2, 2)))

# Second convolution layer
model.add(Conv2D(28, kernel_size=(3,3), activation='relu'))

# Flatten operation (converting matrices into a linear vector)
model.add(Flatten())

# Dense layer with 128 neurons
model.add(Dense(128, activation='relu'))

# 50% Dropout to avoid overfitting
model.add(Dropout(0.5))

# Output layer with 10 neurons (one for each digit) and Softmax
model.add(Dense(10, activation='softmax'))

# Model summary
model.summary()

# 4. Compilation and Training

adamOptimizer = Adam(learning_rate=0.001)
model.compile(optimizer=adamOptimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Training for 5 epochs
history = model.fit(x=x_train, y=y_train, validation_data=(x_val, y_val), epochs=5, batch_size=16, shuffle=True)

# 5. Evaluation and Prediction

# Evaluating the trained model with the test data
score = model.evaluate(x_test, y_test)
print('\nTest Loss: {:.3f}\nTest Accuracy: {:.3f}'.format(score[0], score[1]))

# Choosing an example image to test prediction
image_index = random.randint(0, len(y_test) - 1)
pyplot.imshow(x_test[image_index].reshape(28, 28), cmap='Greys')
pyplot.title(f"True Digit: {y_test[image_index]}")
pyplot.show()

# Predicting the digit for that image
pred = model.predict(x_test[image_index].reshape(1, 28, 28, 1))
print('\nThe predicted value is:', pred.argmax())

# 6. Plotting Training History

# Accuracy history
pyplot.figure()
pyplot.plot(history.history['accuracy'])
pyplot.plot(history.history['val_accuracy'])
pyplot.title('Model accuracy on training and validation')
pyplot.ylabel('Accuracy')
pyplot.xlabel('Epoch')
pyplot.legend(['Train', 'Validation'], loc='upper left')
pyplot.show()

# Loss history
pyplot.figure()
pyplot.plot(history.history['loss'])
pyplot.plot(history.history['val_loss'])
pyplot.title('Model loss on training and validation')
pyplot.ylabel('Loss')
pyplot.xlabel('Epoch')
pyplot.legend(['Train', 'Validation'], loc='upper left')
pyplot.show()