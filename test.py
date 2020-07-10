import keras
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# To test the neural network...

mnist = tf.keras.datasets.mnist
(x_train, y_train),(x_test, y_test) = mnist.load_data()

x_test = tf.keras.utils.normalize(x_test, axis=1)

for indx in range(len(x_test)):
    x_test[indx] = np.ceil(x_test[indx])


model = tf.keras.models.load_model('epic_num_reader.model')
print(x_test[:1])
predictions = model.predict(x_test[:1])

count = 0
for x in range(len(predictions)):
    guess = (np.argmax(predictions[x]))
    actual = y_test[x]
    print("I predict this number is a:", guess)
    print("Number Actually Is a:", actual)
    if guess != actual:
        #print("--------------")
        #print('WRONG')
        #print('---------------')
        count+=1
    plt.imshow(x_test[x], cmap=plt.cm.binary)
    plt.show()

print("The program got", count, 'wrong, out of', len(x_test))
print(str(100 - ((count/len(x_test))*100)) + '% correct')