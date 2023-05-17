import numpy as np
import cv2
import os

username = input("Enter your username: ")
username = username.strip()

img_path = os.path.join("C:\\Users", username, "Desktop", "verde2.jpeg")
img = cv2.imread(img_path)

# HSV color ranges
color_range = {
    "Red": (np.array([0, 50, 50]), np.array([10, 255, 255])),
    "Yellow": (np.array([10, 50, 50]), np.array([40, 255, 255])),
    "Green": (np.array([35, 50, 50]), np.array([80, 255, 255]))
}

# Convert to HSV color space
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Gaussian blur and Canny edge detection
blur = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (5, 5), 0)
edges = cv2.Canny(blur, threshold1=30, threshold2=100)

# Traffic light detection
semaforo = None

minDist = 30
param1 = 50
param2 = 30
minRadius = 5
maxRadius = 50

for color, (poco, mucho) in color_range.items():
    color_mask = cv2.inRange(hsv, poco, mucho)
    cv2.imshow("color_mask1", color_mask)
    color_mask = cv2.bitwise_and(color_mask, edges)
    cv2.imshow("color_mask2", color_mask)
    

    circles = cv2.HoughCircles(color_mask, cv2.HOUGH_GRADIENT, 1, minDist, param1, param2, minRadius, maxRadius)

    if circles is not None:
        semaforo = color
        circles = np.round(circles[0, :]).astype(int)

        if circles.ndim == 2 and circles.shape[1] == 3:
            #print("Circles array:", circles)
            x, y, r = circles[0]
            center = (x, y)
            radius = r
            cv2.circle(img, center, radius, (0, 0, 255), 2)
        elif circles.ndim == 1 and circles.size == 3:
            x, y, r = circles
            center = (x, y)
            radius = r
            cv2.circle(img, center, radius, (0, 0, 255), 2)
        break

# Traffic light status
if semaforo is not None:
    print("The color of the traffic light is:", semaforo)
else:
    print("No traffic light detected")

# Display the result
cv2.imshow("Traffic Light Detected", img)
cv2.waitKey(0)
cv2.destroyAllWindows()