import streamlit as st
from streamlit_audiorecorder import audiorecorder as ar
import speech_recognition as sr
import tempfile
import os

# Set up Streamlit page
def main():
    st.title("Real-time Speech to Text")
    st.write("Click the button below to record audio. Your speech will be converted to text and displayed below.")

    # Record audio using streamlit-audiorecorder
    audio_data = ar("Start Recording", "Recording...")

    if audio_data:
        st.audio(audio_data, format='audio/wav')
        recognizer = sr.Recognizer()

        # Use a temporary file to store the recorded audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_data)
            temp_path = tmp_file.name

        # Recognize the speech using Google Web Speech API
        with sr.AudioFile(temp_path) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                st.text_area("Recognized Text", text, height=200)
            except sr.UnknownValueError:
                st.error("Could not understand the audio. Please try again.")
            except sr.RequestError:
                st.error("Could not request results, please check your internet connection.")

        # Clean up the temporary file
        os.remove(temp_path)

if __name__ == "__main__":
    main()

