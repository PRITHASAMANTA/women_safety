Women Safety System 🚨

A real-time Women Safety System that uses gesture recognition and facial emotion analysis to detect potential danger and trigger immediate alerts via sound and SMS.

---

## 🔬 **Project Description**

This system intelligently monitors video input to detect:

- ✋ **Help Gesture**: Open palm detection using **MediaPipe Hands**.
- 😨 **Fear Emotion**: Detected via facial analysis using **DeepFace**.
- 👩‍🦰 **Gender Detection**: For optional log reporting.
- 🔔 **Alert Mechanism**: 
  - Plays an **alert sound** (`alert.mp3`)
  - Sends an **SMS alert** using **Twilio API**
  - Logs events in both `.txt` and `.csv` files.

---

## 🛠 **Technologies Used**

- Python 3.10
- OpenCV
- MediaPipe
- DeepFace
- TensorFlow / Keras
- Twilio API
- playsound
- PyInstaller (for packaging into `.exe`)
- CSV / TXT Logging

---

## 🚀 **Setup Instructions**

### 1️⃣ Clone the repository

##bash
git clone https://github.com/yourusername/women-safety-system.git
cd women-safety-system

2️⃣ Install dependencies
pip install opencv-python mediapipe deepface playsound twilio

3️⃣ Add required files
alert.mp3 — Place your alert sound file in the root directory.

4️⃣ Setup Twilio
Create a free Twilio account.

Get your Account SID, Auth Token, and Twilio phone number.

Update your integrated_gesture_fear.py with your credentials.

python
Copy
Edit
account_sid = "your_account_sid"
auth_token = "your_auth_token"
from_ = "+1YourTwilioNumber"
to = "+91YourVerifiedPhoneNumber"
5️⃣ Run the application
bash
Copy
Edit
python integrated_gesture_fear.py
💾 Packaging as Standalone .exe
Use PyInstaller to create a standalone executable:

bash
Copy
Edit
pyinstaller --onefile --add-data "alert.mp3;." --add-data "path_to_hand_landmark_tracking_cpu.binarypb;mediapipe/modules/hand_landmark" integrated_gesture_fear.py
📂 Generated Logs
alert_log.txt

alert_log.csv

Both files store timestamped alert data for future analysis.

🎯 Project Status
✅ Gesture detection
✅ Emotion (Fear) detection
✅ Real-time sound & SMS alerts
✅ Logging to file
✅ .exe packaging complete

📄 Author
Pritha Samanta
Meghnad Saha Institute of Technology
Guide: Biplab Kumar Barman

🔮 Future Scope
Mobile app version

GPS integration

Cloud-based emergency response

Improved multi-person detection


