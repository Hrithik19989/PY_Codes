from keras.models import Sequential
from keras.layers import Dense
import numpy as np

model = Sequential([
    Dense(64, activation='relu', input_shape=(100,)),
    Dense(10, activation='softmax')
])
model.summary()

x = np.random.random((1, 100))

output = model.predict(x)
print("Output:\n", output)