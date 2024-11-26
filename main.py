import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
import numpy as np
import queue
import json
from google.cloud import speech

# Streamlit app configuration
st.title("Live Speech-to-Text App with Microphone")

# Extract Google API key from secrets
api_key_info = json.loads(st.secrets["mykey"])
api_key = api_key_info.get("api_key") or api_key_info.get("private_key")

# Queue to handle audio frames
audio_queue = queue.Queue()

# Google Speech-to-Text configuration
client = speech.SpeechClient.from_service_account_info(api_key_info)

class SpeechToTextProcessor(AudioProcessorBase):
    def __init__(self):
        super().__init__()
        self.sampling_rate = 16000
        self.language_code = "en-US"

    def recv(self, frame):
        audio_data = frame.to_ndarray().flatten().astype(np.int16)
        audio_queue.put(audio_data)
        return frame

def process_audio_stream():
    audio_frames = []

    while True:
        audio_data = audio_queue.get()
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

# Start listening using WebRTC
webrtc_streamer(
    key="speech-to-text",
    mode=WebRtcMode.SENDONLY,
    audio_processor_factory=SpeechToTextProcessor,
    media_stream_constraints={"audio": True, "video": False},
)
