import streamlit as st
import speech_recognition as sr
import tempfile
import os

# Set up Streamlit page
def main():
    st.title("Real-time Speech to Text")
    st.write("Click the button below to start speaking. Your speech will be converted to text and displayed below.")

    recognizer = sr.Recognizer()

    # Button to start listening
    if st.button("Start Listening"):
        try:
            with sr.Microphone() as source:
                st.write("Listening...")
                audio = recognizer.listen(source)
                st.write("Processing...")
                
                # Recognize the speech using Google Web Speech API
                text = recognizer.recognize_google(audio)
                st.text_area("Recognized Text", text, height=200)
        except sr.UnknownValueError:
            st.error("Could not understand the audio. Please try again.")
        except sr.RequestError:
            st.error("Could not request results, please check your internet connection.")
        except AttributeError:
            st.error("Could not find a microphone. Please ensure it is connected properly.")

if __name__ == "__main__":
    main()
