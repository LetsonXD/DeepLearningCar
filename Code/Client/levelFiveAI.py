#Imports
import os
import random
import fnmatch
import datetime
import pickle
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
np.set_printoptions(formatter={'float_kind':lambda x: "%.4f" % x})
import pandas as pd
pd.set_option('display.width', 300)
pd.set_option('display.float_format', '{:,.4f}'.format)
pd.set_option('display.max_colwidth', 200)
import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Dropout, Flatten, Dense
from keras.models import load_model
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import cv2
from imgaug import augmenters as img_aug
import matplotlib.pyplot as plt
from PIL import Image

# Enables testing 
_TESTING = True

#Gets all the images from the image file ad strips the file path and the steering angle
file_path = 'images'
file_list = os.listdir(file_path)
image_paths = []
steering_angles = []
pattern = "*.png"
for filename in file_list:
    if fnmatch.fnmatch(filename, pattern):
        image_paths.append(os.path.join(file_path,filename))
        angle = int(filename[-7:-4])  
        steering_angles.append(angle)

#Displays an example image that was stripped
if _TESTING:
    image_index = 20
    plt.imshow(Image.open(image_paths[image_index]))
    print("image_path: %s" % image_paths[image_index] )
    print("steering_Angle: %d" % steering_angles[image_index] )

#Starts building the Dataframe
df = pd.DataFrame()
df['ImagePath'] = image_paths
df['Angle'] = steering_angles

#samples and bins worked out toguh trail and error
num_of_bins = 30
samples_per_bin = 500
hist, bins = np.histogram(df['Angle'], num_of_bins)

fig, axes = plt.subplots(1,1, figsize=(12,4))
axes.hist(df['Angle'], bins=num_of_bins, width=1, color='blue')

#Splits the data into traing and validation at 3:1
X_train, X_valid, y_train, y_valid = train_test_split( image_paths, steering_angles, test_size=0.2)
print("Training data: %d\nValidation data: %d" % (len(X_train), len(X_valid)))

# Displays the range of steering angles
if _TESTING:
    # plot the distributions of train and valid angles
    fig, axes = plt.subplots(1,2, figsize=(12,4))
    axes[0].hist(y_train, bins=num_of_bins, width=1, color='blue')
    axes[0].set_title('Training Data')
    axes[1].hist(y_valid, bins=num_of_bins, width=1, color='red')
    axes[1].set_title('Validation Data')

