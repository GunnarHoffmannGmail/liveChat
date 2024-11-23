import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, ClientSettings
import speech_recognition as sr

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
        except sr.UnknownValueError:
            st.write("Listening...")
        except sr.RequestError:
            st.write("Sorry, my speech service is down.")

# Streamlit app layout
st.title("Live Chat Mode with Speech Recognition")
st.subheader("This app listens to live speech and displays recognized text in real-time.")

if st.button("Start Live Chat Listening"):
    webrtc_streamer(key="speech-recognition", audio_processor_factory=SpeechRecognitionProcessor, client_settings=WEBRTC_CLIENT_SETTINGS)
