import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
import numpy as np
import queue
import json
from google.cloud import speech
import threading

# Set up Google API credentials from Streamlit secrets
google_api_key_json = st.secrets["mykey"]

# Initialize the Google Cloud Speech client
client = speech.SpeechClient.from_service_account_info(json.loads(google_api_key_json))

# Streamlit app configuration
st.title("Live Speech-to-Text App with Microphone")
st.text("Press 'Start' to begin capturing your speech!")

# Queue to handle audio frames
audio_queue = queue.Queue()

# Control flag for stopping the listening thread
stop_listening = threading.Event()

class SpeechToTextProcessor(AudioProcessorBase):
    def __init__(self):
        super().__init__()
        self.sampling_rate = 16000
        self.language_code = "en-US"

    def recv(self, frame):
        if not stop_listening.is_set():
            audio_data = frame.to_ndarray().flatten().astype(np.int16)
            audio_queue.put(audio_data)
        return frame

# Function to process audio and transcribe using Google Speech-to-Text
def process_audio_stream():
    audio_frames = []

    while not stop_listening.is_set():
        try:
            audio_data = audio_queue.get(timeout=1)
        except queue.Empty:
            continue

        if audio_data is None:
            break
        audio_frames.append(audio_data)

        if len(audio_frames) > 100:  # Process after 100 chunks for efficiency
            audio_content = np.concatenate(audio_frames).tobytes()
            audio_frames = []

            # Configure Google Speech-to-Text
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code="en-US",
            )
            audio = speech.RecognitionAudio(content=audio_content)
            response = client.recognize(config=config, audio=audio)

            if response.results:
                for result in response.results:
                    transcript = result.alternatives[0].transcript
                    st.session_state.transcript += transcript + "\n"
                    st.experimental_rerun()

# Initialize session state for transcript
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""

# Display the transcript
st.text_area("Transcript", value=st.session_state.transcript, height=200)

# Start listening in a separate thread
if st.button("Start Listening"):
    stop_listening.clear()
    listen_thread = threading.Thread(target=process_audio_stream, daemon=True)
    listen_thread.start()

# Stop listening
if st.button("Stop Listening"):
    stop_listening.set()
    audio_queue.put(None)  # To unblock the queue in case it's waiting

webrtc_streamer(
    key="speech-to-text",
    mode=WebRtcMode.SENDONLY,
    audio_processor_factory=SpeechToTextProcessor,
    media_stream_constraints={"audio": True, "video": False},
)
