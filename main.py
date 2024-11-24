import streamlit as st
import base64
from streamlit.components.v1 import html

# Set up Streamlit page
def main():
    st.title("Real-time Speech to Text")
    st.write("Click the buttons below to start or stop speaking. Your speech will be converted to text and displayed live below.")

    # HTML5 Audio Recorder with Start and Stop buttons
    audio_recorder_html = """
    <script>
        let stream;
        let mediaRecorder;
        let audioChunks = [];

        async function startRecording() {
            stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];
            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };
            mediaRecorder.start();
            document.getElementById("status").innerText = "Recording...";
        }

        function stopRecording() {
            mediaRecorder.stop();
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const reader = new FileReader();
                reader.readAsDataURL(audioBlob);
                reader.onloadend = () => {
                    const base64AudioMessage = reader.result.split(',')[1];
                    recognizeSpeech(base64AudioMessage);
                };
                document.getElementById("status").innerText = "Recording stopped.";
            };
        }

        async function recognizeSpeech(base64Audio) {
            const response = await fetch('https://speech.googleapis.com/v1p1beta1/speech:recognize?key=YOUR_API_KEY', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "config": {
                        "encoding": "LINEAR16",
                        "sampleRateHertz": 44100,
                        "languageCode": "en-US"
                    },
                    "audio": {
                        "content": base64Audio
                    }
                })
            });
            const result = await response.json();
            if (result.results && result.results.length > 0) {
                const transcript = result.results[0].alternatives[0].transcript;
                const textArea = document.getElementById("recognizedText");
                textArea.value += transcript + " ";
            } else {
                alert("Could not understand the audio. Please try again.");
            }
        }
    </script>
    <button onclick="startRecording()">Start Recording</button>
    <button onclick="stopRecording()">Stop Recording</button>
    <p id="status">Press start to begin recording.</p>
    <textarea id="recognizedText" style="width: 100%; height: 200px;"></textarea>
    """

    # Embed HTML5 Audio Recorder
    html(audio_recorder_html)

if __name__ == "__main__":
    main()


