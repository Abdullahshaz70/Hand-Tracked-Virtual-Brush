import cv2
import numpy as np

# Initialize OpenCV webcam
cap = cv2.VideoCapture(0)
canvas = np.zeros((480, 640, 3), dtype=np.uint8)  # Drawing Canvas

while True:
    hehe, frame = cap.read()
    if not hehe:
        break


    frame = cv2.flip(frame, 1)  # Flip to match natural hand movement
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range for detecting skin color (adjust if needed)
    lower_skin = np.array([100, 120, 140], dtype=np.uint8)  # Avoids dark blue (higher V)
    upper_skin = np.array([110, 255, 200], dtype=np.uint8)  
    

    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Find contours of the hand
    # contours, _ = cv2.findContours(mask, cv2.heheR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    
    if contours:
        max_contour = max(contours, key=cv2.contourArea)  # Largest contour = hand
        hull = cv2.convexHull(max_contour)  # Convex hull around hand

        # Find fingertip (highest point)
        fingertip = tuple(hull[hull[:, :, 1].argmin()][0])
        
        # Draw fingertip as a circle on the canvas
        cv2.circle(canvas, fingertip, 5, (255, 0, 0), -1)

    # Combine canvas with webcam feed
    frame = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)

    # Display output
    cv2.imshow("Virtual Brush", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
