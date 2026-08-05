import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, BatchNormalization
import numpy as np
from keras.callbacks import EarlyStopping, ModelCheckpoint

# ---- CONFIGURATION PARAMETERS ----
SEQUENCE_LENGTH = 30  # Number of frames tracked per gesture sequence
DATA_DIMENSION = 126   # 21 landmarks * 3 coordinates (X, Y, Z) * 2 hands
TOTAL_CLASSES = 3      # Update this to match your total number of actions/signs

# ---- DEEP RNN (LSTM) MODEL BUILD ----
rnn_model = Sequential([
    LSTM(64, return_sequences=True, activation='tanh', input_shape=(SEQUENCE_LENGTH, DATA_DIMENSION)),
    BatchNormalization(),
    Dropout(0.2),
    
    LSTM(128, return_sequences=True, activation='tanh'),
    Dropout(0.2),
    
    LSTM(64, return_sequences=False, activation='tanh'),
    BatchNormalization(),
    Dropout(0.2),
    
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    
    Dense(TOTAL_CLASSES, activation='softmax')
])

# ---- COMPILE THE MODEL ----
# Using tf.keras here is fine, but if it throws an error, use: keras.optimizers.Adam()
rnn_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['categorical_accuracy']
)

rnn_model.summary()

# ---- FIXING THE NORMALIZATION LOGIC ----
def normalize_hand_landmarks(multi_hand_landmarks):
    """Safely normalizes points relative to the wrist (landmark 0) from MediaPipe."""
    all_hands = []
    if multi_hand_landmarks:
        for hand_landmarks in multi_hand_landmarks:
            wrist = hand_landmarks.landmark[0]
            normalized_list = []
            for lm in hand_landmarks.landmark:
                normalized_list.extend([lm.x - wrist.x, lm.y - wrist.y, lm.z - wrist.z])
            all_hands.append(normalized_list)
            
    # Pad or slice to maintain exactly 126 dimensions (2 hands data)
    if len(all_hands) == 1:
        return np.concatenate([all_hands[0], np.zeros(21*3)])
    elif len(all_hands) >= 2:
        return np.concatenate([all_hands[0], all_hands[1]])
        
    return np.zeros(DATA_DIMENSION)

callbacks = [
    EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True),
    ModelCheckpoint('best_rnn_sign_model.h5', monitor='val_loss', save_best_only=True)
]

# ---- CORRECTED REAL-TIME LOOP CODE SNIPPET ----
predictions_history = []
actions = ['Letter_A', 'Letter_B', 'Hello'] # Dynamic label array matching TOTAL_CLASSES
sequence = [np.zeros(DATA_DIMENSION) for _ in range(30)] # Simulated live buffer

if len(sequence) == 30:
    # 1. Predict and extract the first batch row cleanly using [0]
    res = rnn_model.predict(np.expand_dims(sequence, axis=0), verbose=0)[0]
    
    # 2. Extract max index from the 1D probability array
    max_idx = np.argmax(res)
    
    # 3. Apply confidence threshold
    if res[max_idx] > 0.85:
        predictions_history.append(max_idx)
        predictions_history = predictions_history[-5:] # Keep last 5 frames
        
        # 4. Statistical smoothing (Voting system)
        if len(predictions_history) > 0:
            stable_prediction_index = max(set(predictions_history), key=predictions_history.count)
            predicted_label = actions[stable_prediction_index]
            print(f"Predicted Sign: {predicted_label} (Confidence: {res[stable_prediction_index]:.2f})")
