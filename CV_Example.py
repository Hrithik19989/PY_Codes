import cv2

# Load an image in color
image = cv2.imread('image.jpg')

# Display the image in a window
cv2.imshow('Original Image', image)

# Wait for any key press to close the window
cv2.waitKey(0)
cv2.destroyAllWindows()

import cv2

image1= cv2.imread('image.jpg')

# Convert BGR to Grayscale
gray_image = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)

# Convert BGR to RGB (useful for matplotlib)
rgb_image = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)

cv2.imshow('Grayscale Image', gray_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

import cv2

image2 = cv2.imread('image.jpg')

# Resize image to specific dimensions (Width, Height)
resized_image = cv2.resize(image2, (300, 200))

# Crop image using array slicing: [startY:endY, startX:endX]
cropped_image = image2[50:200, 100:300]

cv2.imshow('Resized', resized_image)
cv2.imshow('Cropped', cropped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

import cv2

image3 = cv2.imread('image.jpg')

# Apply Gaussian Blur (kernel size must be positive and odd)
blurred_image = cv2.GaussianBlur(image3, (7, 7), 0)

cv2.imshow('Blurred Image', blurred_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

import cv2

image4= cv2.imread('image.jpg')
gray = cv2.cvtColor(image4, cv2.COLOR_BGR2GRAY)

# Apply Canny Edge Detection (threshold1, threshold2)
edges = cv2.Canny(gray, 100, 200)

cv2.imshow('Edges', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()

import cv2

image5 = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# Apply binary thresholding
# Any pixel value > 127 becomes 255 (white), else 0 (black)
ret, thresholded = cv2.threshold(image5, 127, 255, cv2.THRESH_BINARY)

cv2.imshow('Thresholded', thresholded)
cv2.waitKey(0)
cv2.destroyAllWindows()


