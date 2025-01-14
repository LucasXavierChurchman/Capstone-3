import random
import cv2.cv2 as cv2
import numpy as np
import pandas as pd
import tensorflow as tf
from imutils import paths
from keras.applications.resnet50 import ResNet50
from keras.applications.xception import Xception
from keras.layers import Input
from keras.layers.core import Dense, Dropout, Flatten
from keras.layers.pooling import AveragePooling2D
from keras.models import Model
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer

def load_images_and_labels(target_labels, type):
    '''
    Loads all images from directories with names in target_labels
    a label and image array

    Arguments:
        target_labels: list of labels. Must be same as folders in data direcotry
        type: type of images to be loaded (google or broadcast)

    Returns:
        images: numpy array of images
        labels: numpy array of labels

    TODO: Make this work with np.load() and skimage (if possible)
    '''
    images = []
    labels = []

    for label in target_labels:
        if type == 'google':
            image_dir = '../data/google_imgs/{}'.format(label)
        if type == 'broadcast':
            image_dir = '../data/broadcast_imgs/{}'.format(label)
        print('Loading from {}'.format(image_dir))
        image_paths = list(paths.list_images(image_dir))

        for path in image_paths:
            img = cv2.imread(path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (240, 240))
            paths.list_images('../data/google_imgs/{}'.format(label))

            images.append(img)
            labels.append(label)

    images = np.array(images)
    labels = np.array(labels)

    return images, labels

def train_CNN(images, labels, epochs):
    '''
    Train the CNN with the training data and given number of epochs

    Arguments:
        images: numpy array of rgb images
        labels: numpy array of image class labels
        epochs: number of epochs for training

    Returns:
        model: trained keras model
        history: model history csv
        conmat: model confusion matrix

    TODO: Allow other hyper parameters as inputs, Tune/add layers, try different
    augmentations
    '''

    #turn string labels into binary labels
    lb = LabelBinarizer()
    labels = lb.fit_transform(labels)

    #Train test split
    X_train, X_test, y_train, y_test = train_test_split(images, labels, 
                                                        test_size = 0.20,
                                                        stratify = labels,
                                                        random_state = 17)

    #need 2 column array for target. [0,1] = dunk, [1,0] = jumpshot/three
    y_train = np.hstack((y_train, 1-y_train))
    y_test = np.hstack((y_test, 1-y_test))

    # Transformations
    ImageNet_mean = np.array([ 123.68, 116.779, 103.939 ])
    train_transformations = ImageDataGenerator(
                        rotation_range=45,
                        zoom_range=0.25,
                        width_shift_range=0.2,
                        height_shift_range=0.2,
                        fill_mode="wrap") #constant, nearest, reflect or wrap

    validation_transformations = ImageDataGenerator(ImageNet_mean)  

    train_transformations.mean = ImageNet_mean
    validation_transformations.mean = ImageNet_mean   

    #load transferred learning model
    transferred_model = ResNet50(weights = 'imagenet',
                                include_top = False,
                                input_tensor= Input(shape=(240, 240, 3)))

    #build model head
    head_model = transferred_model.output
    head_model = AveragePooling2D(pool_size=(7, 7))(head_model)
    head_model = Flatten(name="flatten")(head_model)
    head_model = Dense(512, activation="relu")(head_model)
    head_model = Dropout(0.50)(head_model)
    head_model = Dense(2, activation="sigmoid")(head_model)

    model = Model(inputs=transferred_model.input, outputs=head_model)

    #freeze layers from transferred model
    for layer in transferred_model.layers:
	    layer.trainable = False

    #initialize stochastic gradient descent optimizer
    opt = SGD(lr=0.0001, momentum=0.9, decay=0.0001)

    #compile and fit model
    model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])
    history = model.fit(X_train, y_train, 
                        validation_data = (X_test, y_test),
                        epochs = epochs)

    #get predictions and generate confusion matrix data
    y_pred = model.predict(X_test)
    con_mat = confusion_matrix(y_test.argmax(axis =1), y_pred.argmax(axis = 1))

    return model, history, con_mat
 
if __name__ == '__main__':
    random.seed(17)
    epochs = 200
    category = 'broadcast'
    target_labels = ['dunk', 'three']
    images, labels = load_images_and_labels(target_labels, type = category)
    model, history, con_mat = train_CNN(images, labels, epochs = epochs)

    model.save('../models/{}_{}_epochs.model'.format(category, epochs))

    hist_df = pd.DataFrame(history.history)
    hist_csv = '../models/{}_{}_epochs_history.csv'.format(category, epochs)
    with open(hist_csv, mode='w') as f:
        hist_df.to_csv(f)

    np.savetxt('../models/{}_{}_epochs_conmat.csv'.format(category, epochs), con_mat)
