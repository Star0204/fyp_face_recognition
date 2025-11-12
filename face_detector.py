# 1. Import the OpenCV library
import cv2

# 2. Load a pre-trained model for face detection (Haar Cascade)
# This file comes with OpenCV and is great for simple detection.
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 3. Initialize video capture from your default webcam (usually index 0)
cap = cv2.VideoCapture(0)

# 4. Start a loop to read frames from the webcam continuously
while True:
    # Read one frame from the webcam
    # 'ret' is a boolean (True/False) on whether it succeeded
    # 'frame' is the actual image captured
    ret, frame = cap.read()
    if not ret:
        break # If frame not captured, exit the loop

    # 5. Convert the frame to grayscale for the detector
    # Detection is typically more accurate on grayscale images.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 6. Detect faces in the grayscale frame
    # This returns a list of rectangles (x, y, width, height) for each face found.
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # 7. Draw a green rectangle around each detected face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # 8. Display the resulting frame in a window named "Face Detection"
    cv2.imshow('Face Detection', frame)

    # 9. Wait for the 'q' key to be pressed to quit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 10. Clean up: release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()