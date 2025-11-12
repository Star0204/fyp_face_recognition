// Wait for the page to be fully loaded
document.addEventListener("DOMContentLoaded", () => {
    // Get all the buttons and elements
    const recordButton = document.getElementById("recordButton");
    const stopButton = document.getElementById("stopButton");
    const audioPlayback = document.getElementById("audioPlayback");
    const status = document.getElementById("status");
    const form = document.getElementById("upload-form");

    let mediaRecorder;
    let audioChunks = [];
    let audioBlob;

    // --- Recording Logic ---

    // When Record button is clicked
    recordButton.addEventListener("click", async () => {
        try {
            // Request microphone access
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);

            // When data is available (i.e., we are recording)
            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };

            // When recording is stopped
            mediaRecorder.onstop = () => {
                // NEW CODE
                audioBlob = new Blob(audioChunks, { type: audioChunks[0].type || 'audio/webm' });
                
                // Create a URL so we can play it back
                const audioUrl = URL.createObjectURL(audioBlob);
                audioPlayback.src = audioUrl;

                // Reset for next recording
                audioChunks = [];
                recordButton.disabled = false;
                stopButton.disabled = true;
                status.textContent = "Recording stopped. Ready to upload or re-record.";
            };

            // Start recording
            mediaRecorder.start();
            recordButton.disabled = true;
            stopButton.disabled = false;
            status.textContent = "Recording...";

        } catch (err) {
            console.error("Error accessing microphone:", err);
            status.textContent = "Error: Could not access microphone.";
        }
    });

    // When Stop button is clicked
    stopButton.addEventListener("click", () => {
        if (mediaRecorder && mediaRecorder.state === "recording") {
            mediaRecorder.stop();
        }
    });

    // --- Form Submission Logic ---

    // When the "Upload Person" button is clicked
    form.addEventListener("submit", async (event) => {
        // Prevent the form from submitting the old-fashioned way
        event.preventDefault(); 

        const nameInput = document.getElementById("name");
        const fileInput = document.getElementById("file");

        // Check if all fields are filled
        if (!nameInput.value || !fileInput.files[0] || !audioBlob) {
            alert("Please provide a name, a photo, and record a narration.");
            return;
        }

        // Create a FormData object to send all data
        const formData = new FormData();
        formData.append("name", nameInput.value);
        formData.append("file", fileInput.files[0]);
        formData.append("audio", audioBlob, `${nameInput.value}.webm`);

        status.textContent = "Uploading... please wait.";

        try {
            // Send all data to our Flask server
            const response = await fetch("/upload", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                status.textContent = "Upload successful! Page will refresh.";
                // Reload the page to clear the form
                setTimeout(() => window.location.reload(), 2000);
            } else {
                status.textContent = "Upload failed. Check terminal for errors.";
            }
        } catch (err) {
            console.error("Upload error:", err);
            status.textContent = "Upload failed. See console for details.";
        }
    });
});