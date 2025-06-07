import cv2
import mediapipe as mp
import keyboard  # for controlling keys

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Start video capture
cap = cv2.VideoCapture(0)

def count_fingers(hand_landmarks):
    fingers = []

    # Thumb
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    tips = [8, 12, 16, 20]
    bottoms = [6, 10, 14, 18]

    for tip, bottom in zip(tips, bottoms):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[bottom].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return sum(fingers)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            finger_count = count_fingers(hand_landmarks)

            # Control Hill Climb Racing based on fingers
            if finger_count == 0:
                keyboard.release("right")
                keyboard.press("left")
                print("Brake Pressed")
            elif finger_count == 5:
                keyboard.release("left")
                keyboard.press("right")
                print("Gas Pressed")
            else:
                keyboard.release("left")
                keyboard.release("right")

            cv2.putText(frame, f"Fingers: {finger_count}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
hands.close()
cv2.destroyAllWindows()
