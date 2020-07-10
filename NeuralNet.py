#import keras
#import tensorflow as tf
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Softmax, Dropout, BatchNormalization
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.utils import to_categorical, normalize
from tensorflow.keras.datasets import mnist
import matplotlib.pyplot as plt
import numpy as np

# Load Data
(x_train, y_train),(x_test, y_test) = mnist.load_data()


def normalizeData(x_train, x_test, y_train, y_test):
    x_train = normalize(x_train, axis=1)
    x_test = normalize(x_test, axis=1)

    print('Before: ')
    print(x_train[0])

    for indx in range(len(x_train)):
        x_train[indx] = np.ceil(x_train[indx])

    for indx in range(len(x_test)):
        x_test[indx] = np.ceil(x_test[indx])

    train0 = np.where(x_train == 0)
    train1 = np.where(x_train == 1)

    x_train[train0] = 1
    x_train[train1] = 0

    test0 = np.where(x_test == 0)
    test1 = np.where(x_test == 1)

    x_test[test0] = 1
    x_test[test1] = 0

    print('After: ')
    print(x_train[0])
    #plt.imshow(x_test[0], cmap=plt.cm.binary)
    #plt.show()

    x_train = x_train.reshape(60000, 28, 28, 1)
    x_test = x_test.reshape(10000, 28, 28, 1)

    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)

    return x_train, x_test, y_train, y_test


def generateModel(load=False):
    """ Generates a new model """
    model = Sequential()

    model.add(Conv2D(32, kernel_size=3, activation='relu', input_shape=(28,28,1)))
    model.add(BatchNormalization())
    model.add(Conv2D(32, kernel_size=3, activation='relu'))
    model.add(BatchNormalization())
    model.add(Conv2D(32, kernel_size=5, strides=2, padding='same', activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.4))

    model.add(Conv2D(64, kernel_size=3, activation='relu'))
    model.add(BatchNormalization())
    model.add(Conv2D(64, kernel_size=3, activation='relu'))
    model.add(BatchNormalization())
    model.add(Conv2D(64, kernel_size=5, strides=2, padding='same', activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.4))

    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(BatchNormalization()) 
    model.add(Dropout(0.4))
    model.add(Dense(10, activation='softmax'))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    if load:
        model = load_model('epic_num_reader.model')

    print('Model generated.')

    return model


def trainModel(model, xTrain, yTrain, xTest, yTest, save=True):
    """ Trains model using x_train and y_train """
    model.fit(xTrain, yTrain, validation_data=(xTest, yTest), epochs=3)

    if save:
        model.save('epic_num_reader.model')
        print("Model saved")

    return model


def showSomePredictions(model, xTestSet, yTestSet, numberOfImages=5):
    print(xTestSet[:1])
    print(xTestSet.shape)
    print(xTestSet[:1].shape)
    print(xTestSet[1].shape)
    predictions = model.predict(xTestSet[:numberOfImages])
    numErrors = 0

    for x in range(len(predictions)):
        guess = (np.argmax(predictions[x]))
        actual = np.argmax(yTestSet[x])
        print("I predict this number is a:", guess)
        print("Number Actually Is a:", actual)

        if guess != actual:
            numErrors += 1

        plt.imshow(xTestSet[x].reshape((28, 28)), cmap=plt.cm.binary)
        plt.show()

    print("The program got", numErrors, 'wrong, out of', len(xTestSet))
    print(str(100 - ((numErrors / len(xTestSet)) * 100)) + '% correct')



trainX, testX, trainY, testY = normalizeData(x_train, x_test, y_train, y_test)

model = generateModel(load=False)

model = trainModel(model, trainX, trainY, testX, testY, save=True)

showSomePredictions(model, testX, testY)



