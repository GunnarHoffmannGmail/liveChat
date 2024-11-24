import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import speech_recognition as sr

# WebRTC configuration
RTC_CONFIGURATION = {
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
}

# Media stream constraints
MEDIA_STREAM_CONSTRAINTS = {
    "audio": True,
    "video": False,
}

# Custom audio processor for speech recognition
class SpeechRecognitionProcessor(AudioProcessorBase):
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.text_placeholder = st.empty()

    def recv(self, frame):
        st.write("Received audio frame")
        audio_data = frame.to_ndarray()
        st.write(f"Audio data shape: {audio_data.shape}")
        audio = sr.AudioData(audio_data.tobytes(), frame.sample_rate, frame.sample_width)

        try:
            st.write("Recognizing speech...")
            text = self.recognizer.recognize_google(audio)
            st.write(f"Recognized text: {text}")
            if text:
                self.text_placeholder.text(f"Recognized: {text}")
        except sr.UnknownValueError:
            self.text_placeholder.text("Listening...")
            st.write("Listening...")
        except sr.RequestError:
            self.text_placeholder.text("Sorry, my speech service is down.")
            st.write("Sorry, my speech service is down.")
        except Exception as e:
            self.text_placeholder.text(f"Error: {str(e)}")
            st.error(f"Error: {str(e)}")
            st.write(f"Error: {str(e)}")

# Streamlit app layout
st.title("Live Speech Recognition")
st.subheader("This app listens to live speech and displays recognized text in real-time.")

# Initialize session state for controlling the WebRTC streamer
if "webrtc_started" not in st.session_state:
    st.session_state.webrtc_started = False

# Start and Stop buttons
if st.button("Start Listening"):
    st.session_state.webrtc_started = True
    st.write("Started listening")

if st.button("Stop Listening"):
    st.session_state.webrtc_started = False
    st.write("Stopped listening")

# Start the WebRTC streamer if the start button was pressed
if st.session_state.webrtc_started:
    st.write("Initializing WebRTC streamer...")
    webrtc_streamer(
        key="speech-recognition",
        audio_processor_factory=SpeechRecognitionProcessor,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints=MEDIA_STREAM_CONSTRAINTS
    )
    st.write("WebRTC streamer initialized")
else:
    st.write("WebRTC streamer not started")





