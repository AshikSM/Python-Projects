import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Open webcam
cap = cv2.VideoCapture(0)
prev_y = None  # Store previous Y position
pause_state = False  # Track pause/resume state
last_pause_time = 0  # Track time for pause toggle

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip and convert image
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process frame with Mediapipe
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Extract index finger tip position
            index_finger_tip = hand_landmarks.landmark[8]  # Index finger tip
            h, w, _ = frame.shape
            index_x, index_y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

            # Count how many fingers are up
            finger_tips = [8, 12, 16, 20, 4]  # Index, Middle, Ring, Pinky, Thumb
            fingers_up = 0

            for tip in finger_tips:
                fingertip = hand_landmarks.landmark[tip]
                base_y = hand_landmarks.landmark[tip - 2].y * h  # Base of finger
                if fingertip.y * h < base_y:  # Finger is up
                    fingers_up += 1

            # Draw landmarks on hand
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Gesture: Scroll Shorts (Up and Down)
            if prev_y is not None:
                if index_y < prev_y - 20:  # Move Up (Next Short/Reel)
                    pyautogui.press("down")
                    print("Scrolling Down (Next Short)...")
                elif index_y > prev_y + 20:  # Move Down (Previous Short/Reel)
                    pyautogui.press("up")
                    print("Scrolling Up (Previous Short)...")

            prev_y = index_y  # Update previous Y position

            # Gesture: Pause/Resume when showing all 5 fingers
            current_time = time.time()
            if fingers_up == 5 and (current_time - last_pause_time > 2):  # Add a 2-second delay
                pyautogui.press("space")  # Toggle pause/play
                pause_state = not pause_state
                last_pause_time = current_time
                print("Video Paused" if pause_state else "Video Resumed")

    # Show webcam feed
    cv2.imshow("Gesture Controller", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
