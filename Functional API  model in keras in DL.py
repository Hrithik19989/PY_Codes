from keras.models import Model
from keras.layers import Input, Dense
import numpy as np

inputs = Input(shape=(100,))
x = Dense(64, activation='relu')(inputs)
outputs = Dense(10, activation='softmax')(x)

model = Model(inputs=inputs, outputs=outputs)

model.summary()

x_input = np.random.random((1, 100))

output = model.predict(x_input)
print("Output:\n", output)