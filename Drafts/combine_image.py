import cv2
import numpy as np

# Read the video file
video_capture = cv2.VideoCapture('input_video.mp4')

# Check if the video file was successfully opened
if not video_capture.isOpened():
    print("Error: Could not open video file.")
    exit()

# Read the first frame
ret, frame1 = video_capture.read()

# Check if the first frame was read successfully
if not ret:
    print("Error: Could not read the first frame.")
    exit()

# Read the second frame
ret, frame2 = video_capture.read()

# Check if the second frame was read successfully
if not ret:
    print("Error: Could not read the second frame.")
    exit()

# Invert the second frame
frame2_inverted = cv2.bitwise_not(frame2)

# Overlay the inverted second frame on the first frame with 50% transparency
alpha = 0.5
overlay = cv2.addWeighted(frame1, alpha, frame2_inverted, 1 - alpha, 0)

# Save the resulting frame as an image
cv2.imwrite('overlay_image.jpg', overlay)

# Release the video capture object
video_capture.release()

print("Overlay image saved successfully.")
