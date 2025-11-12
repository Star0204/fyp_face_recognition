import os
from flask import Flask, request, render_template, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

# 1. Initialize the Flask app
app = Flask(__name__)

# Define paths
KNOWN_FACES_DIR = "known_faces"
NARRATIONS_DIR = "narrations"
app.config['UPLOAD_FOLDER'] = KNOWN_FACES_DIR
app.config['NARRATION_FOLDER'] = NARRATIONS_DIR

# Ensure the upload folders exist
os.makedirs(KNOWN_FACES_DIR, exist_ok=True)
os.makedirs(NARRATIONS_DIR, exist_ok=True)

# 2. Create the main web page (route)
@app.route('/')
def index():
    return render_template('index.html')

# 3. Update the /upload route to handle photo AND audio
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Get the name from the form data
        name = request.form['name']
        if not name:
            return jsonify({"error": "No name provided"}), 400

        # --- Handle the Photo File ---
        if 'file' not in request.files:
            return jsonify({"error": "No photo file part"}), 400
        
        photo_file = request.files['file']
        if photo_file.filename == '':
            return jsonify({"error": "No selected photo file"}), 400

        if photo_file:
            # Create a secure version of the name for the folder
            person_folder_name = secure_filename(name)
            person_folder_path = os.path.join(app.config['UPLOAD_FOLDER'], person_folder_name)
            os.makedirs(person_folder_path, exist_ok=True)
            
            # Save the photo
            photo_filename = secure_filename(photo_file.filename)
            photo_file.save(os.path.join(person_folder_path, photo_filename))
            print(f"Saved photo to {person_folder_path}")

        # --- Handle the Audio File ---
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file part"}), 400
            
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({"error": "No audio data"}), 400
        
        if audio_file:
            # Create a secure name for the audio file (e.g., "Yi_Kan.wav")
            audio_filename = f"{secure_filename(name)}.webm"
            audio_file.save(os.path.join(app.config['NARRATION_FOLDER'], audio_filename))
            print(f"Saved narration to {app.config['NARRATION_FOLDER']}")

        # --- Re-run encoding after saving new photo ---
        print("Re-running face encoding...")
        os.system("python encode_faces.py")
        print("Encoding complete!")

        # Send a success response back to the JavaScript
        return jsonify({"success": True, "message": "Files uploaded successfully"}), 200

# 4. Run the app
if __name__ == '__main__':
    app.run(debug=True)