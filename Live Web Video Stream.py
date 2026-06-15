import cv2

# Initialize the webcamera (0 is usually the default built-in camera)
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # If the frame was not grabbed successfully, break the loop
    if not ret:
        print("Error: Could not read frame.")
        break

    # Process the frame (e.g., convert to grayscale)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frames
    cv2.imshow('Live Webcam - Color', frame)
    cv2.imshow('Live Webcam - Grayscale', gray_frame)

    # Stop the stream when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera capture object and close windows
cap.release()
cv2.destroyAllWindows()
