import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import speech_recognition as sr
import queue
import threading
import av

# Configure WebRTC Client Settings
RTC_CLIENT_SETTINGS = ClientSettings(
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"audio": True, "video": False},
)

# Queue to hold audio frames
audio_queue = queue.Queue()

# Audio processing callback
def audio_callback(frame: av.AudioFrame):
    audio_data = frame.to_ndarray()
    audio_queue.put(audio_data)
    return frame

# Transcription function
def transcribe_audio():
    recognizer = sr.Recognizer()
    while True:
        if not audio_queue.empty():
            audio_data = audio_queue.get()
            with sr.AudioFile(audio_data) as source:
                try:
                    # Recognize speech using Google Web Speech API
                    text = recognizer.recognize_google(source)
                    st.session_state.transcription = text
                except sr.UnknownValueError:
                    st.session_state.transcription = "Could not understand the audio"
                except sr.RequestError as e:
                    st.session_state.transcription = f"API Error: {e}"

# Streamlit app
st.title("Real-Time Audio Transcription with Streamlit WebRTC")

# WebRTC Streamer
webrtc_ctx = webrtc_streamer(
    key="speech-to-text",
    mode=WebRtcMode.SENDRECV,
    client_settings=RTC_CLIENT_SETTINGS,
    audio_frame_callback=audio_callback,
)

# Start transcription in a separate thread
if "transcription" not in st.session_state:
    st.session_state.transcription = ""
    threading.Thread(target=transcribe_audio, daemon=True).start()

# Display transcription in real-time
st.text_area("Real-Time Transcription:", value=st.session_state.transcription, height=200)

