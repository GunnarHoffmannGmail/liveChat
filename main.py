import streamlit as st
import sounddevice as sd
import speech_recognition as sr
import tempfile
import wavio
import os

# Set up Streamlit page
def main():
    st.title("Real-time Speech to Text")
    st.write("Click the button below to start speaking. Your speech will be converted to text and displayed below.")

    recognizer = sr.Recognizer()

    # Button to start listening
    if st.button("Start Listening"):
        try:
            # Record audio using sounddevice
            duration = 5  # seconds
            fs = 44100  # Sample rate
            st.write("Listening for 5 seconds...")
            audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
            sd.wait()  # Wait until the recording is finished

            # Save the audio to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                wavio.write(tmp_file.name, audio_data, fs, sampwidth=2)
                temp_path = tmp_file.name

            # Recognize the speech using Google Web Speech API
            with sr.AudioFile(temp_path) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio)
                st.text_area("Recognized Text", text, height=200)

            # Clean up the temporary file
            os.remove(temp_path)
        except sr.UnknownValueError:
            st.error("Could not understand the audio. Please try again.")
        except sr.RequestError:
            st.error("Could not request results, please check your internet connection.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()



