import streamlit as st
import speech_recognition as sr
import tempfile
import os
import base64
from streamlit.components.v1 import html

# Set up Streamlit page
def main():
    st.title("Real-time Speech to Text")
    st.write("Click the button below to start speaking. Your speech will be converted to text and displayed below.")

    recognizer = sr.Recognizer()

    # HTML5 Audio Recorder
    audio_recorder_html = """
    <script>
        let stream;
        let mediaRecorder;
        let audioChunks = [];

        async function startRecording() {
            stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const reader = new FileReader();
                reader.readAsDataURL(audioBlob);
                reader.onloadend = () => {
                    const base64AudioMessage = reader.result.split(',')[1];
                    const audioInput = document.getElementById("audioInput");
                    audioInput.value = base64AudioMessage;
                    document.getElementById("audioForm").submit();
                };
            };
            mediaRecorder.start();
            setTimeout(() => {
                mediaRecorder.stop();
            }, 5000); // Record for 5 seconds
        }
    </script>
    <button onclick="startRecording()">Start Recording</button>
    <form id="audioForm" action="#" method="post">
        <input type="hidden" id="audioInput" name="audio">
    </form>
    """

    # Embed HTML5 Audio Recorder
    html(audio_recorder_html)

    # Retrieve recorded audio from form submission
    if "audio" in st.experimental_get_query_params():
        audio_base64 = st.experimental_get_query_params()["audio"][0]
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
                st.text_area("Recognized Text", text, height=200)
        except sr.UnknownValueError:
            st.error("Could not understand the audio. Please try again.")
        except sr.RequestError:
            st.error("Could not request results, please check your internet connection.")
        finally:
            # Clean up the temporary file
            os.remove(temp_path)

if __name__ == "__main__":
    main()

