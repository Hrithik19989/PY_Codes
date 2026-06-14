import cv2

# Load image and preprocess
image = cv2.imread('image.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
_, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)

# Find contours in the binary image
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    # Approximate the contour perimeter to resolve sharp corners
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
    
    # Extract coordinates for drawing text labels
    x, y, w, h = cv2.boundingRect(approx)

    # Identify shape based on the number of vertex sides
    if len(approx) == 3:
        shape_name = "Triangle"
    elif len(approx) == 4:
        # Check aspect ratio to distinguish square from rectangle
        aspect_ratio = float(w) / h
        shape_name = "Square" if 0.95 <= aspect_ratio <= 1.05 else "Rectangle"
    elif len(approx) == 5:
        shape_name = "Pentagon"
    else:
        shape_name = "Circle"

    # Draw the outline and label on the image
    cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
    cv2.putText(image, shape_name, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

cv2.imshow("Detected Shapes", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
