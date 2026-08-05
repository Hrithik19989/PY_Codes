import cv2
import mediapipe as mp
import numpy as np
import time
import threading
import os

# --- ALARM SYSTEM MODULE ---
last_alarm_time = 0
ALARM_COOLDOWN = 1.5  # Seconds to wait before playing another beep

def play_sound_worker():
    """Worker function to play a sharp system beep in the background."""
    try:
        if os.name == 'nt':  # Windows OS
            import winsound
            winsound.Beep(2500, 400)  # 2500Hz pitch for 400 milliseconds
        else:  # macOS / Linux terminal bell
            print('\a', end='', flush=True)
    except Exception:
        pass

def trigger_alarm():
    """Checks the cooldown window and launches the background sound thread."""
    global last_alarm_time
    current_time = time.time()
    if current_time - last_alarm_time > ALARM_COOLDOWN:
        last_alarm_time = current_time
        threading.Thread(target=play_sound_worker, daemon=True).start()

# --- CONSTANTS & THRESHOLDS ---
MODEL_PATH = "face_landmarker.task"
EYE_AR_THRESH = 0.22      # Eye aspect ratio threshold (closed eyes)
MOUTH_AR_THRESH = 0.55    # Mouth aspect ratio threshold (yawning)
EYE_CLOSED_FRAMES = 15    # Number of consecutive frames to trigger drowsiness alarm

# --- LANDMARK INDEX MAPS (MediaPipe Task Topology) ---
LEFT_EYE_TOP_BOTTOM = [159, 145]
LEFT_EYE_LEFT_RIGHT = [33, 133]
RIGHT_EYE_TOP_BOTTOM = [386, 374]
RIGHT_EYE_LEFT_RIGHT = [362, 263]
MOUTH_TOP_BOTTOM = [13, 14]
MOUTH_LEFT_RIGHT = [78, 308]

def calculate_ratio(landmarks, vertical_idx, horizontal_idx, img_w, img_h):
    """Calculates the ratio of vertical distance to horizontal distance."""
    # FIX: Access landmark objects properly via index from the list
    pt_v1 = landmarks[vertical_idx[0]]
    pt_v2 = landmarks[vertical_idx[1]]
    pt_h1 = landmarks[horizontal_idx[0]]
    pt_h2 = landmarks[horizontal_idx[1]]
    
    p_vert1 = np.array([pt_v1.x * img_w, pt_v1.y * img_h])
    p_vert2 = np.array([pt_v2.x * img_w, pt_v2.y * img_h])
    p_horiz1 = np.array([pt_h1.x * img_w, pt_h1.y * img_h])
    p_horiz2 = np.array([pt_h2.x * img_w, pt_h2.y * img_h])
    
    dist_vert = np.linalg.norm(p_vert1 - p_vert2)
    dist_horiz = np.linalg.norm(p_horiz1 - p_horiz2)
    return dist_vert / (dist_horiz + 1e-6)

# --- INITIALIZE MEDIAPIPE FACE LANDMARKER ---
BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=RunningMode.VIDEO
)

frame_counter = 0
cap = cv2.VideoCapture(0)

# Track unique frame timestamps required by running_mode=VIDEO
frame_timestamp_ms = 0

with FaceLandmarker.create_from_options(options) as landmarker:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
            
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # FIX: Ensure monotonically increasing timestamp for the pipeline
        frame_timestamp_ms += 33 
        detection_result = landmarker.detect_for_video(mp_image, frame_timestamp_ms)
        
        alarm_status = "NORMAL"
        
        if detection_result.face_landmarks:
            face_landmarks = detection_result.face_landmarks[0]
            
            left_ear = calculate_ratio(face_landmarks, LEFT_EYE_TOP_BOTTOM, LEFT_EYE_LEFT_RIGHT, w, h)
            right_ear = calculate_ratio(face_landmarks, RIGHT_EYE_TOP_BOTTOM, RIGHT_EYE_LEFT_RIGHT, w, h)
            ear = (left_ear + right_ear) / 2.0
            mar = calculate_ratio(face_landmarks, MOUTH_TOP_BOTTOM, MOUTH_LEFT_RIGHT, w, h)
            
            # --- COMBINED DROWSINESS & YAWN DETECTION LOGIC ---
            if ear < EYE_AR_THRESH:
                frame_counter += 1
                if frame_counter >= EYE_CLOSED_FRAMES:
                    alarm_status = "SLEEP MODE DETECTED!"
                    trigger_alarm()
            else:
                frame_counter = 0
                
            if mar > MOUTH_AR_THRESH:
                if alarm_status != "SLEEP MODE DETECTED!":
                    alarm_status = "YAWNING DETECTED!"
                    trigger_alarm()
            
            # --- HUD VISUALIZATION CONFIGURATION ---
            color = (0, 0, 255) if "SLEEP" in alarm_status else ((0, 255, 255) if "YAWNING" in alarm_status else (0, 255, 0))
            cv2.putText(frame, f"STATUS: {alarm_status}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)
            cv2.putText(frame, f"EAR: {ear:.2f}", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f"MAR: {mar:.2f}", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        else:
            frame_counter = 0
            cv2.putText(frame, "No Face Detected", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
        cv2.imshow("Drowsiness Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
