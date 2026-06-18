import cv2
from ultralytics import YOLO

# Load a pre-trained YOLOv8 Nano model (automatically downloads the weights file if missing)
model = YOLO('yolov8n.pt')

# Target standard web camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run deep learning inference on the frame
    # stream=True utilizes generator loops to save system memory
    results = model(frame, stream=True)

    # Parse and unpack prediction data loops
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # Unpack coordinates: top-left (x1, y1), bottom-right (x2, y2)
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            # Extract target object confidence score and class index labels
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            # Only visualize object outputs with confidence thresholds over 40%
            if confidence > 0.40:
                # Draw box around objects
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Format label tag text string
                label_text = f"{class_name} {confidence:.2f}"
                cv2.putText(frame, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display active deep learning framework prediction windows
    cv2.imshow('YOLOv8 Live AI Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
