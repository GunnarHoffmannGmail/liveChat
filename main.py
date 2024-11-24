import streamlit as st
import speech_recognition as sr

# Set up Streamlit page
def main():
    st.title("Real-time Speech to Text")
    st.write("Click the button below and start speaking. Your speech will be converted to text and displayed in real-time.")

    # Instantiate the recognizer
    recognizer = sr.Recognizer()

    # Button to start listening
    if st.button("Start Listening"):
        with sr.Microphone() as source:
            st.write("Listening...")
            try:
                # Capture the audio from microphone
                audio = recognizer.listen(source)
                # Recognize the speech using Google Web Speech API
                text = recognizer.recognize_google(audio)
                # Display the recognized text in a text area
                st.text_area("Recognized Text", text, height=200)
            except sr.UnknownValueError:
                st.error("Could not understand the audio. Please try again.")
            except sr.RequestError:
                st.error("Could not request results, please check your internet connection.")

if __name__ == "__main__":
    main()
