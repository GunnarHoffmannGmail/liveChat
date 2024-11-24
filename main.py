import streamlit as st
import speech_recognition as sr
import tempfile
import os
import base64
from streamlit.components.v1 import html

# Set up Streamlit page
def main():
    st.title("Real-time Speech to Text")
    st.write("Click the buttons below to start or stop speaking. Your speech will be converted to text and displayed live below.")

    recognizer = sr.Recognizer()

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
                    const audioInput = document.getElementById("audioInput");
                    audioInput.value = base64AudioMessage;
                    audioInput.dispatchEvent(new Event('change'));
                };
                document.getElementById("status").innerText = "Recording stopped.";
            };
        }
    </script>
    <button onclick="startRecording()">Start Recording</button>
    <button onclick="stopRecording()">Stop Recording</button>
    <p id="status">Press start to begin recording.</p>
    <input type="hidden" id="audioInput" onchange="sendAudioToStreamlit()">
    <script>
        function sendAudioToStreamlit() {
            const audioValue = document.getElementById("audioInput").value;
            if (audioValue) {
                const audioInputField = document.getElementById("audioInputHidden");
                audioInputField.value = audioValue;
                audioInputField.dispatchEvent(new Event('input'));
            }
        }
    </script>
    <input type="hidden" id="audioInputHidden">
    """

    # Embed HTML5 Audio Recorder
    audio_data = html(audio_recorder_html)

    # Handle audio data submission
    audio_base64 = st.text_input("", key="audioInputHidden")

    if audio_base64:
        audio_bytes = base64.b64decode(audio_base64)

        # Save the audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_bytes)
            temp_path = tmp_file.name

        # Recognize the speech using Google Web Speech API
        try:
            with sr.AudioFile(temp_path) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio)
                if "recognized_text" not in st.session_state:
                    st.session_state["recognized_text"] = ""
                st.session_state["recognized_text"] += " " + text
                st.text_area("Recognized Text", st.session_state["recognized_text"], height=200)
        except sr.UnknownValueError:
            st.error("Could not understand the audio. Please try again.")
        except sr.RequestError:
            st.error("Could not request results, please check your internet connection.")
        finally:
            # Clean up the temporary file
            os.remove(temp_path)

if __name__ == "__main__":
    main()

