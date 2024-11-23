import streamlit as st
import openai
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import speech_recognition as sr

# Set up OpenAI API key1
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Custom audio processor for speech recognition
class SpeechRecognitionProcessor(AudioProcessorBase):
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recv(self, frame):
        audio_data = frame.to_ndarray()
        audio = sr.AudioData(audio_data.tobytes(), frame.sample_rate, frame.sample_width)

        try:
            text = self.recognizer.recognize_google(audio)
            if text:
                st.write(f"Recognized: {text}")
                response = process_input(text)
                st.write(f"Response: {response}")
        except sr.UnknownValueError:
            st.write("Listening...")
        except sr.RequestError:
            st.write("Sorry, my speech service is down.")

# Function to process input using OpenAI GPT-3
def process_input(text):
    response = openai.Completion.create(
        engine="davinci",
        prompt=text,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Streamlit app layout
st.title("Live Chat Mode with Speech Recognition")
st.subheader("This app listens to live speech and displays recognized text in real-time.")

if st.button("Start Live Chat Listening"):
    webrtc_streamer(key="speech-recognition", audio_processor_factory=SpeechRecognitionProcessor)
