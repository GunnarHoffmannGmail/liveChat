import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
import numpy as np
import queue
import json
import threading
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

# Initialize session state for transcript and debugging info
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""
if 'debug_info' not in st.session_state:
    st.session_state.debug_info = ""

class SpeechToTextProcessor(AudioProcessorBase):
    def __init__(self):
        super().__init__()
        self.sampling_rate = 16000
        self.language_code = "en-US"

    def recv(self, frame):
        audio_data = frame.to_ndarray().flatten().astype(np.int16)
        audio_queue.put(audio_data)
        st.session_state.debug_info += "Received audio frame\n"
        st.session_state.debug_info = st.session_state.debug_info[-1000:]  # Limit debug info to last 1000 characters
        return frame

def process_audio_stream():
    audio_frames = []

    while True:
        try:
            audio_data = audio_queue.get(timeout=1)
        except queue.Empty:
            st.session_state.debug_info += "Queue is empty, waiting for audio data...\n"
            st.session_state.debug_info = st.session_state.debug_info[-1000:]  # Limit debug info to last 1000 characters
            continue

        if audio_data is None:
            break
        audio_frames.append(audio_data)

        if len(audio_frames) > 100:  # Process after 100 chunks for efficiency
            st.session_state.debug_info += "Processing audio frames...\n"
            st.session_state.debug_info = st.session_state.debug_info[-1000:]  # Limit debug info to last 1000 characters
            audio_content = np.concatenate(audio_frames).tobytes()
            audio_frames = []

            # Configure Google Speech-to-Text
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code="en-US",
            )
            audio = speech.RecognitionAudio(content=audio_content)
            try:
                response = client.recognize(config=config, audio=audio)
                if response.results:
                    for result in response.results:
                        transcript = result.alternatives[0].transcript
                        st.session_state.transcript += transcript + "\n"
                        st.session_state.debug_info += f"Transcript received: {transcript}\n"
                        st.session_state.debug_info = st.session_state.debug_info[-1000:]  # Limit debug info to last 1000 characters
                else:
                    st.session_state.debug_info += "No transcription result received.\n"
                    st.session_state.debug_info = st.session_state.debug_info[-1000:]  # Limit debug info to last 1000 characters
            except Exception as e:
                st.session_state.debug_info += f"Error during transcription: {e}\n"
                st.session_state.debug_info = st.session_state.debug_info[-1000:]  # Limit debug info to last 1000 characters

# Display the transcript and debug information
st.text_area("Transcript", value=st.session_state.transcript, height=200, key="transcript_area")
st.text_area("Debug Info", value=st.session_state.debug_info, height=200, key="debug_info_area")

# Start processing audio in a separate thread
def start_audio_processing():
    st.write("Debug 0")
    if 'processing_thread' not in st.session_state:
        st.write("Debug 1")
        processing_thread = threading.Thread(target=process_audio_stream, daemon=True)
        processing_thread.start()
        st.session_state.processing_thread = processing_thread

# Start listening using WebRTC and initiate processing
webrtc_streamer(
    key="speech-to-text",
    mode=WebRtcMode.SENDONLY,
    audio_processor_factory=SpeechToTextProcessor,
    media_stream_constraints={"audio": True, "video": False},
    on_change=start_audio_processing
)
