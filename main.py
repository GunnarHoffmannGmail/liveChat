import streamlit as st
import soundfile as sf
import speech_recognition as sr
import tempfile
import os
import numpy as np
from scipy.io.wavfile import write

# Set up Streamlit page
def main():
    st.title("Real-time Speech to Text")
    st.write("Click the button below to record audio. Your speech will be converted to text and displayed below.")

    # Record audio using Streamlit's built-in recorder
    audio_bytes = st.audio("Record your message", format='audio/wav')

    if audio_bytes is not None:
        st.audio(audio_bytes, format='audio/wav')
        recognizer = sr.Recognizer()

        # Use a temporary file to store the recorded audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_bytes)
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


