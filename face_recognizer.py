import face_recognition
import cv2
import pickle
import os                   # NEW CODE: To check if files exist
from playsound import playsound # NEW CODE: To play the audio file

print("Loading saved encodings...")
# Load the known faces and encodings
with open("encodings.pickle", "rb") as f:
    data = pickle.load(f)

# NEW CODE: Define the path to your narrations folder
NARRATIONS_DIR = "narrations"

# NEW CODE: This variable will help us play the sound only ONCE per person
last_seen_name = None

# Initialize video capture from webcam
cap = cv2.VideoCapture(0)
print("Starting video stream...")

while True:
    # Grab a single frame of video
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the image from BGR color (OpenCV) to RGB color (face_recognition)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find all the faces and face encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    current_name = "Unknown" # Assume "Unknown" for this frame

    # Loop through each face in this frame of video
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(data["encodings"], face_encoding)
        name = "Unknown" # Default name if no match is found

        if True in matches:
            first_match_index = matches.index(True)
            name = data["names"][first_match_index]
        
        current_name = name # Set the name for this frame

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # --- NEW CODE: Audio Playing Logic (outside the loop) ---
    
    # We check if the person seen in this frame is different from the last frame
    if current_name != last_seen_name:
        if current_name != "Unknown":
            # This is a known person we haven't greeted yet!
            
            # Construct the path to their audio file (e.g., "narrations/Test_Person_2.webm")
            audio_file_path = os.path.join(NARRATIONS_DIR, f"{current_name}.webm")
            
            # Check if that audio file actually exists
            if os.path.exists(audio_file_path):
                print(f"Recognized {current_name}. Playing narration...")
                # Play the sound in a separate thread (so the video doesn't freeze)
                playsound(audio_file_path, block=False)
            else:
                print(f"Recognized {current_name}, but no audio file found at {audio_file_path}")
        
        # Update the last seen name
        last_seen_name = current_name
    # --------------------------------------------------------

    # Display the resulting image
    cv2.imshow('Face Recognition', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam and close windows
cap.release()
cv2.destroyAllWindows()