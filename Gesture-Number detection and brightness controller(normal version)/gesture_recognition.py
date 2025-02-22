import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize Tkinter Window
root = tk.Tk()
root.title("Hand Gesture Number Recognition")
root.geometry("300x200")

label = tk.Label(root, text="Show a number with your hand", font=("Arial", 14))
label.pack(pady=20)

# Function to count raised fingers
def count_fingers(hand_landmarks):
    tips = [4, 8, 12, 16, 20]  # Thumb & Finger tip landmarks
    count = 0
    
    for tip in tips[1:]:  # Skip the thumb for now
        if hand_landmarks[tip].y < hand_landmarks[tip - 2].y:  # Tip is above the finger joint
            count += 1
    
    # Check thumb separately (sideways detection)
    if hand_landmarks[4].x < hand_landmarks[3].x:  # Left hand thumb open
        count += 1
    elif hand_landmarks[4].x > hand_landmarks[3].x:  # Right hand thumb open
        count += 1
    
    return count

# Open Webcam
cap = cv2.VideoCapture(0)

def update_frame():
    ret, frame = cap.read()
    if not ret:
        return
    
    frame = cv2.flip(frame, 1)  # Mirror effect
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            num = count_fingers(hand_landmarks.landmark)
            label.config(text=f"Detected Number: {num}")

    cv2.imshow("Hand Gesture Detection", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        cap.release()
        cv2.destroyAllWindows()
        root.quit()
        return

    root.after(10, update_frame)

# Start Webcam and Tkinter Loop
update_frame()
root.mainloop()
