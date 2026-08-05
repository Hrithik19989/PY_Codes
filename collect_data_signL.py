import os
import cv2
import time
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Suppress TensorFlow / oneDNN console logs
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# ---- CONFIGURATION ----
DATA_PATH = os.path.join('sign_data')
ACTIONS = np.array(['Letter_A', 'Letter_B', 'Hello']) 
NO_SEQUENCES = 30     
SEQUENCE_LENGTH = 30  

# Create file directories automatically
for action in ACTIONS:
    for sequence in range(NO_SEQUENCES):
        os.makedirs(os.path.join(DATA_PATH, action, str(sequence)), exist_ok=True)

# ---- MEDIAPIPE TASKS SETUP ----
# Configure the hand landmarker for synchronous IMAGE mode
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.IMAGE, 
    num_hands=2,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5
)

# Custom helper function to draw connections (Replaces legacy mp.solutions)
def draw_landmarks_on_frame(rgb_frame, detection_result):
    if not detection_result or not detection_result.hand_landmarks:
        return rgb_frame
    
    # Static mapping of standard MediaPipe Hand Connections
    connections = [
        (0, 1), (1, 2), (2, 3), (3, 4),        # Thumb
        (0, 5), (5, 6), (6, 7), (7, 8),        # Index Finger
        (5, 9), (9, 10), (10, 11), (11, 12),    # Middle Finger
        (9, 13), (13, 14), (14, 15), (15, 16),  # Ring Finger
        (13, 17), (0, 17),                     # Palm Base connections
        (17, 18), (18, 19), (19, 20)           # Pinky Finger
    ]
    h, w, _ = rgb_frame.shape
    
    for hand_landmarks in detection_result.hand_landmarks:
        # Draw individual joint dots
        for lm in hand_landmarks:
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(rgb_frame, (cx, cy), 3, (0, 255, 0), -1)
        # Draw connection lines between joints
        for connection in connections:
            start_idx = connection[0]
            end_idx = connection[1]
            pt1 = (int(hand_landmarks[start_idx].x * w), int(hand_landmarks[start_idx].y * h))
            pt2 = (int(hand_landmarks[end_idx].x * w), int(hand_landmarks[end_idx].y * h))
            cv2.line(rgb_frame, pt1, pt2, (0, 0, 255), 2)
            
    return rgb_frame

def normalize_hand_landmarks(detection_result):
    """Normalization logic to read from the modern Tasks Result schema."""
    all_hands = []
    if detection_result and detection_result.hand_landmarks:
        for hand_landmarks in detection_result.hand_landmarks:
            wrist = hand_landmarks[0] # Joint index 0 is the wrist
            normalized_list = []
            for lm in hand_landmarks:
                normalized_list.extend([lm.x - wrist.x, lm.y - wrist.y, lm.z - wrist.z])
            all_hands.append(normalized_list)
            
    if len(all_hands) == 1:
        return np.concatenate([all_hands[0], np.zeros(21*3)])
    elif len(all_hands) >= 2:
        return np.concatenate([all_hands[0], all_hands[1]])[:126]
        
    return np.zeros(126)

# ---- MAIN DATA COLLECTION PIPELINE ----
cap = cv2.VideoCapture(0)
print("Starting Camera pipeline. Get ready to sign...")

# Open landmarker context safely using "with"
with vision.HandLandmarker.create_from_options(options) as landmarker:
    break_all = False
    
    for action in ACTIONS:
        if break_all: break
        for sequence in range(NO_SEQUENCES):
            if break_all: break
            for frame_num in range(SEQUENCE_LENGTH):
                
                ret, frame = cap.read()
                if not ret: 
                    break
                
                frame = cv2.flip(frame, 1) 
                img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Convert the frame to MediaPipe Image object format
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
                
                # Synchronous processing guarantees exact alignment per frame
                current_results = landmarker.detect(mp_image)
                
                # Render skeletons on frame using the immediate tracking data
                frame = draw_landmarks_on_frame(frame, current_results)
                
                # Display tracking status windows to user
                if frame_num == 0:
                    cv2.putText(frame, 'STARTING NEW SEQUENCE COLLECTION', (100, 200), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                    cv2.putText(frame, f'Target Action: "{action}" | Video Sample #{sequence}', (15, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
                    cv2.imshow('Webcam Data Collection Feed', frame)
                    cv2.waitKey(1500) 
                else:
                    cv2.putText(frame, f'Recording Action: "{action}" | Video Sample #{sequence} | Frame: {frame_num}', (15, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
                    cv2.imshow('Webcam Data Collection Feed', frame)

                # Process normalization coordinates array
                landmarks = normalize_hand_landmarks(current_results)
                npy_path = os.path.join(DATA_PATH, action, str(sequence), f"{frame_num}.npy")
                np.save(npy_path, landmarks)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break_all = True
                    break
                    
cap.release()
cv2.destroyAllWindows()
print("Data Collection Phase Finished successfully!")
