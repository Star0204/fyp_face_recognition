# Import necessary libraries
import face_recognition
import pickle
import os

print("Starting encoding...")

# Path to the folder with known faces
KNOWN_FACES_DIR = "known_faces"

# Initialize lists to hold encodings and names
known_encodings = []
known_names = []

# Loop through each person in the known_faces directory
for name in os.listdir(KNOWN_FACES_DIR):
    # Construct the full path to the person's directory
    person_dir = os.path.join(KNOWN_FACES_DIR, name)
    
    # Skip if it's not a directory
    if not os.path.isdir(person_dir):
        continue

    # Loop over each image of the person
    for filename in os.listdir(person_dir):
        print(f"Processing {name}'s image: {filename}")
        
        # Load the image file
        image_path = os.path.join(person_dir, filename)
        image = face_recognition.load_image_file(image_path)
        
        # Get face encodings for the face in the current image
        # We assume each image has only one face
        encodings = face_recognition.face_encodings(image)
        
        if len(encodings) > 0:
            # Add the first found encoding and the name to our lists
            known_encodings.append(encodings[0])
            known_names.append(name)
        else:
            print(f"Warning: No face found in {filename}. Skipping.")

# Save the encodings and names to a file
# This file will be used by our live recognition script
data = {"encodings": known_encodings, "names": known_names}
with open("encodings.pickle", "wb") as f:
    f.write(pickle.dumps(data))

print("Encoding complete. Data saved to encodings.pickle")