#Reads images and turn s them into RGB as cv2 saves them as BGR
def my_imread(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

#Augmentation method: Zoom
def zoom(image):
    zoom = img_aug.Affine(scale=(1, 1.3))  # zoom from 100% (no zoom) to 130%
    image = zoom.augment_image(image)
    return image

#Testing for Zoom
if _TESTING:
    fig, axes = plt.subplots(1, 2, figsize=(15, 10))
    image_orig = my_imread(image_paths[image_index])
    image_zoom = zoom(image_orig)
    axes[0].imshow(image_orig)
    axes[0].set_title("orig")
    axes[1].imshow(image_zoom)
    axes[1].set_title("zoomed")

#Augmentation method: Pan
def pan(image):
    # pan left / right / up / down about 10%
    pan = img_aug.Affine(translate_percent= {"x" : (-0.1, 0.1), "y": (-0.1, 0.1)})
    image = pan.augment_image(image)
    return image

#Testing for Pan
if _TESTING:
    fig, axes = plt.subplots(1, 2, figsize=(15, 10))
    image_orig = my_imread(image_paths[image_index])
    image_pan = pan(image_orig)
    axes[0].imshow(image_orig)
    axes[0].set_title("orig")
    axes[1].imshow(image_pan)
    axes[1].set_title("panned")

#Augmentation method: Brightness
def adjust_brightness(image):
    # increase by 100% or decrease brightness by 30%
    brightness = img_aug.Multiply((0.7, 2))
    image = brightness.augment_image(image)
    return image

#Testing for Brightness
if _TESTING:
    fig, axes = plt.subplots(1, 2, figsize=(15, 10))
    image_orig = my_imread(image_paths[image_index])
    image_brightness = adjust_brightness(image_orig)
    axes[0].imshow(image_orig)
    axes[0].set_title("orig")
    axes[1].imshow(image_brightness)
    axes[1].set_title("brightness adjusted")

#Augmentation method: Blur
def blur(image):
    kernel_size = random.randint(1, 3)  # Set to 3 from testing phase
    image = cv2.blur(image,(kernel_size, kernel_size))
    return image

#Testing for Blur
if _TESTING:
    fig, axes = plt.subplots(1, 2, figsize=(15, 10))
    image_orig = my_imread(image_paths[image_index])
    #image_blur = blur(image_orig)
    axes[0].imshow(image_orig)
    axes[0].set_title("orig")
    #axes[1].imshow(image_blur)
    axes[1].set_title("blurred")

#Augmentation method: Flip
def random_flip(image, steering_angle):
    is_flip = random.randint(0, 1)
    if is_flip == 1:
        # randomly flip horizon
        image = cv2.flip(image,1)
        steering_angle = 180 - steering_angle
    return image, steering_angle

#Testing for Flip
if _TESTING:
    fig, axes = plt.subplots(1, 2, figsize=(15, 10))
    image_orig = my_imread(image_paths[image_index])
    image_flip, steering_angle = random_flip(image_orig, steering_angles[image_index])
    axes[0].imshow(image_orig)
    axes[0].set_title("orig, angle=%s" % steering_angles[image_index])
    axes[1].imshow(image_flip)
    axes[1].set_title("flipped, angle=%s" % steering_angle)

# put it all together into one method to randomly augment images
def random_augment(image, steering_angle):
    if np.random.rand() < 0.5:
        image = pan(image)
    if np.random.rand() < 0.5:
        image = zoom(image)
    if np.random.rand() < 0.5:
        image = blur(image)
    if np.random.rand() < 0.5:
        image = adjust_brightness(image)
    image, steering_angle = random_flip(image, steering_angle)
    return image, steering_angle

#Testing the random augmenter
if _TESTING:
    # show a few randomly augmented images
    ncol = 2
    nrow = 10
    fig, axes = plt.subplots(nrow, ncol, figsize=(15, 50))

    for i in range(nrow):
        rand_index = random.randint(0, len(image_paths) - 1)
        image_path = image_paths[rand_index]
        steering_angle_orig = steering_angles[rand_index]

        image_orig = my_imread(image_path)
        image_aug, steering_angle_aug = random_augment(image_orig, steering_angle_orig)

        axes[i][0].imshow(image_orig)
        axes[i][0].set_title("original, angle=%s" % steering_angle_orig)
        axes[i][1].imshow(image_aug)
        axes[i][1].set_title("augmented, angle=%s" % steering_angle_aug)

#preprocessing method to train the A.I. with
def img_preprocess(image):
    height, _, _ = image.shape
    image = image[int(height/2):,:,:]  # remove top half of the image, as it is not relavant for lane following
    image = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)  # Nvidia model said it is best to use YUV color space
    image = cv2.GaussianBlur(image, (3,3), 0) #image is already blurry, may not need this?
    image = cv2.resize(image, (200,66)) # input image size (200,66) Nvidia model
    image = image / 255 # normalizing the data, look into bettr alternatives n the future
    return image

#Testing for preprocessing
if _TESTING:
    fig, axes = plt.subplots(1, 2, figsize=(15, 10))
    image_orig = my_imread(image_paths[image_index])
    image_processed = img_preprocess(image_orig)
    axes[0].imshow(image_orig)
    axes[0].set_title("orig")
    axes[1].imshow(image_processed)
    axes[1].set_title("processed")

#Building the Nvidia model, using an established architecture at the advise of Shengxiang
def nvidia_model():
    model = Sequential(name='Nvidia_Model')
    
    # elu=Expenential Linear Unit, similar to leaky Relu
    # skipping 1st hiddel layer (nomralization layer), as we have normalized the data
    
    # Convolution Layers
    model.add(Conv2D(24, (5, 5), strides=(2, 2), input_shape=(66, 200, 3), activation='elu')) 
    model.add(Conv2D(36, (5, 5), strides=(2, 2), activation='elu')) 
    model.add(Conv2D(48, (5, 5), strides=(2, 2), activation='elu')) 
    model.add(Conv2D(64, (3, 3), activation='elu')) 
    model.add(Conv2D(64, (3, 3), activation='elu')) 
    
    # Fully Connected Layers
    model.add(Flatten())
    model.add(Dense(100, activation='elu'))
    model.add(Dense(50, activation='elu'))
    model.add(Dense(10, activation='elu'))
    
    # output layer: turn angle (from 45-135, 90 is straight, <90 turn left, >90 turn right)
    model.add(Dense(1)) 
    

    # MSE (Mean Squared Error) as loss function
    model.compile(loss='mse', optimizer='Adam')
    
    return model

