import cv2

cap = cv2.VideoCapture(0)  # Try 0, 1, or 2 if needed

if not cap.isOpened():
    print("Error: Cannot access the webcam!")
else:
    print("Webcam is working!")

cap.release()
cv2.destroyAllWindows()
