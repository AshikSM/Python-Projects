import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from tkinter import ttk
import screen_brightness_control as sbc
from PIL import Image, ImageTk

# Initialize MediaPipe Hands & Face Detection
mp_hands = mp.solutions.hands
mp_face = mp.solutions.face_detection
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
face_detection = mp_face.FaceDetection(min_detection_confidence=0.6)
mp_draw = mp.solutions.drawing_utils

# Function to count fingers
def count_fingers(hand_landmarks):
    fingers = [0, 0, 0, 0, 0]
    tips = [4, 8, 12, 16, 20]
    landmarks = hand_landmarks.landmark

    # Thumb
    if landmarks[tips[0]].x > landmarks[tips[0] - 2].x:
        fingers[0] = 1

    # Other fingers
    for i in range(1, 5):
        if landmarks[tips[i]].y < landmarks[tips[i] - 2].y:
            fingers[i] = 1

    return sum(fingers)

# Function to adjust brightness
def adjust_brightness(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]

    distance = np.sqrt((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2)
    brightness = int(np.interp(distance, [0.02, 0.2], [0, 100]))

    sbc.set_brightness(brightness)
    print(f"Brightness: {brightness}%")

# Tkinter GUI Setup
root = tk.Tk()
root.title("Gesture Control App")
root.geometry("600x500")
root.configure(bg="#1e1e1e")  # Dark mode background

# Styling
style = ttk.Style()
style.configure("TLabel", font=("Arial", 16), background="#1e1e1e", foreground="white")
style.configure("TFrame", background="#1e1e1e")

# Labels
title_label = ttk.Label(root, text="Gesture Control", font=("Arial", 20, "bold"))
title_label.pack(pady=10)

video_frame = ttk.Frame(root)
video_frame.pack()

canvas = tk.Canvas(video_frame, width=500, height=350, bg="black")
canvas.pack()

status_label = ttk.Label(root, text="Show a number with your hand!")
status_label.pack(pady=10)

# OpenCV Webcam
cap = cv2.VideoCapture(0)

def update_video():
    ret, frame = cap.read()
    if not ret:
        return
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Face Detection
    face_results = face_detection.process(rgb_frame)
    face_detected = False

    if face_results.detections:
        face_detected = True
        for detection in face_results.detections:
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = frame.shape
            x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Hand Detection
    results = hands.process(rgb_frame)
    detected_number = "No hand detected"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Detect number of fingers
            fingers_count = count_fingers(hand_landmarks)
            detected_number = f"Detected: {fingers_count}"

            # Adjust brightness based on thumb-index finger distance
            adjust_brightness(hand_landmarks)

    # Display Messages
    if face_detected:
        cv2.putText(frame, "Hi U Look Nice", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(frame, detected_number, (50, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Convert frame for Tkinter
    img = Image.fromarray(rgb_frame)
    img = img.resize((500, 350))
    img = ImageTk.PhotoImage(image=img)
    canvas.create_image(0, 0, anchor=tk.NW, image=img)
    canvas.img = img  # Keep a reference

    status_label.config(text=detected_number)
    root.after(10, update_video)

# Start Video Loop
update_video()

root.mainloop()
cap.release()
cv2.destroyAllWindows()