#Initialise model
model = nvidia_model()

#display model
if _TESTING:
    print(model.summary())

def image_data_generator(image_paths, steering_angles, batch_size, is_training):
    while True:
        batch_images = []
        batch_steering_angles = []
        
        for i in range(batch_size):
            random_index = random.randint(0, len(image_paths) - 1)
            image = my_imread(image_paths[random_index])
            steering_angle = steering_angles[random_index]
            if is_training:
                # training: augment image
                image, steering_angle = random_augment(image, steering_angle)
              
            image = img_preprocess(image)
            batch_images.append(image)
            batch_steering_angles.append(steering_angle)
            
        yield( np.asarray(batch_images), np.asarray(batch_steering_angles))

if _TESTING:
    ncol = 2
    nrow = 2

    X_train_batch, y_train_batch = next(image_data_generator(X_train, y_train, nrow, True))
    X_valid_batch, y_valid_batch = next(image_data_generator(X_valid, y_valid, nrow, False))
    fig, axes = plt.subplots(nrow, ncol, figsize=(15, 6))
    fig.tight_layout()

    for i in range(nrow):
        axes[i][0].imshow(X_train_batch[i])
        axes[i][0].set_title("training, angle=%s" % y_train_batch[i])
        axes[i][1].imshow(X_valid_batch[i])
        axes[i][1].set_title("validation, angle=%s" % y_valid_batch[i])

log_path = 'logs/'
ai_path = 'Code/AIModel'
# saves the model weights after each epoch if the validation loss decreased
checkpoint_callback = keras.callbacks.ModelCheckpoint(filepath=os.path.join(ai_path,'lane_navigation_check.h5'), verbose=1, save_best_only=True)
log_dir = log_path + datetime.datetime.now().strftime("%y%m%d_%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)


history = model.fit_generator(image_data_generator( X_train, y_train, batch_size=200, is_training=True),
                              steps_per_epoch=300,
                              epochs=40,
                              validation_data = image_data_generator( X_valid, y_valid, batch_size=200, is_training=False),
                              validation_steps=200,
                              verbose=1,
                              shuffle=1,
                              callbacks=[tensorboard_callback, checkpoint_callback])
# always save model output as soon as model finishes training
model.save(os.path.join(ai_path,'lane_navigation_final.h5'))


history_path = os.path.join(ai_path,'history.pickle')
with open(history_path, 'wb') as f:
    pickle.dump(history.history, f, pickle.HIGHEST_PROTOCOL)
    
history.history

history_path = os.path.join(ai_path,'history.pickle')
with open(history_path, 'rb') as f:
    history = pickle.load(f)

def summarize_prediction(Y_true, Y_pred):
    
    mse = mean_squared_error(Y_true, Y_pred)
    r_squared = r2_score(Y_true, Y_pred)
    
    print(f'mse       = {mse:.2}')
    print(f'r_squared = {r_squared:.2%}')
    print()
    
def predict_and_summarize(X, Y):
    model = load_model(f'{ai_path}/lane_navigation_check.h5')
    Y_pred = model.predict(X)
    summarize_prediction(Y, Y_pred)
    return Y_pred

n_tests = 100
X_test, y_test = next(image_data_generator(X_valid, y_valid, 400, False))

y_pred = predict_and_summarize(X_test, y_test)

n_tests_show = 2
fig, axes = plt.subplots(n_tests_show, 1, figsize=(10, 4 * n_tests_show))
for i in range(n_tests_show):
    axes[i].imshow(X_test[i])
    axes[i].set_title(f"actual angle={y_test[i]}, predicted angle={int(y_pred[i])}, diff = {int(y_pred[i])-y_test[i]}")

plt.show()