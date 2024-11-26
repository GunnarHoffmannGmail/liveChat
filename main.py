import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import numpy as np
import whisper
import av
import queue
import threading

# Configure WebRTC Client Settings
RTC_CLIENT_SETTINGS = ClientSettings(
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"audio": True, "video": False},
)

# Queue for audio frames
audio_queue = queue.Queue()

# Whisper model initialization
model = whisper.load_model("base")  # Choose "base", "small", "medium", or "large" for accuracy/performance tradeoff

# Audio processing callback
def audio_callback(frame: av.AudioFrame):
    audio_data = frame.to_ndarray().flatten().astype(np.float32) / 32768.0  # Normalize 16-bit PCM data
    audio_queue.put(audio_data)
    return frame

# Function to transcribe audio using Whisper
def transcribe_audio():
    while True:
        if not audio_queue.empty():
            audio_buffer = []
            while not audio_queue.empty():
                audio_buffer.extend(audio_queue.get())

            # Convert audio buffer to numpy array
            audio_np = np.array(audio_buffer, dtype=np.float32)

            # Transcribe using Whisper
            try:
                result = model.transcribe(audio_np, fp16=False)
                st.session_state.transcription = result["text"]
            except Exception as e:
                st.session_state.transcription = f"Error: {e}"

# Streamlit app
st.title("Real-Time Audio Transcription with Whisper and Streamlit WebRTC")

# WebRTC Streamer
webrtc_ctx = webrtc_streamer(
    key="speech-to-text",
    mode=WebRtcMode.SENDRECV,
    client_settings=RTC_CLIENT_SETTINGS,
    audio_frame_callback=audio_callback,
)

# Start transcription in a background thread
if "transcription" not in st.session_state:
    st.session_state.transcription = ""
    threading.Thread(target=transcribe_audio, daemon=True).start()

# Display transcription
st.text_area("Real-Time Transcription:", value=st.session_state.transcription, height=200)

