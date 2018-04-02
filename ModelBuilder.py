#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 03:47:00 2017

@author: KwFung
"""
import numpy as np
from CreatePlayer2Set_Binary import createSet

# import the random game training set
dataSet = createSet()
X, Y, allP1Data, allP2Data = dataSet.runRandomGame()
Y = np.asarray(Y)

# Data preprocessing ---------------------------------------------------------------------------------

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 0)

# ----------------------------------------------------------------------------------------------------

# Build ANN
import keras
from keras.models import Sequential
from keras.layers import Dense

# Initialising the ANN
classifier = Sequential()

# Adding the input layer and the first hidden layer
classifier.add(Dense(units = 27, kernel_initializer = 'uniform', activation = 'tanh', input_dim = 9))

# Adding the second hidden layer
classifier.add(Dense(units = 27, kernel_initializer = 'uniform', activation = 'tanh'))

# Adding the third hidden layer
classifier.add(Dense(units = 27, kernel_initializer = 'uniform', activation = 'tanh'))

# Adding the output layer
classifier.add(Dense(units = 1, kernel_initializer = 'uniform', activation = 'sigmoid'))

# Compiling the ANN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Fitting the ANN to the Training set
classifier.fit(X_train, Y_train, batch_size = 10, epochs = 100)

# Predicting the Test set results
Y_pred = classifier.predict(X_test)
new_Y_pred = (Y_pred > 0.5)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(Y_test, new_Y_pred)

# Save the model
from keras.models import load_model
classifier.save('Player2_Model_Binary.h5')
