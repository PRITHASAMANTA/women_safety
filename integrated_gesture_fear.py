import cv2
import mediapipe as mp
from deepface import DeepFace
from playsound import playsound
import threading
from twilio.rest import Client
from datetime import datetime

# ---------- ALERT UTILS ----------

def play_alert():
    playsound("alert.mp3")  # Make sure alert.mp3 is in the same folder

def send_sms_alert():
   
    account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
    auth_token = 'YOUR_TWILIO_AUTH_TOKEN'

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="🚨 ALERT: Help Gesture or Fear Emotion Detected!",
        from_="+19206968608",     # Your Twilio number
        to="+918695261140"        # Your verified number
    )
    print("SMS sent:", message.sid)

def log_event_to_file(event_text):
    with open("alert_log.txt", "a") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {event_text}\n")

# ---------- EMOTION DETECTION ----------

def detect_fear_emotion(frame):
    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        return result[0]['dominant_emotion']
    except:
        return "Unknown"

# ---------- GESTURE DETECTION ----------

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

def is_help_gesture(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    if hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[tips[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    for id in range(1, 5):
        if hand_landmarks.landmark[tips[id]].y < hand_landmarks.landmark[tips[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return all(fingers)

# ---------- MAIN LOOP ----------

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Gesture Detection
    results = hands.process(frame_rgb)
    help_detected = False
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
            if is_help_gesture(handLms):
                help_detected = True
                cv2.putText(frame, "HELP GESTURE DETECTED!", (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # Emotion Detection
    emotion = detect_fear_emotion(frame)
    cv2.putText(frame, f"Emotion: {emotion}", (10, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 100, 255), 2)

    # Gender Detection (optional for info)
    try:
        result = DeepFace.analyze(frame, actions=['gender'], enforce_detection=False)
        gender = result[0]['dominant_gender']
        cv2.putText(frame, f"Gender: {gender}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    except:
        gender = "Unknown"
        cv2.putText(frame, "Face not detected", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 100, 100), 2)

    # Trigger Alert only on gesture or fear
    if help_detected or emotion == "fear":
        cv2.putText(frame, "⚠ SAFETY ALERT!", (10, 160),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 3)

        threading.Thread(target=play_alert).start()
        threading.Thread(target=send_sms_alert).start()
        log_event_to_file("ALERT TRIGGERED: Help Gesture or Fear Emotion Detected")

    # Show Output
    cv2.imshow("Women's Safety System", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
