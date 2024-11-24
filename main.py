import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, ClientSettings
import speech_recognition as sr
import openai
from gtts import gTTS
import os

# Set up OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["openai"]["api_key"]

# WebRTC client settings to ensure the dialog box remains
WEBRTC_CLIENT_SETTINGS = ClientSettings(
    media_stream_constraints={
        "audio": True,
        "video": False,
    },
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    },
)

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
                text_to_speech(response)
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

# Function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    os.system("mpg321 response.mp3")

# Streamlit app layout
st.title("Live Chat Mode with Speech Recognition")
st.subheader("This app listens to live speech and displays recognized text in real-time.")

# Initialize session state for controlling the WebRTC streamer
if "webrtc_started" not in st.session_state:
    st.session_state.webrtc_started = False

# Start and Stop buttons
if st.button("Start Live Chat Listening"):
    st.session_state.webrtc_started = True

if st.button("Stop Live Chat Listening"):
    st.session_state.webrtc_started = False

# Start the WebRTC streamer if the start button was pressed
if st.session_state.webrtc_started:
    webrtc_streamer(key="speech-recognition", audio_processor_factory=SpeechRecognitionProcessor, client_settings=WEBRTC_CLIENT_SETTINGS)
