import cv2
from keras.models import load_model
import numpy as np

# Load model and classifier
emotion_model = load_model("best_model.h5")

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Emotion categories
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)

    for (x, y, w, h) in faces:
        roi_gray = gray_frame[y:y + h, x:x + w]
        roi_gray = cv2.resize(roi_gray, (48, 48))
        img_pixels = np.expand_dims(np.expand_dims(roi_gray, -1), 0)
        img_pixels = img_pixels / 255.0

        predictions = emotion_model.predict(img_pixels)
        max_index = int(np.argmax(predictions))
        predicted_emotion = emotion_labels[max_index]

        # Display on frame
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
        cv2.putText(frame, predicted_emotion, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Trigger alert if emotion is distressing
        if predicted_emotion in ['Fear', 'Angry', 'Sad']:
            print("⚠️ Distress Emotion Detected!")

    cv2.imshow("Emotion Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
