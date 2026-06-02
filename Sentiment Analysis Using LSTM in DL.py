import tensorflow as tf
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.preprocessing.sequence import pad_sequences

# 1. Hyperparameters
vocab_size = 20000  # Only consider the top 20,000 words
max_length = 200    # Max review length (truncate/pad to this length)
embedding_dim = 128
lstm_units = 64
batch_size = 64
epochs = 5

# 2. Load the IMDB Dataset
print("Loading data...")
(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=vocab_size)
print(f"Training sequences: {len(X_train)}, Test sequences: {len(X_test)}")

# 3. Pad Sequences to Ensure Uniform Input Length
print("Padding sequences...")
X_train = pad_sequences(X_train, maxlen=max_length, padding='post', truncating='post')
X_test = pad_sequences(X_test, maxlen=max_length, padding='post', truncating='post')

# 4. Build the LSTM Model
model = Sequential([
    # Embedding layer maps word indices to dense vectors
    Embedding(input_dim=vocab_size, output_dim=embedding_dim),
    
    # LSTM layer processes the sequential data
    LSTM(units=lstm_units, dropout=0.2, recurrent_dropout=0.2),
    
    # Dense output layer with sigmoid activation for binary classification (pos/neg)
    Dense(units=1, activation='sigmoid')
])

# 5. Compile the Model
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.summary()

# 6. Train the Model
print("Training the model...")
history = model.fit(
    X_train, y_train,
    batch_size=batch_size,
    epochs=epochs,
    validation_data=(X_test, y_test)
)

# 7. Evaluate the Model
print("Evaluating the model...")
test_loss, test_acc = model.evaluate(X_test, y_test, batch_size=batch_size)
print(f"\nTest Accuracy: {test_acc:.4f}")
print(f"Test Loss: {test_loss:.4f}")