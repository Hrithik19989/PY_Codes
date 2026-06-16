import cv2

# Load the pre-trained Haar Cascade face detection model
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Load target image
image = cv2.imread('people.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces (returns bounding box array lists)
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Loop over each detected face bounding box region
for (x, y, w, h) in faces:
    # Draw a bounding rectangle around the face region: (image, start_point, end_point, color, thickness)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 3)

cv2.imshow('Face Detection Output', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
